---
name: repair-reopen
description: failed, blocked, review follow-up, 추가 요구사항이 들어온 task를 reopen해서 repair loop를 재개한다.
---

# Repair Reopen

## 언제 사용하나

- task가 `failed`, `blocked`, `review_ready`, `completed` 상태인데 다시 작업을 이어가야 한다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/runtime.md`
- `workflows/tasks/<task-id>/task.json`
- `workflows/tasks/<task-id>/phases.json`
- 가장 최근 `runs/*.json`

## 작업 방식

1. 왜 reopen이 필요한지 note를 한 줄로 잠근다.
2. 필요하면 target phase를 정한다.
3. `python3 scripts/workflow.py reopen <task-id> --note "..." [--phase-id ...]`로 task를 `approved` 상태로 되돌리고 target phase를 `pending`으로 복구한다.
4. 추가 요구사항이면 먼저 `spec.md`를 다시 잠근다.
5. spec이 바뀌었으면 `python3 scripts/workflow.py approve <task-id> --note "..."`로 `task.json.intake`를 다시 잠근다.
6. 필요하면 `plan`으로 phase를 다시 적재한다.
7. 이후 구현 재시작 중 필요한 흐름으로 이어간다.

## 결과

- `state=approved`인 `task.json`
- rerunnable target phase (`status=pending`)
- cleared `blocked_reason`
- new reopen run evidence
