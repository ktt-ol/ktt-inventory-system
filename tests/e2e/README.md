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


## Browsers Playwright cannot start

On some distributions Playwright's downloaded browsers are linked
against libraries that are not on the default search path, and fail
to start. NixOS is one. Point the tests at a browser the system
provides instead:

```sh
E2E_BROWSER_EXECUTABLE=$(which chromium) uv run pytest -v
```
