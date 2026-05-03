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
    def run_cli(self, root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["WORKFLOW_ROOT"] = str(root)
        result = subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expected, msg=f"stdout={result.stdout}\nstderr={result.stderr}")
        return result

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_spec(
        self,
        root: Path,
        task_id: str,
        *,
        open_question: bool = False,
        scope_path: str = "docs/",
        extra_scope: bool = False,
    ) -> None:
        status = "open" if open_question else "resolved"
        answer = "" if open_question else "- A: `spec.md`와 `state.json`만 유지한다.\n- Decision: task state는 단일 JSON으로 관리한다.\n"
        extra_scope_block = ""
        if extra_scope:
            extra_scope_block = (
                "- IMP-02: Guard update\n"
                "  - 대상 저장소: `git-ranker-workflow`\n"
                "  - 변경 경로: `scripts/`\n"
                "  - 정책: state 전이 guard를 보강한다.\n\n"
            )
        spec = (
            "# Single State Harness\n\n"
            f"- Task ID: `{task_id}`\n"
            "- Primary Repo: `git-ranker-workflow`\n"
            "- Status: `draft`\n\n"
            "## Request\n\n"
            "- Harness를 소크라테스식 SDD로 단순화한다.\n\n"
            "## Problem\n\n"
            "- task state가 여러 파일에 분산되어 재개 컨텍스트가 커진다.\n\n"
            "## Goals\n\n"
            "- spec 하나에 state.json 하나만 둔다.\n"
            "- IMP-*를 실행 단위로 사용한다.\n\n"
            "## Non-goals\n\n"
            "- 앱 저장소 기능은 변경하지 않는다.\n\n"
            "## Constraints\n\n"
            "- 승인 전에는 구현하지 않는다.\n\n"
            "## Acceptance\n\n"
            "- new/approve/plan/run/verify/review 흐름이 state.json만 사용한다.\n\n"
            "## Implementation Scopes\n\n"
            "- IMP-01: Runtime artifact model update\n"
            "  - 대상 저장소: `git-ranker-workflow`\n"
            f"  - 변경 경로: `{scope_path}`\n"
            "  - 정책: state.json에 진행 상태와 검증 결과를 기록한다.\n\n"
            f"{extra_scope_block}"
            "## Socratic Clarification Log\n\n"
            "- Q: 상태 파일은 어떻게 관리해야 하는가?\n"
            f"{answer}"
            f"- Status: {status}\n"
        )
        (root / "workflows" / "tasks" / task_id / "spec.md").write_text(spec, encoding="utf-8")

    def bootstrap_planned_task(self, root: Path, task_id: str = "task-001", *, extra_scope: bool = False) -> None:
        self.run_cli(root, "new", task_id, "--title", "Single State Harness", "--primary-repo", "git-ranker-workflow")
        self.write_spec(root, task_id, extra_scope=extra_scope)
        self.run_cli(root, "approve", task_id, "--note", "approved by user")
        self.run_cli(root, "plan", task_id)

    def test_new_creates_spec_and_single_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-001", "--title", "Single State Harness", "--primary-repo", "git-ranker-workflow")

            task_dir = root / "workflows" / "tasks" / "task-001"
            self.assertTrue((task_dir / "spec.md").exists())
            self.assertTrue((task_dir / "state.json").exists())
            self.assertFalse((task_dir / "task.json").exists())
            self.assertFalse((task_dir / "phases.json").exists())
            self.assertFalse((task_dir / "runs").exists())

            state = self.read_json(task_dir / "state.json")
            self.assertEqual(state["state"], "draft")
            self.assertFalse(state["spec_lock"]["approved"])

    def test_approve_requires_resolved_clarifications_and_locks_spec_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "new", "task-002", "--title", "Single State Harness", "--primary-repo", "git-ranker-workflow")
            self.write_spec(root, "task-002", open_question=True)

            result = self.run_cli(root, "approve", "task-002", "--note", "approved by user", expected=1)
            self.assertIn("open clarifications", result.stderr)

            self.write_spec(root, "task-002")
            self.run_cli(root, "approve", "task-002", "--note", "approved by user")

            state = self.read_json(root / "workflows" / "tasks" / "task-002" / "state.json")
            self.assertEqual(state["state"], "approved")
            self.assertTrue(state["spec_lock"]["approved"])
            self.assertTrue(state["spec_lock"]["spec_sha256"])

    def test_plan_parses_implementation_scopes_without_external_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-003")

            state = self.read_json(root / "workflows" / "tasks" / "task-003" / "state.json")
            self.assertEqual(len(state["implementation_scopes"]), 1)
            scope = state["implementation_scopes"][0]
            self.assertEqual(scope["imp_id"], "IMP-01")
            self.assertEqual(scope["status"], "pending")
            self.assertEqual(scope["change_paths"], ["docs/"])
            self.assertEqual(scope["verification"]["commands"][0]["cmd"], "python3 -m unittest discover -s tests -v")

    def test_spec_change_after_approval_blocks_plan_until_reapproval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-004")
            spec_path = root / "workflows" / "tasks" / "task-004" / "spec.md"
            spec_path.write_text(spec_path.read_text(encoding="utf-8") + "\n<!-- changed -->\n", encoding="utf-8")

            result = self.run_cli(root, "plan", "task-004", expected=1)
            self.assertIn("spec.md has changed since approval", result.stderr)

    def test_verify_blocks_spec_change_after_scope_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-005")
            self.run_cli(root, "run", "task-005", "--start")
            self.run_cli(root, "run", "task-005", "--complete", "--changed-path", "docs/runtime.md")
            spec_path = root / "workflows" / "tasks" / "task-005" / "spec.md"
            spec_path.write_text(spec_path.read_text(encoding="utf-8") + "\n<!-- changed -->\n", encoding="utf-8")

            result = self.run_cli(
                root,
                "verify",
                "task-005",
                "--verify-command",
                "python3 -c \"print('ok')\"",
                expected=1,
            )
            self.assertIn("spec.md has changed since approval", result.stderr)

    def test_full_single_state_flow_reaches_completed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-006")

            self.run_cli(root, "run", "task-006", "--start")
            self.run_cli(root, "run", "task-006", "--complete", "--changed-path", "docs/runtime.md")
            self.run_cli(root, "verify", "task-006", "--verify-command", "python3 -c \"print('ok')\"")
            self.run_cli(root, "review", "task-006", "--note", "ready")
            self.run_cli(root, "review", "task-006", "--close", "--user-validation-note", "validated by user")

            state = self.read_json(root / "workflows" / "tasks" / "task-006" / "state.json")
            self.assertEqual(state["state"], "completed")
            self.assertTrue(state["user_validation"]["validated"])
            self.assertEqual(state["implementation_scopes"][0]["verification"]["status"], "passed")

    def test_start_blocks_second_scope_while_one_is_active(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-007", extra_scope=True)

            self.run_cli(root, "run", "task-007", "--start", "--imp-id", "IMP-01")
            result = self.run_cli(root, "run", "task-007", "--start", "--imp-id", "IMP-02", expected=1)
            self.assertIn("complete or fail active implementation scope", result.stderr)

    def test_scope_delta_is_advisory_not_a_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-008")

            self.run_cli(root, "run", "task-008", "--start")
            self.run_cli(root, "run", "task-008", "--complete", "--changed-path", "scripts/workflow.py")

            state = self.read_json(root / "workflows" / "tasks" / "task-008" / "state.json")
            self.assertEqual(state["implementation_scopes"][0]["scope_delta"], ["scripts/workflow.py"])

    def test_task_artifact_paths_do_not_count_as_scope_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-009")

            self.run_cli(root, "run", "task-009", "--start")
            self.run_cli(
                root,
                "run",
                "task-009",
                "--complete",
                "--changed-path",
                "workflows/tasks/task-009/state.json",
            )

            state = self.read_json(root / "workflows" / "tasks" / "task-009" / "state.json")
            self.assertEqual(state["implementation_scopes"][0]["scope_delta"], [])

    def test_dangerous_command_guard_blocks_force_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_cli(
                root,
                "hook",
                "pre_push",
                "--command-text",
                "git push origin main --force",
                expected=1,
            )
            self.assertIn("blocked command", result.stdout)

    def test_doctor_and_status_check_validate_single_state_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.bootstrap_planned_task(root, "task-010")

            self.run_cli(root, "doctor")
            self.run_cli(root, "status", "--all", "--check")

            legacy = root / "workflows" / "tasks" / "task-010" / "phases.json"
            legacy.write_text("{}", encoding="utf-8")
            result = self.run_cli(root, "status", "--all", "--check", expected=1)
            self.assertIn("legacy phases.json must not exist", result.stdout)


if __name__ == "__main__":
    unittest.main()
