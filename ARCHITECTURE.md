# git-ranker Workflow Architecture

## Purpose

This repository is the orchestration layer for an agent-first development
workflow across two application repositories:

- `git-ranker`: backend system of record for APIs, jobs, persistence, and domain
  rules
- `git-ranker-client`: frontend system of record for routes, components, user
  flows, and client-side state

The control plane in this repo exists to make the product legible to coding
agents, not to store application logic.

## Current repo facts

When the application repositories are checked out, this workflow assumes these
high-level facts:

- backend: Spring Boot 3.4, Java 21, JPA, Batch, Security, Actuator, Prometheus,
  structured JSON logging, Testcontainers, ArchUnit
- frontend: Next.js App Router, React 19, TypeScript, ESLint, React Query,
  Zustand, Tailwind, Radix UI

Those facts should shape the workflow and harness choices instead of generic
defaults.

## Core principle

Repository-local knowledge is the system of record. A coding agent should be
able to understand the product, architecture, quality bar, and execution flow
from versioned artifacts in this repository plus the checked-out submodules.

## Control-plane flow

```text
feature request
  -> request intake and acceptance contract
  -> ExecPlan for non-trivial work
  -> backend contract / behavior changes
  -> frontend integration / UI changes
  -> isolated task runtime
  -> Playwright + CDP validation
  -> logs / metrics review
  -> fix loop
  -> PR / merge / debt update
```

## Worktree model

Every non-trivial task should use an isolated runtime footprint keyed by a task
slug, for example `rank-comparison-filtering`.

Expected layout:

```text
.worktrees/
  backend/<task-slug>/
  frontend/<task-slug>/
.runtime/
  <task-slug>/
    logs/
    metrics/
    screenshots/
    videos/
    playwright/
    observability/
```

The goal matches OpenAI's harness model:

- one isolated app instance per task
- one isolated observability context per task
- artifacts are disposable once the task is complete

## Knowledge-store layout

```text
AGENTS.md
ARCHITECTURE.md
PLANS.md
docs/
  design-docs/
  exec-plans/
  generated/
  product-specs/
  references/
  workflows/
```

`AGENTS.md` is only the table of contents. The durable knowledge lives in
`docs/`.

## Cross-repo contract

The repositories are versioned independently, but the workflow treats them as a
single product system. A change request must identify which of the following are
affected:

- backend domain rules
- backend API or event contracts
- frontend route or component behavior
- shared product language and acceptance criteria
- reliability, security, or QA evidence

Any contract change must update both sides of the boundary plus the knowledge
store if the change affects future tasks.

## Layering model

The two repos should converge on one directional dependency model:

```text
Types -> Schemas/Contracts -> Repository/Gateway -> Service/Use Case
      -> Runtime/Delivery -> UI or HTTP surface

Cross-cutting concerns enter only through Providers:
auth, feature flags, telemetry, configuration, external connectors
```

This is intentionally rigid. Agents move faster when the allowed edges are
obvious and mechanically enforceable.

## QA and observability loop

Every user-visible change is expected to produce:

- automated regression evidence
- a Playwright run over the affected journey
- CDP evidence for DOM, console, network, and screenshot state
- log evidence from the isolated task runtime
- metric evidence when performance or throughput matters

The recommended local stack is documented in
[docs/workflows/local-observability-stack.md](docs/workflows/local-observability-stack.md).
The implementation provided in `harness/` uses Loki, Prometheus, and Grafana to
preserve an agent-facing query model for logs and metrics with LogQL and
PromQL.

## What stays out of this repo

- application code that belongs in `git-ranker` or `git-ranker-client`
- private tribal knowledge that should instead be turned into docs
- ad hoc task notes that never graduate into reusable rules

## Current limitations

- the frontend repo does not yet contain committed Playwright or test config
- the harness knows the backend metrics endpoint, but frontend metrics export
  wiring is still generic
- repo-specific start scripts and local env bootstrapping still need to be
  codified into the harness
