# git-ranker-workflow AGENTS

This repository is the control plane for the `git-ranker` backend and the
`git-ranker-client` frontend. Keep this file short. The system of record lives
in [ARCHITECTURE.md](ARCHITECTURE.md) and [docs/](docs/index.md).

## What this repo owns

- Repository-local knowledge store and operating rules for coding agents
- Cross-repo feature delivery workflow, QA loop, and observability workflow
- ExecPlan conventions for long-running tasks
- Guardrails for frontend/backend coordination across the two submodule repos

## Repo map

- `git-ranker/`: backend repo (submodule)
- `git-ranker-client/`: frontend repo (submodule)
- `ARCHITECTURE.md`: top-level control-plane architecture
- `PLANS.md`: rules for long-running ExecPlans
- `docs/`: knowledge store; treat this as the source of truth
- `scripts/`: lightweight verification and scaffolding helpers
- `harness/`: local observability and QA harness configuration
- `.codex/evals/`: eval definitions and templates

## How to start a task

1. Read [ARCHITECTURE.md](ARCHITECTURE.md).
2. Read [docs/index.md](docs/index.md) and the specific docs for the change
   surface.
3. If the request spans multiple files, multiple repos, new behavior, or a
   likely multi-hour effort, create an ExecPlan in
   `docs/exec-plans/active/<yyyy-mm-dd>-<slug>.md` and follow [PLANS.md](PLANS.md).
4. Restate the request in terms of:
   - user-visible outcome
   - impacted repos
   - acceptance checks
   - required Playwright/CDP/Loki evidence
5. Work inside a task-specific isolated runtime footprint under `.runtime/` and
   `.worktrees/`.

## System of record

- Product intent: [docs/product-specs/index.md](docs/product-specs/index.md)
- Architectural rules: [docs/design-docs/index.md](docs/design-docs/index.md)
- UX and UI behavior: [docs/DESIGN.md](docs/DESIGN.md),
  [docs/FRONTEND.md](docs/FRONTEND.md)
- Backend and data behavior: [docs/BACKEND.md](docs/BACKEND.md),
  [docs/SECURITY.md](docs/SECURITY.md), [docs/RELIABILITY.md](docs/RELIABILITY.md)
- Quality and cleanup rules: [docs/QUALITY_SCORE.md](docs/QUALITY_SCORE.md)
- Generated facts: [docs/generated/README.md](docs/generated/README.md)
- Workflow loop: [docs/workflows/feature-delivery-loop.md](docs/workflows/feature-delivery-loop.md),
  [docs/workflows/qa-feedback-loop.md](docs/workflows/qa-feedback-loop.md),
  [docs/workflows/commit-message-convention.md](docs/workflows/commit-message-convention.md)

## Non-negotiables

- Do not turn `AGENTS.md` into a large manual. Promote durable rules into
  `docs/` or scripts.
- Do not implement from vague intent. Convert feature requests into explicit
  acceptance criteria first.
- Do not ship a user-visible change without QA evidence from:
  - automated tests
  - Playwright
  - browser inspection via CDP or equivalent
  - worktree-local logs in Loki or the configured log backend
- Do not treat Slack, chat history, or memory as source of truth. If it matters
  later, check it into the repo.
- Do not handwave cross-repo changes. Contract changes must be reflected in
  backend, frontend, docs, and validation steps.

## Delivery loop

1. Intake and clarify the request.
2. Write or update an ExecPlan if the task is non-trivial.
3. Implement in backend/frontend worktrees.
4. Run build, typecheck, lint, and tests.
5. Boot the isolated stack for the task.
6. Run Playwright journeys.
7. Inspect UI, network, console, and DOM with CDP tooling.
8. Query logs and metrics for the same task runtime.
9. Feed findings back into code, docs, and the ExecPlan.
10. Record outcomes and remaining debt before handoff or merge.
