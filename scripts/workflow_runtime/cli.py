from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from workflow_runtime.engine import WorkflowService
from workflow_runtime.models import WorkflowError, emit, read_json


def read_phase_source(source_path: str | None, use_stdin: bool) -> Any:
    if source_path and use_stdin:
        raise WorkflowError("plan accepts only one input source")
    if source_path:
        path = Path(source_path)
        if not path.exists():
            raise WorkflowError(f"phase input file not found: {source_path}")
        try:
            return read_json(path)
        except json.JSONDecodeError as exc:
            raise WorkflowError(f"invalid JSON file: {source_path}") from exc
    if use_stdin:
        text = sys.stdin.read().strip()
        if not text:
            raise WorkflowError("stdin phase input is empty")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise WorkflowError(f"invalid JSON from stdin: {exc.msg}") from exc
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Workflow control plane CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init")
    subparsers.add_parser("doctor")

    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("task_id")
    new_parser.add_argument("--title", required=True)
    new_parser.add_argument("--primary-repo", required=True)

    approve_parser = subparsers.add_parser("approve")
    approve_parser.add_argument("task_id")
    approve_parser.add_argument("--note", required=True)
    approve_parser.add_argument("--actor", default="user")

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("task_id")
    plan_parser.add_argument("--from", dest="source_path")
    plan_parser.add_argument("--stdin", action="store_true")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("task_id")
    run_parser.add_argument("--phase-id")
    run_parser.add_argument("--start", action="store_true")
    run_parser.add_argument("--complete", action="store_true")
    run_parser.add_argument("--fail", action="store_true")
    run_parser.add_argument("--block", action="store_true")
    run_parser.add_argument("--changed-path", action="append", default=[])
    run_parser.add_argument("--note")
    run_parser.add_argument("--evidence", action="append", default=[])
    run_parser.add_argument("--error-fingerprint")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("task_id")
    verify_parser.add_argument("--phase-id")
    verify_parser.add_argument("--verify-command", action="append", default=[])
    verify_parser.add_argument("--evidence", action="append", default=[])

    review_parser = subparsers.add_parser("review")
    review_parser.add_argument("task_id")
    review_parser.add_argument("--note")
    review_parser.add_argument("--close", action="store_true")
    review_parser.add_argument("--user-validation-note")

    reopen_parser = subparsers.add_parser("reopen")
    reopen_parser.add_argument("task_id")
    reopen_parser.add_argument("--note", required=True)
    reopen_parser.add_argument("--phase-id")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("task_id", nargs="?")
    status_parser.add_argument("--all", action="store_true")
    status_parser.add_argument("--check", action="store_true")
    status_parser.add_argument("--field")
    status_parser.add_argument("--infer-active-task", action="store_true")

    hook_parser = subparsers.add_parser("hook")
    hook_parser.add_argument("event")
    hook_parser.add_argument("--task-id")
    hook_parser.add_argument("--phase-id")
    hook_parser.add_argument("--command-text")
    hook_parser.add_argument("--changed-path", action="append", default=[])
    hook_parser.add_argument("--staged", action="store_true")
    hook_parser.add_argument("--worktree", action="store_true")
    hook_parser.add_argument("--user-validation-note")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = WorkflowService()
    service.ensure_layout()

    try:
        if args.command == "init":
            emit(service.init_workspace())
            return 0

        if args.command == "doctor":
            report = service.doctor_report()
            emit(report)
            return 0 if report["status"] == "passed" else 1

        if args.command == "new":
            service.new_task(args.task_id, args.title, args.primary_repo)
            emit({"status": "created", "task_id": args.task_id})
            return 0

        if args.command == "approve":
            service.approve_task(args.task_id, args.note, args.actor)
            emit({"status": "approved", "task_id": args.task_id})
            return 0

        if args.command == "plan":
            service.plan_task(args.task_id, read_phase_source(args.source_path, args.stdin))
            emit({"status": "planned", "task_id": args.task_id})
            return 0

        if args.command == "run":
            if args.complete:
                service.complete_phase(args.task_id, args.phase_id, args.changed_path, args.note, args.evidence)
                emit({"status": "completed", "task_id": args.task_id})
                return 0
            if args.fail:
                code = service.fail_phase(args.task_id, args.phase_id, args.error_fingerprint, args.note)
                emit({"status": "failed" if code == 1 else "blocked", "task_id": args.task_id})
                return code
            if args.block:
                service.block_phase(args.task_id, args.phase_id, args.note)
                emit({"status": "blocked", "task_id": args.task_id})
                return 2
            service.start_phase(args.task_id, args.phase_id)
            emit({"status": "started", "task_id": args.task_id})
            return 0

        if args.command == "verify":
            code = service.verify_task(args.task_id, args.phase_id, args.verify_command or None, args.evidence)
            emit({"status": "passed" if code == 0 else ("blocked" if code == 2 else "failed"), "task_id": args.task_id})
            return code

        if args.command == "review":
            if args.close:
                if not args.user_validation_note:
                    raise WorkflowError("--close requires --user-validation-note")
                service.close_review(args.task_id, args.user_validation_note)
                emit({"status": "completed", "task_id": args.task_id})
                return 0
            service.review_task(args.task_id, args.note)
            emit({"status": "review_ready", "task_id": args.task_id})
            return 0

        if args.command == "reopen":
            service.reopen_task(args.task_id, args.note, args.phase_id)
            emit({"status": "approved", "task_id": args.task_id})
            return 0

        if args.command == "status":
            if args.infer_active_task:
                task_id = service.infer_active_task() or ""
                if args.field:
                    raise WorkflowError("--field is not supported with --infer-active-task")
                print(task_id)
                return 0
            if args.check:
                errors = service.check_all()
                if errors:
                    emit({"status": "failed", "errors": errors})
                    return 1
                emit({"status": "passed", "tasks": sorted([p.name for p in service.tasks_dir.iterdir() if p.is_dir()])})
                return 0
            if args.all:
                payload = {
                    "tasks": [
                        service.load_task(path.name)
                        for path in sorted(service.tasks_dir.iterdir())
                        if path.is_dir() and (path / "task.json").exists()
                    ]
                }
                emit(payload)
                return 0
            if not args.task_id:
                raise WorkflowError("status requires task_id unless --all or --check is used")
            payload = service.status_payload(args.task_id)
            if args.field:
                task = payload["task"]
                if args.field not in task:
                    raise WorkflowError(f"unknown task field: {args.field}")
                value = task[args.field]
                if isinstance(value, (dict, list)):
                    print(json.dumps(value, ensure_ascii=False))
                else:
                    print("" if value is None else value)
                return 0
            emit(payload)
            return 0

        if args.command == "hook":
            task = service.load_task(args.task_id) if args.task_id else None
            phase = None
            if args.task_id and args.phase_id:
                _, _, phase = service.current_phase(args.task_id, args.phase_id)
            elif args.task_id and task and task["active_phase_id"]:
                _, _, phase = service.current_phase(args.task_id, task["active_phase_id"])

            changed_paths = list(args.changed_path)
            if args.staged:
                changed_paths.extend(service.staged_or_worktree_paths(staged=True))
            if args.worktree:
                changed_paths.extend(service.staged_or_worktree_paths(staged=False))
            if args.event == "pre_push" and not changed_paths:
                changed_paths.extend(service.unpushed_paths())

            result = service.run_hooks(
                args.event,
                task=task,
                phase=phase,
                changed_paths=service.normalize_changed_paths(changed_paths),
                command=args.command_text,
                user_validation_note=args.user_validation_note,
            )
            emit(result.as_payload())
            return 0 if result.status == "passed" else 1

    except WorkflowError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0
