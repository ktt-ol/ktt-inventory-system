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
          };
          shellHook = ''
            unset PYTHONPATH
          '';
        };
      }
    );
}
