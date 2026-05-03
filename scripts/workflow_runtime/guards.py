from __future__ import annotations

import re
import shlex
from typing import Any

from workflow_runtime.models import HookResult


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


def user_validation_guard(note: str | None, state: dict[str, Any]) -> HookResult:
    if note or state.get("user_validation", {}).get("validated"):
        return HookResult("user_validation_guard", "passed", ["user validation provided"])
    return HookResult("user_validation_guard", "failed", ["user validation note is required"])
