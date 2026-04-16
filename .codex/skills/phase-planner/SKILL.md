---
name: phase-planner
description: 승인된 task를 executable phase 집합으로 쪼개고 `phases.json`을 canonical 계획으로 고정한다.
---

# Phase Planner

## 언제 사용하나

- `task.json`이 `approved` 상태고 `task.json.intake`가 현재 `spec.md`와 동기화되어 있다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/artifact-model.md`
- `docs/runtime.md`
- `workflows/tasks/<task-id>/spec.md`
- `workflows/tasks/<task-id>/task.json`

## 작업 방식

1. task를 작은 phase들로 쪼갠다.
2. 각 phase에 `allowed_write_paths`, `acceptance.commands`, `test_policy`, `required_reads`, `starting_points`, `deliverables`, `completion_signal`을 채운 JSON을 작성한다.
3. 추가 요구사항으로 spec을 바꿨다면 `approve`를 다시 실행해 intake를 재잠근 뒤 `python3 scripts/workflow.py plan <task-id> --from <phase-json>` 또는 `--stdin`을 실행한다.
4. `phases.json`은 오직 `plan` 명령만 canonical write owner다.

## 결과

- `workflows/tasks/<task-id>/phases.json`
- `task.json.active_phase_id`
- 다음 세션 kickoff가 읽을 bootstrap metadata
- 다음 stage: `phase-executor`
