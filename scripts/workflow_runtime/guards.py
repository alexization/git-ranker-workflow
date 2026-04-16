from __future__ import annotations

import re
import shlex
from typing import Any, Callable

from workflow_runtime.models import HookResult, path_matches, scope_matches


def phase_scope(task_id: str, phase: dict[str, Any]) -> list[str]:
    return [*phase["allowed_write_paths"], f"workflows/tasks/{task_id}/"]


def out_of_scope_paths(task_id: str, phase: dict[str, Any], changed_paths: list[str]) -> list[str]:
    scopes = phase_scope(task_id, phase)
    violations = []
    for path in changed_paths:
        if not any(scope_matches(path, scope) for scope in scopes):
            violations.append(path)
    return sorted(set(violations))


def write_scope_guard(task_id: str | None, phase: dict[str, Any] | None, changed_paths: list[str]) -> HookResult:
    if not changed_paths:
        return HookResult("write_scope_guard", "passed", ["no changed paths"])
    if task_id is None or phase is None:
        return HookResult("write_scope_guard", "passed", ["no phase context"])

    violations = out_of_scope_paths(task_id, phase, changed_paths)
    if violations:
        return HookResult(
            "write_scope_guard",
            "failed",
            [f"changed paths outside allowed_write_paths: {', '.join(violations)}"],
        )
    return HookResult("write_scope_guard", "passed", ["all changed paths are inside allowed_write_paths"])


def tdd_guard(config: dict[str, Any], changed_paths: list[str], phase: dict[str, Any] | None) -> HookResult:
    if not changed_paths:
        return HookResult("tdd_guard", "passed", ["no changed paths"])

    relevant = [path for path in changed_paths if not path_matches(path, config["ignore_patterns"])]
    implementation_changes = [path for path in relevant if path_matches(path, config["implementation_patterns"])]
    test_changes = [path for path in relevant if path_matches(path, config["test_patterns"])]

    if not implementation_changes:
        return HookResult("tdd_guard", "passed", ["no implementation changes"])
    if test_changes:
        return HookResult("tdd_guard", "passed", [f"test changes detected: {', '.join(sorted(set(test_changes)))}"])

    if phase is None:
        return HookResult(
            "tdd_guard",
            "failed",
            [f"implementation changes require tests: {', '.join(sorted(set(implementation_changes)))}"],
        )

    policy = phase["test_policy"]
    if policy["mode"] == "evidence_only" and policy["evidence"]:
        return HookResult(
            "tdd_guard",
            "passed",
            [f"test evidence accepted: {', '.join(policy['evidence'])}"],
        )

    return HookResult(
        "tdd_guard",
        "failed",
        [f"implementation changes require tests: {', '.join(sorted(set(implementation_changes)))}"],
    )


def dangerous_cmd_guard(config: dict[str, Any], command: str) -> HookResult:
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()

    if tokens and tokens[0].lower() == "git":
        try:
            push_index = next(index for index, token in enumerate(tokens[1:], start=1) if token.lower() == "push")
        except StopIteration:
            push_index = None
        if push_index is not None:
            for token in tokens[push_index + 1 :]:
                normalized = token.lower()
                if normalized.startswith("--force"):
                    return HookResult("dangerous_cmd_guard", "failed", [f"blocked command: {command}"])
                if re.fullmatch(r"-[A-Za-z]*f[A-Za-z]*", token):
                    return HookResult("dangerous_cmd_guard", "failed", [f"blocked command: {command}"])

    for pattern in config["blocked_patterns"]:
        if re.search(pattern, command, flags=re.I):
            return HookResult("dangerous_cmd_guard", "failed", [f"blocked command: {command}"])
    return HookResult("dangerous_cmd_guard", "passed", [f"command allowed: {command}"])


def latest_verified_run_guard(
    task: dict[str, Any],
    phase: dict[str, Any] | None,
    changed_paths: list[str] | None,
    *,
    load_run: Callable[[str, str], dict[str, Any]],
    scope_sensitive: bool,
) -> HookResult:
    if phase is None:
        if scope_sensitive:
            return HookResult("latest_verified_run_guard", "passed", ["no phase context"])
        return HookResult("latest_verified_run_guard", "failed", ["active phase context is required"])

    if scope_sensitive:
        if not changed_paths:
            return HookResult("latest_verified_run_guard", "passed", ["no changed paths detected"])
        if not any(
            any(scope_matches(path, scope) for scope in phase_scope(task["id"], phase))
            for path in changed_paths
        ):
            return HookResult("latest_verified_run_guard", "passed", ["no active phase scope changes detected"])

    run_id = task["last_verified_run_id"]
    if not run_id:
        return HookResult("latest_verified_run_guard", "failed", ["no passed verification recorded for active phase"])

    run = load_run(task["id"], run_id)
    if run["event"] != "verification" or run["result"] != "passed":
        return HookResult("latest_verified_run_guard", "failed", [f"run {run_id} is not a passed verification"])
    if run["phase_id"] != phase["id"]:
        return HookResult(
            "latest_verified_run_guard",
            "failed",
            [f"latest passed verification is for phase {run['phase_id']}, not active phase {phase['id']}"],
        )
    return HookResult("latest_verified_run_guard", "passed", [f"latest passed verification: {run_id}"])


def user_validation_guard(note: str | None, task: dict[str, Any]) -> HookResult:
    if note or task.get("user_validated"):
        return HookResult("user_validation_guard", "passed", ["user validation provided"])
    return HookResult("user_validation_guard", "failed", ["user validation note is required"])
