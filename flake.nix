{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
    }:
    let
      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };
    in
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = nixpkgs.lib;

        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "sdist";
        };

        pyprojectOverrides = final: prev: {
          pillow = prev.pillow.overrideAttrs (old: {
            nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
              pkgs.pkg-config
            ];
            buildInputs = (old.buildInputs or [ ]) ++ [
              pkgs.freetype
              pkgs.lcms2
              pkgs.libjpeg
              pkgs.libtiff
              pkgs.libwebp
              pkgs.openjpeg
              pkgs.zlib-ng
            ];
            pypaBuildFlags = (old.pypaBuildFlags or [ ]) ++ [
              "--config-setting=--disable-platform-guessing"
            ];
          });
        };

        baseSet = pkgs.callPackage pyproject-nix.build.packages {
          python = pkgs.python313;
        };

        pythonSet = baseSet.overrideScope (
          lib.composeManyExtensions [
            pyproject-build-systems.overlays.default
            overlay
            pyprojectOverrides
          ]
        );

        virtualenv = pythonSet.mkVirtualEnv "dev-env"
          workspace.deps.all;

        containerEnv = pythonSet.mkVirtualEnv "container-env" {
          ktt-inventory-system = [ "prod" ];
        };

        compiledLocale = pkgs.runCommand "compiled-locale" {
          nativeBuildInputs = [ pkgs.gettext ];
        } ''
          mkdir -p $out/de/LC_MESSAGES
          msgfmt ${./conf/locale/de/LC_MESSAGES/django.po} \
            -o $out/de/LC_MESSAGES/django.mo
        '';

        staticFiles = pkgs.runCommand "collected-static" {
          nativeBuildInputs = [ containerEnv ];
        } ''
          export DJANGO_SETTINGS_MODULE=inventar.settings_container
          export SECRET_KEY=nix-build-placeholder
          export STATIC_ROOT=$out
          export LOCALE_PATH=${compiledLocale}
          python -m django collectstatic --noinput
        '';

        nginxConf = pkgs.writeText "nginx.conf" ''
          daemon off;
          worker_processes 1;
          error_log /dev/stderr;
          pid /tmp/nginx.pid;

          events {
            worker_connections 64;
          }

          http {
            include ${pkgs.nginx}/conf/mime.types;
            access_log /dev/stdout;

            client_body_temp_path /tmp/client_body;

            gzip on;
            gzip_types text/css application/javascript
                       image/svg+xml;

            server {
              listen 8080;
              listen [::]:8080;
              location /static/ { alias /static/; }
              location /uploaded/ { alias /uploaded/; }
            }
          }
        '';
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            virtualenv
            pkgs.uv
          ];
          env = {
            UV_NO_SYNC = "1";
            UV_PYTHON = "${pkgs.python313.interpreter}";
            UV_PYTHON_DOWNLOADS = "never";
            E2E_BROWSER_EXECUTABLE = "${pkgs.chromium}/bin/chromium";
          };
          shellHook = ''
            unset PYTHONPATH
          '';
        };

        packages.container =
          pkgs.dockerTools.streamLayeredImage {
            name = "local/ktt-inventory";
            tag = "latest";
            contents = [
              containerEnv
              pkgs.dockerTools.fakeNss
              pkgs.cacert
            ];
            fakeRootCommands = ''
              mkdir -p data tmp
              chmod 1777 tmp
            '';
            enableFakechroot = true;
            config = {
              Cmd = [
                "${containerEnv}/bin/gunicorn"
                "inventar.wsgi:application"
                "--bind"
                "0.0.0.0:8000"
                "--workers"
                "2"
              ];
              Env = [
                "DJANGO_SETTINGS_MODULE=inventar.settings_container"
                "LOCALE_PATH=${compiledLocale}"
                "MEDIA_ROOT=/data/uploaded/"
                "DATABASE_PATH=/data/inventar.db"
                "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
                "PYTHONDONTWRITEBYTECODE=1"
              ];
              ExposedPorts = {
                "8000/tcp" = { };
              };
              Volumes = {
                "/data" = { };
              };
            };
          };

        packages.container-nginx =
          pkgs.dockerTools.streamLayeredImage {
            name = "local/ktt-inventory-nginx";
            tag = "latest";
            contents = [
              pkgs.nginx
              (pkgs.dockerTools.fakeNss.override {
                extraGroupLines = [ "nogroup:x:65534:" ];
              })
            ];
            extraCommands = ''
              mkdir -p tmp/client_body
              mkdir -p var/log/nginx
              mkdir -p static uploaded
              cp -r ${staticFiles}/* static/
            '';
            config = {
              Cmd = [
                "${pkgs.nginx}/bin/nginx"
                "-c"
                "${nginxConf}"
              ];
              ExposedPorts = {
                "8080/tcp" = { };
              };
              Volumes = {
                "/uploaded" = { };
              };
            };
          };
      }
    );
}
