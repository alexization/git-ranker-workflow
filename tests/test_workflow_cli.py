from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "workflow.py"


class WorkflowCliTest(unittest.TestCase):
    def run_cli(self, root: Path, *args: str, expected: int = 0, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["WORKFLOW_ROOT"] = str(root)
        result = subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=REPO_ROOT,
            env=env,
            input=stdin,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout={result.stdout}\nstderr={result.stderr}",
        )
        return result

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def init_git_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.name", "Workflow Test"], cwd=root, capture_output=True, text=True, check=True)

    def git_config(self, root: Path, key: str) -> str:
        result = subprocess.run(
            ["git", "config", "--local", "--get", key],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def write_valid_agents(self, root: Path) -> None:
        (root / "AGENTS.md").write_text(
            (
                "# AGENTS.md\n\n"
                "## Mission\n\n"
                "- control plane only\n\n"
                "## Start Here\n\n"
                "1. read docs\n\n"
                "## CRITICAL Rules\n\n"
                "- CRITICAL: approved spec first\n\n"
                "## Architecture Boundaries\n\n"
                "ALWAYS: update app source of truth together.\n"
                "NEVER: bypass app source of truth.\n\n"
                "## Workflow Contract\n\n"
                "1. new\n"
                "2. approve\n"
                "3. plan\n\n"
                "## TDD Contract\n\n"
                "ALWAYS: tests with code.\n\n"
                "## Command Contract\n\n"
                "ALWAYS: use workflow.py.\n\n"
                "## Source Of Truth Order\n\n"
                "1. AGENTS.md\n\n"
                "## Forbidden Actions\n\n"
                "NEVER: edit canonical state manually.\n\n"
                "## Change Discipline\n\n"
                "ALWAYS: keep docs and tests aligned.\n"
            ),
            encoding="utf-8",
        )

    def finalize_spec(self, root: Path, task_id: str, title: str = "Harness V2") -> None:
        spec_path = root / "workflows" / "tasks" / task_id / "spec.md"
        spec_path.write_text(
            (
                f"# {title}\n\n"
                f"- Task ID: `{task_id}`\n"
                "- Primary Repo: `git-ranker-workflow`\n"
                "- Status: `draft`\n\n"
                "## Request\n\n"
                "- Codex 기준 workflow control plane을 강화한다.\n\n"
                "## Problem\n\n"
                "- 승인, phase, verification, hook contract가 느슨해서 자동화 신뢰도가 떨어진다.\n\n"
                "## Goals\n\n"
                "- spec 승인, phase 실행, verification, review를 JSON state로 강제한다.\n\n"
                "## Non-goals\n\n"
                "- 앱 저장소 동작 자체를 다시 설계하지 않는다.\n\n"
                "## Constraints\n\n"
                "- 기존 저장소 위에서 추가 요구사항을 계속 수용해야 한다.\n\n"
                "## Acceptance\n\n"
                "- approve/plan/run/verify/review/reopen 흐름이 CLI와 테스트로 검증된다.\n\n"
                "## Socratic Clarification Log\n\n"
                "- Q: 문서 구조는 어떻게 정리할까?\n"
                "- A: `tasks/`와 `system/`으로 역할을 나눈다.\n"
                "- Decision: 초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.\n"
            ),
            encoding="utf-8",
        )

    def write_phase_input(
        self,
        root: Path,
        commands: list[str],
        *,
        allowed_write_paths: list[str] | None = None,
        test_policy_mode: str = "require_tests",
        test_policy_evidence: list[str] | None = None,
    ) -> Path:
        phase_file = root / "phase-input.json"
        phase_file.write_text(
            json.dumps(
                {
                    "phases": [
                        {
                            "id": "phase-1",
                            "title": "build-runtime",
                            "goal": "create workflow runtime",
                            "inputs": ["spec.md"],
                            "allowed_write_paths": allowed_write_paths or ["scripts/", "tests/"],
                            "acceptance": {"commands": commands},
                            "test_policy": {
                                "mode": test_policy_mode,
                                "evidence": test_policy_evidence or [],
                            },
                        }
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return phase_file

    def write_repo_docs(self, root: Path) -> None:
        docs_dir = root / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "README.md").write_text(
            (
                "# Docs Index\n\n"
                "- AGENTS.md\n"
                "- docs/runtime.md\n"
                "- docs/artifact-model.md\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "artifact-model.md").write_text(
            (
                "# Artifact Model\n\n"
                "- task.json\n"
                "- intake\n"
                "- clarifications\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "runtime.md").write_text(
            (
                "# Runtime\n\n"
                "1. 소크라테스 질문\n"
                "2. approve\n"
                "3. plan\n"
                "4. review --close\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "hooks.md").write_text(
            (
                "# Hooks\n\n"
                "- .githooks/\n"
                "- TDD Guard\n"
                "- Dangerous Command Guard\n"
                "- Circuit Breaker\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "runbook.md").write_text(
            (
                "# Runbook\n\n"
                "- 사용자가 현재 spec 초안에 명시적으로 동의하면 approve 한다.\n"
                "- approve\n"
                "- plan\n"
            ),
            encoding="utf-8",
        )

    def set_breaker_threshold(self, root: Path, threshold: int) -> None:
        hooks_path = root / "workflows" / "system" / "hooks.json"
        payload = self.read_json(hooks_path)
        payload["guards"]["circuit_breaker"]["threshold"] = threshold
        hooks_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def bootstrap_task(
        self,
        root: Path,
        task_id: str,
        *,
        commands: list[str] | None = None,
        allowed_write_paths: list[str] | None = None,
        test_policy_mode: str = "require_tests",
        test_policy_evidence: list[str] | None = None,
    ) -> None:
        self.run_cli(root, "new", task_id, "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
        self.finalize_spec(root, task_id)
        self.run_cli(root, "approve", task_id, "--note", "approved by user")
        phase_file = self.write_phase_input(
            root,
            commands or ["python3 -c \"print('ok')\""],
            allowed_write_paths=allowed_write_paths,
            test_policy_mode=test_policy_mode,
            test_policy_evidence=test_policy_evidence,
        )
        self.run_cli(root, "plan", task_id, "--from", str(phase_file))

    def test_init_creates_system_layout_and_doctor_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-001",
                test_policy_mode="evidence_only",
                test_policy_evidence=["workflow CLI exercised by unit tests"],
            )
            self.run_cli(root, "doctor")
            self.run_cli(root, "status", "--check", "--all")

            task = self.read_json(root / "workflows" / "tasks" / "task-001" / "task.json")
            self.assertEqual(task["state"], "approved")
            self.assertEqual(task["intake"]["clarifications"][0]["resolved"], True)
            self.assertTrue((root / "workflows" / "system" / "hooks.json").exists())
            self.assertFalse((root / "workflows" / "config").exists())
            self.assertFalse((root / "workflows" / "schemas").exists())
            self.assertEqual(self.git_config(root, "core.hooksPath"), ".githooks")

            spec_text = (root / "workflows" / "tasks" / "task-001" / "spec.md").read_text(encoding="utf-8")
            self.assertIn("## Approval", spec_text)

    def test_plan_requires_explicit_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-002")
            self.run_cli(root, "approve", "task-002", "--note", "approved by user")
            self.run_cli(root, "plan", "task-002", expected=1)

    def test_approve_requires_structured_socratic_log_and_locks_intake(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002a", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            spec_path = root / "workflows" / "tasks" / "task-002a" / "spec.md"
            self.finalize_spec(root, "task-002a")
            spec_path.write_text(spec_path.read_text(encoding="utf-8").replace("- Decision: 초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.\n", ""), encoding="utf-8")

            result = self.run_cli(root, "approve", "task-002a", "--note", "approved by user", expected=1)
            self.assertIn("Socratic Clarification Log", result.stderr)

            self.finalize_spec(root, "task-002a")
            self.run_cli(root, "approve", "task-002a", "--note", "approved by user")

            task = self.read_json(root / "workflows" / "tasks" / "task-002a" / "task.json")
            self.assertEqual(task["intake"]["request_summary"], "Codex 기준 workflow control plane을 강화한다.")
            self.assertEqual(task["intake"]["goals"], ["spec 승인, phase 실행, verification, review를 JSON state로 강제한다."])
            self.assertEqual(len(task["intake"]["clarifications"]), 1)
            self.assertEqual(task["intake"]["clarifications"][0]["decision"], "초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.")

    def test_plan_requires_locked_intake_even_for_approved_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002b", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-002b")
            self.run_cli(root, "approve", "task-002b", "--note", "approved by user")

            task_path = root / "workflows" / "tasks" / "task-002b" / "task.json"
            task = self.read_json(task_path)
            task["intake"]["clarifications"] = []
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            phase_file = self.write_phase_input(root, ["python3 -c \"print('ok')\""])
            result = self.run_cli(root, "plan", "task-002b", "--from", str(phase_file), expected=1)
            self.assertIn("task.intake.clarifications", result.stderr)

    def test_status_reports_spec_readiness_for_draft_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002c", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-002c")
            spec_path = root / "workflows" / "tasks" / "task-002c" / "spec.md"
            spec_path.write_text(spec_path.read_text(encoding="utf-8").replace("- Decision: 초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.\n", ""), encoding="utf-8")

            result = self.run_cli(root, "status", "task-002c")
            payload = json.loads(result.stdout)
            self.assertEqual(payload["task"]["state"], "draft")
            self.assertFalse(payload["spec"]["ready_for_approval"])
            self.assertEqual(payload["spec"]["clarification_count"], 0)
            self.assertTrue(payload["spec"]["unresolved_clarifications"])

    def test_tdd_guard_blocks_completion_without_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(root, "task-003")
            self.run_cli(root, "run", "task-003", "--start")
            self.run_cli(
                root,
                "run",
                "task-003",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
                expected=1,
            )

    def test_write_scope_blocks_out_of_phase_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-004",
                test_policy_mode="evidence_only",
                test_policy_evidence=["generated code validated through existing test harness"],
            )
            self.run_cli(root, "run", "task-004", "--start")
            self.run_cli(
                root,
                "run",
                "task-004",
                "--complete",
                "--changed-path",
                "docs/README.md",
                expected=1,
            )

    def test_review_requires_last_verified_run_and_closeout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(root, "task-005")
            self.run_cli(root, "run", "task-005", "--start")
            self.run_cli(
                root,
                "run",
                "task-005",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
                "--changed-path",
                "tests/test_workflow_cli.py",
            )
            self.run_cli(root, "review", "task-005", "--note", "review ready", expected=1)
            self.run_cli(root, "verify", "task-005")
            self.run_cli(root, "review", "task-005", "--note", "review ready")
            self.run_cli(root, "review", "task-005", "--close", "--user-validation-note", "validated")

            task = self.read_json(root / "workflows" / "tasks" / "task-005" / "task.json")
            self.assertEqual(task["state"], "completed")
            self.assertTrue(task["user_validated"])
            self.assertIsNotNone(task["last_verified_run_id"])
            self.assertNotEqual(task["latest_run_id"], task["last_verified_run_id"])

    def test_pre_push_requires_verification_for_active_phase_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-006",
                test_policy_mode="evidence_only",
                test_policy_evidence=["runtime guard is exercised by CLI tests"],
            )
            self.run_cli(
                root,
                "hook",
                "pre_push",
                "--task-id",
                "task-006",
                "--phase-id",
                "phase-1",
                "--changed-path",
                "scripts/workflow.py",
                "--command-text",
                "git push origin feature",
                expected=1,
            )

            self.run_cli(root, "run", "task-006", "--start")
            self.run_cli(
                root,
                "run",
                "task-006",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
            )
            self.run_cli(root, "verify", "task-006")
            self.run_cli(
                root,
                "hook",
                "pre_push",
                "--task-id",
                "task-006",
                "--phase-id",
                "phase-1",
                "--changed-path",
                "scripts/workflow.py",
                "--command-text",
                "git push origin feature",
            )

    def test_reopen_resets_failed_task_for_repair_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-007",
                test_policy_mode="evidence_only",
                test_policy_evidence=["repair loop uses explicit reopen flow"],
            )
            self.run_cli(root, "run", "task-007", "--start")
            self.run_cli(
                root,
                "run",
                "task-007",
                "--fail",
                "--error-fingerprint",
                "same-error",
                "--note",
                "boom",
                expected=1,
            )
            self.run_cli(root, "reopen", "task-007", "--note", "retry after repair", "--phase-id", "phase-1")

            task = self.read_json(root / "workflows" / "tasks" / "task-007" / "task.json")
            phases = self.read_json(root / "workflows" / "tasks" / "task-007" / "phases.json")
            self.assertEqual(task["state"], "approved")
            self.assertIsNone(task["blocked_reason"])
            self.assertIsNone(task["last_verified_run_id"])
            self.assertEqual(task["active_phase_id"], "phase-1")
            self.assertEqual(phases["phases"][0]["status"], "pending")

    def test_circuit_breaker_triggers_from_verification_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-008",
                commands=["python3 -c \"import sys; sys.exit(1)\""],
                test_policy_mode="evidence_only",
                test_policy_evidence=["verification failure path is intentional in this test"],
            )
            self.set_breaker_threshold(root, 2)

            self.run_cli(root, "run", "task-008", "--start")
            self.run_cli(
                root,
                "run",
                "task-008",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
            )
            self.run_cli(root, "verify", "task-008", expected=1)

            self.run_cli(root, "reopen", "task-008", "--note", "retry after failed verification", "--phase-id", "phase-1")
            self.run_cli(root, "run", "task-008", "--start")
            self.run_cli(
                root,
                "run",
                "task-008",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
            )
            self.run_cli(root, "verify", "task-008", expected=2)

            task = self.read_json(root / "workflows" / "tasks" / "task-008" / "task.json")
            self.assertEqual(task["state"], "blocked")
            self.assertEqual(task["blocked_reason"], "repeated verification failure in phase-1")

    def test_doctor_fails_when_agents_constitution_is_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.run_cli(root, "init")
            self.write_repo_docs(root)
            (root / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")

            result = self.run_cli(root, "doctor", expected=1)
            report = json.loads(result.stdout)
            self.assertTrue(any("AGENTS.md missing heading" in error for error in report["errors"]))
            self.assertTrue(any("AGENTS.md missing constitution marker" in error for error in report["errors"]))

    def test_init_and_doctor_enforce_git_hooks_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.run_cli(root, "init")
            self.assertEqual(self.git_config(root, "core.hooksPath"), ".githooks")

            subprocess.run(["git", "config", "--local", "core.hooksPath", ".git/hooks"], cwd=root, capture_output=True, text=True, check=True)
            result = self.run_cli(root, "doctor", expected=1)
            report = json.loads(result.stdout)
            self.assertTrue(any("core.hooksPath" in error for error in report["errors"]))

    def test_doctor_fails_when_runbook_loses_socratic_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.run_cli(root, "init")
            self.write_repo_docs(root)
            self.write_valid_agents(root)
            (root / "docs" / "runbook.md").write_text("# Runbook\n\n- approve\n", encoding="utf-8")

            result = self.run_cli(root, "doctor", expected=1)
            report = json.loads(result.stdout)
            self.assertTrue(any("docs/runbook.md missing required marker" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
