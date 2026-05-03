from __future__ import annotations

from workflow_runtime.constants import CURRENT_TASK_CONTRACT_VERSION
from workflow_runtime.models import now_iso


def default_spec(task_id: str, title: str, primary_repo: str) -> str:
    return (
        f"# {title}\n\n"
        f"- Task ID: `{task_id}`\n"
        f"- Primary Repo: `{primary_repo}`\n"
        f"- Status: `draft`\n\n"
        "## Request\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Problem\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Goals\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Non-goals\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Constraints\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Acceptance\n\n"
        "- (AI가 소크라테스 문답을 통해 작성합니다.)\n\n"
        "## Implementation Scopes\n\n"
        "- IMP-01: (AI가 확정한 첫 번째 구현 범위)\n"
        "  - 대상 저장소: `git-ranker-workflow`\n"
        "  - 변경 경로: `docs/`\n"
        "  - 정책: 사용자 승인 전에는 구현하지 않습니다.\n\n"
        "## Socratic Clarification Log\n\n"
        "- Q: 아직 확인이 필요한 요구사항은 무엇인가?\n"
        "- Status: open\n"
    )


def empty_state_payload(task_id: str, title: str, primary_repo: str) -> dict[str, object]:
    timestamp = now_iso()
    return {
        "task_id": task_id,
        "title": title,
        "contract_version": CURRENT_TASK_CONTRACT_VERSION,
        "state": "draft",
        "primary_repo": primary_repo,
        "created_at": timestamp,
        "updated_at": timestamp,
        "spec_lock": {
            "approved": False,
            "approved_at": None,
            "approved_by": None,
            "approval_note": None,
            "spec_sha256": None,
        },
        "current_focus": {
            "imp_id": None,
            "status": "idle",
            "started_at": None,
            "note": "",
        },
        "implementation_scopes": [],
        "events": [],
        "next_action": "Resolve open Socratic clarifications, then approve the spec.",
        "blockers": [],
        "user_validation": {
            "validated": False,
            "note": None,
            "validated_at": None,
        },
    }


def approval_block(actor: str, note: str, timestamp: str) -> str:
    return (
        "\n## Approval\n\n"
        f"- Actor: `{actor}`\n"
        f"- Timestamp: `{timestamp}`\n"
        f"- Note: {note}\n"
    )
