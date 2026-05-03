from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable


SOURCE_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SURFACE_FILES = (
    Path(".githooks/pre-push"),
    Path("workflows/system/hooks.json"),
)


def current_hooks_path(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "config", "--local", "--get", "core.hooksPath"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def runtime_surface_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in RUNTIME_SURFACE_FILES:
        target = root / relative
        source = SOURCE_ROOT / relative
        if not target.exists():
            errors.append(f"missing canonical artifact: {relative}")
            continue
        if source.exists() and target.read_bytes() != source.read_bytes():
            errors.append(f"{relative} is out of sync with source; run `python3 scripts/workflow.py init`")
    return errors


def build_doctor_report(
    root: Path,
    *,
    load_hooks_config: Callable[[], dict[str, Any]],
    check_all: Callable[[], list[str]],
) -> dict[str, Any]:
    checks: list[str] = []
    errors: list[str] = []

    load_hooks_config()
    checks.append("workflow system hook config is readable")

    hooks_path = current_hooks_path(root)
    if hooks_path == ".githooks":
        checks.append("git core.hooksPath points to .githooks")
    elif hooks_path is None:
        checks.append("git core.hooksPath is not configured; hooks are optional in the simplified SDD harness")
    else:
        errors.append(f"git core.hooksPath must be .githooks or unset, got: {hooks_path}")

    task_errors = check_all()
    if task_errors:
        errors.extend(task_errors)
    else:
        checks.append("task artifacts are internally consistent")

    runtime_errors = runtime_surface_errors(root)
    if runtime_errors:
        errors.extend(runtime_errors)
    else:
        checks.append("runtime surface matches source")

    return {"status": "failed" if errors else "passed", "checks": checks, "errors": errors}
