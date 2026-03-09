# Harness

This directory contains the local runtime and observability skeleton for the
OpenAI-style harness workflow used by this repository.

## What lives here

- `task.env.example`: environment template for a task-scoped runtime
- `observability/`: Docker Compose and config for Loki, Prometheus, and Grafana

## Suggested flow

1. Create a task runtime:

       ./scripts/init-task-runtime.sh <task-slug>

2. Review and adjust `.runtime/<task-slug>/task.env`.

3. Start the observability stack:

       docker compose \
         --env-file .runtime/<task-slug>/task.env \
         -f harness/observability/docker-compose.yml \
         up -d

4. Start backend and frontend using the same task slug and matching ports.

5. Run Playwright, inspect with CDP, and query the local stack.

## Current state

The config is intentionally generic because the repo-specific build, start, and
test commands are not yet codified into this harness. Once those commands are
standardized, bind their log and metric endpoints into this harness.
