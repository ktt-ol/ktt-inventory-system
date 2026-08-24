---
date: 2026-08-24
---

(adr-0007)=
# ADR-0007 Barcode code range spans what the model stores

## Context and Problem Statement

`Barcode.code` is a `CharField(max_length=10)` with no lower
bound, but the `item` URL pattern is built from
`BARCODE_CODE_LENGTH`, defaulting to `(4, 6)`. A code outside
that range is storable but not addressable, and because
`get_absolute_url()` runs during template rendering, a single
such code raises `NoReverseMatch` and fails the whole page.

## Considered Options

1. **Widen the range to span the model** — default `(1, 10)`,
   so every code the model can store has a URL.
2. **Validate codes against the range** — reject codes outside
   `BARCODE_CODE_LENGTH` on the model. Consistent, but
   invalidates existing codes and needs a data migration.
3. **Fall back to `item_by_id`** — catch the mismatch in
   `get_absolute_url()`. Robust against drift, but gives an
   item two addresses depending on its code length, which
   conflicts with the sticker schemes in ADR-0003.

## Decision Outcome

Chosen option: widen the range to `(1, 10)`.

The model is the authority on what a code may be; the URL
config should follow it rather than constrain it behind its
back. Option 2 would relabel physical stickers already in the
space, and option 3 would make an item's address depend on how
long its code happens to be.

The range stays configurable — it also drives the search
field's maxlength — so a Django system check reports a
configured maximum below the model's `max_length` instead of
letting it resurface as a render-time crash.
