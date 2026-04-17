from __future__ import annotations

import json
import os
import shutil
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

    def run_hook_script(
        self,
        root: Path,
        hook_name: str,
        *args: str,
        expected: int = 0,
        env_extra: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["WORKFLOW_ROOT"] = str(root)
        if env_extra:
            env.update(env_extra)
        result = subprocess.run(
            [str(root / ".githooks" / hook_name), *args],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout={result.stdout}\nstderr={result.stderr}",
        )
        return result

    def init_git_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, capture_output=True, text=True, check=True)
        subprocess.run(["git", "config", "user.name", "Workflow Test"], cwd=root, capture_output=True, text=True, check=True)

    def install_runtime_surface(self, root: Path) -> None:
        shutil.copytree(
            REPO_ROOT / "scripts",
            root / "scripts",
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    def git_add(self, root: Path, *paths: str) -> None:
        subprocess.run(["git", "add", *paths], cwd=root, capture_output=True, text=True, check=True)

    def git_commit(self, root: Path, message: str) -> None:
        subprocess.run(["git", "commit", "-m", message], cwd=root, capture_output=True, text=True, check=True)

    def git_commit_no_verify(self, root: Path, message: str) -> None:
        subprocess.run(["git", "commit", "--no-verify", "-m", message], cwd=root, capture_output=True, text=True, check=True)

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
                "- Status: resolved\n"
                "- Q: 이 workflow가 반드시 보장해야 하는 핵심 목표는 무엇일까?\n"
                "- A: spec 승인, phase 실행, verification, review의 제어 지점을 JSON state로 잠그는 것이다.\n"
                "- Decision: workflow는 승인과 실행 상태를 artifact 기반으로 고정해야 한다.\n"
                "- Status: resolved\n"
            ),
            encoding="utf-8",
        )

    def write_phase_input(
        self,
        root: Path,
        commands: list[str],
        *,
        phase_count: int = 1,
        inputs: list[str] | None = None,
        allowed_write_paths: list[str] | None = None,
        test_policy_mode: str = "require_tests",
        test_policy_evidence: list[str] | None = None,
        include_bootstrap_fields: bool = True,
    ) -> Path:
        phase_file = root / "phase-input.json"
        phases = []
        for index in range(1, phase_count + 1):
            phase = {
                "id": f"phase-{index}",
                "title": f"build-runtime-{index}",
                "goal": f"create workflow runtime {index}",
                "inputs": inputs if inputs is not None else ["spec.md"],
                "allowed_write_paths": allowed_write_paths or ["scripts/", "tests/"],
                "acceptance": {"commands": commands if index == 1 else [f"python3 -c \"print('phase {index} ok')\""]},
                "test_policy": {
                    "mode": test_policy_mode,
                    "evidence": test_policy_evidence or [],
                },
            }
            if include_bootstrap_fields:
                phase.update(
                    {
                        "required_reads": ["spec.md", "task.json", "phases.json"],
                        "starting_points": [f"Inspect active phase {index}", "Review allowed write scope"],
                        "deliverables": [f"Complete phase {index} changes"],
                        "completion_signal": f"phase-{index} acceptance commands pass",
                    }
                )
            phases.append(phase)
        phase_file.write_text(
            json.dumps(
                {"phases": phases},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return phase_file

    def write_spec_with_clarifications(
        self,
        root: Path,
        task_id: str,
        clarifications: list[tuple[str, str | None, str | None, str]],
        *,
        title: str = "Harness V2",
    ) -> None:
        lines = [
            f"# {title}",
            "",
            f"- Task ID: `{task_id}`",
            "- Primary Repo: `git-ranker-workflow`",
            "- Status: `draft`",
            "",
            "## Request",
            "",
            "- Codex 기준 workflow control plane을 강화한다.",
            "",
            "## Problem",
            "",
            "- 승인, phase, verification, hook contract가 느슨해서 자동화 신뢰도가 떨어진다.",
            "",
            "## Goals",
            "",
            "- spec 승인, phase 실행, verification, review를 JSON state로 강제한다.",
            "",
            "## Non-goals",
            "",
            "- 앱 저장소 동작 자체를 다시 설계하지 않는다.",
            "",
            "## Constraints",
            "",
            "- 기존 저장소 위에서 추가 요구사항을 계속 수용해야 한다.",
            "",
            "## Acceptance",
            "",
            "- approve/plan/run/verify/review/reopen 흐름이 CLI와 테스트로 검증된다.",
            "",
            "## Socratic Clarification Log",
            "",
        ]
        for question, answer, decision, status in clarifications:
            lines.append(f"- Q: {question}")
            if answer is not None:
                lines.append(f"- A: {answer}")
            if decision is not None:
                lines.append(f"- Decision: {decision}")
            lines.append(f"- Status: {status}")
        spec_path = root / "workflows" / "tasks" / task_id / "spec.md"
        spec_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

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
                "- status\n"
                "- kickoff_required_for_phase\n"
                "- required_reads\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "runtime.md").write_text(
            (
                "# Runtime\n\n"
                "1. 소크라테스 질문\n"
                "2. Status: open\n"
                "2. approve\n"
                "3. plan\n"
                "4. kickoff\n"
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
                "- workflow.py hook\n"
            ),
            encoding="utf-8",
        )
        (docs_dir / "runbook.md").write_text(
            (
                "# Runbook\n\n"
                "- Status: open\n"
                "- 사용자가 현재 spec 초안에 명시적으로 동의하면 approve 한다.\n"
                "- approve\n"
                "- plan\n"
                "- kickoff\n"
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
            self.assertEqual(task["intake"]["clarifications"][0]["status"], "resolved")
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
            spec_path.write_text(
                spec_path.read_text(encoding="utf-8").replace(
                    "- Status: resolved\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )

            result = self.run_cli(root, "approve", "task-002a", "--note", "approved by user", expected=1)
            self.assertIn("Status", result.stderr)

            self.finalize_spec(root, "task-002a")
            self.run_cli(root, "approve", "task-002a", "--note", "approved by user")

            task = self.read_json(root / "workflows" / "tasks" / "task-002a" / "task.json")
            self.assertEqual(task["intake"]["request_summary"], "Codex 기준 workflow control plane을 강화한다.")
            self.assertEqual(task["intake"]["goals"], ["spec 승인, phase 실행, verification, review를 JSON state로 강제한다."])
            self.assertEqual(len(task["intake"]["clarifications"]), 2)
            self.assertEqual(task["intake"]["clarifications"][0]["decision"], "초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.")
            self.assertEqual(task["intake"]["clarifications"][0]["status"], "resolved")

    def test_plan_requires_locked_intake_even_for_approved_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002b", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-002b")
            self.run_cli(root, "approve", "task-002b", "--note", "approved by user")

            task_path = root / "workflows" / "tasks" / "task-002b" / "task.json"
            task = self.read_json(task_path)
            task["intake"]["clarifications"][0]["status"] = "open"
            task["intake"]["clarifications"][0]["decision"] = None
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            phase_file = self.write_phase_input(root, ["python3 -c \"print('ok')\""])
            result = self.run_cli(root, "plan", "task-002b", "--from", str(phase_file), expected=1)
            self.assertIn("must all be resolved", result.stderr)

    def test_status_reports_spec_readiness_for_draft_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002c", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.write_spec_with_clarifications(
                root,
                "task-002c",
                [
                    ("문서 구조는 어떻게 정리할까?", "`tasks/`와 `system/`으로 역할을 나눈다.", "초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.", "resolved"),
                    ("사용자 확인이 더 필요한 부분은 무엇일까?", None, None, "open"),
                ],
            )

            result = self.run_cli(root, "status", "task-002c")
            payload = json.loads(result.stdout)
            self.assertEqual(payload["task"]["state"], "draft")
            self.assertFalse(payload["spec"]["ready_for_approval"])
            self.assertEqual(payload["spec"]["clarification_count"], 2)
            self.assertEqual(payload["spec"]["open_clarification_count"], 1)
            self.assertEqual(payload["spec"]["resolved_clarification_count"], 1)
            self.assertEqual(payload["spec"]["open_clarifications"], ["사용자 확인이 더 필요한 부분은 무엇일까?"])

    def test_plan_keeps_legacy_empty_inputs_compatible_without_required_reads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002cc", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")

            task_path = root / "workflows" / "tasks" / "task-002cc" / "task.json"
            task = self.read_json(task_path)
            task.pop("contract_version", None)
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            self.finalize_spec(root, "task-002cc")
            self.run_cli(root, "approve", "task-002cc", "--note", "approved by user")
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                inputs=[],
                include_bootstrap_fields=False,
                test_policy_mode="evidence_only",
                test_policy_evidence=["legacy empty-input plans should remain plannable"],
            )

            self.run_cli(root, "plan", "task-002cc", "--from", str(phase_file))

            phases = self.read_json(root / "workflows" / "tasks" / "task-002cc" / "phases.json")
            self.assertNotIn("required_reads", phases["phases"][0])

            status = json.loads(self.run_cli(root, "status", "task-002cc").stdout)
            self.assertEqual(status["active_phase_bootstrap"]["required_reads"], [])

    def test_approve_rejects_open_clarifications_before_locking_intake(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002d", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.write_spec_with_clarifications(
                root,
                "task-002d",
                [
                    ("문서 구조는 어떻게 정리할까?", "`tasks/`와 `system/`으로 역할을 나눈다.", "초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.", "resolved"),
                    ("추가로 확인이 필요한 구현 포인트는 무엇일까?", None, None, "open"),
                ],
            )

            result = self.run_cli(root, "approve", "task-002d", "--note", "approved by user", expected=1)
            self.assertIn("open clarifications", result.stderr)

            self.finalize_spec(root, "task-002d")
            self.run_cli(root, "approve", "task-002d", "--note", "approved by user")

            task = self.read_json(root / "workflows" / "tasks" / "task-002d" / "task.json")
            self.assertTrue(all(item["status"] == "resolved" for item in task["intake"]["clarifications"]))

    def test_status_reports_open_clarifications_before_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002e", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.write_spec_with_clarifications(
                root,
                "task-002e",
                [
                    ("문서 구조는 어떻게 정리할까?", "`tasks/`와 `system/`으로 역할을 나눈다.", "초안 작성은 `spec.md`, 승인 고정은 `task.json.intake`가 소유한다.", "resolved"),
                    ("이 구현에서 아직 애매한 부분은 무엇일까?", "상태 전이 규칙은 정했지만 출력 형식이 더 필요하다.", None, "open"),
                ],
            )

            result = self.run_cli(root, "status", "task-002e")
            payload = json.loads(result.stdout)
            self.assertFalse(payload["spec"]["ready_for_approval"])
            self.assertEqual(payload["spec"]["clarification_count"], 2)
            self.assertEqual(payload["spec"]["open_clarification_count"], 1)
            self.assertEqual(payload["spec"]["resolved_clarification_count"], 1)
            self.assertEqual(payload["spec"]["open_clarifications"], ["이 구현에서 아직 애매한 부분은 무엇일까?"])

    def test_reapprove_upgrades_task_to_v3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002f", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")

            task_path = root / "workflows" / "tasks" / "task-002f" / "task.json"
            task = self.read_json(task_path)
            task["contract_version"] = 2
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            self.finalize_spec(root, "task-002f")
            self.run_cli(root, "approve", "task-002f", "--note", "approved by user")

            task = self.read_json(task_path)
            self.assertEqual(task["contract_version"], 3)
            self.assertTrue(all(item["status"] == "resolved" for item in task["intake"]["clarifications"]))

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

    def test_verify_requires_completed_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-005a",
                test_policy_mode="evidence_only",
                test_policy_evidence=["verification should only run after phase completion"],
            )
            self.run_cli(root, "run", "task-005a", "--start")

            result = self.run_cli(root, "verify", "task-005a", expected=1)
            self.assertIn("verification requires phase status completed", result.stderr)

            task = self.read_json(root / "workflows" / "tasks" / "task-005a" / "task.json")
            phases = self.read_json(root / "workflows" / "tasks" / "task-005a" / "phases.json")
            self.assertIsNone(task["last_verified_run_id"])
            self.assertEqual(task["state"], "in_progress")
            self.assertEqual(phases["phases"][0]["status"], "in_progress")

    def test_hook_post_change_blocks_missing_tests_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(root, "task-005b")
            self.run_cli(root, "run", "task-005b", "--start")

            result = self.run_cli(
                root,
                "hook",
                "post_change",
                "--task-id",
                "task-005b",
                "--phase-id",
                "phase-1",
                "--changed-path",
                "scripts/workflow.py",
                expected=1,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertTrue(any("implementation changes require tests" in message for message in payload["messages"]))

    def test_hook_pre_phase_complete_blocks_out_of_scope_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-005c",
                test_policy_mode="evidence_only",
                test_policy_evidence=["scope guard should still reject out-of-scope files"],
            )
            self.run_cli(root, "run", "task-005c", "--start")

            result = self.run_cli(
                root,
                "hook",
                "pre_phase_complete",
                "--task-id",
                "task-005c",
                "--phase-id",
                "phase-1",
                "--changed-path",
                "docs/README.md",
                expected=1,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertTrue(any("outside allowed_write_paths" in message for message in payload["messages"]))

    def test_hook_pre_review_requires_and_then_accepts_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(root, "task-005d")
            self.run_cli(root, "run", "task-005d", "--start")
            self.run_cli(
                root,
                "run",
                "task-005d",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
                "--changed-path",
                "tests/test_workflow_cli.py",
            )

            fail_result = self.run_cli(
                root,
                "hook",
                "pre_review",
                "--task-id",
                "task-005d",
                "--phase-id",
                "phase-1",
                expected=1,
            )
            fail_payload = json.loads(fail_result.stdout)
            self.assertEqual(fail_payload["status"], "failed")
            self.assertTrue(any("no passed verification" in message for message in fail_payload["messages"]))

            self.run_cli(root, "verify", "task-005d")
            pass_result = self.run_cli(
                root,
                "hook",
                "pre_review",
                "--task-id",
                "task-005d",
                "--phase-id",
                "phase-1",
            )
            pass_payload = json.loads(pass_result.stdout)
            self.assertEqual(pass_payload["status"], "passed")
            self.assertTrue(any("latest passed verification" in message for message in pass_payload["messages"]))

    def test_hook_pre_complete_requires_user_validation_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-005e",
                test_policy_mode="evidence_only",
                test_policy_evidence=["pre_complete should require explicit validation note"],
            )

            fail_result = self.run_cli(root, "hook", "pre_complete", "--task-id", "task-005e", expected=1)
            fail_payload = json.loads(fail_result.stdout)
            self.assertEqual(fail_payload["status"], "failed")
            self.assertTrue(any("user validation note is required" in message for message in fail_payload["messages"]))

            pass_result = self.run_cli(
                root,
                "hook",
                "pre_complete",
                "--task-id",
                "task-005e",
                "--user-validation-note",
                "validated",
            )
            pass_payload = json.loads(pass_result.stdout)
            self.assertEqual(pass_payload["status"], "passed")
            self.assertTrue(any("user validation provided" in message for message in pass_payload["messages"]))

    def test_hook_unknown_pre_phase_start_fails_after_surface_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-005f",
                test_policy_mode="evidence_only",
                test_policy_evidence=["pre_phase_start event has been removed from the canonical hook surface"],
            )

            result = self.run_cli(root, "hook", "pre_phase_start", "--task-id", "task-005f", "--phase-id", "phase-1", expected=1)
            self.assertIn("unknown hook event", result.stderr)

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

    def test_hook_requires_explicit_task_when_active_task_is_ambiguous(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-006a",
                test_policy_mode="evidence_only",
                test_policy_evidence=["ambiguous active-task detection should fail closed"],
            )
            self.bootstrap_task(
                root,
                "task-006b",
                test_policy_mode="evidence_only",
                test_policy_evidence=["second active task makes hook inference ambiguous"],
            )

            commit_result = self.run_cli(
                root,
                "hook",
                "pre_commit",
                "--changed-path",
                "scripts/workflow.py",
                expected=1,
            )
            self.assertIn("WORKFLOW_TASK_ID", commit_result.stderr)

            push_result = self.run_cli(
                root,
                "hook",
                "pre_push",
                "--changed-path",
                "scripts/workflow.py",
                "--command-text",
                "git push origin feature",
                expected=1,
            )
            self.assertIn("WORKFLOW_TASK_ID", push_result.stderr)

    def test_githook_pre_commit_blocks_implementation_change_without_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(root, "task-006c")

            scripts_dir = root / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            self.git_add(root, "scripts/sample.py")

            result = self.run_hook_script(root, "pre-commit", expected=1)
            self.assertIn("implementation changes require tests", result.stdout)

    def test_githook_pre_commit_passes_with_matching_test_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(root, "task-006d")

            scripts_dir = root / "scripts"
            tests_dir = root / "tests"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            tests_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            (tests_dir / "test_sample.py").write_text("def test_sample():\n    assert True\n", encoding="utf-8")
            self.git_add(root, "scripts/sample.py", "tests/test_sample.py")

            result = self.run_hook_script(root, "pre-commit")
            self.assertIn("test changes detected", result.stdout)

    def test_githook_pre_push_blocks_force_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")

            result = self.run_hook_script(root, "pre-push", "origin", "feature", "--force", expected=1)
            self.assertIn("blocked command", result.stdout)

    def test_githook_pre_push_passes_for_main_sync_publish_when_head_matches_develop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")

            self.git_add(root, ".")
            self.git_commit_no_verify(root, "bootstrap runtime surface")
            subprocess.run(["git", "branch", "-M", "main"], cwd=root, capture_output=True, text=True, check=True)
            subprocess.run(["git", "branch", "develop", "HEAD"], cwd=root, capture_output=True, text=True, check=True)

            result = self.run_hook_script(root, "pre-push", "origin", "main")
            self.assertIn("command allowed", result.stdout)
            self.assertNotIn("requires explicit --task-id", result.stderr)

    def test_githook_pre_push_keeps_task_guard_when_main_differs_from_develop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")

            self.git_add(root, ".")
            self.git_commit_no_verify(root, "bootstrap runtime surface")
            subprocess.run(["git", "branch", "-M", "main"], cwd=root, capture_output=True, text=True, check=True)
            subprocess.run(["git", "branch", "develop", "HEAD"], cwd=root, capture_output=True, text=True, check=True)

            (root / "notes.txt").write_text("main diverged from develop\n", encoding="utf-8")
            self.git_add(root, "notes.txt")
            self.git_commit_no_verify(root, "main diverged")

            result = self.run_hook_script(root, "pre-push", "origin", "main", expected=1)
            self.assertIn("do not map to a single task", result.stderr)

    def test_githook_pre_push_requires_verification_for_unpushed_scope_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-006e",
                test_policy_mode="evidence_only",
                test_policy_evidence=["pre-push script should enforce latest verification on unpushed scope changes"],
            )

            scripts_dir = root / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            self.git_add(root, "scripts/sample.py")
            self.git_commit(root, "hook pre-push smoke")

            result = self.run_hook_script(root, "pre-push", "origin", "feature", expected=1)
            self.assertIn("no passed verification recorded for active phase", result.stdout)

    def test_githook_pre_push_passes_after_phase_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-006f",
                test_policy_mode="evidence_only",
                test_policy_evidence=["verified unpushed scope changes should pass pre-push"],
            )

            scripts_dir = root / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            self.run_cli(root, "run", "task-006f", "--start")
            self.run_cli(
                root,
                "run",
                "task-006f",
                "--complete",
                "--changed-path",
                "scripts/sample.py",
            )
            self.run_cli(root, "verify", "task-006f")

            self.git_add(root, "scripts/sample.py")
            self.git_commit(root, "verified pre-push smoke")

            result = self.run_hook_script(root, "pre-push", "origin", "feature")
            self.assertIn("latest passed verification", result.stdout)

    def test_githook_pre_push_passes_for_completed_task_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-006g",
                test_policy_mode="evidence_only",
                test_policy_evidence=["completed task scope should still bind pre-push verification"],
            )

            scripts_dir = root / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            self.run_cli(root, "run", "task-006g", "--start")
            self.run_cli(
                root,
                "run",
                "task-006g",
                "--complete",
                "--changed-path",
                "scripts/sample.py",
            )
            self.run_cli(root, "verify", "task-006g")
            self.run_cli(root, "review", "task-006g", "--note", "ready")
            self.run_cli(root, "review", "task-006g", "--close", "--user-validation-note", "validated")

            self.git_add(root, "scripts/sample.py", "workflows/tasks/task-006g")
            self.git_commit_no_verify(root, "completed task pre-push smoke")

            result = self.run_hook_script(root, "pre-push", "origin", "feature")
            self.assertIn("latest passed verification", result.stdout)

    def test_githook_pre_push_prefers_scoped_completed_task_over_unrelated_active_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-006h",
                test_policy_mode="evidence_only",
                test_policy_evidence=["completed task scope should remain usable even when another task is active"],
            )
            scripts_dir = root / "scripts"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            self.run_cli(root, "run", "task-006h", "--start")
            self.run_cli(
                root,
                "run",
                "task-006h",
                "--complete",
                "--changed-path",
                "scripts/sample.py",
            )
            self.run_cli(root, "verify", "task-006h")
            self.run_cli(root, "review", "task-006h", "--note", "ready")
            self.run_cli(root, "review", "task-006h", "--close", "--user-validation-note", "validated")

            self.git_add(root, "scripts/sample.py", "workflows/tasks/task-006h")
            self.git_commit_no_verify(root, "completed task with unrelated active task")

            self.bootstrap_task(
                root,
                "task-006i",
                allowed_write_paths=["docs/"],
                test_policy_mode="evidence_only",
                test_policy_evidence=["unrelated active task should not steal pre-push context"],
            )

            result = self.run_hook_script(root, "pre-push", "origin", "feature")
            self.assertIn("latest passed verification", result.stdout)

    def test_githook_pre_push_fails_when_unpushed_diff_only_partially_maps_to_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.bootstrap_task(
                root,
                "task-006j",
                test_policy_mode="evidence_only",
                test_policy_evidence=["pre-push inference must require the full unpushed diff to map to one task"],
            )

            scripts_dir = root / "scripts"
            notes_dir = root / "notes"
            scripts_dir.mkdir(parents=True, exist_ok=True)
            notes_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / "sample.py").write_text("print('sample')\n", encoding="utf-8")
            (notes_dir / "mixed.txt").write_text("not covered by any task scope\n", encoding="utf-8")
            self.run_cli(root, "run", "task-006j", "--start")
            self.run_cli(
                root,
                "run",
                "task-006j",
                "--complete",
                "--changed-path",
                "scripts/sample.py",
            )
            self.run_cli(root, "verify", "task-006j")
            self.run_cli(root, "review", "task-006j", "--note", "ready")
            self.run_cli(root, "review", "task-006j", "--close", "--user-validation-note", "validated")

            self.git_add(root, "scripts/sample.py", "notes/mixed.txt", "workflows/tasks/task-006j")
            self.git_commit_no_verify(root, "mixed scope pre-push smoke")

            result = self.run_hook_script(root, "pre-push", "origin", "feature", expected=1)
            self.assertIn("do not map to a single task", result.stderr)

    def test_githook_pre_push_passes_without_task_when_no_unpushed_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")

            result = self.run_hook_script(root, "pre-push", "origin", "feature")
            self.assertIn("no changed paths detected", result.stdout)

    def test_doctor_detects_runtime_surface_drift_and_init_resyncs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")

            hooks_path = root / "workflows" / "system" / "hooks.json"
            pre_push_path = root / ".githooks" / "pre-push"
            hooks_payload = self.read_json(hooks_path)
            hooks_payload["guards"]["dangerous_cmd_guard"]["blocked_patterns"] = []
            hooks_path.write_text(json.dumps(hooks_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            pre_push_path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")

            drift_result = self.run_cli(root, "doctor", expected=1)
            drift_report = json.loads(drift_result.stdout)
            self.assertTrue(any("hooks.json is out of sync" in error for error in drift_report["errors"]))
            self.assertTrue(any(".githooks/pre-push is out of sync" in error for error in drift_report["errors"]))

            self.run_cli(root, "init")
            self.assertEqual(hooks_path.read_text(encoding="utf-8"), (REPO_ROOT / "workflows" / "system" / "hooks.json").read_text(encoding="utf-8"))
            self.assertEqual(pre_push_path.read_text(encoding="utf-8"), (REPO_ROOT / ".githooks" / "pre-push").read_text(encoding="utf-8"))
            self.run_cli(root, "doctor")

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

    def test_kickoff_is_required_before_starting_next_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-007b", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-007b")
            self.run_cli(root, "approve", "task-007b", "--note", "approved by user")
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["kickoff gate is exercised by CLI tests"],
            )
            self.run_cli(root, "plan", "task-007b", "--from", str(phase_file))
            self.run_cli(root, "run", "task-007b", "--start")
            self.run_cli(root, "run", "task-007b", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007b")

            status = json.loads(self.run_cli(root, "status", "task-007b").stdout)
            self.assertEqual(status["task"]["state"], "approved")
            self.assertEqual(status["task"]["active_phase_id"], "phase-2")
            self.assertEqual(status["task"]["kickoff_required_for_phase"], "phase-2")
            self.assertIsNone(status["task"]["last_kickoff_run_id"])

            start_result = self.run_cli(root, "run", "task-007b", "--start", expected=1)
            self.assertIn("kickoff is required", start_result.stderr)

            kickoff_result = self.run_cli(root, "kickoff", "task-007b")
            kickoff_payload = json.loads(kickoff_result.stdout)
            self.assertEqual(kickoff_payload["status"], "kickoff_recorded")
            self.assertEqual(kickoff_payload["phase_id"], "phase-2")
            self.assertEqual(kickoff_payload["summary"]["completion_signal"], "phase-2 acceptance commands pass")

            self.run_cli(root, "run", "task-007b", "--start")
            status = json.loads(self.run_cli(root, "status", "task-007b").stdout)
            self.assertEqual(status["task"]["state"], "in_progress")
            self.assertIsNone(status["task"]["kickoff_required_for_phase"])
            self.assertIsNotNone(status["task"]["last_kickoff_run_id"])

    def test_pre_v3_multi_phase_task_reapproves_and_requires_kickoff_for_phase_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-007bb", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")

            task_path = root / "workflows" / "tasks" / "task-007bb" / "task.json"
            task = self.read_json(task_path)
            task["contract_version"] = 2
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            self.finalize_spec(root, "task-007bb")
            self.run_cli(root, "approve", "task-007bb", "--note", "approved by user")
            task = self.read_json(task_path)
            self.assertEqual(task["contract_version"], 3)
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["reapproved pre-v3 tasks should still require kickoff for later phases"],
            )
            self.run_cli(root, "plan", "task-007bb", "--from", str(phase_file))
            self.run_cli(root, "run", "task-007bb", "--start")
            self.run_cli(root, "run", "task-007bb", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007bb")

            status = json.loads(self.run_cli(root, "status", "task-007bb").stdout)
            self.assertEqual(status["task"]["active_phase_id"], "phase-2")
            self.assertEqual(status["task"]["kickoff_required_for_phase"], "phase-2")

            start_result = self.run_cli(root, "run", "task-007bb", "--start", expected=1)
            self.assertIn("kickoff is required", start_result.stderr)

    def test_replan_invalidates_existing_kickoff_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-007c", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-007c")
            self.run_cli(root, "approve", "task-007c", "--note", "approved by user")
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["kickoff reset is exercised by CLI tests"],
            )
            self.run_cli(root, "plan", "task-007c", "--from", str(phase_file))
            self.run_cli(root, "run", "task-007c", "--start")
            self.run_cli(root, "run", "task-007c", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007c")
            self.run_cli(root, "kickoff", "task-007c")

            replan_file = self.write_phase_input(
                root,
                ["python3 -c \"print('replanned ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["replanned phases should clear stale kickoff receipts"],
            )
            self.run_cli(root, "plan", "task-007c", "--from", str(replan_file))

            status = json.loads(self.run_cli(root, "status", "task-007c").stdout)
            self.assertEqual(status["task"]["active_phase_id"], "phase-1")
            self.assertIsNone(status["task"]["kickoff_required_for_phase"])
            self.assertIsNone(status["task"]["last_kickoff_run_id"])

    def test_reopen_resets_kickoff_requirement_for_target_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-007d", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-007d")
            self.run_cli(root, "approve", "task-007d", "--note", "approved by user")
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["reopen should require a fresh kickoff for the repaired phase"],
            )
            self.run_cli(root, "plan", "task-007d", "--from", str(phase_file))
            self.run_cli(root, "run", "task-007d", "--start")
            self.run_cli(root, "run", "task-007d", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007d")
            self.run_cli(root, "kickoff", "task-007d")
            self.run_cli(root, "run", "task-007d", "--start")
            self.run_cli(
                root,
                "run",
                "task-007d",
                "--fail",
                "--phase-id",
                "phase-2",
                "--error-fingerprint",
                "phase-2-boom",
                "--note",
                "boom",
                expected=1,
            )
            self.run_cli(root, "reopen", "task-007d", "--note", "retry after repair", "--phase-id", "phase-2")

            status = json.loads(self.run_cli(root, "status", "task-007d").stdout)
            self.assertEqual(status["task"]["state"], "approved")
            self.assertEqual(status["task"]["active_phase_id"], "phase-2")
            self.assertEqual(status["task"]["kickoff_required_for_phase"], "phase-2")
            self.assertIsNone(status["task"]["last_kickoff_run_id"])

    def test_reopening_earlier_phase_resets_downstream_phases_to_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-007e", "--title", "Harness V2", "--primary-repo", "git-ranker-workflow")
            self.finalize_spec(root, "task-007e")
            self.run_cli(root, "approve", "task-007e", "--note", "approved by user")
            phase_file = self.write_phase_input(
                root,
                ["python3 -c \"print('ok')\""],
                phase_count=2,
                test_policy_mode="evidence_only",
                test_policy_evidence=["reopening an upstream phase should invalidate downstream phase state"],
            )
            self.run_cli(root, "plan", "task-007e", "--from", str(phase_file))
            self.run_cli(root, "run", "task-007e", "--start")
            self.run_cli(root, "run", "task-007e", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007e")
            self.run_cli(root, "kickoff", "task-007e")
            self.run_cli(root, "run", "task-007e", "--start")
            self.run_cli(
                root,
                "run",
                "task-007e",
                "--fail",
                "--phase-id",
                "phase-2",
                "--error-fingerprint",
                "phase-2-boom",
                "--note",
                "boom",
                expected=1,
            )

            self.run_cli(root, "reopen", "task-007e", "--note", "repair upstream contract", "--phase-id", "phase-1")

            status = json.loads(self.run_cli(root, "status", "task-007e").stdout)
            phases = self.read_json(root / "workflows" / "tasks" / "task-007e" / "phases.json")
            self.assertEqual(status["task"]["state"], "approved")
            self.assertEqual(status["task"]["active_phase_id"], "phase-1")
            self.assertIsNone(status["task"]["kickoff_required_for_phase"])
            self.assertEqual(phases["phases"][0]["status"], "pending")
            self.assertEqual(phases["phases"][1]["status"], "pending")

            self.run_cli(root, "run", "task-007e", "--start")
            self.run_cli(root, "run", "task-007e", "--complete", "--changed-path", "scripts/workflow.py")
            self.run_cli(root, "verify", "task-007e")

            status = json.loads(self.run_cli(root, "status", "task-007e").stdout)
            self.assertEqual(status["task"]["state"], "approved")
            self.assertEqual(status["task"]["active_phase_id"], "phase-2")
            self.assertEqual(status["task"]["kickoff_required_for_phase"], "phase-2")

    def test_reopen_resets_completed_task_for_follow_up(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-007a",
                test_policy_mode="evidence_only",
                test_policy_evidence=["completed task should reopen into a rerunnable phase"],
            )
            self.run_cli(root, "run", "task-007a", "--start")
            self.run_cli(
                root,
                "run",
                "task-007a",
                "--complete",
                "--changed-path",
                "scripts/workflow.py",
            )
            self.run_cli(root, "verify", "task-007a")
            self.run_cli(root, "review", "task-007a", "--note", "ready")
            self.run_cli(root, "review", "task-007a", "--close", "--user-validation-note", "validated")
            self.run_cli(root, "reopen", "task-007a", "--note", "follow-up change")

            task = self.read_json(root / "workflows" / "tasks" / "task-007a" / "task.json")
            phases = self.read_json(root / "workflows" / "tasks" / "task-007a" / "phases.json")
            self.assertEqual(task["state"], "approved")
            self.assertEqual(task["active_phase_id"], "phase-1")
            self.assertIsNone(task["last_verified_run_id"])
            self.assertFalse(task["user_validated"])
            self.assertEqual(phases["phases"][0]["status"], "pending")

            self.run_cli(root, "run", "task-007a", "--start")

    def test_doctor_reports_incomplete_task_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_git_repo(root)
            self.install_runtime_surface(root)
            self.run_cli(root, "init")
            self.write_repo_docs(root)
            self.write_valid_agents(root)

            broken_runs = root / "workflows" / "tasks" / "task-broken" / "runs"
            broken_runs.mkdir(parents=True, exist_ok=True)

            result = self.run_cli(root, "doctor", expected=1)
            report = json.loads(result.stdout)
            self.assertTrue(any("incomplete task directory" in error for error in report["errors"]))

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

    def test_dangerous_command_guard_blocks_short_force_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init")

            result = self.run_cli(
                root,
                "hook",
                "pre_command",
                "--command-text",
                "git push -f origin feature",
                expected=1,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertTrue(any("blocked command" in message for message in payload["messages"]))

    def test_new_rejects_task_id_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init")

            result = self.run_cli(
                root,
                "new",
                "../../../escape-task",
                "--title",
                "Harness V2",
                "--primary-repo",
                "git-ranker-workflow",
                expected=1,
            )
            self.assertIn("task_id", result.stderr)
            self.assertFalse((root / "escape-task").exists())
            self.assertFalse((root / "workflows" / "escape-task").exists())

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

    def test_check_fails_when_approved_task_points_to_completed_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_task(
                root,
                "task-010",
                test_policy_mode="evidence_only",
                test_policy_evidence=["artifact consistency check should reject non-startable approved phase"],
            )

            task_path = root / "workflows" / "tasks" / "task-010" / "task.json"
            task = self.read_json(task_path)
            task["state"] = "approved"
            task_path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            phases_path = root / "workflows" / "tasks" / "task-010" / "phases.json"
            phases = self.read_json(phases_path)
            phases["phases"][0]["status"] = "completed"
            phases_path.write_text(json.dumps(phases, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            result = self.run_cli(root, "status", "--check", "--all", expected=1)
            payload = json.loads(result.stdout)
            self.assertTrue(any("approved task requires active phase status pending" in error for error in payload["errors"]))

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
