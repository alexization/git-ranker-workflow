---
summary: UI and interaction design rules for agent-authored frontend changes.
read_when:
  - changing visible UI
  - altering copy, layout, or interaction flow
---

# Design

## Goal

Frontend changes must be legible to users and to future agents. Design choices
should be deliberate enough that screenshots, DOM snapshots, and acceptance docs
all tell the same story.

## Rules

- Start from user journeys, not component churn.
- Reuse existing visual patterns unless a design doc says the new pattern is
  intentionally different.
- Capture meaningful empty, loading, success, and error states.
- Name visual states explicitly in docs and tests.
- If a visible workflow changes, update the relevant product and QA docs in the
  same task.

## Required evidence for visual changes

- before/after screenshots or the first implementation screenshot plus expected
  final state
- a Playwright assertion for the intended state
- a CDP check for console cleanliness and final DOM state

