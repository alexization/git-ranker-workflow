from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from workflow_runtime.constants import CURRENT_TASK_CONTRACT_VERSION, EVENT_LIMIT
from workflow_runtime.doctor import build_doctor_report
from workflow_runtime.git_ops import git_paths, unpushed_git_paths
from workflow_runtime.guards import dangerous_cmd_guard, user_validation_guard
from workflow_runtime.models import (
    HookResult,
    WorkflowError,
    compact_output,
    inspect_spec,
    normalize_repo_path,
    now_iso,
    read_json,
    scope_matches,
    spec_sha256,
    scope_to_progress,
    validate_relative_repo_path,
    validate_spec_for_approval,
    validate_state,
    validate_task_id,
    write_json,
)
from workflow_runtime.templates import approval_block, default_spec, empty_state_payload


SOURCE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = Path(os.environ.get("WORKFLOW_ROOT", SOURCE_ROOT))
ACTIVE_TASK_STATES = {"approved", "in_progress", "failed", "review_ready"}


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
            (SOURCE_ROOT / ".githooks" / "pre-push", self.root / ".githooks" / "pre-push"),
        )
        for source, target in surfaces:
            if not source.exists() or source == target:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if overwrite or not target.exists():
                shutil.copy2(source, target)

    def ensure_layout(self, *, sync: bool = False) -> None:
        self.system_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.sync_runtime_surface(overwrite=sync)

    def task_dir(self, task_id: str) -> Path:
        return self.tasks_dir / validate_task_id(task_id)

    def spec_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "spec.md"

    def state_path(self, task_id: str) -> Path:
        return self.task_dir(task_id) / "state.json"

    def load_hooks_config(self) -> dict[str, Any]:
        self.ensure_layout()
        return read_json(self.hooks_config_path)

    def load_state(self, task_id: str) -> dict[str, Any]:
        path = self.state_path(task_id)
        if not path.exists():
            raise WorkflowError(f"state not found: {task_id}")
        payload = read_json(path)
        validate_state(payload)
        return payload

    def save_state(self, task_id: str, payload: dict[str, Any]) -> None:
        payload["updated_at"] = now_iso()
        validate_state(payload)
        write_json(self.state_path(task_id), payload)

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
        try:
            self.spec_path(task_id).write_text(default_spec(task_id, title, primary_repo), encoding="utf-8")
            self.save_state(task_id, empty_state_payload(task_id, title, primary_repo))
        except Exception:
            shutil.rmtree(task_dir, ignore_errors=True)
            raise

    def add_event(
        self,
        state: dict[str, Any],
        event_type: str,
        *,
        imp_id: str | None = None,
        result: str = "passed",
        note: str = "",
        commands: list[dict[str, Any]] | None = None,
    ) -> None:
        state["events"].append(
            {
                "timestamp": now_iso(),
                "type": event_type,
                "imp_id": imp_id,
                "result": result,
                "note": note,
                "commands": commands or [],
            }
        )
        if len(state["events"]) > EVENT_LIMIT:
            state["events"] = state["events"][-EVENT_LIMIT:]

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
        state = self.load_state(task_id)
        if state["state"] not in {"draft", "approved", "failed"}:
            raise WorkflowError("approve requires draft, approved, or failed state")
        if not note.strip():
            raise WorkflowError("approval note is required")

        readiness = validate_spec_for_approval(self.spec_path(task_id))
        timestamp = now_iso()
        self.append_approval_to_spec(task_id, note.strip(), actor, timestamp)
        locked_hash = spec_sha256(self.spec_path(task_id))
        state["contract_version"] = CURRENT_TASK_CONTRACT_VERSION
        state["state"] = "approved"
        state["spec_lock"] = {
            "approved": True,
            "approved_at": timestamp,
            "approved_by": actor,
            "approval_note": note.strip(),
            "spec_sha256": locked_hash,
        }
        state["next_action"] = "Run plan to initialize implementation scope progress."
        state["blockers"] = []
        self.add_event(
            state,
            "approve",
            note=f"approved spec with {readiness['implementation_scope_count']} implementation scopes",
        )
        self.save_state(task_id, state)

    def ensure_spec_locked(self, task_id: str, state: dict[str, Any]) -> dict[str, Any]:
        if not state["spec_lock"]["approved"]:
            raise WorkflowError("spec is not approved")
        if spec_sha256(self.spec_path(task_id)) != state["spec_lock"]["spec_sha256"]:
            raise WorkflowError("spec.md has changed since approval; rerun approve before continuing")
        readiness = inspect_spec(self.spec_path(task_id))
        if not readiness["ready_for_approval"]:
            raise WorkflowError("approved task requires approval-ready spec.md")
        return readiness

    def plan_task(self, task_id: str) -> None:
        state = self.load_state(task_id)
        if state["state"] not in {"approved", "in_progress", "failed"}:
            raise WorkflowError("plan requires approved, in_progress, or failed state")
        readiness = self.ensure_spec_locked(task_id, state)

        existing = {scope["imp_id"]: scope for scope in state["implementation_scopes"]}
        planned: list[dict[str, Any]] = []
        for scope in readiness["intake"]["implementation_scopes"]:
            progress = existing.get(scope["imp_id"])
            if progress is None:
                progress = scope_to_progress(scope)
            else:
                progress["title"] = scope["title"]
                progress["target_repos"] = scope["target_repos"]
                progress["change_paths"] = scope["change_paths"]
                progress["policy"] = scope["policy"]
                if not progress["verification"].get("commands"):
                    progress["verification"]["commands"] = scope_to_progress(scope)["verification"]["commands"]
            planned.append(progress)

        state["implementation_scopes"] = planned
        state["state"] = "approved"
        state["current_focus"] = {"imp_id": None, "status": "idle", "started_at": None, "note": ""}
        state["next_action"] = "Run the next pending IMP with `run --start`."
        state["blockers"] = []
        self.add_event(state, "plan", note=f"planned {len(planned)} implementation scopes")
        self.save_state(task_id, state)

    def implementation_scope(self, state: dict[str, Any], imp_id: str) -> dict[str, Any]:
        for scope in state["implementation_scopes"]:
            if scope["imp_id"] == imp_id:
                return scope
        raise WorkflowError(f"implementation scope not found: {imp_id}")

    def next_startable_scope(self, state: dict[str, Any]) -> dict[str, Any]:
        for scope in state["implementation_scopes"]:
            if scope["status"] in {"pending", "failed"}:
                return scope
        raise WorkflowError("no pending implementation scope")

    def active_scope(self, state: dict[str, Any]) -> dict[str, Any]:
        imp_id = state["current_focus"].get("imp_id")
        if not imp_id:
            raise WorkflowError("no active implementation scope")
        return self.implementation_scope(state, imp_id)

    def start_scope(self, task_id: str, imp_id: str | None, note: str | None = None) -> None:
        state = self.load_state(task_id)
        if state["state"] not in {"approved", "in_progress", "failed"}:
            raise WorkflowError(f"state does not allow start: {state['state']}")
        self.ensure_spec_locked(task_id, state)
        if not state["implementation_scopes"]:
            raise WorkflowError("plan must run before implementation starts")
        active = next((existing for existing in state["implementation_scopes"] if existing["status"] == "in_progress"), None)
        if active:
            raise WorkflowError(f"complete or fail active implementation scope before starting another: {active['imp_id']}")

        scope = self.implementation_scope(state, imp_id) if imp_id else self.next_startable_scope(state)
        if scope["status"] not in {"pending", "failed"}:
            raise WorkflowError(f"implementation scope state does not allow start: {scope['status']}")
        timestamp = now_iso()
        scope["status"] = "in_progress"
        scope["started_at"] = timestamp
        scope["completed_at"] = None
        scope["note"] = note or ""
        scope["verification"]["status"] = "not_run"
        scope["verification"]["last_run_at"] = None
        scope["verification"]["results"] = []
        state["state"] = "in_progress"
        state["current_focus"] = {
            "imp_id": scope["imp_id"],
            "status": "in_progress",
            "started_at": timestamp,
            "note": note or "",
        }
        state["next_action"] = f"Implement {scope['imp_id']} then run --complete."
        state["blockers"] = []
        self.add_event(state, "start", imp_id=scope["imp_id"], note=note or "")
        self.save_state(task_id, state)

    def scope_delta(self, task_id: str, scope: dict[str, Any], changed_paths: list[str]) -> list[str]:
        allowed = [*scope["change_paths"], f"workflows/tasks/{task_id}/"]
        delta = []
        for path in changed_paths:
            if not any(scope_matches(path, allowed_path) for allowed_path in allowed):
                delta.append(path)
        return sorted(set(delta))

    def complete_scope(
        self,
        task_id: str,
        imp_id: str | None,
        changed_paths: list[str],
        note: str | None,
        evidence: list[str],
    ) -> None:
        state = self.load_state(task_id)
        if imp_id:
            scope = self.implementation_scope(state, imp_id)
        else:
            scope = self.active_scope(state)
        if scope["status"] != "in_progress":
            raise WorkflowError("implementation scope must be in_progress before completion")

        final_paths = sorted(set(changed_paths or self.staged_or_worktree_paths(staged=False)))
        scope["status"] = "completed"
        scope["changed_paths"] = final_paths
        scope["scope_delta"] = self.scope_delta(task_id, scope, final_paths)
        scope["completed_at"] = now_iso()
        scope["note"] = note or ("; ".join(evidence) if evidence else "")
        state["state"] = "in_progress"
        state["current_focus"] = {"imp_id": None, "status": "idle", "started_at": None, "note": ""}
        if scope["scope_delta"]:
            state["next_action"] = f"Review scope delta for {scope['imp_id']} before verification."
        else:
            state["next_action"] = f"Run verify for {scope['imp_id']}."
        self.add_event(
            state,
            "complete",
            imp_id=scope["imp_id"],
            note=note or "",
            commands=[{"changed_paths": final_paths, "scope_delta": scope["scope_delta"]}],
        )
        self.save_state(task_id, state)

    def fail_scope(self, task_id: str, imp_id: str | None, note: str | None) -> int:
        state = self.load_state(task_id)
        scope = self.implementation_scope(state, imp_id) if imp_id else self.active_scope(state)
        scope["status"] = "failed"
        scope["note"] = note or ""
        state["state"] = "failed"
        state["blockers"] = [note or f"failed implementation scope: {scope['imp_id']}"]
        state["current_focus"] = {
            "imp_id": scope["imp_id"],
            "status": "failed",
            "started_at": scope.get("started_at"),
            "note": note or "",
        }
        state["next_action"] = f"Repair or reopen {scope['imp_id']}."
        self.add_event(state, "fail", imp_id=scope["imp_id"], result="failed", note=note or "")
        self.save_state(task_id, state)
        return 1

    def command_payloads(self, commands: list[str] | None, scope: dict[str, Any]) -> list[dict[str, str]]:
        if commands:
            return [{"cmd": command.strip(), "cwd": "."} for command in commands if command.strip()]
        return list(scope["verification"]["commands"])

    def verification_target(self, state: dict[str, Any], imp_id: str | None) -> dict[str, Any]:
        if imp_id:
            return self.implementation_scope(state, imp_id)
        focus = state["current_focus"].get("imp_id")
        if focus:
            scope = self.implementation_scope(state, focus)
            if scope["status"] == "completed":
                return scope
        for scope in state["implementation_scopes"]:
            if scope["status"] == "completed" and scope["verification"]["status"] != "passed":
                return scope
        raise WorkflowError("no completed implementation scope requires verification")

    def verify_task(self, task_id: str, imp_id: str | None, commands: list[str] | None, evidence: list[str]) -> int:
        state = self.load_state(task_id)
        self.ensure_spec_locked(task_id, state)
        scope = self.verification_target(state, imp_id)
        if scope["status"] != "completed":
            raise WorkflowError("verification requires completed implementation scope")

        command_list = self.command_payloads(commands, scope)
        if not command_list:
            raise WorkflowError("verification commands are required")

        results: list[dict[str, str]] = []
        overall = "passed"
        for command in command_list:
            guard = self.run_hooks("pre_command", command=command["cmd"])
            if guard.status != "passed":
                results.append({"command": command["cmd"], "cwd": command["cwd"], "status": "failed", "output": "; ".join(guard.messages)})
                overall = "failed"
                break

            cwd = self.root / command["cwd"]
            result = subprocess.run(command["cmd"], cwd=cwd, shell=True, capture_output=True, text=True)
            status = "passed" if result.returncode == 0 else "failed"
            results.append(
                {
                    "command": command["cmd"],
                    "cwd": command["cwd"],
                    "status": status,
                    "output": compact_output(result.stdout, result.stderr),
                }
            )
            if status == "failed":
                overall = "failed"
                break

        scope["verification"]["status"] = overall
        scope["verification"]["last_run_at"] = now_iso()
        scope["verification"]["results"] = results

        if overall == "passed":
            state["blockers"] = []
            if self.all_scopes_verified(state):
                state["next_action"] = "Run review to request user validation."
            else:
                state["next_action"] = "Run the next pending IMP with `run --start`."
            self.add_event(state, "verify", imp_id=scope["imp_id"], result="passed", note="; ".join(evidence), commands=results)
            self.save_state(task_id, state)
            return 0

        scope["status"] = "failed"
        state["state"] = "failed"
        state["blockers"] = [f"verification failed for {scope['imp_id']}"]
        state["next_action"] = f"Repair {scope['imp_id']} and rerun verification."
        self.add_event(state, "verify", imp_id=scope["imp_id"], result="failed", note="; ".join(evidence), commands=results)
        self.save_state(task_id, state)
        return 1

    def all_scopes_verified(self, state: dict[str, Any]) -> bool:
        return bool(state["implementation_scopes"]) and all(
            scope["status"] == "completed" and scope["verification"]["status"] == "passed"
            for scope in state["implementation_scopes"]
        )

    def review_task(self, task_id: str, note: str | None) -> None:
        state = self.load_state(task_id)
        if not self.all_scopes_verified(state):
            raise WorkflowError("review requires every implementation scope to be completed and verified")
        state["state"] = "review_ready"
        state["next_action"] = "Ask the user to validate the result, then run review --close."
        self.add_event(state, "review_ready", note=note or "")
        self.save_state(task_id, state)

    def close_review(self, task_id: str, note: str) -> None:
        state = self.load_state(task_id)
        if state["state"] != "review_ready":
            raise WorkflowError("review closeout requires state=review_ready")
        hook = self.run_hooks("pre_complete", state=state, user_validation_note=note)
        if hook.status != "passed":
            raise WorkflowError("; ".join(hook.messages))

        timestamp = now_iso()
        state["user_validation"] = {"validated": True, "note": note, "validated_at": timestamp}
        state["state"] = "completed"
        state["next_action"] = "done"
        state["blockers"] = []
        self.add_event(state, "review_closeout", result="passed", note=note)
        self.save_state(task_id, state)

    def reopen_task(self, task_id: str, note: str, imp_id: str | None) -> None:
        state = self.load_state(task_id)
        if state["state"] not in {"in_progress", "failed", "review_ready", "completed"}:
            raise WorkflowError("reopen requires in_progress, failed, review_ready, or completed state")
        if not state["implementation_scopes"]:
            raise WorkflowError("reopen requires planned implementation scopes")

        target = self.implementation_scope(state, imp_id) if imp_id else None
        if target is None:
            target = next((scope for scope in state["implementation_scopes"] if scope["status"] == "failed"), None)
        if target is None:
            target = self.implementation_scope(state, state["current_focus"]["imp_id"]) if state["current_focus"].get("imp_id") else state["implementation_scopes"][0]

        target_index = state["implementation_scopes"].index(target)
        for scope in state["implementation_scopes"][target_index:]:
            scope["status"] = "pending"
            scope["completed_at"] = None
            scope["verification"]["status"] = "not_run"
            scope["verification"]["last_run_at"] = None
            scope["verification"]["results"] = []

        state["state"] = "approved"
        state["current_focus"] = {"imp_id": None, "status": "idle", "started_at": None, "note": ""}
        state["user_validation"] = {"validated": False, "note": None, "validated_at": None}
        state["blockers"] = []
        state["next_action"] = f"Restart {target['imp_id']} with run --start."
        self.add_event(state, "reopen", imp_id=target["imp_id"], note=note)
        self.save_state(task_id, state)

    def task_ids_by_state(self, states: set[str]) -> list[str]:
        if not self.tasks_dir.exists():
            return []
        active: list[str] = []
        for candidate in sorted(self.tasks_dir.iterdir()):
            if not candidate.is_dir():
                continue
            state_file = candidate / "state.json"
            if not state_file.exists():
                continue
            state = read_json(state_file)
            if state.get("state") in states:
                active.append(state.get("task_id") or candidate.name)
        return active

    def active_task_ids(self) -> list[str]:
        return self.task_ids_by_state(ACTIVE_TASK_STATES)

    def infer_active_task(self) -> str | None:
        active = self.active_task_ids()
        if len(active) == 1:
            return active[0]
        return None

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

    def run_hooks(
        self,
        event: str,
        *,
        state: dict[str, Any] | None = None,
        command: str | None = None,
        user_validation_note: str | None = None,
    ) -> HookResult:
        config = self.load_hooks_config()
        guards = config["events"].get(event)
        if guards is None:
            raise WorkflowError(f"unknown hook event: {event}")

        messages: list[str] = []
        for guard_name in guards:
            if guard_name == "dangerous_cmd_guard":
                result = dangerous_cmd_guard(config["guards"]["dangerous_cmd_guard"], command or "")
            elif guard_name == "user_validation_guard":
                if state is None:
                    raise WorkflowError("pre_complete requires task context")
                result = user_validation_guard(user_validation_note, state)
            else:
                raise WorkflowError(f"unknown guard: {guard_name}")

            messages.extend(result.messages)
            if result.status != "passed":
                return HookResult(event, result.status, messages)
        return HookResult(event, "passed", messages)

    def status_payload(self, task_id: str) -> dict[str, Any]:
        state = self.load_state(task_id)
        spec = inspect_spec(self.spec_path(task_id))
        lock_hash = state["spec_lock"].get("spec_sha256")
        return {
            "state": state,
            "spec": spec,
            "spec_lock_current": bool(lock_hash and lock_hash == spec.get("spec_sha256")),
        }

    def incomplete_task_error(self, task_dir: Path) -> str | None:
        missing = []
        if not (task_dir / "spec.md").exists():
            missing.append("spec.md")
        if not (task_dir / "state.json").exists():
            missing.append("state.json")
        if missing:
            return f"{task_dir.name}: incomplete task directory missing {', '.join(missing)}"
        return None

    def check_all(self) -> list[str]:
        self.ensure_layout()
        errors: list[str] = []
        for task_dir in sorted(self.tasks_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            if not any(candidate.is_file() for candidate in task_dir.rglob("*")):
                continue
            task_id = task_dir.name
            try:
                incomplete = self.incomplete_task_error(task_dir)
                if incomplete:
                    raise WorkflowError(incomplete.removeprefix(f"{task_id}: "))
                if (task_dir / "task.json").exists():
                    raise WorkflowError("legacy task.json must not exist")
                if (task_dir / "phases.json").exists():
                    raise WorkflowError("legacy phases.json must not exist")
                if (task_dir / "runs").exists():
                    raise WorkflowError("legacy runs directory must not exist")

                state = self.load_state(task_id)
                spec = inspect_spec(self.spec_path(task_id))
                if state["state"] != "draft":
                    if not spec["ready_for_approval"]:
                        raise WorkflowError("approved-or-later task requires approval-ready spec.md")
                    if state["spec_lock"]["spec_sha256"] != spec.get("spec_sha256"):
                        raise WorkflowError("state.spec_lock.spec_sha256 is out of sync with spec.md")
                if state["state"] in {"review_ready", "completed"} and not self.all_scopes_verified(state):
                    raise WorkflowError(f"{state['state']} state requires every implementation scope to be verified")
            except WorkflowError as exc:
                errors.append(f"{task_id}: {exc}")
        return errors

    def doctor_report(self) -> dict[str, Any]:
        self.ensure_layout()
        return build_doctor_report(self.root, load_hooks_config=self.load_hooks_config, check_all=self.check_all)

    def normalize_changed_paths(self, paths: list[str]) -> list[str]:
        return sorted(set(normalize_repo_path(path) for path in paths))
