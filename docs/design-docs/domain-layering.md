---
summary: Required dependency direction and layer meanings across backend and frontend.
read_when:
  - adding a new module
  - reviewing dependency direction
  - designing cross-repo contracts
---

# Domain Layering

## Dependency direction

All code should depend only in the following forward direction:

```text
Types -> Schemas/Contracts -> Repository/Gateway -> Service/Use Case
      -> Runtime/Delivery -> UI or HTTP surface
```

Cross-cutting concerns enter only through explicitly named provider interfaces:

- auth providers
- feature-flag providers
- telemetry providers
- config providers
- external connector providers

No other reverse or sideways dependencies are allowed.

## Layer meaning

### Types

Pure domain types and names. No IO. No framework imports.

### Schemas/Contracts

Validation rules, request/response shapes, event payloads, serialized forms, and
frontend/backend contract models.

### Repository/Gateway

Persistence or remote access layers. Database clients, HTTP clients, queues, and
third-party APIs live here behind narrow interfaces.

### Service/Use Case

Business logic. The place where ranking behavior, orchestration, and policy are
implemented.

### Runtime/Delivery

The runtime boundary that wires providers and use cases into the actual program.
Examples:

- backend handlers, jobs, schedulers
- frontend loaders, route state wiring, query orchestration

### UI or HTTP surface

The final user or network surface:

- frontend components and route shells
- backend controllers, route modules, or transport handlers

## Repo-specific mapping

### `git-ranker` backend

- Types: domain entities and value objects
- Schemas/Contracts: DTOs, validation schemas, API contracts, job payloads
- Repository/Gateway: DB access, cache, queue, external API connectors
- Service/Use Case: ranking algorithms, workflows, business rules
- Runtime/Delivery: route wiring, workers, scheduled tasks
- HTTP surface: API endpoints and transport adapters

### `git-ranker-client` frontend

- Types: view-agnostic domain models
- Schemas/Contracts: API client contracts, form schemas, router payloads
- Repository/Gateway: API clients and local persistence adapters
- Service/Use Case: client-side orchestration and derived state logic
- Runtime/Delivery: route loaders, providers, suspense/query setup
- UI surface: pages, sections, components, and interaction handlers

## Guardrails to encode later

These rules should eventually become lint rules or structural tests:

- boundary parsing happens at contracts, not ad hoc in UI or handlers
- services may not import UI modules
- repositories may not import runtime or surface layers
- no direct third-party IO from UI or business logic
- cross-repo contracts must be named and versioned explicitly

