---
summary: Analysis of OpenAI's February 11, 2026 harness-engineering article and how it maps to this repo.
read_when:
  - understanding why this repository is structured this way
  - checking whether a workflow rule is grounded in the source article
---

# OpenAI harness-engineering analysis

Source:

- https://openai.com/index/harness-engineering/

## Extracted operating principles

1. Start from an empty repo and make the environment, not the human, do the
   heavy lifting.
2. Treat repository-local knowledge as the system of record.
3. Keep `AGENTS.md` short and use it as a map into richer docs.
4. Increase agent legibility through bootable isolated runtimes, browser
   inspection, and queryable observability.
5. Enforce architecture and taste mechanically instead of depending on memory.
6. Prefer fast correction loops over heavyweight blocking gates.
7. Continuously garbage-collect drift through explicit quality rules.

## Direct mappings in this repository

- `AGENTS.md` is intentionally short and points into `docs/`.
- `docs/` mirrors the knowledge-store layout described in the article.
- `PLANS.md` and `docs/exec-plans/` provide the living-document execution model.
- `harness/` is reserved for per-task runtime and observability wiring.
- `docs/workflows/qa-feedback-loop.md` encodes the Playwright plus CDP plus log
  analysis loop.
- `docs/QUALITY_SCORE.md` and `docs/exec-plans/tech-debt-tracker.md` encode the
  continuous cleanup model.

## Important nuance

The article describes a single large app repository. This project is split into
two application repositories plus one orchestration repository. The adaptation
here is to make the control plane live in this repo while keeping application
logic in the backend and frontend repos.

