---
summary: End-to-end feature workflow from user request to QA feedback loop.
read_when:
  - starting a feature
  - deciding what the next task phase should be
---

# Feature Delivery Loop

## Phase 1: Intake

Convert the request into the shape defined in
[../product-specs/request-intake.md](../product-specs/request-intake.md).

## Phase 2: Plan

For any non-trivial task, create an ExecPlan. The plan becomes the living record
for progress, discoveries, decisions, evidence, and outcomes.

## Phase 3: Implement

Make the smallest set of backend and frontend changes that satisfy the plan
while preserving the architectural layer rules.

## Phase 4: Verify locally

Run build, typecheck, lint, and automated tests in the affected repos.

## Phase 5: Boot isolated runtime

Launch the backend, frontend, and observability stack for the task-specific
runtime slug.

## Phase 6: QA

Run Playwright for the changed user journeys. Inspect the final UI and network
state using CDP tooling.

## Phase 7: Observe

Query the isolated runtime's logs and metrics. Confirm the system
behavior matches the plan, not just the UI.

## Phase 8: Feedback

If QA or observability reveals a gap:

- update code
- update the ExecPlan
- rerun the relevant checks
- capture the new evidence

## Phase 9: Retrospective

At the end of the task:

- update `Outcomes & Retrospective`
- promote durable lessons into docs or scripts
- add remaining debt to the tracker if it cannot be fixed now
