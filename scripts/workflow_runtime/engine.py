from __future__ import annotations

import copy
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from workflow_runtime.constants import PHASE_TRANSITIONS, TASK_TRANSITIONS
from workflow_runtime.doctor import build_doctor_report
from workflow_runtime.git_ops import git_paths, unpushed_git_paths
from workflow_runtime.guards import (
    dangerous_cmd_guard,
    latest_verified_run_guard,
    out_of_scope_paths,
    phase_scope,
    tdd_guard,
    user_validation_guard,
    write_scope_guard,
)
from workflow_runtime.models import (
    ensure_locked_intake,
    HookResult,
    WorkflowError,
    compact_output,
    inspect_spec,
    normalize_repo_path,
    now_iso,
    read_json,
    scope_matches,
    validate_phases,
    validate_relative_repo_path,
    validate_run,
    validate_spec_for_approval,
    validate_task_id,
    validate_task,
    write_json,
)
from workflow_runtime.templates import approval_block, default_spec, empty_phases_payload, empty_task_payload

SOURCE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = Path(os.environ.get("WORKFLOW_ROOT", SOURCE_ROOT))
ACTIVE_TASK_STATES = {"approved", "in_progress", "failed", "blocked", "review_ready"}
PRE_PUSH_TASK_STATES = ACTIVE_TASK_STATES | {"completed"}


class WorkflowService:
    def __init__(self, root: Path | None = None):
        self.root = Path(root or DEFAULT_ROOT).resolve()
        self.workflows_dir = self.root / "workflows"
        self.system_dir = self.workflows_dir / "system"
        self.tasks_dir = self.workflows_dir / "tasks"
        self.hooks_config_path = self.system_dir / "hooks.json"

    def sync_runtime_surface(self, *, overwrite: bool) -> None:
        surfaces = (
            (SOURCE_ROOT / "workflows" / "system" / "hooks.json", self.hooks_config_path),
            (SOURCE_ROOT / ".githooks" / "pre-commit", self.root / ".githooks" / "pre-commit"),
            (SOURCE_ROOT / ".githooks" / "pre-push", self.root / ".githooks" / "pre-push"),
        )
        for source, target in surfaces:
            if not source.exists():
                continue
            if source == target:
                continue
            if target.exists():
                try:
                    if source.samefile(target):
                        continue
                except FileNotFoundError:
                    pass
            target.parent.mkdir(parents=True, exist_ok=True)
            if overwrite or not target.exists():
                shutil.copy2(source, target)

    def ensure_layout(self, *, sync: bool = False) -> None:
        self.system_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.sync_runtime_surface(overwrite=sync)

    def task_dir(self, task_id: str) -> Path:
        return self.tasks_dir / validate_task_id(task_id)

    def task_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "task.json"

    def spec_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "spec.md"

    def phases_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "phases.json"

    def runs_dir(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "runs"

    def run_path(self, task_id: str, run_id: str) -> Path:
        return self.runs_dir(task_id) / f"{run_id}.json"

    def load_hooks_config(self) -> dict[str, Any]:
        self.ensure_layout()
        return read_json(self.hooks_config_path)

    def load_task(self, task_id: str) -> dict[str, Any]:
        path = self.task_path(task_id)
        if not path.exists():
            raise WorkflowError(f"task not found: {task_id}")
        payload = read_json(path)
        validate_task(payload)
        return payload

    def save_task(self, task_id: str, payload: dict[str, Any]) -> None:
        validate_task(payload)
        write_json(self.task_path(task_id), payload)

    def load_phases(self, task_id: str) -> dict[str, Any]:
        path = self.phases_path(task_id)
        if not path.exists():
            raise WorkflowError(f"phases not found: {task_id}")
        payload = read_json(path)
        validate_phases(payload)
        return payload

    def save_phases(self, task_id: str, payload: dict[str, Any]) -> None:
        validate_phases(payload)
        write_json(self.phases_path(task_id), payload)

    def load_run(self, task_id: str, run_id: str) -> dict[str, Any]:
        path = self.run_path(task_id, run_id)
        if not path.exists():
            raise WorkflowError(f"run not found: {run_id}")
        payload = read_json(path)
        validate_run(payload)
        return payload

    def write_run(self, task_id: str, payload: dict[str, Any]) -> None:
        validate_run(payload)
        write_json(self.run_path(task_id, payload["id"]), payload)

    def configure_git_hooks(self) -> str | None:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        config = subprocess.run(
            ["git", "config", "--local", "core.hooksPath", ".githooks"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if config.returncode != 0:
            raise WorkflowError(config.stderr.strip() or "failed to configure core.hooksPath")
        return ".githooks"

    def init_workspace(self) -> dict[str, Any]:
        self.ensure_layout(sync=True)
        hooks_path = self.configure_git_hooks()
        return {
            "status": "ready",
            "root": str(self.root),
            "paths": {
                "tasks": str(self.tasks_dir),
                "system": str(self.system_dir),
            },
            "git_hooks_path": hooks_path,
        }

    def new_task(self, task_id: str, title: str, primary_repo: str) -> None:
        self.ensure_layout()
        task_dir = self.task_dir(task_id)
        if task_dir.exists():
            raise WorkflowError(f"task already exists: {task_id}")
        task_dir.mkdir(parents=True, exist_ok=False)
        self.runs_dir(task_id).mkdir(parents=True, exist_ok=True)

        self.spec_path(task_id).write_text(default_spec(task_id, title, primary_repo), encoding="utf-8")
        self.save_task(task_id, empty_task_payload(task_id, title, primary_repo))
        self.save_phases(task_id, empty_phases_payload(task_id))

    def update_task_state(self, task: dict[str, Any], next_state: str) -> None:
        current = task["state"]
        allowed = TASK_TRANSITIONS[current]
        if next_state not in allowed:
            raise WorkflowError(f"invalid task transition: {current} -> {next_state}")
        task["state"] = next_state

    def update_phase_state(self, phase: dict[str, Any], next_state: str) -> None:
        current = phase["status"]
        allowed = PHASE_TRANSITIONS[current]
        if next_state not in allowed:
            raise WorkflowError(f"invalid phase transition: {current} -> {next_state}")
        phase["status"] = next_state

    def append_approval_to_spec(self, task_id: str, note: str, actor: str, timestamp: str) -> None:
        spec_path = self.spec_path(task_id)
        spec = spec_path.read_text(encoding="utf-8")
        block = approval_block(actor, note, timestamp)
        if "\n## Approval\n" in spec:
            spec = re.sub(r"\n## Approval\n.*", block, spec, flags=re.S)
        else:
            spec += block
        spec_path.write_text(spec, encoding="utf-8")

    def approve_task(self, task_id: str, note: str, actor: str) -> None:
        task = self.load_task(task_id)
        if task["state"] not in {"draft", "approved"}:
            raise WorkflowError("approve requires draft or approved task")
        if not note.strip():
            raise WorkflowError("approval note is required")

        intake = validate_spec_for_approval(self.spec_path(task_id))
        timestamp = now_iso()
        task["state"] = "approved"
        task["approved_at"] = timestamp
        task["approval"] = {"actor": actor, "note": note.strip(), "timestamp": timestamp}
        task["intake"] = intake
        self.append_approval_to_spec(task_id, note.strip(), actor, timestamp)
        self.save_task(task_id, task)

    def normalize_phase(self, payload: dict[str, Any], fallback_order: int) -> dict[str, Any]:
        try:
            phase = copy.deepcopy(payload)
            phase["id"] = phase["id"].strip()
            phase["title"] = phase["title"].strip()
            phase["goal"] = phase["goal"].strip()
            phase["order"] = phase.get("order", fallback_order)
            phase["status"] = "pending"
            phase["retry_count"] = 0
            phase["inputs"] = [item.strip() for item in phase.get("inputs", [])]
            phase["allowed_write_paths"] = [validate_relative_repo_path(item) for item in phase["allowed_write_paths"]]
            phase["acceptance"] = {
                "commands": [command.strip() for command in phase["acceptance"]["commands"]],
            }
            policy = phase.get("test_policy") or {"mode": "require_tests", "evidence": []}
            phase["test_policy"] = {
                "mode": policy["mode"],
                "evidence": [item.strip() for item in policy.get("evidence", []) if item.strip()],
            }
            return phase
        except KeyError as exc:
            raise WorkflowError(f"phase input missing key: {exc.args[0]}") from exc

    def plan_task(self, task_id: str, source_payload: Any) -> None:
        task = self.load_task(task_id)
        if task["state"] != "approved":
            raise WorkflowError("plan requires approved task")
        if source_payload is None:
            raise WorkflowError("plan requires explicit phase input via --from or --stdin")
        spec = inspect_spec(self.spec_path(task_id))
        if not spec["ready_for_approval"]:
            raise WorkflowError("plan requires approval-ready spec.md")
        intake = ensure_locked_intake(task["intake"])
        if intake != spec["intake"]:
            raise WorkflowError("spec.md and task.intake are out of sync; rerun approve before plan")

        phases_input = source_payload["phases"] if isinstance(source_payload, dict) and "phases" in source_payload else source_payload
        if not isinstance(phases_input, list) or not phases_input:
            raise WorkflowError("phases input must be a non-empty array")

        normalized = [self.normalize_phase(phase, index) for index, phase in enumerate(phases_input, start=1)]
        normalized = sorted(normalized, key=lambda item: item["order"])
        phases_payload = {
            "task_id": task_id,
            "generated_at": now_iso(),
            "phases": normalized,
        }
        self.save_phases(task_id, phases_payload)

        task["active_phase_id"] = normalized[0]["id"]
        task["last_verified_run_id"] = None
        task["blocked_reason"] = None
        task["user_validated"] = False
        task["user_validation_note"] = None
        self.save_task(task_id, task)

    def current_phase(self, task_id: str, phase_id: str | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        task = self.load_task(task_id)
        phases_payload = self.load_phases(task_id)
        if not phases_payload["phases"]:
            raise WorkflowError("task has no phases")
        target_id = phase_id or task["active_phase_id"]
        if target_id is None:
            raise WorkflowError("task has no active phase")
        for phase in phases_payload["phases"]:
            if phase["id"] == target_id:
                return task, phases_payload, phase
        raise WorkflowError(f"phase not found: {target_id}")

    def next_pending_phase_id(self, phases_payload: dict[str, Any]) -> str | None:
        pending = sorted(
            (phase for phase in phases_payload["phases"] if phase["status"] == "pending"),
            key=lambda item: item["order"],
        )
        return pending[0]["id"] if pending else None

    def task_ids_by_state(self, states: set[str]) -> list[str]:
        if not self.tasks_dir.exists():
            return []

        active = []
        for candidate in sorted(self.tasks_dir.iterdir()):
            if not candidate.is_dir():
                continue
            task_file = candidate / "task.json"
            if not task_file.exists():
                continue
            task = read_json(task_file)
            if task.get("state") in states:
                active.append(task.get("id") or candidate.name)
        return active

    def active_task_ids(self) -> list[str]:
        return self.task_ids_by_state(ACTIVE_TASK_STATES)

    def infer_active_task(self) -> str | None:
        active = self.active_task_ids()
        if len(active) == 1:
            return active[0]
        return None

    def task_matches_changed_paths(self, task: dict[str, Any], phase: dict[str, Any], changed_paths: list[str]) -> bool:
        scopes = phase_scope(task["id"], phase)
        return any(any(scope_matches(path, scope) for scope in scopes) for path in changed_paths)

    def scoped_task_ids(self, changed_paths: list[str], *, states: set[str]) -> list[str]:
        if not changed_paths:
            return []

        matches: list[str] = []
        for task_id in self.task_ids_by_state(states):
            task = self.load_task(task_id)
            active_phase_id = task.get("active_phase_id")
            if not active_phase_id:
                continue
            try:
                _, _, phase = self.current_phase(task_id, active_phase_id)
            except WorkflowError:
                continue
            if self.task_matches_changed_paths(task, phase, changed_paths):
                matches.append(task_id)
        return matches

    def infer_hook_task(self, event: str, changed_paths: list[str]) -> str | None:
        if event == "pre_push":
            if not changed_paths:
                return None
            matches = self.scoped_task_ids(changed_paths, states=PRE_PUSH_TASK_STATES)
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise WorkflowError(
                    f"{event} requires explicit --task-id or WORKFLOW_TASK_ID when changed paths match multiple tasks: {', '.join(matches)}"
                )
            raise WorkflowError(
                f"{event} requires explicit --task-id or WORKFLOW_TASK_ID when unpushed changes do not map to a single task"
            )

        active = self.active_task_ids()
        if len(active) > 1:
            raise WorkflowError(
                f"{event} requires explicit --task-id or WORKFLOW_TASK_ID when multiple active tasks exist: {', '.join(active)}"
            )
        if len(active) == 1:
            return active[0]
        return None

    def build_run(
        self,
        task_id: str,
        phase_id: str | None,
        event: str,
        commands: list[dict[str, str]],
        result: str,
        evidence: list[str],
        error_fingerprint: str | None,
        next_action: str,
    ) -> dict[str, Any]:
        return {
            "id": f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid4().hex[:8]}",
            "task_id": task_id,
            "phase_id": phase_id,
            "event": event,
            "commands": commands,
            "result": result,
            "evidence": evidence,
            "error_fingerprint": error_fingerprint,
            "next_action": next_action,
            "timestamp": now_iso(),
        }

    def staged_or_worktree_paths(self, staged: bool = False) -> list[str]:
        try:
            return git_paths(self.root, staged=staged)
        except Exception:
            return []

    def unpushed_paths(self) -> list[str]:
        try:
            return unpushed_git_paths(self.root)
        except Exception:
            return []

    def circuit_breaker_path(self) -> Path:
        config = self.load_hooks_config()["guards"]["circuit_breaker"]
        return self.root / config["state_file"]

    def record_circuit_breaker(self, fingerprint: str) -> HookResult:
        config = self.load_hooks_config()["guards"]["circuit_breaker"]
        window = timedelta(seconds=int(config["window_seconds"]))
        threshold = int(config["threshold"])
        path = self.circuit_breaker_path()
        state = {"fingerprints": {}}
        if path.exists():
            state = read_json(path)

        now = datetime.now(timezone.utc)
        entries = state["fingerprints"].get(fingerprint, [])
        fresh_entries = []
        for entry in entries:
            try:
                entry_time = datetime.fromisoformat(entry)
            except ValueError:
                continue
            if now - entry_time <= window:
                fresh_entries.append(entry)
        fresh_entries.append(now_iso())
        state["fingerprints"][fingerprint] = fresh_entries
        write_json(path, state)

        if len(fresh_entries) >= threshold:
            return HookResult("circuit_breaker", "blocked", [f"circuit breaker open for {fingerprint}"])
        return HookResult("circuit_breaker", "passed", [f"failure count for {fingerprint}: {len(fresh_entries)}"])

    def run_hooks(
        self,
        event: str,
        task: dict[str, Any] | None = None,
        phase: dict[str, Any] | None = None,
        changed_paths: list[str] | None = None,
        command: str | None = None,
        user_validation_note: str | None = None,
    ) -> HookResult:
        config = self.load_hooks_config()
        guards = config["events"].get(event)
        if guards is None:
            raise WorkflowError(f"unknown hook event: {event}")

        messages: list[str] = []
        for guard_name in guards:
            if guard_name == "tdd_guard":
                result = tdd_guard(config["guards"]["tdd_guard"], changed_paths or [], phase)
            elif guard_name == "dangerous_cmd_guard":
                result = dangerous_cmd_guard(config["guards"]["dangerous_cmd_guard"], command or "")
            elif guard_name == "write_scope_guard":
                result = write_scope_guard(task["id"] if task else None, phase, changed_paths or [])
            elif guard_name == "latest_verified_run_guard":
                if task is None and event == "pre_push" and not (changed_paths or []):
                    result = HookResult("latest_verified_run_guard", "passed", ["no changed paths detected"])
                elif task is None:
                    raise WorkflowError(f"{event} requires task context")
                else:
                    result = latest_verified_run_guard(
                        task,
                        phase,
                        changed_paths or [],
                        load_run=self.load_run,
                        scope_sensitive=(event == "pre_push"),
                    )
            elif guard_name == "user_validation_guard":
                if task is None:
                    raise WorkflowError("pre_complete requires task context")
                result = user_validation_guard(user_validation_note, task)
            else:
                raise WorkflowError(f"unknown guard: {guard_name}")

            messages.extend(result.messages)
            if result.status != "passed":
                return HookResult(event, result.status, messages)
        return HookResult(event, "passed", messages)

    def open_circuit_if_needed(
        self,
        task: dict[str, Any],
        phases_payload: dict[str, Any],
        phase: dict[str, Any],
        fingerprint: str,
        note: str,
    ) -> int:
        breaker = self.record_circuit_breaker(fingerprint)
        if breaker.status != "blocked":
            return 1

        if phase["status"] != "blocked" and phase["status"] in {"failed", "completed", "in_progress", "pending"}:
            self.update_phase_state(phase, "blocked")
        task["state"] = "blocked"
        task["blocked_reason"] = note
        self.save_phases(task["id"], phases_payload)
        self.save_task(task["id"], task)
        return 2

    def start_phase(self, task_id: str, phase_id: str | None) -> None:
        task, phases_payload, phase = self.current_phase(task_id, phase_id)
        if task["state"] not in {"approved", "in_progress", "failed", "blocked"}:
            raise WorkflowError(f"task state does not allow start: {task['state']}")
        if phase["status"] not in {"pending", "failed", "blocked"}:
            raise WorkflowError(f"phase state does not allow start: {phase['status']}")

        self.update_phase_state(phase, "in_progress")
        task["state"] = "in_progress"
        task["active_phase_id"] = phase["id"]
        task["blocked_reason"] = None
        task["last_verified_run_id"] = None
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)

    def complete_phase(
        self,
        task_id: str,
        phase_id: str | None,
        changed_paths: list[str],
        note: str | None,
        evidence: list[str],
    ) -> None:
        task, phases_payload, phase = self.current_phase(task_id, phase_id)
        if phase["status"] != "in_progress":
            raise WorkflowError("phase must be in_progress before completion")

        final_paths = sorted(set(changed_paths or self.staged_or_worktree_paths(staged=False)))
        violations = out_of_scope_paths(task_id, phase, final_paths)
        if violations:
            raise WorkflowError(f"changed paths outside allowed_write_paths: {', '.join(violations)}")

        for event in ("post_change", "pre_phase_complete"):
            hook_result = self.run_hooks(event, task=task, phase=phase, changed_paths=final_paths)
            if hook_result.status != "passed":
                raise WorkflowError("; ".join(hook_result.messages))

        self.update_phase_state(phase, "completed")
        run = self.build_run(
            task_id,
            phase["id"],
            "phase_completion",
            [{"command": "phase completion", "status": "passed", "output": ", ".join(final_paths)}],
            "passed",
            evidence + ([note] if note else []),
            None,
            "verify",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        task["last_verified_run_id"] = None
        task["blocked_reason"] = None
        task["active_phase_id"] = phase["id"]
        task["state"] = "in_progress"
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)

    def fail_phase(self, task_id: str, phase_id: str | None, fingerprint: str | None, note: str | None) -> int:
        task, phases_payload, phase = self.current_phase(task_id, phase_id)
        if phase["status"] not in {"pending", "in_progress", "failed"}:
            raise WorkflowError("phase cannot be failed from current state")

        if phase["status"] == "pending":
            self.update_phase_state(phase, "in_progress")
        if phase["status"] != "failed":
            self.update_phase_state(phase, "failed")
        phase["retry_count"] += 1

        run = self.build_run(
            task_id,
            phase["id"],
            "phase_failure",
            [{"command": "phase failure", "status": "failed", "output": note or ""}],
            "failed",
            [note] if note else [],
            fingerprint,
            "repair or retry",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        task["last_verified_run_id"] = None
        task["active_phase_id"] = phase["id"]

        if fingerprint:
            code = self.open_circuit_if_needed(
                task,
                phases_payload,
                phase,
                fingerprint,
                note or f"repeated failure in {phase['id']}",
            )
            if code == 2:
                return 2

        task["state"] = "failed"
        task["blocked_reason"] = None
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)
        return 1

    def block_phase(self, task_id: str, phase_id: str | None, note: str | None) -> None:
        task, phases_payload, phase = self.current_phase(task_id, phase_id)
        reason = note or f"manual block on {phase['id']}"
        if phase["status"] not in {"pending", "in_progress", "failed", "completed"}:
            raise WorkflowError("phase cannot be blocked from current state")
        if phase["status"] != "blocked":
            self.update_phase_state(phase, "blocked")

        run = self.build_run(
            task_id,
            phase["id"],
            "phase_blocked",
            [{"command": "phase blocked", "status": "blocked", "output": reason}],
            "blocked",
            [reason],
            None,
            "manual intervention",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        task["last_verified_run_id"] = None
        task["state"] = "blocked"
        task["blocked_reason"] = reason
        task["active_phase_id"] = phase["id"]
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)

    def verification_fingerprint(self, phase: dict[str, Any], command: str) -> str:
        return f"verification:{phase['id']}:{command.strip()}"

    def verify_task(self, task_id: str, phase_id: str | None, commands: list[str] | None, evidence: list[str]) -> int:
        task, phases_payload, phase = self.current_phase(task_id, phase_id)
        if phase["status"] != "completed":
            raise WorkflowError("verification requires phase status completed")

        command_list = commands or phase["acceptance"]["commands"]
        if not command_list:
            raise WorkflowError("verification commands are required")

        command_results: list[dict[str, str]] = []
        overall = "passed"
        failure_fingerprint: str | None = None
        block_reason: str | None = None
        for command in command_list:
            guard = self.run_hooks("pre_command", task=task, phase=phase, command=command)
            if guard.status != "passed":
                overall = "blocked"
                block_reason = "; ".join(guard.messages)
                command_results.append({"command": command, "status": "blocked", "output": block_reason})
                break

            result = subprocess.run(command, cwd=self.root, shell=True, capture_output=True, text=True)
            status = "passed" if result.returncode == 0 else "failed"
            output = compact_output(result.stdout, result.stderr)
            command_results.append({"command": command, "status": status, "output": output})
            if status == "failed":
                overall = "failed"
                failure_fingerprint = self.verification_fingerprint(phase, command)
                break

        next_action = "review" if overall == "passed" else ("manual intervention" if overall == "blocked" else "repair")
        run = self.build_run(
            task_id,
            phase["id"],
            "verification",
            command_results,
            overall,
            evidence,
            failure_fingerprint,
            next_action,
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        task["active_phase_id"] = phase["id"]

        if overall == "passed":
            task["last_verified_run_id"] = run["id"]
            task["blocked_reason"] = None
            next_phase = self.next_pending_phase_id(phases_payload)
            if phase["status"] == "completed" and next_phase:
                task["active_phase_id"] = next_phase
                task["state"] = "approved"
            else:
                task["state"] = "in_progress"
            self.save_phases(task_id, phases_payload)
            self.save_task(task_id, task)
            return 0

        task["last_verified_run_id"] = None
        if phase["status"] != "failed":
            self.update_phase_state(phase, "failed" if overall == "failed" else "blocked")
        phase["retry_count"] += 1

        if overall == "blocked":
            task["state"] = "blocked"
            task["blocked_reason"] = block_reason or f"verification blocked for {phase['id']}"
            self.save_phases(task_id, phases_payload)
            self.save_task(task_id, task)
            return 2

        code = self.open_circuit_if_needed(
            task,
            phases_payload,
            phase,
            failure_fingerprint or f"verification:{phase['id']}",
            f"repeated verification failure in {phase['id']}",
        )
        if code == 2:
            return 2

        task["state"] = "failed"
        task["blocked_reason"] = None
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)
        return 1

    def review_task(self, task_id: str, note: str | None) -> None:
        task = self.load_task(task_id)
        phases_payload = self.load_phases(task_id)
        if not phases_payload["phases"]:
            raise WorkflowError("review requires planned phases")
        if any(phase["status"] != "completed" for phase in phases_payload["phases"]):
            raise WorkflowError("review requires all phases to be completed")

        _, _, phase = self.current_phase(task_id, task["active_phase_id"])
        hook = self.run_hooks("pre_review", task=task, phase=phase)
        if hook.status != "passed":
            raise WorkflowError("; ".join(hook.messages))

        if task["state"] != "review_ready":
            self.update_task_state(task, "review_ready")
        run = self.build_run(
            task_id,
            phase["id"],
            "review_ready",
            [{"command": "review gate", "status": "passed", "output": "; ".join(hook.messages)}],
            "passed",
            [note] if note else [],
            None,
            "user validation",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        self.save_task(task_id, task)

    def close_review(self, task_id: str, note: str) -> None:
        task = self.load_task(task_id)
        if task["state"] != "review_ready":
            raise WorkflowError("review closeout requires state=review_ready")

        task["user_validated"] = True
        task["user_validation_note"] = note
        hook = self.run_hooks("pre_complete", task=task, user_validation_note=note)
        if hook.status != "passed":
            raise WorkflowError("; ".join(hook.messages))

        self.update_task_state(task, "completed")
        task["blocked_reason"] = None
        run = self.build_run(
            task_id,
            task["active_phase_id"],
            "review_closeout",
            [{"command": "complete task", "status": "passed", "output": note}],
            "passed",
            [note],
            None,
            "done",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        self.save_task(task_id, task)

    def reopen_task(self, task_id: str, note: str, phase_id: str | None) -> None:
        task = self.load_task(task_id)
        phases_payload = self.load_phases(task_id)
        if task["state"] not in {"failed", "blocked", "review_ready", "completed"}:
            raise WorkflowError("reopen requires failed, blocked, review_ready, or completed task")

        target_phase: dict[str, Any] | None = None
        if phase_id:
            for candidate in phases_payload["phases"]:
                if candidate["id"] == phase_id:
                    target_phase = candidate
                    break
            if target_phase is None:
                raise WorkflowError(f"phase not found: {phase_id}")
        else:
            ordered = sorted(phases_payload["phases"], key=lambda item: item["order"])
            target_phase = next((phase for phase in ordered if phase["status"] in {"failed", "blocked", "pending"}), None)
            if target_phase is None and task["active_phase_id"]:
                for candidate in ordered:
                    if candidate["id"] == task["active_phase_id"]:
                        target_phase = candidate
                        break

        if target_phase and target_phase["status"] in {"failed", "blocked", "completed"}:
            self.update_phase_state(target_phase, "pending")

        task["state"] = "approved"
        task["blocked_reason"] = None
        task["last_verified_run_id"] = None
        task["user_validated"] = False
        task["user_validation_note"] = None
        if target_phase is not None:
            task["active_phase_id"] = target_phase["id"]

        run = self.build_run(
            task_id,
            target_phase["id"] if target_phase else task["active_phase_id"],
            "reopened",
            [{"command": "reopen task", "status": "passed", "output": note}],
            "passed",
            [note],
            None,
            "plan or run",
        )
        self.write_run(task_id, run)
        task["latest_run_id"] = run["id"]
        self.save_phases(task_id, phases_payload)
        self.save_task(task_id, task)

    def status_payload(self, task_id: str) -> dict[str, Any]:
        return {"task": self.load_task(task_id), "phases": self.load_phases(task_id), "spec": inspect_spec(self.spec_path(task_id))}

    def check_all(self) -> list[str]:
        self.ensure_layout()
        errors = []
        for task_dir in sorted(self.tasks_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            task_id = task_dir.name
            try:
                task = self.load_task(task_id)
                phases = self.load_phases(task_id)
                spec = inspect_spec(self.spec_path(task_id))
                active_phase = None
                if task["active_phase_id"] is not None:
                    active_phase = next((phase for phase in phases["phases"] if phase["id"] == task["active_phase_id"]), None)
                    if active_phase is None:
                        raise WorkflowError("active phase does not exist")
                elif task["state"] != "draft" and phases["phases"]:
                    raise WorkflowError("planned task requires active phase")

                if active_phase is not None:
                    if task["state"] == "approved" and active_phase["status"] != "pending":
                        raise WorkflowError("approved task requires active phase status pending")
                    if task["state"] == "in_progress" and active_phase["status"] not in {"in_progress", "completed"}:
                        raise WorkflowError("in_progress task requires active phase status in_progress or completed")
                    if task["state"] == "failed" and active_phase["status"] != "failed":
                        raise WorkflowError("failed task requires active phase status failed")
                    if task["state"] == "blocked" and active_phase["status"] != "blocked":
                        raise WorkflowError("blocked task requires active phase status blocked")
                    if task["state"] in {"review_ready", "completed"} and active_phase["status"] != "completed":
                        raise WorkflowError(f"{task['state']} task requires active phase status completed")
                if task["state"] != "draft":
                    if not spec["ready_for_approval"]:
                        raise WorkflowError("approved-or-later task requires approval-ready spec.md")
                    if ensure_locked_intake(task["intake"]) != spec["intake"]:
                        raise WorkflowError("task.intake is out of sync with spec.md")
                if task["latest_run_id"] is not None:
                    self.load_run(task_id, task["latest_run_id"])
                if task["last_verified_run_id"] is not None:
                    run = self.load_run(task_id, task["last_verified_run_id"])
                    if run["event"] != "verification" or run["result"] != "passed":
                        raise WorkflowError("last_verified_run_id must point to passed verification")
                if task["state"] in {"review_ready", "completed"} and any(
                    phase["status"] != "completed" for phase in phases["phases"]
                ):
                    raise WorkflowError("review_ready/completed task requires every phase to be completed")
                for run_file in sorted(self.runs_dir(task_id).glob("*.json")):
                    validate_run(read_json(run_file))
            except WorkflowError as exc:
                errors.append(f"{task_id}: {exc}")
        return errors

    def doctor_report(self) -> dict[str, Any]:
        self.ensure_layout()
        return build_doctor_report(self.root, load_hooks_config=self.load_hooks_config, check_all=self.check_all)

    def normalize_changed_paths(self, paths: list[str]) -> list[str]:
        return sorted(set(normalize_repo_path(path) for path in paths))
