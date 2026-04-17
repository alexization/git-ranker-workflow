---
name: socratic-spec-authoring
description: 소크라테스 질문으로 `spec.md`를 잠그고, 사용자 명시적 승인 뒤 `task.json`을 `approved`로 고정한다.
---

# Socratic Spec Authoring

## 언제 사용하나

- `request-intake`로 task skeleton이 만들어졌고 구현 전 승인된 requirement가 필요하다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/artifact-model.md`
- `docs/runtime.md`
- `workflows/tasks/<task-id>/spec.md`
- `workflows/tasks/<task-id>/task.json`

## 작업 방식

1. 질문으로 request, problem, goals, non-goals, constraints, acceptance를 `spec.md`에 기록한다.
2. `Socratic Clarification Log`는 clarification마다 `Q:`로 시작하고 마지막 줄에 `Status:`를 둔다. `open`은 `Q:`와 선택적 `A:`를 허용하고, `resolved`는 `Q:`/`A:`/`Decision:`/`Status: resolved`를 순서대로 가진다.
3. `status`에서 `open_clarification_count=0`이고 `validation_errors`가 비어 있을 때까지 질문 루프를 반복한다. 질문은 고정 목록이 아니며, spec 작성 중 새 애매점이 생기면 언제든 추가하거나 다시 연다.
4. placeholder가 남아 있지 않은지 확인한다.
5. 사용자가 현재 `spec.md` 초안에 명시적으로 동의했을 때만 `python3 scripts/workflow.py approve <task-id> --note ...`를 실행한다.
6. `approve`가 `spec.md`를 `task.json.intake`로 잠근다는 점을 전제로, 승인 전에는 phase 생성이나 구현을 시작하지 않는다.

## 결과

- 승인된 `spec.md`
- locked `task.json.intake`
- `state=approved`인 `task.json`
- 다음 stage: `phase-planner`
