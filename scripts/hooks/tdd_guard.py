#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_runtime.engine import WorkflowService  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run TDD Guard")
    parser.add_argument("--task-id")
    parser.add_argument("--phase-id")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()

    service = WorkflowService()
    task = service.load_task(args.task_id) if args.task_id else None
    phase = None
    if args.task_id and args.phase_id:
        _, _, phase = service.current_phase(args.task_id, args.phase_id)
    elif task and task["active_phase_id"]:
        _, _, phase = service.current_phase(args.task_id, task["active_phase_id"])

    changed_paths = list(args.changed_path)
    if args.staged:
        changed_paths.extend(service.staged_or_worktree_paths(staged=True))
    result = service.tdd_guard(sorted(set(changed_paths)), phase)
    print(json.dumps(result.as_payload(), indent=2, ensure_ascii=False))
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
