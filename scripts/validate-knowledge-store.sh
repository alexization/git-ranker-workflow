#!/usr/bin/env sh
set -eu

required_files='
AGENTS.md
ARCHITECTURE.md
PLANS.md
harness/README.md
harness/task.env.example
harness/observability/docker-compose.yml
scripts/bootstrap-submodules.sh
docs/index.md
docs/DESIGN.md
docs/FRONTEND.md
docs/BACKEND.md
docs/PRODUCT_SENSE.md
docs/QUALITY_SCORE.md
docs/RELIABILITY.md
docs/SECURITY.md
docs/design-docs/index.md
docs/product-specs/index.md
docs/exec-plans/README.md
docs/exec-plans/_template.md
docs/generated/README.md
docs/workflows/feature-delivery-loop.md
docs/workflows/qa-feedback-loop.md
docs/workflows/local-observability-stack.md
'

missing=0

for file in $required_files; do
  if [ ! -f "$file" ]; then
    printf 'missing required file: %s\n' "$file" >&2
    missing=1
  fi
done

if [ ! -d "docs/exec-plans/active" ]; then
  printf 'missing required directory: docs/exec-plans/active\n' >&2
  missing=1
fi

if [ ! -d "docs/exec-plans/completed" ]; then
  printf 'missing required directory: docs/exec-plans/completed\n' >&2
  missing=1
fi

if [ "$missing" -ne 0 ]; then
  exit 1
fi

printf 'knowledge store validation passed\n'
