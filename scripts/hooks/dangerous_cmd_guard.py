#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_runtime.engine import WorkflowService  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Dangerous Command Guard")
    parser.add_argument("--command", required=True)
    args = parser.parse_args()

    service = WorkflowService()
    result = service.dangerous_cmd_guard(args.command)
    print(json.dumps(result.as_payload(), indent=2, ensure_ascii=False))
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
