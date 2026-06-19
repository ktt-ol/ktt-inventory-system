# E2E Tests

Playwright-based browser tests for the inventory system.

## Setup

```sh
cd tests/e2e
uv sync
uv run playwright install chromium
```

## Running

Start the dev server first, then run the tests:

```sh
./manage.py runserver
```

```sh
cd tests/e2e
uv run pytest -v
```

## NixOS

The Playwright Python package depends on `greenlet`, which needs
`libstdc++`. On NixOS, provide it via `LD_LIBRARY_PATH`:

```sh
nix shell nixpkgs#stdenv.cc.cc.lib -c bash -c \
  'export LD_LIBRARY_PATH=$NIX_CC/lib; uv run pytest -v'
```

The `conftest.py` uses system Chromium (`which chromium`)
automatically, so `playwright install` is not needed when
Chromium is available via NixOS.
