# Decisions

This directory contains decision records. See [0000-use-adr.md](0000-use-adr.md)
for why we use this approach.

For new ADRs, please use [adr-template.md](adr-template.md) as basis. It is
intentionally kept minimal, if you want to add more details, then follow the
pick from the full template at <https://adr.github.io/madr/#full-template>.

More information on MADR is available at <https://adr.github.io/madr/>.

General information about architectural decision records is available at
<https://adr.github.io/>.

## Cross-Referencing

Each ADR has a MyST label for Sphinx cross-referencing. Place the label after
the YAML frontmatter and before the heading:

```markdown
---
date: 2026-01-06
---

(adr-0001)=
# 0001 - Decision Title
```

Reference ADRs using the `{ref}` role:

```markdown
See {ref}`adr-0001` for details.
```

This renders as a clickable link with the ADR title.

## Immutability

ADRs are immutable after acceptance. Do not edit the substance of an accepted ADR.

When a decision changes, create a new ADR and mark the old one as
"Superseded by ADR-NNNN". This preserves the decision-making history.
