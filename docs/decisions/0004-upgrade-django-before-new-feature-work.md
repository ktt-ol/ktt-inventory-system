---
date: 2026-06-19
---

(adr-0004)=
# ADR-0004 Upgrade Django before new feature work

## Context and Problem Statement

Django 3.2 is end of life. New feature work is planned (code
registry, public item views). Should we upgrade to the current
Django LTS first?

## Considered Options

1. **Upgrade first** — fix deprecations and move to current LTS
   before building new features.
2. **Build features first** — keep Django 3.2, upgrade later.

## Decision Outcome

Chosen option: upgrade first.

Building on an EOL framework means new code inherits deprecated
patterns that need changing later anyway. The upgrade is
mechanical (import renames, URL pattern syntax) and takes hours.
Doing it first gives new features a stable, supported base.
