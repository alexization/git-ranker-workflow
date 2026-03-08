#!/usr/bin/env sh
set -eu

./scripts/validate-knowledge-store.sh

if ./scripts/check-submodules.sh; then
  printf 'workflow verification passed\n'
else
  printf 'workflow verification is partial: submodules are not initialized\n' >&2
  exit 2
fi
