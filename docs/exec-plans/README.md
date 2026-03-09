---
summary: How ExecPlans are stored and maintained in this repository.
read_when:
  - creating or resuming a non-trivial task
---

# Exec Plans

## Layout

- `active/`: plans that are still being executed
- `completed/`: plans whose work and retrospective are complete
- `_template.md`: starting point for new plans
- `tech-debt-tracker.md`: backlog of durable issues discovered by the workflow

## Naming

`<yyyy-mm-dd>-<slug>.md`

Example:

`2026-03-07-ranking-filter-panel.md`

## Workflow

1. Create from `_template.md`.
2. Fill in the request intake and context before coding.
3. Update `Progress`, `Decision Log`, and `Surprises & Discoveries` during work.
4. Record artifact paths for Playwright, CDP, logs, and metrics when relevant.
5. Move the plan to `completed/` when the work and retrospective are finished.
