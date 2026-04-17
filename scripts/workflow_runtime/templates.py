from __future__ import annotations

from workflow_runtime.constants import CURRENT_TASK_CONTRACT_VERSION
from workflow_runtime.models import empty_task_intake, now_iso


def default_spec(task_id: str, title: str, primary_repo: str) -> str:
    return (
        f"# {title}\n\n"
        f"- Task ID: `{task_id}`\n"
        f"- Primary Repo: `{primary_repo}`\n"
        f"- Status: `draft`\n\n"
        "## Request\n\n"
        "- TODO: 요청 배경과 기대 결과를 한 문단 또는 bullet로 정리한다.\n\n"
        "## Problem\n\n"
        "- TODO: 지금 무엇이 문제인지, 왜 바꿔야 하는지 적는다.\n\n"
        "## Goals\n\n"
        "- TODO: 이번 작업에서 반드시 만족해야 하는 결과를 적는다.\n\n"
        "## Non-goals\n\n"
        "- TODO: 이번 작업에 포함하지 않을 범위를 적는다.\n\n"
        "## Constraints\n\n"
        "- TODO: 기술, 일정, 운영, 정책 제약을 적는다.\n\n"
        "## Acceptance\n\n"
        "- TODO: 완료를 판단할 수 있는 관찰 가능한 기준을 적는다.\n\n"
        "## Socratic Clarification Log\n\n"
        "- TODO: spec 작성 중 생기는 질문을 `Q:`, 선택적 `A:`, `Status:` 형식으로 기록한다. `Status: open` 질문이 남아 있으면 approve 할 수 없다.\n"
        "- Q: 아직 확인이 필요한 요구사항은 무엇인가?\n"
        "- Status: open\n"
    )


def empty_task_payload(task_id: str, title: str, primary_repo: str) -> dict[str, object]:
    return {
        "id": task_id,
        "title": title,
        "contract_version": CURRENT_TASK_CONTRACT_VERSION,
        "state": "draft",
        "primary_repo": primary_repo,
        "created_at": now_iso(),
        "approved_at": None,
        "approval": None,
        "active_phase_id": None,
        "latest_run_id": None,
        "last_verified_run_id": None,
        "kickoff_required_for_phase": None,
        "last_kickoff_run_id": None,
        "blocked_reason": None,
        "user_validated": False,
        "user_validation_note": None,
        "intake": empty_task_intake(),
    }


def empty_phases_payload(task_id: str) -> dict[str, object]:
    return {
        "task_id": task_id,
        "generated_at": now_iso(),
        "phases": [],
    }


def approval_block(actor: str, note: str, timestamp: str) -> str:
    return (
        "\n## Approval\n\n"
        f"- Actor: `{actor}`\n"
        f"- Timestamp: `{timestamp}`\n"
        f"- Note: {note}\n"
    )
