# Runbook

## Initialize

```bash
python3 scripts/workflow.py init
python3 scripts/workflow.py doctor
```

`init` creates the minimal runtime surface and configures `.githooks/pre-push`. Pre-commit hooks are not used.

## Create A Task

```bash
python3 scripts/workflow.py new task-001 --title "..." --primary-repo git-ranker-workflow
```

Edit `workflows/tasks/task-001/spec.md` through a Socratic clarification loop. The spec is not executable while any clarification has `Status: open`.

## Approve And Plan

After presenting the spec confirmation summary to the user:

```bash
python3 scripts/workflow.py approve task-001 --note "user approved spec"
python3 scripts/workflow.py plan task-001
```

`approve` locks the spec hash. `plan` reads the `IMP-*` scopes from `spec.md` and initializes `state.json`.

## Implement

```bash
python3 scripts/workflow.py run task-001 --start
python3 scripts/workflow.py run task-001 --complete --changed-path path/to/file
```

Use `--imp-id IMP-02` when starting or completing a specific implementation scope.

## Verify

```bash
python3 scripts/workflow.py verify task-001
python3 scripts/workflow.py verify task-001 --imp-id IMP-01 --verify-command "python3 -m unittest discover -s tests -v"
```

Verification results are written to `state.json`.

## Review And Close

```bash
python3 scripts/workflow.py review task-001 --note "ready for user validation"
python3 scripts/workflow.py review task-001 --close --user-validation-note "validated by user"
```

Completion is impossible without a user validation note.

## Repair

```bash
python3 scripts/workflow.py reopen task-001 --note "additional requirement" --imp-id IMP-02
```

Reopen resets the target IMP and downstream IMPs to `pending`.
