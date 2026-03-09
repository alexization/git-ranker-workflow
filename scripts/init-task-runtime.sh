#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  printf 'usage: %s <task-slug>\n' "$0" >&2
  exit 1
fi

slug="$1"
runtime_dir=".runtime/$slug"
env_file="$runtime_dir/task.env"

mkdir -p "$runtime_dir/logs"
mkdir -p "$runtime_dir/metrics"
mkdir -p "$runtime_dir/screenshots"
mkdir -p "$runtime_dir/videos"
mkdir -p "$runtime_dir/playwright"
mkdir -p "$runtime_dir/observability"
mkdir -p ".worktrees/backend"
mkdir -p ".worktrees/frontend"

if [ ! -f "$env_file" ]; then
  sed "s/^TASK_SLUG=.*/TASK_SLUG=$slug/" harness/task.env.example > "$env_file"
fi

printf 'initialized task runtime: %s\n' "$runtime_dir"
printf 'environment file: %s\n' "$env_file"
