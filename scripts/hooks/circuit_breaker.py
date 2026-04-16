#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_runtime.engine import WorkflowService  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a failure fingerprint")
    parser.add_argument("--error-fingerprint", required=True)
    args = parser.parse_args()

    service = WorkflowService()
    result = service.record_circuit_breaker(args.error_fingerprint)
    print(json.dumps(result.as_payload(), indent=2, ensure_ascii=False))
    return 0 if result.status != "blocked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
