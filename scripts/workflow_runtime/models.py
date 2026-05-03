from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from workflow_runtime.constants import (
    CURRENT_TASK_CONTRACT_VERSION,
    IMPLEMENTATION_STATES,
    SPEC_REQUIRED_SECTIONS,
    TASK_STATES,
    VERIFICATION_STATES,
)


class WorkflowError(Exception):
    pass


@dataclass
class HookResult:
    event: str
    status: str
    messages: list[str]

    def as_payload(self) -> dict[str, Any]:
        return {"event": self.event, "status": self.status, "messages": self.messages}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def compact_output(stdout: str, stderr: str, limit: int = 800) -> str:
    text = (stdout + "\n" + stderr).strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def normalize_repo_path(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    return normalized


def validate_task_id(value: str) -> str:
    task_id = _require_string(value, "task_id").strip()
    if task_id in {".", ".."}:
        raise WorkflowError(f"task_id must not be {task_id!r}")
    if "/" in task_id or "\\" in task_id:
        raise WorkflowError(f"task_id must not contain path separators: {value}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task_id):
        raise WorkflowError(
            "task_id may only contain letters, numbers, dot, underscore, and hyphen, and must start with an alphanumeric character"
        )
    return task_id


def path_matches(path: str, patterns: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    pure = PurePosixPath(normalized)
    return any(pure.match(pattern) or fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def has_glob(pattern: str) -> bool:
    return any(token in pattern for token in "*?[")


def validate_relative_repo_path(value: str, *, allow_glob: bool = True) -> str:
    normalized = normalize_repo_path(value)
    if not normalized:
        raise WorkflowError("path must not be empty")
    if normalized == ".":
        return normalized
    if normalized.startswith("/") or normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise WorkflowError(f"path must be repo-relative: {value}")
    if not allow_glob and has_glob(normalized):
        raise WorkflowError(f"path must not contain glob tokens: {value}")
    return normalized


def scope_matches(path: str, scope: str) -> bool:
    normalized_path = normalize_repo_path(path)
    normalized_scope = validate_relative_repo_path(scope)
    if normalized_scope == ".":
        return True
    if normalized_scope.endswith("/"):
        scope_root = normalized_scope.rstrip("/")
        return normalized_path == scope_root or normalized_path.startswith(f"{scope_root}/")
    if has_glob(normalized_scope):
        return path_matches(normalized_path, [normalized_scope])
    return normalized_path == normalized_scope


def spec_sha256(spec_path: Path) -> str:
    return hashlib.sha256(spec_path.read_bytes()).hexdigest()


def _require_mapping(payload: Any, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise WorkflowError(f"{label} must be an object")
    return payload


def _require_keys(payload: dict[str, Any], required: list[str], label: str) -> None:
    missing = [key for key in required if key not in payload]
    if missing:
        raise WorkflowError(f"{label} missing required keys: {', '.join(missing)}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError(f"{label} must be a non-empty string")
    return value


def _require_optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError(f"{label} must be null or a non-empty string")
    return value


def _require_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise WorkflowError(f"{label} must be a boolean")
    return value


def _require_int(value: Any, label: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise WorkflowError(f"{label} must be an integer")
    if value < minimum:
        raise WorkflowError(f"{label} must be >= {minimum}")
    return value


def _require_string_list(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise WorkflowError(f"{label} must be an array")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise WorkflowError(f"{label}[{index}] must be a non-empty string")
        result.append(item.strip())
    if not allow_empty and not result:
        raise WorkflowError(f"{label} must not be empty")
    return result


def _strip_markdown_prefix(line: str) -> str:
    stripped = line.strip()
    stripped = re.sub(r"^[-*+]\s+", "", stripped)
    stripped = re.sub(r"^\d+\.\s+", "", stripped)
    return stripped.strip()


def _markdown_lines(body: str) -> list[str]:
    return [_strip_markdown_prefix(line) for line in body.splitlines() if line.strip()]


def _normalize_summary(body: str, label: str) -> str:
    lines = _markdown_lines(body)
    if not lines:
        raise WorkflowError(f"{label} must not be empty")
    return " ".join(lines)


def _normalize_items(body: str, label: str) -> list[str]:
    items = _markdown_lines(body)
    if not items:
        raise WorkflowError(f"{label} must not be empty")
    return items


def _values_from_markdown(text: str) -> list[str]:
    ticked = re.findall(r"`([^`]+)`", text)
    if ticked:
        return [item.strip() for item in ticked if item.strip()]
    _, _, value = text.partition(":")
    return [item.strip() for item in value.split(",") if item.strip()]


def _normalize_implementation_scopes(body: str) -> tuple[list[dict[str, Any]], list[str]]:
    scopes: list[dict[str, Any]] = []
    errors: list[str] = []
    current: dict[str, Any] | None = None

    def finish() -> None:
        if current is None:
            return
        missing = [key for key in ("target_repos", "change_paths", "policy") if not current.get(key)]
        if missing:
            errors.append(f"Implementation Scope {current['imp_id']} missing: {', '.join(missing)}")
        scopes.append(current.copy())

    for line in _markdown_lines(body):
        match = re.match(r"^(IMP-\d+):\s*(.+)$", line)
        if match:
            finish()
            current = {
                "imp_id": match.group(1),
                "title": match.group(2).strip(),
                "target_repos": [],
                "change_paths": [],
                "policy": "",
            }
            continue

        if current is None:
            errors.append("Implementation Scopes must contain IMP-* entries")
            continue

        if line.startswith("대상 저장소:") or line.startswith("Target Repo:") or line.startswith("Target Repos:"):
            current["target_repos"] = _values_from_markdown(line)
        elif line.startswith("변경 경로:") or line.startswith("Change Paths:"):
            current["change_paths"] = [validate_relative_repo_path(item) for item in _values_from_markdown(line)]
        elif line.startswith("정책:") or line.startswith("Policy:"):
            _, _, policy = line.partition(":")
            current["policy"] = policy.strip()

    finish()

    ids = [scope["imp_id"] for scope in scopes]
    if len(ids) != len(set(ids)):
        errors.append("Implementation Scopes must use unique IMP ids")
    return scopes, errors


def _normalize_clarifications(body: str, *, strict: bool) -> tuple[list[dict[str, Any]], list[str]]:
    clarifications: list[dict[str, Any]] = []
    errors: list[str] = []
    current: dict[str, Any] = {}

    def push_error(message: str) -> None:
        if strict:
            raise WorkflowError(f"Socratic Clarification Log {message}")
        errors.append(f"Socratic Clarification Log {message}")

    for line in _markdown_lines(body):
        if line.startswith("Q:"):
            if current:
                push_error("must end each clarification with a Status line")
                current = {}
            question = line[2:].strip()
            if not question:
                push_error("contains an empty question")
                continue
            current = {"question": question}
            continue

        if line.startswith("A:"):
            if "question" not in current or "answer" in current or "status" in current:
                push_error("must place each answer after a question")
                continue
            answer = line[2:].strip()
            if not answer:
                push_error("contains an empty answer")
                continue
            current["answer"] = answer
            continue

        if line.startswith("Decision:"):
            if "question" not in current or "answer" not in current or "decision" in current or "status" in current:
                push_error("must place each decision after a question and answer")
                continue
            decision = line[len("Decision:") :].strip()
            if not decision:
                push_error("contains an empty decision")
                continue
            current["decision"] = decision
            continue

        if line.startswith("Status:"):
            if "question" not in current or "status" in current:
                push_error("must place each status after a question")
                continue
            status = line[len("Status:") :].strip().lower()
            if status not in {"open", "resolved"}:
                push_error("must declare status as open or resolved")
                continue
            if status == "open" and "decision" in current:
                push_error("open clarifications must not contain Decision")
                continue
            if status == "resolved" and ("answer" not in current or "decision" not in current):
                push_error("resolved clarifications require answer and decision")
                continue
            clarifications.append(
                {
                    "question": current["question"],
                    "answer": current.get("answer"),
                    "decision": current.get("decision"),
                    "status": status,
                }
            )
            current = {}
            continue

        push_error("must only contain Q:, A:, Decision:, and Status: entries")

    if current:
        push_error("must end each clarification with a Status line")
    return clarifications, errors


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.M))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def empty_spec_intake() -> dict[str, Any]:
    return {
        "request_summary": None,
        "problem_summary": None,
        "goals": [],
        "non_goals": [],
        "constraints": [],
        "acceptance": [],
        "implementation_scopes": [],
        "clarifications": [],
    }


def inspect_spec(spec_path: Path) -> dict[str, Any]:
    readiness = {
        "ready_for_approval": False,
        "missing_sections": [],
        "placeholder_sections": [],
        "validation_errors": [],
        "clarification_count": 0,
        "open_clarification_count": 0,
        "resolved_clarification_count": 0,
        "open_clarifications": [],
        "implementation_scope_count": 0,
        "implementation_scope_ids": [],
        "intake": empty_spec_intake(),
        "spec_sha256": None,
    }
    if not spec_path.exists():
        readiness["validation_errors"].append("spec.md is missing")
        return readiness

    spec = spec_path.read_text(encoding="utf-8")
    readiness["spec_sha256"] = hashlib.sha256(spec.encode("utf-8")).hexdigest()
    sections = markdown_sections(spec)
    readiness["missing_sections"] = [name for name in SPEC_REQUIRED_SECTIONS if name not in sections]
    if readiness["missing_sections"]:
        return readiness

    placeholder_sections: list[str] = []
    for name in SPEC_REQUIRED_SECTIONS:
        lines = [line.strip() for line in sections[name].splitlines() if line.strip()]
        if not lines or any("TODO:" in line or "(AI가 소크라테스 문답을 통해 작성합니다.)" in line for line in lines):
            placeholder_sections.append(name)
    readiness["placeholder_sections"] = placeholder_sections
    if placeholder_sections:
        return readiness

    try:
        clarifications, clarification_errors = _normalize_clarifications(
            sections["Socratic Clarification Log"],
            strict=False,
        )
        scopes, scope_errors = _normalize_implementation_scopes(sections["Implementation Scopes"])
        intake = {
            "request_summary": _normalize_summary(sections["Request"], "Request"),
            "problem_summary": _normalize_summary(sections["Problem"], "Problem"),
            "goals": _normalize_items(sections["Goals"], "Goals"),
            "non_goals": _normalize_items(sections["Non-goals"], "Non-goals"),
            "constraints": _normalize_items(sections["Constraints"], "Constraints"),
            "acceptance": _normalize_items(sections["Acceptance"], "Acceptance"),
            "implementation_scopes": scopes,
            "clarifications": clarifications,
        }
        readiness["intake"] = intake
        readiness["clarification_count"] = len(clarifications)
        readiness["open_clarification_count"] = sum(1 for item in clarifications if item["status"] == "open")
        readiness["resolved_clarification_count"] = sum(1 for item in clarifications if item["status"] == "resolved")
        readiness["open_clarifications"] = [item["question"] for item in clarifications if item["status"] == "open"]
        readiness["implementation_scope_count"] = len(scopes)
        readiness["implementation_scope_ids"] = [item["imp_id"] for item in scopes]
        readiness["validation_errors"].extend(clarification_errors)
        readiness["validation_errors"].extend(scope_errors)
    except WorkflowError as exc:
        readiness["validation_errors"].append(str(exc))

    if readiness["clarification_count"] == 0:
        readiness["validation_errors"].append("Socratic Clarification Log requires at least one clarification entry")
    if readiness["implementation_scope_count"] == 0:
        readiness["validation_errors"].append("Implementation Scopes requires at least one IMP-* entry")
    readiness["ready_for_approval"] = not (
        readiness["missing_sections"]
        or readiness["placeholder_sections"]
        or readiness["validation_errors"]
        or readiness["open_clarifications"]
    )
    return readiness


def validate_spec_for_approval(spec_path: Path) -> dict[str, Any]:
    readiness = inspect_spec(spec_path)
    if readiness["missing_sections"]:
        raise WorkflowError(f"spec.md missing required sections: {', '.join(readiness['missing_sections'])}")
    if readiness["placeholder_sections"]:
        raise WorkflowError(
            f"spec.md still contains placeholder content in: {', '.join(readiness['placeholder_sections'])}"
        )
    if readiness["validation_errors"]:
        raise WorkflowError("; ".join(readiness["validation_errors"]))
    if readiness["open_clarifications"]:
        raise WorkflowError(
            "Socratic Clarification Log still has open clarifications: "
            + "; ".join(readiness["open_clarifications"])
        )
    return readiness


def default_verification_commands(target_repos: list[str]) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    if "git-ranker-workflow" in target_repos:
        commands.append({"cmd": "python3 -m unittest discover -s tests -v", "cwd": "."})
    if "git-ranker" in target_repos:
        commands.append({"cmd": "./gradlew test", "cwd": "git-ranker"})
    if "git-ranker-client" in target_repos:
        commands.append({"cmd": "npm test", "cwd": "git-ranker-client"})
    return commands


def scope_to_progress(scope: dict[str, Any]) -> dict[str, Any]:
    return {
        "imp_id": scope["imp_id"],
        "title": scope["title"],
        "target_repos": scope["target_repos"],
        "change_paths": scope["change_paths"],
        "policy": scope["policy"],
        "status": "pending",
        "changed_paths": [],
        "scope_delta": [],
        "started_at": None,
        "completed_at": None,
        "note": "",
        "verification": {
            "status": "not_run",
            "commands": default_verification_commands(scope["target_repos"]),
            "last_run_at": None,
            "results": [],
        },
    }


def validate_command_payload(payload: Any, label: str) -> dict[str, str]:
    payload = _require_mapping(payload, label)
    _require_keys(payload, ["cmd", "cwd"], label)
    return {
        "cmd": _require_string(payload["cmd"], f"{label}.cmd").strip(),
        "cwd": validate_relative_repo_path(_require_string(payload["cwd"], f"{label}.cwd").strip()),
    }


def validate_state(payload: dict[str, Any]) -> None:
    payload = _require_mapping(payload, "state")
    _require_keys(
        payload,
        [
            "task_id",
            "title",
            "contract_version",
            "state",
            "primary_repo",
            "created_at",
            "updated_at",
            "spec_lock",
            "current_focus",
            "implementation_scopes",
            "events",
            "next_action",
            "blockers",
            "user_validation",
        ],
        "state",
    )
    _require_string(payload["task_id"], "state.task_id")
    _require_string(payload["title"], "state.title")
    _require_int(payload["contract_version"], "state.contract_version", minimum=1)
    if payload["state"] not in TASK_STATES:
        raise WorkflowError(f"state.state must be one of {sorted(TASK_STATES)}")
    _require_string(payload["primary_repo"], "state.primary_repo")
    _require_string(payload["created_at"], "state.created_at")
    _require_string(payload["updated_at"], "state.updated_at")

    spec_lock = _require_mapping(payload["spec_lock"], "state.spec_lock")
    _require_keys(spec_lock, ["approved", "approved_at", "approved_by", "approval_note", "spec_sha256"], "state.spec_lock")
    _require_bool(spec_lock["approved"], "state.spec_lock.approved")
    _require_optional_string(spec_lock["approved_at"], "state.spec_lock.approved_at")
    _require_optional_string(spec_lock["approved_by"], "state.spec_lock.approved_by")
    _require_optional_string(spec_lock["approval_note"], "state.spec_lock.approval_note")
    _require_optional_string(spec_lock["spec_sha256"], "state.spec_lock.spec_sha256")
    if spec_lock["approved"] and not spec_lock["spec_sha256"]:
        raise WorkflowError("approved state requires state.spec_lock.spec_sha256")

    focus = _require_mapping(payload["current_focus"], "state.current_focus")
    _require_keys(focus, ["imp_id", "status", "started_at", "note"], "state.current_focus")
    _require_optional_string(focus["imp_id"], "state.current_focus.imp_id")
    _require_string(focus["status"], "state.current_focus.status")
    _require_optional_string(focus["started_at"], "state.current_focus.started_at")
    if not isinstance(focus["note"], str):
        raise WorkflowError("state.current_focus.note must be a string")

    scopes = payload["implementation_scopes"]
    if not isinstance(scopes, list):
        raise WorkflowError("state.implementation_scopes must be an array")
    seen: set[str] = set()
    for index, scope in enumerate(scopes):
        scope = _require_mapping(scope, f"state.implementation_scopes[{index}]")
        _require_keys(
            scope,
            [
                "imp_id",
                "title",
                "target_repos",
                "change_paths",
                "policy",
                "status",
                "changed_paths",
                "scope_delta",
                "started_at",
                "completed_at",
                "note",
                "verification",
            ],
            f"state.implementation_scopes[{index}]",
        )
        imp_id = _require_string(scope["imp_id"], f"state.implementation_scopes[{index}].imp_id")
        if imp_id in seen:
            raise WorkflowError(f"duplicate implementation scope id: {imp_id}")
        seen.add(imp_id)
        _require_string(scope["title"], f"state.implementation_scopes[{index}].title")
        _require_string_list(scope["target_repos"], f"state.implementation_scopes[{index}].target_repos", allow_empty=False)
        _require_string_list(scope["change_paths"], f"state.implementation_scopes[{index}].change_paths", allow_empty=False)
        _require_string(scope["policy"], f"state.implementation_scopes[{index}].policy")
        status = _require_string(scope["status"], f"state.implementation_scopes[{index}].status")
        if status not in IMPLEMENTATION_STATES:
            raise WorkflowError(f"state.implementation_scopes[{index}].status is invalid: {status}")
        _require_string_list(scope["changed_paths"], f"state.implementation_scopes[{index}].changed_paths")
        _require_string_list(scope["scope_delta"], f"state.implementation_scopes[{index}].scope_delta")
        _require_optional_string(scope["started_at"], f"state.implementation_scopes[{index}].started_at")
        _require_optional_string(scope["completed_at"], f"state.implementation_scopes[{index}].completed_at")
        if not isinstance(scope["note"], str):
            raise WorkflowError(f"state.implementation_scopes[{index}].note must be a string")

        verification = _require_mapping(scope["verification"], f"state.implementation_scopes[{index}].verification")
        _require_keys(verification, ["status", "commands", "last_run_at", "results"], f"state.implementation_scopes[{index}].verification")
        verification_status = _require_string(verification["status"], f"state.implementation_scopes[{index}].verification.status")
        if verification_status not in VERIFICATION_STATES:
            raise WorkflowError(f"state.implementation_scopes[{index}].verification.status is invalid: {verification_status}")
        commands = verification["commands"]
        if not isinstance(commands, list):
            raise WorkflowError(f"state.implementation_scopes[{index}].verification.commands must be an array")
        for command_index, command in enumerate(commands):
            validate_command_payload(command, f"state.implementation_scopes[{index}].verification.commands[{command_index}]")
        _require_optional_string(verification["last_run_at"], f"state.implementation_scopes[{index}].verification.last_run_at")
        if not isinstance(verification["results"], list):
            raise WorkflowError(f"state.implementation_scopes[{index}].verification.results must be an array")

    if not isinstance(payload["events"], list):
        raise WorkflowError("state.events must be an array")
    if not isinstance(payload["next_action"], str):
        raise WorkflowError("state.next_action must be a string")
    _require_string_list(payload["blockers"], "state.blockers")

    validation = _require_mapping(payload["user_validation"], "state.user_validation")
    _require_keys(validation, ["validated", "note", "validated_at"], "state.user_validation")
    _require_bool(validation["validated"], "state.user_validation.validated")
    _require_optional_string(validation["note"], "state.user_validation.note")
    _require_optional_string(validation["validated_at"], "state.user_validation.validated_at")
    if payload["state"] == "completed" and not validation["validated"]:
        raise WorkflowError("completed state requires user validation")
