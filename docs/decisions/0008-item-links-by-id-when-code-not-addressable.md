---
date: 2026-09-16
---

(adr-0008)=
# ADR-0008 An item links by id when its code is not addressable

## Context and Problem Statement

The model stores codes the `item` URL pattern cannot address
(ADR-0007). Reversing one raises, and that happens while a template
builds a link, so a single bad code breaks every page that lists the
item.

## Considered Options

1. Check the code against the range before reversing.
2. Catch `NoReverseMatch` and link by id instead.
3. Pick an addressable code when the item has several.
4. Reject unaddressable codes on save.

## Decision Outcome

Chosen: catch `NoReverseMatch` and link by id.

The reverse already knows what it can address. A check would copy the
pattern's rules somewhere they can drift, and a length check would
still miss a code rejected for its characters.

Option 3 is more behaviour for a rare case, and it rests on query
ordering that nothing pins. Option 4 changes what the model accepts,
which is its own decision, and it strands the codes already stored.

## Consequences

`Item.barcode_url()` holds the answer and `item_by_id` redirects on it
rather than on `has_barcode()`, so the view cannot redirect to itself.

`/item/M01/` still 404s. This is about the pages that link the item.
