---
date: 2026-06-20
---

(adr-0005)=
# ADR-0005 Keep E2E tests as separate uv project

## Context and Problem Statement

The inventory system is switching from requirements.txt to uv for
dependency management. E2E tests already have their own
pyproject.toml and uv.lock in tests/e2e/. The question is whether
to merge them into the root project or keep them separate.

## Considered Options

1. **Separate uv project** — E2E tests keep their own
   pyproject.toml and .venv in tests/e2e/, without Django as a
   dependency.
2. **Merged into root project** — E2E tests become a dependency
   group in the root pyproject.toml, sharing one environment.
3. **uv workspace** — root project and E2E tests as workspace
   members with a shared lockfile and .venv.

## Decision Outcome

Chosen option: separate uv project.

E2E tests treat the inventory system as an opaque service —
they interact only through the browser via Playwright. A
separate project enforces this at the dependency level: Django
is not installed, so test code cannot accidentally import
models, ORM, or settings. Options 2 and 3 share an environment
where Django is importable, reducing the boundary to a
convention. Conventions erode; dependency boundaries hold.

## Consequences

Test data setup must use management commands or API endpoints,
not direct ORM access.
