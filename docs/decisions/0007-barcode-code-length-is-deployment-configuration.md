---
date: 2026-08-24
---

(adr-0007)=
# ADR-0007 Barcode code length is deployment configuration

## Context and Problem Statement

The `item` URL pattern is built from `BARCODE_CODE_LENGTH`, which
defaults to `(4, 6)`. `Barcode.code` has no lower bound, so a shorter
code is storable but not addressable. `get_absolute_url()` runs during
template rendering, so one such code fails every page that lists the
item.

## Considered Options

1. **Widen the shipped default** so it spans what the model stores.
2. **Set the range in the container settings module.**
3. **Read the range from the environment** and set it per deployment.
4. **Remove the length bound from the URL pattern.**

## Decision Outcome

Chosen option: read the range from the environment.

The setting exists because deployments differ, so the value belongs
with the deployment rather than in the shipped default or the shared
image. The container settings module already reads other
per-deployment values this way. Removing the bound was rejected
because it would drop the configurability other deployments rely on.

## Consequences

Nothing validates a code against the range on the way in, so a
deployment that narrows it can still create codes that crash
rendering. The pattern's character class is a second bound: a code
containing punctuation is unaddressable at any configured length.
