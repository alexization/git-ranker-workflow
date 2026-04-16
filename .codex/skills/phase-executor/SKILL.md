---
name: phase-executor
description: 현재 active phase 하나만 실행하고 hook을 통과시켜 phase state를 전이한다.
---

# Phase Executor

## 언제 사용하나

- `phases.json`이 준비됐고 현재 active phase를 실행해야 한다.

## 먼저 확인할 것

- `AGENTS.md`
- `docs/runtime.md`
- `docs/hooks.md`
- `workflows/tasks/<task-id>/task.json`
- `workflows/tasks/<task-id>/phases.json`

## 작업 방식

1. `task.json.kickoff_required_for_phase`가 active phase와 같으면 새 세션이 먼저 `python3 scripts/workflow.py kickoff <task-id>`를 실행해 bootstrap proof를 남긴다.
2. `python3 scripts/workflow.py run <task-id> --start`로 phase를 시작한다.
3. phase의 허용 write path 안에서만 구현한다.
4. phase를 닫을 때는 `python3 scripts/workflow.py run <task-id> --complete --changed-path ...`를 사용한다.
5. TDD Guard가 막히면 테스트를 추가하거나 `test_policy.mode=evidence_only`와 `test_policy.evidence`를 먼저 보강한다.

## 결과

- phase run evidence
- updated `task.json` / `phases.json`
- 다음 stage: `verification-runner`
