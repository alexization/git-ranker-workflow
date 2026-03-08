---
summary: Frontend implementation and QA rules for git-ranker-client.
read_when:
  - working in the frontend repo
  - validating a user-visible change
---

# Frontend

## Current repo facts

- framework: Next.js App Router under `src/app`
- language: TypeScript with strict mode
- runtime: React 19
- data/state: React Query and Zustand
- linting: ESLint via `eslint.config.mjs`

## Current gap

No committed unit-test or Playwright config was found in `git-ranker-client`
during this setup. That means the workflow requirement is stricter than the
current repo state. For any meaningful frontend feature, part of the work should
be adding or wiring the missing QA harness.

## What agents must optimize for

- predictable route behavior
- explicit data loading and failure handling
- testable UI states
- clear contract boundaries with the backend

## Required workflow for user-visible changes

1. Confirm or create acceptance criteria in product language.
2. Identify affected routes, components, and client contracts.
3. Implement the change.
4. Run frontend build, lint, and any available tests.
5. Boot the isolated task runtime.
6. Run the Playwright journey for the changed surface.
7. Inspect the final state with CDP:
   - screenshot
   - DOM snapshot
   - console logs
   - failed network requests
8. Record artifact paths in the ExecPlan.

## Frontend contract rules

- Parse and validate incoming server data at the boundary.
- Do not let raw backend payloads leak through the UI tree.
- Put orchestration in loaders, hooks, or services; keep components focused on
  rendering and event wiring.
- Make loading, empty, and error states explicit.

## Minimum QA bar

Every frontend feature should leave behind:

- at least one Playwright path for the happy path
- at least one assertion for the most important failure or empty state
- a reproducible screenshot or video path
- a CDP artifact path for the final DOM and console state

## Expected commands to codify

- `npm run build`
- `npm run lint`
- a future committed Playwright command such as `npx playwright test`
