---
name: verification-runner
description: active phase의 acceptance command를 실행하고 `runs/*.json`에 verification evidence를 남긴다.
---

# Verification Runner

## 언제 사용하나

- phase 구현이 끝났고 `run --complete`까지 닫은 뒤 검증을 실행해야 한다.

## 먼저 확인할 것

- `docs/runtime.md`
- `docs/hooks.md`
- `workflows/tasks/<task-id>/phases.json`
- `workflows/tasks/<task-id>/task.json`

## 작업 방식

1. `acceptance.commands`를 확인한다.
2. 현재 active phase가 `completed` 상태인지 확인한다.
3. `python3 scripts/workflow.py verify <task-id>`를 실행한다.
4. `task.json.last_verified_run_id`가 현재 phase의 passed verification으로 갱신됐는지 확인한다.

## 결과

- `runs/<run-id>.json`
- `task.json.latest_run_id`
- `task.json.last_verified_run_id`
- 다음 stage: 다음 pending phase가 있으면 `phase-executor`, 없으면 `review-closeout`
