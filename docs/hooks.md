# Hooks

## Policy

Hooks are intentionally light. The SDD harness should guide implementation through `spec.md`, `state.json`, and verification commands instead of blocking ordinary development activity at commit time.

## Active Guards

### Dangerous Command Guard

- Runs for `pre_command` and `pre_push`.
- Blocks destructive shell patterns such as `git reset --hard`, `git clean -fd`, force push, and destructive SQL.
- Used by `verify` before command execution and by `.githooks/pre-push`.

### User Validation Guard

- Runs for `pre_complete`.
- Requires `review --close --user-validation-note ...` before a task can become `completed`.

## Removed Guards

- pre-commit write-scope guard
- pre-commit TDD guard
- latest verified run pre-push guard
- circuit breaker
- phase kickoff proof

Testing is still required, but it is expressed through IMP verification commands and recorded in `state.json` instead of being enforced by git hooks.
