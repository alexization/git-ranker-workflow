---
summary: Analysis of OpenAI's PLANS.md article and how it is adapted here.
read_when:
  - writing or reviewing an ExecPlan
  - deciding what a self-contained plan must include
---

# OpenAI ExecPlans analysis

Source:

- https://developers.openai.com/cookbook/articles/codex_exec_plans

## Extracted rules

- plans are for multi-hour or multi-session work
- plans are living documents
- plans must be self-contained for a novice reader
- plans must describe observable outcomes
- plans must track progress, discoveries, decisions, and retrospective outcomes

## Adaptation in this repository

The generic OpenAI structure is extended with repository-specific requirements:

- impacted repo list
- task runtime slug
- explicit frontend/backend contract notes
- Playwright, CDP, and log-query evidence
- recovery notes for cross-repo or environment failures

## Why the adaptation is needed

This repository coordinates two separately versioned repos. A plan that only
describes code edits is not enough. It must also describe the integration
surface, the QA harness, and the observability evidence that proves the change
worked across the system.

