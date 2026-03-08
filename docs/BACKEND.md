---
summary: Backend implementation, contract, and observability rules for git-ranker.
read_when:
  - working in the backend repo
  - modifying APIs, jobs, persistence, or ranking logic
---

# Backend

## Current repo facts

- framework: Spring Boot 3.4
- language/runtime: Java 21
- architecture hints: domain, infrastructure, global, and batch packages
- observability already present: Actuator, Prometheus endpoint, structured
  logback JSON encoder, trace-id MDC support
- test stack already present: JUnit 5, Testcontainers, ArchUnit, Jacoco

## What agents must optimize for

- explicit contracts
- narrow IO boundaries
- observable behavior
- safe migrations
- reproducible startup and request behavior

## Required workflow for backend changes

1. Define the affected contract and acceptance behavior.
2. Identify the layer changes required: contract, repository, service, runtime.
3. Implement the change.
4. Run backend build and tests.
5. Boot the isolated task runtime.
6. Exercise the changed API or worker path.
7. Query logs, metrics, and traces for the affected path.
8. Record evidence and findings in the ExecPlan.

## Contract rules

- Parse inputs at the boundary.
- Version or clearly document contract changes.
- Never let controllers or handlers own business logic.
- Prefer explicit repositories or gateways over ad hoc IO scattered through the
  codebase.

## Observability bar

Every important backend change should leave behind:

- structured log evidence for the changed flow
- at least one metric or timing check for latency-sensitive paths
- trace evidence when multiple async steps or external calls are involved
- a note describing which log query proves the behavior worked

## Expected commands to codify

- `./gradlew build`
- `./gradlew test`
- `./gradlew integrationTest` when Docker-backed integration coverage matters
