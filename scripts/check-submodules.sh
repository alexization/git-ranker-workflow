#!/usr/bin/env sh
set -eu

check_dir() {
  path="$1"

  if [ ! -d "$path" ]; then
    printf 'missing directory: %s\n' "$path" >&2
    return 1
  fi

  if [ -z "$(find "$path" -mindepth 1 -maxdepth 1 2>/dev/null)" ]; then
    printf 'submodule appears uninitialized: %s\n' "$path" >&2
    return 2
  fi

  printf 'submodule looks populated: %s\n' "$path"
}

status=0
check_dir git-ranker || status=$?
check_dir git-ranker-client || status=$?
exit "$status"

