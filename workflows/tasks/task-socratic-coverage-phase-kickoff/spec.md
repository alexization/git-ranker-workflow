# Strengthen spec coverage gate and phase kickoff session contract

- Task ID: `task-socratic-coverage-phase-kickoff`
- Primary Repo: `git-ranker-workflow`
- Status: `draft`

## Request

- 소크라테스식 질문으로 spec을 잠글 때 AI가 요구사항을 충분히 이해할 때까지 질의를 계속하고, 그 결과가 명시적 coverage gate로 강제되도록 control plane을 강화한다.
- phase는 항상 독립적인 작업 단위여야 하며, 한 phase의 구현과 검증이 끝난 뒤 다음 phase는 새 세션에서만 시작할 수 있도록 kickoff contract를 도입한다.
- 다음 phase를 시작하는 새 세션은 `task.json`, `phases.json`, `spec.md`를 읽고 어디서부터 무엇을 해야 하는지 복원할 수 있어야 한다.
- 이 PR에는 다른 작업으로 이미 완료된 `git-ranker` backend 결과를 가리키는 workflow repo의 `git-ranker` gitlink 업데이트도 함께 반영해야 한다.

## Problem

- 현재 `approve`는 필수 섹션과 최소 한 개의 `Q/A/Decision` triplet만 검사하므로, AI가 요구사항을 충분히 파악했는지와 추가 질문이 더 필요한지까지는 보장하지 못한다.
- 현재 phase 상태는 JSON에 기록되지만, 다음 phase를 새 세션에서 시작하기 전에 어떤 정보를 읽고 어떤 순서로 시작해야 하는지까지는 runtime contract로 고정되어 있지 않다.
- 이 상태에서는 spec 품질이 얕은 문답으로 승인될 수 있고, multi-phase 작업에서 다음 phase가 이전 채팅 맥락에 암묵적으로 의존하게 되어 control plane이 세션 독립성을 보장하지 못한다.
- 현재 PR 브랜치에는 workflow control-plane 변경만 있고, 같은 작업 흐름에서 이미 완료된 `git-ranker` backend 기준 커밋을 가리키는 submodule gitlink는 빠져 있어 reviewer가 실제 baseline을 한 번에 확인하기 어렵다.

## Goals

- `approve` 전에 목표, 범위, 비범위, 제약, acceptance를 모두 덮는 clarification coverage gate를 도입한다.
- `status`가 아직 덜 물어본 clarification 축을 드러내고, approval readiness를 coverage 기준으로 판단하게 한다.
- 각 phase가 다음 세션 시작에 필요한 bootstrap 정보를 `phases.json`에 담도록 확장한다.
- `kickoff`와 phase-start gating을 도입해, 검증이 끝난 다음 phase는 새 세션 kickoff 절차를 거친 뒤에만 시작되도록 한다.
- `doctor`와 consistency check가 incomplete task artifact를 더 명확하게 보고하도록 개선한다.
- 관련 문서, skills, hooks surface, 테스트를 함께 갱신한다.
- workflow control-plane 변경을 publish할 때 함께 검토되어야 하는 `git-ranker` submodule pointer를 같은 PR 브랜치에 반영한다.

## Non-goals

- 실제 Codex 런타임의 메모리 초기화 여부를 외부 session ID로 증명하는 통합까지 이번 작업 범위에 넣지 않는다.
- phase 중간 지점에서 세션을 갈아타는 resume workflow는 이번 작업 목표가 아니다.
- 앱 저장소(`git-ranker`, `git-ranker-client`)의 런타임 계약이나 제품 기능을 변경하지 않는다.

## Constraints

- root `AGENTS.md` workflow 계약을 따른다. 승인된 spec과 canonical phase 없이 구현을 시작하지 않는다.
- task/phase/run state는 `python3 scripts/workflow.py ...` 명령으로만 전이한다.
- workflow 계약 변경이므로 `AGENTS.md`, `docs/`, `.codex/skills/`, `.githooks/`, `tests/`를 함께 갱신한다.
- 다음 phase 시작점 복원은 `task.json`, `phases.json`, `spec.md`를 기준으로 설계하고 `runs/*.json`은 보조 evidence로만 사용한다.
- fresh-session 증명은 Codex client integration이 아니라 control-plane proof 수준으로 고정한다.
- `git-ranker` 서브모듈 반영은 workflow repo의 gitlink 업데이트만 다루고, backend 저장소 내부 변경 자체를 이 저장소에서 재작성하거나 재검증 대상으로 복제하지 않는다.

## Acceptance

- clarification coverage가 부족한 spec은 `approve`에 실패하고, `status`는 누락 축을 JSON으로 노출한다.
- 승인된 intake의 clarification에는 coverage category가 잠기고, docs와 skill이 그 계약을 설명한다.
- `phases.json` 각 phase는 다음 세션 시작에 필요한 bootstrap 필드를 포함한다.
- `python3 scripts/workflow.py kickoff <task-id>`가 active phase bootstrap summary를 기록하고, matching kickoff 없이는 `run --start`가 실패한다.
- `verify` 성공 후 다음 pending phase가 있으면 task는 다음 phase kickoff를 요구하는 상태로 전이한다.
- 새 CLI 프로세스 기준 테스트로 `phase-1 verify -> phase-2 kickoff -> phase-2 start` 흐름이 검증된다.
- incomplete task directory가 있을 때 consistency check/doctor가 원인을 명확히 보고한다.
- PR 브랜치의 `git-ranker` gitlink가 backend PR `#89`의 커밋 `fbc672c6384eb896183f838be7413e195e388dc5`를 가리키고, review summary에도 그 사실이 반영된다.

## Socratic Clarification Log

- Q: [goal] 소크라테스식 질문 품질은 최소 질문 개수로 볼까요, 아니면 요구사항 coverage로 볼까요?
- A: 질문 수보다 요구사항 축을 모두 덮었는지가 중요합니다. 범위, 목적, 비범위, 제약, acceptance가 빠지지 않아야 합니다.
- Decision: `approve`는 최소 질문 수가 아니라 clarification coverage gate로 판단한다.

- Q: [constraint] 다음 phase를 시작하는 새 세션은 어떤 source of truth를 읽고 시작해야 하나요?
- A: `task.json`, `phases.json`과 현재 잠긴 `spec.md`를 읽고 어디서부터 시작해야 하는지 알 수 있어야 합니다.
- Decision: phase-start bootstrap은 `task.json`/`phases.json` + `spec.md` 기준으로 복원 가능해야 한다.

- Q: [scope] phase별 독립 세션 요구는 어떤 수준으로 강제할까요?
- A: phase 경계에서만 새 세션을 강제하고, 새 phase 시작 전 kickoff proof가 없으면 시작하지 못하게 해야 합니다.
- Decision: 각 phase는 이전 phase verification 통과 후 `kickoff` 절차를 거친 새 세션에서만 시작할 수 있도록 control-plane gate를 둔다.

- Q: [acceptance] fresh-session 증명은 실제 외부 세션 ID가 꼭 필요한가요?
- A: 현재 저장소 단독으로는 어렵기 때문에 control-plane proof 수준에서 kickoff acknowledgement를 남기는 방식이 적절합니다.
- Decision: fresh-session 증명은 external session ID integration이 아니라 kickoff evidence 기반 control-plane proof로 고정한다.

- Q: [non_goal] 이번 follow-up에서 `git-ranker` 저장소 내부 구현까지 이 저장소에서 다시 수정해야 하나요?
- A: 아닙니다. 이미 다른 작업에서 완료된 backend 결과를 가리키는 workflow repo의 gitlink만 맞추면 됩니다.
- Decision: 이번 follow-up은 workflow repo의 `git-ranker` submodule pointer 반영만 다루고, backend 소스 변경은 `git-ranker` 저장소의 source of truth에 맡긴다.

## Approval

- Actor: `user`
- Timestamp: `2026-04-16T08:33:23+00:00`
- Note: User requested that the published PR also include the git-ranker submodule pointer update.
