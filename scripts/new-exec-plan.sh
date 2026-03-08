#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  printf 'usage: %s <slug>\n' "$0" >&2
  exit 1
fi

slug="$1"
date_prefix="$(date +%F)"
target="docs/exec-plans/active/${date_prefix}-${slug}.md"

if [ -e "$target" ]; then
  printf 'plan already exists: %s\n' "$target" >&2
  exit 1
fi

cp docs/exec-plans/_template.md "$target"
printf 'created %s\n' "$target"

