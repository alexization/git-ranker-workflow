from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable, Iterable

from workflow_runtime.constants import (
    AGENTS_REQUIRED_HEADINGS,
    AGENTS_REQUIRED_KEYWORDS,
    DOC_FILES,
    DOC_REQUIRED_MARKERS,
    STALE_REFERENCE_PATTERNS,
    STALE_REFERENCE_SCAN_EXCLUDES,
)


def validate_agents_constitution(agents_path: Path) -> list[str]:
    text = agents_path.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []
    for heading in AGENTS_REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"AGENTS.md missing heading: {heading}")
    for keyword in AGENTS_REQUIRED_KEYWORDS:
        if keyword not in text:
            errors.append(f"AGENTS.md missing constitution marker: {keyword}")
    return errors


def validate_doc_markers(doc_path: Path, relative: str, markers: list[str]) -> list[str]:
    text = doc_path.read_text(encoding="utf-8", errors="ignore")
    return [f"{relative} missing required marker: {marker}" for marker in markers if marker not in text]


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


def iter_control_plane_files(root: Path) -> Iterable[Path]:
    roots = [
        Path("AGENTS.md"),
        Path("docs"),
        Path(".codex/skills"),
        Path(".github"),
        Path("scripts"),
        Path("tests"),
        Path("workflows/system"),
        Path(".githooks"),
    ]
    for relative in roots:
        target = root / relative
        if not target.exists():
            continue
        if target.is_file():
            yield target
            continue
        for candidate in target.rglob("*"):
            if candidate.is_file() and "__pycache__" not in candidate.parts and candidate.suffix != ".pyc":
                yield candidate


def stale_reference_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_control_plane_files(root):
        relative = path.relative_to(root)
        if relative in STALE_REFERENCE_SCAN_EXCLUDES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in STALE_REFERENCE_PATTERNS:
            if pattern in text:
                errors.append(f"{relative} still references {pattern}")
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
    if hooks_path is None:
        errors.append("git core.hooksPath is not configured; run `python3 scripts/workflow.py init`")
    elif hooks_path != ".githooks":
        errors.append(f"git core.hooksPath must be .githooks, got: {hooks_path}")
    else:
        checks.append("git core.hooksPath points to .githooks")

    task_errors = check_all()
    if task_errors:
        errors.extend(task_errors)
    else:
        checks.append("task artifacts are internally consistent")

    repo_surface = any((root / name).exists() for name in ("AGENTS.md", "docs", ".github", ".codex"))
    if repo_surface:
        agents_path = root / "AGENTS.md"
        if not agents_path.exists():
            errors.append("missing canonical document: AGENTS.md")
        else:
            agents_errors = validate_agents_constitution(agents_path)
            if agents_errors:
                errors.extend(agents_errors)
            else:
                checks.append("AGENTS constitution is complete")

        for relative in DOC_FILES:
            doc_path = root / relative
            if not doc_path.exists():
                errors.append(f"missing canonical document: {relative}")
                continue
            markers = DOC_REQUIRED_MARKERS.get(relative)
            if markers:
                errors.extend(validate_doc_markers(doc_path, relative, markers))
        for relative in (".githooks/pre-commit", ".githooks/pre-push", "workflows/system/hooks.json"):
            if not (root / relative).exists():
                errors.append(f"missing canonical artifact: {relative}")
        for legacy_dir in ("workflows/config", "workflows/runtime", "workflows/schemas"):
            if (root / legacy_dir).exists():
                errors.append(f"legacy directory must not exist: {legacy_dir}")

        stale_errors = stale_reference_errors(root)
        if stale_errors:
            errors.extend(stale_errors)
        else:
            checks.append("no stale legacy references remain in control-plane files")

    return {"status": "failed" if errors else "passed", "checks": checks, "errors": errors}
