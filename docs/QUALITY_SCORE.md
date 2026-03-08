---
summary: Quality scoring rubric and continuous cleanup loop.
read_when:
  - reviewing architecture drift
  - scheduling cleanup or follow-up refactors
---

# Quality Score

Use a simple A to F score per major surface:

- contract clarity
- test coverage
- docs freshness
- observability coverage
- layering discipline
- UX state completeness

## Grade meanings

- `A`: clear boundaries, current docs, strong tests, observable behavior
- `B`: acceptable but missing one non-critical reinforcement
- `C`: functional but agent legibility is degraded
- `D`: drift is visible and likely to spread
- `F`: unsafe to scale without cleanup

## Garbage-collection rule

If a change uncovers a durable bad pattern, either:

- fix it in the same task, or
- add it to [exec-plans/tech-debt-tracker.md](exec-plans/tech-debt-tracker.md)
  with a clear trigger and consequence

The desired operating mode is continuous small cleanup, not occasional large
rewrite weeks.

