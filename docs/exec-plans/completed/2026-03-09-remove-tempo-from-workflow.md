```md
# Remove Tempo From The Default Workflow

This ExecPlan is a living document. Maintain it according to `PLANS.md` at the
repository root.

## Purpose / Big Picture

Remove Grafana Tempo and distributed-tracing expectations from the default local
workflow so the control plane matches the product's single-server operating
model.

Request intake:

    Problem:
    The current workflow and harness assume Tempo-backed tracing analysis even
    though the operating environment is a single-server deployment.
    User-visible outcome:
    Workflow guidance and local observability setup focus on logs and metrics,
    not Tempo or trace analysis.
    Affected repos:
    knowledge-store only
    Contract surface:
    Workflow docs, ExecPlan template language, local observability harness, and
    runtime scaffolding.
    Acceptance checks:
    Tempo is no longer part of the local observability stack, and workflow docs
    no longer require trace evidence for normal task validation.
    QA evidence:
    `./scripts/verify-workflow.sh`
    targeted diff review for docs and harness files
    Non-goals:
    Changing backend application code or removing Playwright trace artifacts.
    Risks:
    Removing too much observability guidance could make performance debugging
    weaker if logs and metrics are not described clearly enough.

Task runtime slug:

    remove-tempo-from-workflow

## Progress

- [x] Collected Tempo and trace references across workflow docs and harness files
  on 2026-03-09.
- [x] Update docs to align the workflow with logs-and-metrics observability.
- [x] Remove Tempo from the local observability harness and runtime scaffold.
- [x] Re-run workflow verification and record outcomes.

## Surprises & Discoveries

- Observation:
  Tempo is wired not only in docs but also in the Grafana datasource
  provisioning, runtime env file, and task-runtime scaffold.
  Evidence:
  `rg` results across `docs/`, `harness/`, and `scripts/`.

## Decision Log

- Decision:
  Keep Playwright traces as test artifacts, but remove Tempo and distributed
  tracing from the observability workflow.
  Rationale:
  The user wants single-server observability to focus on logs and metrics, not
  Grafana Tempo.
  Date/Author:
  2026-03-09 / Codex

## Outcomes & Retrospective

- Outcome:
  Completed. The default workflow now treats logs and metrics as the local
  observability baseline, and the Tempo service plus datasource wiring have been
  removed from the harness.
  Remaining gap:
  Playwright traces remain available as test artifacts, but Grafana Tempo and
  distributed tracing are no longer part of the default workflow.
  Lesson:
  The workflow should follow the actual operating topology rather than copying
  every capability from a reference implementation.

## Context and Orientation

The current control-plane docs adapt OpenAI's harness article and include
Tempo/TraceQL language. In this project, the operating environment is not
distributed, so the default workflow should not require distributed tracing.
The main change surface is documentation plus the harness files under
`harness/observability/`.

## Plan of Work

Update the workflow, architecture, reliability, backend, and ExecPlan docs so
they ask for logs and metrics rather than Tempo-based tracing evidence. Remove
Tempo from the local Docker Compose stack, Grafana datasource provisioning, task
env template, and task runtime bootstrap script. Keep Playwright trace artifacts
untouched because they are test outputs, not Grafana Tempo traces.

## Concrete Steps

Update:

    AGENTS.md
    ARCHITECTURE.md
    PLANS.md
    docs/workflows/feature-delivery-loop.md
    docs/workflows/qa-feedback-loop.md
    docs/workflows/local-observability-stack.md
    docs/BACKEND.md
    docs/RELIABILITY.md
    docs/design-docs/core-beliefs.md
    docs/exec-plans/README.md
    docs/exec-plans/_template.md
    docs/product-specs/request-intake.md
    harness/README.md
    harness/task.env.example
    harness/observability/docker-compose.yml
    harness/observability/grafana/provisioning/datasources/datasources.yml
    scripts/init-task-runtime.sh

Delete:

    harness/observability/tempo.yml

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
    - metrics checks when relevant: not applicable

## Idempotence and Recovery

The doc and harness edits are safe to rerun. If Tempo is ever needed again, it
can be restored from git history together with the removed workflow language.

## Artifacts and Notes

Record paths for:

    - verification output: ./scripts/verify-workflow.sh -> passed on 2026-03-09

## Interfaces and Dependencies

This task depends on the workflow docs, the local observability harness, and the
task-runtime bootstrap script. It intentionally leaves application-repo code and
Playwright artifact behavior unchanged.
```
