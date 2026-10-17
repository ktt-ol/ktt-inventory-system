---
date: 2026-06-19
---

(adr-0001)=
# ADR-0001 Auto-link URLs in item text fields

## Context and Problem Statement

The item detail page renders `description` and `note` inside
`<pre>` tags. URLs in these fields are plain text — not
clickable. Users need to discover links to manuals, wiki pages,
and documentation from the item page.

## Considered Options

1. **Dedicated URL model field** — add a URLField to the Item
   model.
2. **Auto-link with `urlize`** — apply Django's `urlize` template
   filter to existing text fields.
3. **Markdown rendering** — render text fields as Markdown.

## Decision Outcome

Chosen option: `urlize` on `description` and `note` fields.

No model change needed, supports multiple URLs in existing
content, and is sufficient for the item discovery use case. A
dedicated field would limit to one URL and require a migration.
Markdown changes the semantics of existing content and risks
cluttering the UI.
