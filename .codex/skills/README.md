# Skills

이 디렉터리는 `git-ranker-workflow`에서만 쓰는 최소 workflow skill만 유지한다.

## Canonical Ownership

- 프로젝트 헌법은 `AGENTS.md`가 가진다.
- artifact model, runtime, hook rule, runbook은 `docs/`가 가진다.
- current task state와 evidence는 `workflows/tasks/<task-id>/`가 가진다.
- 전역 guard 정책은 `workflows/system/hooks.json`이 가진다.
- 내부 런타임 구현은 `scripts/workflow_runtime/`이 가진다.
- skill은 위 규칙을 복제하지 않고, 한 단계의 handoff와 CLI 진입점만 안내한다.
- `python3 scripts/workflow.py init`는 runtime surface를 source 기준으로 다시 동기화하고, `doctor`는 drift를 실패로 보고한다.

## Active Skill Set

- `request-intake`
- `socratic-spec-authoring`
- `phase-planner`
- `boundary-check`
- `phase-executor`
- `verification-runner`
- `review-closeout`
- `repair-reopen`

## Recommended Order

1. `request-intake`
2. `socratic-spec-authoring`
3. `phase-planner`
4. `boundary-check -> phase-executor -> verification-runner`를 active phase마다 반복
5. 모든 phase가 끝나면 `review-closeout`
6. 실패, block, follow-up이면 `repair-reopen`

새 workflow에서는 markdown spec과 JSON state를 분리한다. `spec.md`는 사람용 요구사항 초안이고, `approve`가 이를 `task.json.intake`로 잠근다. `task.json`/`phases.json`/`runs/*.json`은 자동화용 canonical source다.
