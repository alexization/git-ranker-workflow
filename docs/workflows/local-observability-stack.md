---
summary: Local per-task observability model using Loki, Prometheus, Tempo, and Grafana.
read_when:
  - setting up the task runtime
  - deciding where logs, metrics, and traces should go
---

# Local Observability Stack

## Goal

Mirror the agent-facing observability workflow described by OpenAI:

- one isolated observability context per task
- logs, metrics, and traces queryable by the agent
- disposable runtime after the task completes

## Implementation choice

OpenAI's article describes local queryable logs, metrics, and traces with
LogQL, PromQL, and TraceQL. This repository uses Loki, Prometheus, Tempo, and
Grafana as a practical equivalent for self-hosted local development.

This is an implementation inference, not a direct quote from OpenAI.

## Directory contract

```text
.runtime/<task-slug>/
  logs/
  metrics/
  traces/
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

### TraceQL

```text
{ resource.task_slug = "<task-slug>" } | duration > 2s
```

## Config location

See `harness/observability/`.

## Current project-specific wiring

- backend metrics are available from Spring Actuator on port `9090` at
  `/actuator/prometheus`
- backend logs are already structured through `logback-spring.xml`
- frontend metrics and trace export are not yet committed as part of the client
  repo, so the harness keeps those pieces generic for now
