---
date: 2026-06-20
---

(adr-0006)=
# ADR-0006 E2E test data via management commands

## Context and Problem Statement

E2E tests run in a separate uv project without Django
(ADR-0005). They need known test data in the dev server's
database but cannot use the ORM directly. How should E2E
test data be seeded?

## Considered Options

1. **Management command via subprocess** — a custom
   `manage.py ensure_e2e_data` command that creates test
   data idempotently. The E2E conftest calls it as a
   subprocess before tests run.
2. **Django fixture file + loaddata** — a static JSON
   fixture loaded via `manage.py loaddata`. Breaks when
   models change (PKs, fields).
3. **Dedicated pre-built test database** — a pre-built
   SQLite file swapped in before the dev server starts.
   Hard to maintain across schema changes.
4. **HTTP-based setup via admin/API** — create data
   through the Django admin or a test API endpoint.
   Requires auth setup, slower, more fragile.

## Decision Outcome

Chosen option: management command via subprocess.

The command uses `get_or_create`, making it idempotent and
resilient to model changes. It runs as a subprocess from
the E2E conftest, respecting the Django/E2E boundary from
ADR-0005. No static fixture files to maintain, no auth
setup needed, and the command is also useful for manual
testing.
