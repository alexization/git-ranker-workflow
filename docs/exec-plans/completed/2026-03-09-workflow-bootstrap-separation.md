```md
# Separate Workspace Bootstrap From Feature Workflow

This ExecPlan is a living document. Maintain it according to `PLANS.md` at the
repository root.

## Purpose / Big Picture

Keep one-time workspace bootstrap concerns out of the main feature-delivery
workflow so agents spend context on repeated delivery work, not on obvious local
setup state.

Request intake:

    Problem:
    The main workflow docs and verification path currently mix one-time
    submodule bootstrap with repeated feature delivery, and the docs claim a
    workspace state that is not true in this checkout.
    User-visible outcome:
    Workflow guidance focuses on feature delivery and feedback loops, while
    one-time workspace bootstrap no longer blocks workflow verification.
    Affected repos:
    knowledge-store only
    Contract surface:
    Workflow documentation, verification scripts, and setup wording.
    Acceptance checks:
    Main workflow docs no longer state that submodules are already initialized
    in this workspace, and `./scripts/verify-workflow.sh` succeeds without
    requiring populated submodule directories.
    QA evidence:
    `./scripts/verify-workflow.sh`
    targeted doc review for architecture, harness, and tech-debt wording
    Non-goals:
    Populating the submodules, wiring frontend Playwright, or changing
    application repos.
    Risks:
    Removing too much setup guidance could make workspace recovery harder if the
    bootstrap path becomes undocumented.

Task runtime slug:

    workflow-bootstrap-separation

## Progress

- [x] Reviewed the current workflow docs and scripts against the requested
  change on 2026-03-09.
- [x] Update the workflow docs to remove inaccurate bootstrap assumptions from
  the main path.
- [x] Adjust workflow verification so one-time workspace bootstrap is not a
  blocking gate.
- [x] Re-run verification and record outcomes.

## Surprises & Discoveries

- Observation:
  The current workspace contains empty `git-ranker/` and `git-ranker-client/`
  directories, so the workflow mismatch is immediately visible.
  Evidence:
  `scripts/check-submodules.sh` returns code 2 and `ls -la git-ranker
  git-ranker-client` shows empty directories.

## Decision Log

- Decision:
  Keep bootstrap utilities available, but remove them from the main workflow
  verification path.
  Rationale:
  One-time setup should stay recoverable without consuming context on every
  feature task.
  Date/Author:
  2026-03-09 / Codex

## Outcomes & Retrospective

- Outcome:
  Completed. The main workflow docs no longer claim that this workspace has
  populated submodules, and `verify-workflow.sh` now validates the workflow
  knowledge store without treating one-time workspace bootstrap as a task gate.
  Remaining gap:
  Submodule population is still a workspace-specific concern in this checkout,
  but it no longer blocks workflow verification.
  Lesson:
  Keep workspace bootstrap and feature-loop verification separate when their
  frequency and failure modes differ.

## Context and Orientation

This repository is the control plane for cross-repo delivery. The user wants
the OpenAI-style feature loop to stay visible, but does not want obvious,
one-time submodule setup to sit on the hot path. The current mismatch appears in
`ARCHITECTURE.md`, `harness/README.md`, `docs/exec-plans/tech-debt-tracker.md`,
and `scripts/verify-workflow.sh`.

## Plan of Work

First, correct docs that state the current workspace has initialized submodules
or that frame submodule state as part of the core workflow. Next, simplify
`scripts/verify-workflow.sh` so it validates the workflow knowledge store only.
Leave the bootstrap helper scripts in place as recovery utilities, but keep
them out of the repeated delivery gate.

## Concrete Steps

Update:

    ARCHITECTURE.md
    harness/README.md
    docs/exec-plans/tech-debt-tracker.md
    scripts/verify-workflow.sh

Then run:

    ./scripts/verify-workflow.sh

Expected observation:

    workflow verification passed

## Validation and Acceptance

Describe:

    - test commands: ./scripts/verify-workflow.sh
    - Playwright journeys: not applicable
    - CDP checks: not applicable
    - Loki or log-backend queries: not applicable
    - metrics or trace checks when relevant: not applicable

## Idempotence and Recovery

The doc edits and verification script change are safe to rerun. If wording needs
to be rolled back, restore the affected files from git. Bootstrap scripts remain
available if a future workspace needs submodule initialization.

## Artifacts and Notes

Record paths for:

    - verification output: ./scripts/verify-workflow.sh -> passed on 2026-03-09
    - setup utility check: ./scripts/check-submodules.sh -> reports uninitialized
      submodules in this workspace, but is no longer part of the workflow gate

## Interfaces and Dependencies

This task depends on the control-plane docs, shell verification scripts, and
the existing bootstrap helpers in `scripts/bootstrap-submodules.sh` and
`scripts/check-submodules.sh`.
```
