---
name: review-closeout
description: latest passed verification을 기준으로 review readiness와 user validation closeout을 남긴다.
---

# Review Closeout

## 언제 사용하나

- verification이 통과했고 review/user validation을 닫아야 한다.

## 먼저 확인할 것

- `docs/runtime.md`
- `workflows/tasks/<task-id>/task.json`
- `workflows/tasks/<task-id>/phases.json`
- `workflows/tasks/<task-id>/runs/*.json`

## 작업 방식

1. 모든 phase가 `completed`인지 확인한다.
2. `python3 scripts/workflow.py review <task-id> --note ...`로 review readiness를 기록한다.
3. 사용자 검증이 끝나면 `python3 scripts/workflow.py review <task-id> --close --user-validation-note ...`로 완료를 닫는다.
4. explicit user validation 없이 `completed`로 전이하지 않는다.

## 결과

- review run evidence
- final completion evidence
- `state=completed`인 `task.json`
