```md
# Standardize Korean Commit Messages Across Repos

This ExecPlan is a living document. Maintain it according to `PLANS.md` at the
repository root.

## Purpose / Big Picture

Define one reusable commit-message convention for the control-plane repo and the
`git-ranker` and `git-ranker-client` submodules so future work uses the same
title and body structure.

Request intake:

    Problem:
    There is no durable, shared commit-message convention or reusable template
    for the root repo and the two application repos.
    User-visible outcome:
    Contributors and agents can write Korean commit messages in one standard
    format such as `feat: 핵심적인 작업 내용`, with short bullet lists for
    detailed work items.
    Affected repos:
    knowledge-store only
    Contract surface:
    Workflow documentation, agent guidance, and a reusable git commit template
    file.
    Acceptance checks:
    The repo contains a documented convention, a reusable template file, and
    clear guidance that the same rule applies to the root repo and both
    submodules.
    QA evidence:
    doc review
    git diff review
    Non-goals:
    Automatically installing git config in each repo or rewriting past commits.
    Risks:
    Over-specifying the format could make simple commits cumbersome if the
    template is too heavy.

Task runtime slug:

    commit-message-convention

## Progress

- [x] Clarified the requested commit-message format and reuse requirement on
  2026-03-09.
- [x] Add the shared convention doc and template file.
- [x] Link the convention from the main repo guidance.
- [x] Review the diff and record usage notes.

## Surprises & Discoveries

- Observation:
  The current repo has no existing durable commit-message convention.
  Evidence:
  `rg` found no relevant workflow docs for commit formatting.

## Decision Log

- Decision:
  Use one workflow doc plus one reusable template file instead of duplicating
  separate rules per repo.
  Rationale:
  The convention must stay consistent across three related repositories.
  Date/Author:
  2026-03-09 / Codex

## Outcomes & Retrospective

- Outcome:
  Completed. The shared convention doc, reusable template, agent-facing links,
  and knowledge-store validation entries are in place.
  Remaining gap:
  The rule is documented and reusable, but each local repository still needs a
  developer to opt into `git config commit.template` if they want git to preload
  the template automatically.
  Lesson:
  Keep commit rules near workflow docs, but expose a concrete file that git can
  use directly.

## Context and Orientation

This control-plane repo defines durable workflow rules for itself and the two
application repos. The new rule should be discoverable by agents without making
`AGENTS.md` large, and the template should be directly reusable from the root
repo and submodules.

## Plan of Work

Add a compact workflow doc under `docs/workflows/` that defines the allowed
prefixes, Korean subject format, and bullet-list body. Add a reusable
`.gitmessage.ko.txt` template in the repository root. Update the docs index and
`AGENTS.md` minimally so agents can discover the new rule quickly.

## Concrete Steps

Update:

    AGENTS.md
    docs/index.md

Add:

    docs/workflows/commit-message-convention.md
    .gitmessage.ko.txt

Review:

    git diff --stat

Expected observation:

    The convention is documented once and the same template can be referenced
    from the root repo or submodules.

## Validation and Acceptance

Describe:

    - test commands: not applicable
    - Playwright journeys: not applicable
    - CDP checks: not applicable
    - Loki or log-backend queries: not applicable
    - metrics or trace checks when relevant: not applicable

## Idempotence and Recovery

The documentation and template edits are safe to rerun. If the convention needs
to be relaxed later, update the doc and template together so they do not drift.

## Artifacts and Notes

Record paths for:

    - convention doc: docs/workflows/commit-message-convention.md
    - reusable template: .gitmessage.ko.txt
    - verification output: ./scripts/verify-workflow.sh -> passed on 2026-03-09

## Interfaces and Dependencies

This task depends on the repo guidance files, workflow docs, and git's
`commit.template` capability for optional local use.
```
