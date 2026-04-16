from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from workflow_runtime.constants import (
    CLARIFICATION_REQUIRED_CATEGORIES,
    CURRENT_TASK_CONTRACT_VERSION,
    PHASE_STATES,
    SPEC_REQUIRED_SECTIONS,
    TASK_STATES,
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


def compact_output(stdout: str, stderr: str, limit: int = 600) -> str:
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


def validate_relative_repo_path(value: str, *, allow_glob: bool = True) -> str:
    normalized = normalize_repo_path(value)
    if not normalized:
        raise WorkflowError("path must not be empty")
    if normalized == ".":
        raise WorkflowError("path must not be repo root")
    if normalized.startswith("/") or normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise WorkflowError(f"path must be repo-relative: {value}")
    if not allow_glob and any(token in normalized for token in "*?["):
        raise WorkflowError(f"path must not contain glob tokens: {value}")
    return normalized


def has_glob(pattern: str) -> bool:
    return any(token in pattern for token in "*?[")


def scope_matches(path: str, scope: str) -> bool:
    normalized_path = normalize_repo_path(path)
    normalized_scope = validate_relative_repo_path(scope)
    if normalized_scope.endswith("/"):
        scope_root = normalized_scope.rstrip("/")
        return normalized_path == scope_root or normalized_path.startswith(f"{scope_root}/")
    if has_glob(normalized_scope):
        return path_matches(normalized_path, [normalized_scope])
    return normalized_path == normalized_scope


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


def _require_string_list(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise WorkflowError(f"{label} must be an array")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise WorkflowError(f"{label}[{index}] must be a non-empty string")
        result.append(item)
    if not allow_empty and not result:
        raise WorkflowError(f"{label} must not be empty")
    return result


def _require_int(value: Any, label: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise WorkflowError(f"{label} must be an integer")
    if value < minimum:
        raise WorkflowError(f"{label} must be >= {minimum}")
    return value


def empty_task_intake() -> dict[str, Any]:
    return {
        "request_summary": None,
        "problem_summary": None,
        "goals": [],
        "non_goals": [],
        "constraints": [],
        "acceptance": [],
        "clarifications": [],
    }


def task_contract_version(payload: dict[str, Any]) -> int:
    value = payload.get("contract_version")
    if value is None:
        return 1
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise WorkflowError("task.contract_version must be an integer >= 1")
    return value


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


def _parse_clarification_question(raw: str, *, strict: bool) -> tuple[str | None, str]:
    match = re.match(r"^\[([A-Za-z][A-Za-z0-9_-]*)\]\s*(.*)$", raw)
    if not match:
        if strict:
            raise WorkflowError("Socratic Clarification Log must declare a coverage category like [scope] on each question")
        return None, raw

    category = match.group(1).strip().lower().replace("-", "_")
    question = match.group(2).strip()
    if not question:
        raise WorkflowError("Socratic Clarification Log contains an empty question")
    return category, question


def _normalize_clarifications(body: str, *, strict: bool, require_coverage: bool) -> tuple[list[dict[str, Any]], list[str]]:
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
                push_error("must use complete Q/A/Decision triplets")
                current = {}
            raw_question = line[2:].strip()
            if not raw_question:
                push_error("contains an empty question")
                continue
            try:
                category, question = _parse_clarification_question(raw_question, strict=require_coverage)
            except WorkflowError as exc:
                push_error(str(exc).replace("Socratic Clarification Log ", ""))
                continue
            current = {"question": question}
            if category is not None:
                current["category"] = category
            continue

        if line.startswith("A:"):
            if "question" not in current or "answer" in current:
                push_error("must place each answer after a question")
                continue
            answer = line[2:].strip()
            if not answer:
                push_error("contains an empty answer")
                continue
            current["answer"] = answer
            continue

        if line.startswith("Decision:"):
            if "question" not in current or "answer" not in current or "decision" in current:
                push_error("must place each decision after a question and answer")
                continue
            decision = line[len("Decision:") :].strip()
            if not decision:
                push_error("contains an empty decision")
                continue
            current["decision"] = decision
            current["resolved"] = True
            clarifications.append(current)
            current = {}
            continue

        push_error("must only contain Q:, A:, and Decision: entries")

    if current:
        push_error("must end with a complete Q/A/Decision triplet")
    return clarifications, errors


def inspect_spec(spec_path: Path, *, require_coverage: bool = False) -> dict[str, Any]:
    readiness = {
        "ready_for_approval": False,
        "missing_sections": [],
        "placeholder_sections": [],
        "validation_errors": [],
        "clarification_count": 0,
        "coverage_present": [],
        "coverage_missing": [],
        "unresolved_clarifications": [],
        "intake": empty_task_intake(),
    }
    if not spec_path.exists():
        readiness["validation_errors"].append("spec.md is missing")
        return readiness

    spec = spec_path.read_text(encoding="utf-8")
    sections = markdown_sections(spec)
    readiness["missing_sections"] = [name for name in SPEC_REQUIRED_SECTIONS if name not in sections]
    if readiness["missing_sections"]:
        return readiness

    placeholder_sections: list[str] = []
    for name in SPEC_REQUIRED_SECTIONS:
        body = sections[name]
        content_lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not content_lines:
            placeholder_sections.append(name)
            continue
        if any("TODO:" in line for line in content_lines):
            placeholder_sections.append(name)
    readiness["placeholder_sections"] = placeholder_sections
    if placeholder_sections:
        return readiness

    try:
        clarifications, clarification_errors = _normalize_clarifications(
            sections["Socratic Clarification Log"],
            strict=False,
            require_coverage=require_coverage,
        )
        intake = {
            "request_summary": _normalize_summary(sections["Request"], "Request"),
            "problem_summary": _normalize_summary(sections["Problem"], "Problem"),
            "goals": _normalize_items(sections["Goals"], "Goals"),
            "non_goals": _normalize_items(sections["Non-goals"], "Non-goals"),
            "constraints": _normalize_items(sections["Constraints"], "Constraints"),
            "acceptance": _normalize_items(sections["Acceptance"], "Acceptance"),
            "clarifications": clarifications,
        }
        readiness["intake"] = intake
        readiness["clarification_count"] = len(clarifications)
        readiness["validation_errors"].extend(clarification_errors)
    except WorkflowError as exc:
        readiness["validation_errors"].append(str(exc))

    present_categories = sorted({item["category"] for item in readiness["intake"]["clarifications"] if item.get("category")})
    readiness["coverage_present"] = present_categories
    if require_coverage:
        missing_categories = [item for item in CLARIFICATION_REQUIRED_CATEGORIES if item not in present_categories]
        readiness["coverage_missing"] = missing_categories
        if missing_categories:
            readiness["validation_errors"].append(
                f"Socratic Clarification Log missing coverage categories: {', '.join(missing_categories)}"
            )

    if readiness["clarification_count"] == 0:
        readiness["unresolved_clarifications"].append("Socratic Clarification Log requires at least one complete Q/A/Decision triplet")
    readiness["unresolved_clarifications"].extend(readiness["validation_errors"])
    readiness["ready_for_approval"] = not (
        readiness["missing_sections"] or readiness["placeholder_sections"] or readiness["unresolved_clarifications"]
    )
    return readiness


def validate_spec_for_approval(spec_path: Path, *, require_coverage: bool = False) -> dict[str, Any]:
    readiness = inspect_spec(spec_path, require_coverage=require_coverage)
    if readiness["missing_sections"]:
        raise WorkflowError(f"spec.md missing required sections: {', '.join(readiness['missing_sections'])}")
    if readiness["placeholder_sections"]:
        raise WorkflowError(
            f"spec.md still contains placeholder content in: {', '.join(readiness['placeholder_sections'])}"
        )
    if readiness["unresolved_clarifications"]:
        raise WorkflowError("; ".join(readiness["unresolved_clarifications"]))
    return readiness["intake"]


def validate_locked_intake(payload: dict[str, Any], label: str = "task.intake") -> dict[str, Any]:
    payload = _require_mapping(payload, label)
    _require_keys(
        payload,
        [
            "request_summary",
            "problem_summary",
            "goals",
            "non_goals",
            "constraints",
            "acceptance",
            "clarifications",
        ],
        label,
    )
    request_summary = _require_optional_string(payload["request_summary"], f"{label}.request_summary")
    problem_summary = _require_optional_string(payload["problem_summary"], f"{label}.problem_summary")
    goals = _require_string_list(payload["goals"], f"{label}.goals")
    non_goals = _require_string_list(payload["non_goals"], f"{label}.non_goals")
    constraints = _require_string_list(payload["constraints"], f"{label}.constraints")
    acceptance = _require_string_list(payload["acceptance"], f"{label}.acceptance")
    clarifications = payload["clarifications"]
    if not isinstance(clarifications, list):
        raise WorkflowError(f"{label}.clarifications must be an array")

    normalized_clarifications: list[dict[str, Any]] = []
    for index, clarification in enumerate(clarifications):
        clarification = _require_mapping(clarification, f"{label}.clarifications[{index}]")
        _require_keys(clarification, ["question", "answer", "decision", "resolved"], f"{label}.clarifications[{index}]")
        normalized_clarifications.append(
            {
                **(
                    {
                        "category": _require_string(
                            clarification["category"],
                            f"{label}.clarifications[{index}].category",
                        )
                    }
                    if "category" in clarification
                    else {}
                ),
                "question": _require_string(clarification["question"], f"{label}.clarifications[{index}].question"),
                "answer": _require_string(clarification["answer"], f"{label}.clarifications[{index}].answer"),
                "decision": _require_string(clarification["decision"], f"{label}.clarifications[{index}].decision"),
                "resolved": _require_bool(clarification["resolved"], f"{label}.clarifications[{index}].resolved"),
            }
        )

    return {
        "request_summary": request_summary,
        "problem_summary": problem_summary,
        "goals": goals,
        "non_goals": non_goals,
        "constraints": constraints,
        "acceptance": acceptance,
        "clarifications": normalized_clarifications,
    }


def ensure_locked_intake(payload: dict[str, Any], label: str = "task.intake", *, require_coverage: bool = False) -> dict[str, Any]:
    intake = validate_locked_intake(payload, label)
    required_list_fields = ["goals", "non_goals", "constraints", "acceptance", "clarifications"]
    if intake["request_summary"] is None:
        raise WorkflowError(f"{label}.request_summary must be locked before approval")
    if intake["problem_summary"] is None:
        raise WorkflowError(f"{label}.problem_summary must be locked before approval")
    for name in required_list_fields:
        if not intake[name]:
            raise WorkflowError(f"{label}.{name} must not be empty")
    unresolved = [item["question"] for item in intake["clarifications"] if not item["resolved"]]
    if unresolved:
        raise WorkflowError(f"{label}.clarifications must all be resolved")
    if require_coverage:
        uncategorized = [item["question"] for item in intake["clarifications"] if not item.get("category")]
        if uncategorized:
            raise WorkflowError(f"{label}.clarifications require category for every question")
        missing_categories = [
            item
            for item in CLARIFICATION_REQUIRED_CATEGORIES
            if item not in {entry["category"] for entry in intake["clarifications"] if entry.get("category")}
        ]
        if missing_categories:
            raise WorkflowError(f"{label}.clarifications missing coverage categories: {', '.join(missing_categories)}")
    return intake


def validate_task(payload: dict[str, Any]) -> None:
    payload = _require_mapping(payload, "task")
    _require_keys(
        payload,
        [
            "id",
            "title",
            "state",
            "primary_repo",
            "created_at",
            "approved_at",
            "approval",
            "active_phase_id",
            "latest_run_id",
            "last_verified_run_id",
            "blocked_reason",
            "user_validated",
            "user_validation_note",
            "intake",
        ],
        "task",
    )
    _require_string(payload["id"], "task.id")
    _require_string(payload["title"], "task.title")
    _require_string(payload["primary_repo"], "task.primary_repo")
    contract_version = task_contract_version(payload)
    if payload["state"] not in TASK_STATES:
        raise WorkflowError(f"task.state must be one of {sorted(TASK_STATES)}")
    _require_string(payload["created_at"], "task.created_at")
    _require_optional_string(payload["approved_at"], "task.approved_at")
    _require_optional_string(payload["active_phase_id"], "task.active_phase_id")
    _require_optional_string(payload["latest_run_id"], "task.latest_run_id")
    _require_optional_string(payload["last_verified_run_id"], "task.last_verified_run_id")
    _require_optional_string(payload.get("kickoff_required_for_phase"), "task.kickoff_required_for_phase")
    _require_optional_string(payload.get("last_kickoff_run_id"), "task.last_kickoff_run_id")
    _require_optional_string(payload["blocked_reason"], "task.blocked_reason")
    _require_bool(payload["user_validated"], "task.user_validated")
    _require_optional_string(payload["user_validation_note"], "task.user_validation_note")
    intake = validate_locked_intake(payload["intake"])

    approval = payload["approval"]
    if approval is not None:
        approval = _require_mapping(approval, "task.approval")
        _require_keys(approval, ["actor", "note", "timestamp"], "task.approval")
        _require_string(approval["actor"], "task.approval.actor")
        _require_string(approval["note"], "task.approval.note")
        _require_string(approval["timestamp"], "task.approval.timestamp")

    if (payload["approved_at"] is None) != (payload["approval"] is None):
        raise WorkflowError("task approval metadata must be fully set or fully null")
    if payload["state"] == "draft" and payload["approval"] is not None:
        raise WorkflowError("draft task cannot carry approval metadata")
    if payload["state"] == "blocked" and not payload["blocked_reason"]:
        raise WorkflowError("blocked task requires blocked_reason")
    if payload["state"] != "blocked" and payload["blocked_reason"] is not None:
        raise WorkflowError("blocked_reason is only valid when state=blocked")
    if payload["user_validated"] and not payload["user_validation_note"]:
        raise WorkflowError("user validation note is required when user_validated=true")
    if payload["user_validation_note"] and not payload["user_validated"]:
        raise WorkflowError("user_validation_note requires user_validated=true")
    if payload["state"] in {"review_ready", "completed"} and not payload["last_verified_run_id"]:
        raise WorkflowError("review_ready/completed task requires last_verified_run_id")
    if payload["state"] != "draft":
        ensure_locked_intake(intake, require_coverage=contract_version >= CURRENT_TASK_CONTRACT_VERSION)


def validate_phases(payload: dict[str, Any]) -> None:
    payload = _require_mapping(payload, "phases")
    _require_keys(payload, ["task_id", "generated_at", "phases"], "phases")
    _require_string(payload["task_id"], "phases.task_id")
    _require_string(payload["generated_at"], "phases.generated_at")
    phase_list = payload["phases"]
    if not isinstance(phase_list, list):
        raise WorkflowError("phases.phases must be an array")

    phase_ids: list[str] = []
    orders: list[int] = []
    for index, phase in enumerate(phase_list, start=1):
        phase = _require_mapping(phase, f"phase[{index}]")
        _require_keys(
            phase,
            [
                "id",
                "order",
                "title",
                "goal",
                "inputs",
                "allowed_write_paths",
                "acceptance",
                "status",
                "retry_count",
                "test_policy",
            ],
            f"phase[{index}]",
        )
        phase_id = _require_string(phase["id"], f"phase[{index}].id").strip()
        order = _require_int(phase["order"], f"phase[{index}].order", minimum=1)
        _require_string(phase["title"], f"phase[{index}].title")
        _require_string(phase["goal"], f"phase[{index}].goal")
        _require_string_list(phase["inputs"], f"phase[{index}].inputs")

        write_paths = _require_string_list(phase["allowed_write_paths"], f"phase[{index}].allowed_write_paths", allow_empty=False)
        normalized_paths = [validate_relative_repo_path(path) for path in write_paths]
        if len(set(normalized_paths)) != len(normalized_paths):
            raise WorkflowError(f"phase[{index}] allowed_write_paths must be unique")

        acceptance = _require_mapping(phase["acceptance"], f"phase[{index}].acceptance")
        _require_keys(acceptance, ["commands"], f"phase[{index}].acceptance")
        _require_string_list(acceptance["commands"], f"phase[{index}].acceptance.commands", allow_empty=False)
        if "required_reads" in phase:
            _require_string_list(phase["required_reads"], f"phase[{index}].required_reads", allow_empty=False)
        if "starting_points" in phase:
            _require_string_list(phase["starting_points"], f"phase[{index}].starting_points", allow_empty=False)
        if "deliverables" in phase:
            _require_string_list(phase["deliverables"], f"phase[{index}].deliverables", allow_empty=False)
        if "completion_signal" in phase:
            _require_string(phase["completion_signal"], f"phase[{index}].completion_signal")

        if phase["status"] not in PHASE_STATES:
            raise WorkflowError(f"phase[{index}].status must be one of {sorted(PHASE_STATES)}")
        _require_int(phase["retry_count"], f"phase[{index}].retry_count", minimum=0)

        policy = _require_mapping(phase["test_policy"], f"phase[{index}].test_policy")
        _require_keys(policy, ["mode", "evidence"], f"phase[{index}].test_policy")
        mode = _require_string(policy["mode"], f"phase[{index}].test_policy.mode")
        evidence = _require_string_list(policy["evidence"], f"phase[{index}].test_policy.evidence")
        if mode not in {"require_tests", "evidence_only"}:
            raise WorkflowError(f"phase[{index}].test_policy.mode is invalid: {mode}")
        if mode == "evidence_only" and not evidence:
            raise WorkflowError(f"phase[{index}] evidence_only requires non-empty evidence")

        phase_ids.append(phase_id)
        orders.append(order)

    if len(set(phase_ids)) != len(phase_ids):
        raise WorkflowError("phase ids must be unique")
    expected_orders = list(range(1, len(orders) + 1))
    if sorted(orders) != expected_orders:
        raise WorkflowError(
            f"phase orders must be contiguous starting at 1: expected {expected_orders}, got {sorted(orders)}"
        )


def validate_run(payload: dict[str, Any]) -> None:
    payload = _require_mapping(payload, "run")
    _require_keys(
        payload,
        [
            "id",
            "task_id",
            "phase_id",
            "event",
            "commands",
            "result",
            "evidence",
            "error_fingerprint",
            "next_action",
            "timestamp",
        ],
        "run",
    )
    _require_string(payload["id"], "run.id")
    _require_string(payload["task_id"], "run.task_id")
    _require_optional_string(payload["phase_id"], "run.phase_id")
    _require_string(payload["event"], "run.event")
    commands = payload["commands"]
    if not isinstance(commands, list):
        raise WorkflowError("run.commands must be an array")
    for index, command in enumerate(commands):
        command = _require_mapping(command, f"run.commands[{index}]")
        _require_keys(command, ["command", "status", "output"], f"run.commands[{index}]")
        _require_string(command["command"], f"run.commands[{index}].command")
        status = _require_string(command["status"], f"run.commands[{index}].status")
        if status not in {"passed", "failed", "blocked", "skipped"}:
            raise WorkflowError(f"run.commands[{index}].status is invalid: {status}")
        if not isinstance(command["output"], str):
            raise WorkflowError(f"run.commands[{index}].output must be a string")

    result = _require_string(payload["result"], "run.result")
    if result not in {"passed", "failed", "blocked"}:
        raise WorkflowError(f"run.result is invalid: {result}")
    _require_string_list(payload["evidence"], "run.evidence")
    _require_optional_string(payload["error_fingerprint"], "run.error_fingerprint")
    _require_string(payload["next_action"], "run.next_action")
    _require_string(payload["timestamp"], "run.timestamp")


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.M))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections
