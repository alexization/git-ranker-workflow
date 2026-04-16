---
name: request-intake
description: 새 요청을 실행 가능한 single task로 줄이고 `workflows/tasks/<task-id>/` 생성으로 handoff한다.
---

# Request Intake

## 언제 사용하나

- 새 작업 요청을 받았고 아직 task artifact가 없다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/README.md`
- `docs/runtime.md`

## 작업 방식

1. 요청을 하나의 task로 줄인다.
2. primary repo와 완료 조건을 한 줄씩 잠근다.
3. `python3 scripts/workflow.py new <task-id> --title ... --primary-repo ...`로 task skeleton을 만든다.
4. 생성 위치는 항상 `workflows/tasks/<task-id>/` 하나다. draft 단계에서는 `spec.md`만 채우고 `task.json.intake`는 `approve`가 잠근다.
5. 구현으로 바로 가지 말고 `socratic-spec-authoring`으로 넘긴다.

## 결과

- `workflows/tasks/<task-id>/spec.md`
- `workflows/tasks/<task-id>/task.json`
- 다음 stage: `socratic-spec-authoring`
