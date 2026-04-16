# AGENTS.md

`git-ranker-workflow`는 `git-ranker-workflow`, `git-ranker`, `git-ranker-client`를 묶는 Codex용 workflow control plane 저장소다.

## Mission

- 이 저장소는 하위 저장소 작업을 위한 spec, phase, verification, review control plane만 소유한다.
- 앱 동작, API, UI, 런타임 계약의 진짜 source of truth는 각 앱 저장소의 `AGENTS.md`, `README.md`, 코드, 테스트다.
- 이 저장소는 작업을 어떻게 정의하고, 승인하고, 실행하고, 검증하고, 닫는지만 책임진다.

## Start Here

1. [docs/README.md](docs/README.md)로 문서 맵을 확인한다.
2. 현재 작업이 있으면 `workflows/tasks/<task-id>/spec.md`, `task.json`, `phases.json`, `runs/*.json`을 읽는다.
3. 전역 guard와 breaker 설정은 `workflows/system/hooks.json`에서 확인한다.
4. 실제 앱 동작을 바꾸는 작업이면 대상 저장소의 문서와 테스트를 먼저 읽는다.

## CRITICAL Rules

- CRITICAL: 승인되지 않은 spec으로 구현이나 phase 실행을 시작하지 않는다.
- CRITICAL: task state는 `python3 scripts/workflow.py ...` 명령으로만 전이한다. `task.json`, `phases.json`, `runs/*.json`을 수동 편집하지 않는다.
- CRITICAL: 구현 계획의 canonical source는 `workflows/tasks/<task-id>/phases.json` 하나다.
- CRITICAL: `allowed_write_paths` 밖 변경은 phase 위반이다. 범위가 바뀌면 spec/phase를 다시 잠근다.
- CRITICAL: 구현 코드 변경에는 대응 테스트가 필요하다. 예외는 `test_policy.mode=evidence_only`와 non-empty `test_policy.evidence`뿐이다.
- CRITICAL: user validation 기록 없이 `completed`로 전이하지 않는다.

## Architecture Boundaries

- `git-ranker-workflow`: harness 헌법, task artifact, phase orchestration, guard/hook, review closeout
- `git-ranker`: backend/source-of-truth for server behavior, domain logic, backend tests
- `git-ranker-client`: frontend/source-of-truth for UI behavior, client tests

ALWAYS: 앱 계약을 바꾸는 변경은 해당 앱 저장소의 문서와 테스트를 함께 갱신한다.
ALWAYS: 이 저장소에는 앱 동작을 복제한 prose 문서를 두지 않는다.
NEVER: control plane 문서를 앱 source-of-truth보다 우선시하지 않는다.

## Workflow Contract

1. `new`가 `workflows/tasks/<task-id>/spec.md`와 `task.json` skeleton을 만든다.
2. 소크라테스 질문으로 `spec.md`를 잠근다. `Socratic Clarification Log`는 `Q:`, `A:`, `Decision:` triplet만 사용한다.
3. 사용자가 동의하면 `approve`가 같은 task 디렉터리의 `spec.md`에 Approval block을 추가하고, `spec.md` 내용을 `task.json.intake`로 잠근 뒤 `task.json`을 `approved`로 전이한다.
4. 추가 요구사항으로 spec을 다시 잠그면 `approve`를 다시 실행해 `task.json.intake`를 재잠근다.
5. `plan --from <json>` 또는 `plan --stdin`이 phase 초안을 읽어 `phases.json`으로 적재한다. `spec.md`와 `task.json.intake`가 어긋나 있으면 plan을 시작하지 않는다.
6. `run --start`가 active phase를 시작한다.
7. 구현 후 `run --complete --changed-path ...`가 write scope와 TDD guard를 통과해야 한다.
8. `verify`가 acceptance command를 실행하고 `runs/*.json`에 evidence를 남긴다.
9. 모든 phase가 완료되면 `review`가 review readiness를 기록한다.
10. `review --close --user-validation-note ...`만 최종 완료를 닫을 수 있다.
11. 실패, block, 추가 요구사항이 생기면 `reopen`으로 repair loop를 재개한다.

## TDD Contract

ALWAYS: 구현 변경은 같은 phase 안에서 테스트 변경과 함께 제출한다.
ALWAYS: 테스트를 생략하는 경우에는 `test_policy.mode=evidence_only`와 명시적 근거를 phase에 적는다.
ALWAYS: TDD Guard가 막으면 테스트 또는 phase policy를 먼저 보강한다.
NEVER: guard를 우회하기 위해 훅 설정을 임시로 낮추거나 artifact를 직접 수정하지 않는다.
NEVER: verification 통과 전 review 단계로 건너뛰지 않는다.

## Command Contract

표준 명령은 아래만 사용한다.

```bash
python3 scripts/workflow.py init
python3 scripts/workflow.py doctor
python3 scripts/workflow.py new <task-id> --title "..." --primary-repo <repo>
python3 scripts/workflow.py approve <task-id> --note "..."
python3 scripts/workflow.py plan <task-id> --from /path/to/phases.json
python3 scripts/workflow.py plan <task-id> --stdin
python3 scripts/workflow.py run <task-id> --start
python3 scripts/workflow.py run <task-id> --complete --changed-path ...
python3 scripts/workflow.py verify <task-id>
python3 scripts/workflow.py review <task-id> --note "..."
python3 scripts/workflow.py review <task-id> --close --user-validation-note "..."
python3 scripts/workflow.py reopen <task-id> --note "..."
python3 scripts/workflow.py status <task-id>
```

- `scripts/workflow.py`는 영구적인 CLI entrypoint다.
- 실제 실행 엔진은 `scripts/workflow_runtime/cli.py`, `engine.py`, `models.py`, `guards.py`, `doctor.py`, `git_ops.py`가 분담한다.
- `workflow.py`를 유지하는 이유는 사람과 AI가 하나의 안정적인 명령 surface만 기억하면 되기 때문이다.

## Source Of Truth Order

1. `AGENTS.md`: 헌법과 강제 규칙
2. `docs/`: artifact, runtime, hooks, runbook 설명
3. `workflows/tasks/<task-id>/`: 현재 작업의 spec, state, phase, evidence
4. `workflows/system/hooks.json`: 전역 guard/breaker 정책
5. 대상 앱 저장소의 문서, 코드, 테스트: 실제 앱 동작

## Forbidden Actions

NEVER: `task.json`, `phases.json`, `runs/*.json`을 수동 편집해서 상태를 맞춘다.
NEVER: `phases.json` 대신 prose TODO, PR 본문, 채팅 로그를 canonical 계획으로 쓴다.
NEVER: `allowed_write_paths` 밖 파일을 조용히 수정한다.
NEVER: destructive command를 guard 없이 실행한다.

## Change Discipline

ALWAYS: workflow 계약이 바뀌면 `AGENTS.md`, 관련 `docs/`, `.codex/skills/`, `.githooks/`, `tests/`를 함께 갱신한다.
ALWAYS: 전역 정책은 `workflows/system/hooks.json` 하나에 잠근다.
ALWAYS: commit 메시지는 루트의 `.gitmessage.ko.txt` 형식을 따른다.
ALWAYS: doctor와 테스트가 통과하는 상태로 변경을 마무리한다.
