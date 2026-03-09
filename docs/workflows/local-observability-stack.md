---
summary: Local per-task observability model using Loki, Prometheus, and Grafana.
read_when:
  - setting up the task runtime
  - deciding where logs and metrics should go
---

# Local Observability Stack

## Goal

Mirror the agent-facing observability workflow described by OpenAI:

- one isolated observability context per task
- logs and metrics queryable by the agent
- disposable runtime after the task completes

## Implementation choice

OpenAI's article describes queryable local observability. This repository uses
Loki, Prometheus, and Grafana as the default local stack for self-hosted
development.

Because the operating environment is a single-server deployment, the default
workflow intentionally does not include Tempo or distributed tracing.

## Directory contract

```text
.runtime/<task-slug>/
  logs/
  metrics/
  observability/
```

## Required labels

Every emitted signal should carry at least:

- `task_slug`
- `service`
- `repo`
- `environment=local`

## Example queries

### LogQL

```text
{task_slug="<task-slug>",service="backend"} |= "startup complete"
```

### PromQL

```text
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{task_slug="<task-slug>"}[5m])))
```

## Config location

See `harness/observability/`.

## Current project-specific wiring

- backend metrics are available from Spring Actuator on port `9090` at
  `/actuator/prometheus`
- backend logs are already structured through `logback-spring.xml`
- frontend metrics export is not yet committed as part of the client repo, so
  the harness keeps that piece generic for now
