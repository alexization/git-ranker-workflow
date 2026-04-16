---
name: boundary-check
description: active phase의 allowed_write_paths 경계를 먼저 확인하고 범위를 벗어나면 phase를 수정하거나 재계획한다.
---

# Boundary Check

## 언제 사용하나

- 구현 전에 수정 대상 파일이 현재 phase 경계 안에 들어가는지 확인해야 한다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/artifact-model.md`
- `docs/hooks.md`
- `workflows/tasks/<task-id>/task.json`
- `workflows/tasks/<task-id>/phases.json`
- `workflows/system/hooks.json`

## 작업 방식

1. active phase의 `allowed_write_paths`를 읽는다.
2. 수정하려는 파일 목록이 범위 안에 있는지 먼저 대조한다.
3. 범위를 벗어나면 임의로 수정하지 말고 `phases.json`을 다시 계획하거나 승인 범위를 갱신한다.
4. phase를 닫을 때는 `python3 scripts/workflow.py run <task-id> --complete --changed-path ...`로 write scope를 다시 검증한다.

## 결과

- 범위 안이면 구현 진행
- 범위 밖이면 phase 재계획 또는 승인 범위 수정
