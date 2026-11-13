---
date: 2026-11-13
---

(adr-0009)=
# ADR-0009 Verify handling of errors

## Context and Problem Statement

We need an easy way to verify two things on a deployment: that debug mode is
off, and that the error templates render.

## Considered Options

2. Add the routes behind a setting, off by default.
3. Add the routes, open to everyone.
4. Add the routes, and require staff for the 500 one.

## Decision Outcome

Chosen option: add the routes, and require staff for the 500 one.

A setting would be one more thing to switch on and forget. Open was rejected
because Django tries to mail the admins on every 500 when `DEBUG = False`.

## Consequences

Checking the 500 page needs a staff login. Each check mails the admins.
