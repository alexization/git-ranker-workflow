#!/usr/bin/env sh
set -eu

git submodule sync --recursive
git submodule update --init --recursive

printf 'submodule bootstrap complete\n'
