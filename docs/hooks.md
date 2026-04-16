# Hooks

## Canonical Hook Config

- 설정 파일: [workflows/system/hooks.json](../workflows/system/hooks.json)
- 구현 파일: [scripts/workflow_runtime/guards.py](../scripts/workflow_runtime/guards.py), [scripts/workflow_runtime/cli.py](../scripts/workflow_runtime/cli.py)
- trigger surface: workflow CLI, `.githooks/`, CI

## Hook Events

- `pre_command`
- `pre_commit`
- `post_change`
- `pre_phase_complete`
- `pre_review`
- `pre_complete`
- `pre_push`

## Guards

### TDD Guard

- 구현 파일이 바뀌면 대응 테스트 변경이 있어야 한다.
- 예외는 phase의 `test_policy.mode=evidence_only`와 non-empty `test_policy.evidence`로만 허용한다.
- docs, workflow JSON, markdown, template-only 변경은 guard 대상에서 제외한다.

### Write Scope Guard

- staged 변경과 phase completion 변경이 `allowed_write_paths` 밖이면 차단한다.
- task artifact 디렉터리 `workflows/tasks/<task-id>/`는 항상 허용 범위에 포함된다.

### Dangerous Command Guard

- `rm -rf`, `git reset --hard`, `git checkout --`, `git clean -fd`, force push, destructive DB command를 차단한다.
- workflow CLI가 acceptance command를 실행하기 전에도 같은 guard를 적용한다.

### Latest Verification Guard

- `pre_review`에서는 active phase에 대한 latest passed verification을 요구한다.
- `pre_push`에서는 unpushed diff를 기준으로 task를 먼저 해석하고, 그 scope와 겹칠 때 latest passed verification을 요구한다.
- 단, `.githooks/pre-push`는 현재 브랜치가 `main`이고 로컬 `main` tip이 로컬 `develop` tip과 같으면 task 추론 전에 동기화 publish로 간주하고 통과시킨다.
- active task가 없더라도 unpushed diff가 정확히 하나의 completed task scope에 매핑되면 그 task를 push gate context로 재사용한다.
- unpushed diff가 어느 task에도 단일하게 매핑되지 않으면 `pre_push`는 fail-closed 한다.

### User Validation Guard

- `pre_complete`에서는 non-empty user validation note를 요구한다.
- `review --close --user-validation-note ...`만 최종 완료를 닫을 수 있다.

### Circuit Breaker

- 동일한 `error_fingerprint`가 60초 안에 5회 반복되면 task와 phase를 `blocked`로 전이한다.
- `run --fail`뿐 아니라 verification 실패 누적도 동일하게 breaker 입력으로 취급한다.
- 상태는 `workflows/system/circuit-breaker.json`에 저장한다.

## Trigger Surfaces

- `python3 scripts/workflow.py hook ...`
- `.githooks/pre-commit`
- `.githooks/pre-push`
- `.github/workflows/workflow-control-plane.yml`

git hook만으로는 충분하지 않다. 로컬 CLI와 phase runner가 같은 hook 설정을 읽어야 guard가 유지된다.
phase boundary의 fresh-session kickoff proof는 git hook이 아니라 workflow runtime이 `kickoff`와 `run --start` 사이에서 직접 강제한다.
`python3 scripts/workflow.py init`는 로컬 git 저장소의 `core.hooksPath`를 `.githooks`로 맞추고, `doctor`는 이 설정이 빠지면 실패한다.
`init`는 `.githooks/pre-commit`, `.githooks/pre-push`, `workflows/system/hooks.json`을 source 기준으로 다시 동기화한다.
`doctor`는 위 runtime surface가 source와 drift하면 실패하고 `python3 scripts/workflow.py init`를 다시 요구한다.
`pre_commit`은 active task가 하나로 추론되지 않으면 fail-closed 한다. 이때는 `WORKFLOW_TASK_ID` 또는 `--task-id`로 task binding을 명시해야 한다.
`pre_push`는 먼저 현재 브랜치가 `main`인지와 로컬 `main`/`develop` tip 일치를 확인한다. 이 동기화 publish가 아니면 기존처럼 unpushed diff를 task scope에 매핑하고, scope가 단일 task로 정해지지 않으면 fail-closed 한다.
