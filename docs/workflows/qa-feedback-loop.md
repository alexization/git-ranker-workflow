---
summary: Playwright, CDP, and log-driven feedback loop for user-visible changes.
read_when:
  - validating a fix or feature
  - debugging a regression
---

# QA Feedback Loop

## Required inputs

- task runtime slug
- affected user journey name
- expected final UI state
- expected backend or log behavior

## Loop

1. Boot the isolated backend and frontend for the task.
2. Run the Playwright journey that exercises the change.
3. Capture:
   - screenshots
   - video when useful
   - Playwright traces or reports
4. Inspect the same run through CDP:
   - DOM snapshot
   - console output
   - failed requests
   - final URL and app state
5. Query logs for the same time window and task slug.
6. If performance or async orchestration matters, inspect metrics and traces too.
7. Compare observations against the acceptance section of the ExecPlan.
8. If anything disagrees, fix the system and rerun the loop.

## Minimum artifact set

- `.runtime/<slug>/playwright/`
- `.runtime/<slug>/screenshots/`
- `.runtime/<slug>/videos/` when relevant
- `.runtime/<slug>/logs/`
- `.runtime/<slug>/observability/queries.md` or equivalent note

## Why this exists

This is the core OpenAI harness pattern applied locally: the agent must be able
to see the product behavior directly, not infer success from code changes alone.

