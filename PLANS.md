# ExecPlans for git-ranker-workflow

This document adapts OpenAI's `PLANS.md` pattern to a two-repository product
workflow. Use it for any task that is likely to take more than one session,
spans multiple files or repos, changes contracts, or requires non-trivial QA.

## When to create an ExecPlan

Create an ExecPlan when any of the following are true:

- the request spans backend and frontend
- the request changes API, schema, routing, or product behavior
- the work is expected to last more than 30 minutes
- you need a reproducible QA and feedback loop
- you expect to stop and resume later

Store plans in `docs/exec-plans/active/<yyyy-mm-dd>-<slug>.md`.

## Non-negotiable rules

- Every ExecPlan must be self-contained.
- Every ExecPlan must remain a living document.
- Every ExecPlan must let a novice continue from only the working tree and the
  plan file.
- Every ExecPlan must describe observable outcomes, not just code edits.
- Every ExecPlan must define the validation loop clearly.

## Repo-specific additions

Every plan in this repository must also include:

- impacted repo list: backend, frontend, or both
- request intake summary in plain language
- contract boundary notes
- exact task runtime slug
- expected Playwright journeys
- expected CDP evidence
- expected Loki or log-backend queries
- rollback or retry notes for each risky step

## Required sections

Every ExecPlan must keep these sections current:

- `Purpose / Big Picture`
- `Progress`
- `Surprises & Discoveries`
- `Decision Log`
- `Outcomes & Retrospective`
- `Context and Orientation`
- `Plan of Work`
- `Concrete Steps`
- `Validation and Acceptance`
- `Idempotence and Recovery`
- `Artifacts and Notes`
- `Interfaces and Dependencies`

## Formatting

The plan file itself should contain one single fenced code block labeled `md`.
Do not nest other fenced blocks inside the plan. Use indentation for commands,
snippets, and transcripts.

## Required execution rhythm

1. Clarify the user's request in product language.
2. Identify impacted repos and documents.
3. Research before implementation.
4. Update the plan before and after every material milestone.
5. Validate behavior in the isolated task runtime.
6. Record the evidence path for screenshots, videos, traces, and logs.
7. Update docs when a new durable rule or system fact is discovered.

## Plan naming

Use a sortable filename:

`docs/exec-plans/active/2026-03-07-rank-comparison-filtering.md`

## Template

Start from `docs/exec-plans/_template.md`.

