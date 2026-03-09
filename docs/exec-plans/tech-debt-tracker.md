---
summary: Durable debt surfaced by the AI workflow and not yet encoded away.
read_when:
  - deciding whether to open a cleanup plan
  - looking for recurring workflow friction
---

# Tech Debt Tracker

## Open items

### 1. Generated fact pipelines are not implemented

- Problem: `docs/generated/` is defined but not populated automatically.
- Consequence: agents must still read code directly for many repo facts.
- Desired fix: add generators for API surface, schema, route map, and dependency
  graph documents.

### 2. Harness command wiring is still generic

- Problem: the workflow defines Playwright/CDP/Loki loops, but the exact app
  commands are not yet wired to this project's real scripts.
- Consequence: the docs are operationally ready, but runtime automation still
  needs repo-specific command binding.
- Desired fix: codify build, start, and test commands in `harness/` and
  verification scripts.

### 3. Frontend automated QA harness is missing from the repo

- Problem: `git-ranker-client` currently has no committed Playwright config or
  frontend test files.
- Consequence: the OpenAI-style browser feedback loop cannot yet be enforced by
  code in the frontend repo itself.
- Desired fix: add Playwright, artifact paths, and at least one critical user
  journey spec to `git-ranker-client`.
