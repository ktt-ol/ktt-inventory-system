---
date: 2026-06-19
---

(adr-0002)=
# ADR-0002 URL code registry as separate Django app in same repo

## Context and Problem Statement

The space needs short, stable URLs on stickers for things that
are not inventory items — wifi instructions, wiki pages, chat
channels. A code registry maps a short code to a redirect
target. This is a generic URL shortener, independent of the
inventory domain.

## Considered Options

1. **Separate repository and deployment** — own Django project
   or microservice.
2. **Separate Django app in the same repository** — own
   models, views, and URLs, shared deployment.
3. **Inline in the inventory app** — add the redirect model
   and view to the existing app.

## Decision Outcome

Chosen option: separate Django app in the same repository.

Keeps the registry domain-isolated — no imports from inventory
models, no FK to Item — while avoiding infrastructure overhead
of a second deployment. App-level separation makes future
extraction straightforward once better dependency tooling
(e.g. uv workspaces) is available. The registry is a URL
shortener and must not gain knowledge of its consumers.

## Consequences

The code registry app must not import from or reference the
inventory app. The connection between a registry code and an
inventory item is by convention (shared code string), not by
model relationship.
