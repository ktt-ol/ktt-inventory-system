---
date: 2026-06-19
---

(adr-0003)=
# ADR-0003 Inventory stickers vs URL stickers

## Context and Problem Statement

Physical stickers in the space serve two distinct user intents.
Scanning a sticker on a machine may mean "what is this thing?"
(expecting the inventory page) or "help me with this" (expecting
a manual, wiki page, or chat link). Both use QR codes but lead
to different destinations.

## Considered Options

1. **Single URL scheme** — all stickers go through the code
   registry, which redirects to either inventory or external
   targets.
2. **Two URL schemes** — inventory stickers encode the inventory
   URL directly; URL stickers encode a code registry short URL.

## Decision Outcome

Chosen option: two URL schemes.

An inventory sticker encodes the inventory item URL
(`/item/<CODE>/`) — scanning it always lands on the item page,
which serves as the hub for further links. A URL sticker encodes
a code registry URL (`/c/<CODE>/`) — scanning it redirects to
any target (manual, wiki, chat). This matches user expectation:
an inventory label leads to the item, a help sticker leads to
help. A single scheme would force all inventory items through
the registry, adding setup overhead without benefit.

## Related

- {ref}`adr-0002` — the code registry that serves URL stickers
- {ref}`adr-0001` — how inventory item pages make URLs
  discoverable once landed
