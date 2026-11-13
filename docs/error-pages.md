(error-pages)=
# Error pages

Two routes fail on purpose, so you can check that a deployment has
debug mode off and renders the error templates:

- `/error/404/` renders `404.html`
- `/error/500/` raises an exception, which renders `500.html`

`/error/500/` answers staff users. For anyone else it returns 404.

See {ref}`adr-0009` for why these exist.
