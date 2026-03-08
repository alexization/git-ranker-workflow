```md
# <Short, action-oriented title>

This ExecPlan is a living document. Maintain it according to `PLANS.md` at the
repository root.

## Purpose / Big Picture

Explain what user-visible behavior will exist after this change and how to see
it working.

Request intake:

    Problem:
    User-visible outcome:
    Affected repos:
    Contract surface:
    Acceptance checks:
    QA evidence:
    Non-goals:
    Risks:

Task runtime slug:

    <task-slug>

## Progress

- [ ] Example incomplete step.
- [ ] Example partially completed step.
- [x] Example completed step with timestamp.

## Surprises & Discoveries

- Observation:
  Evidence:

## Decision Log

- Decision:
  Rationale:
  Date/Author:

## Outcomes & Retrospective

- Outcome:
  Remaining gap:
  Lesson:

## Context and Orientation

Describe the current system state, key files, terms, and constraints as if the
reader knows nothing about the repo.

## Plan of Work

Describe the sequence of changes in prose. Name exact files, modules, and
surfaces to edit.

## Concrete Steps

List exact commands, working directories, and expected observations.

## Validation and Acceptance

Describe:

    - test commands
    - Playwright journeys
    - CDP checks
    - Loki or log-backend queries
    - metrics or trace checks when relevant

## Idempotence and Recovery

Describe which steps are safe to rerun and how to recover from partial failure.

## Artifacts and Notes

Record paths for:

    - screenshots
    - videos
    - Playwright reports
    - DOM snapshots
    - console captures
    - log query output
    - metric or trace captures

## Interfaces and Dependencies

List the interfaces, contracts, libraries, providers, and service boundaries the
task depends on or creates.
```

