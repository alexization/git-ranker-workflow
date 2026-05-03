# AGENTS.md

`git-ranker-workflow`는 `git-ranker-workflow`, `git-ranker`, `git-ranker-client`를 위한 Codex SDD(Spec-Driven Development) control plane 저장소다.

## Mission

- 소크라테스 문답으로 `spec.md`를 명확히 잠근다.
- 승인된 `spec.md`의 `Implementation Scopes`(`IMP-*`)를 실행 단위로 삼는다.
- 하나의 spec에는 하나의 mutable state file인 `state.json`만 둔다.
- 앱 동작, API, UI, 런타임 계약의 source of truth는 각 앱 저장소의 문서, 코드, 테스트다.

## Start Here

1. [docs/README.md](docs/README.md)로 문서 맵을 확인한다.
2. 현재 작업이 있으면 `workflows/tasks/<task-id>/spec.md`와 `state.json`을 읽는다.
3. 실제 앱 동작을 바꾸는 작업이면 대상 저장소의 `AGENTS.md`, `README.md`, 코드, 테스트를 먼저 읽는다.

## Critical Rules

- CRITICAL: 승인되지 않은 spec으로 구현을 시작하지 않는다.
- CRITICAL: `Status: open` clarification이 하나라도 있으면 승인하지 않는다.
- CRITICAL: 구현 단위는 `Implementation Scopes`의 `IMP-*`다. 별도 phase 계획을 만들지 않는다.
- CRITICAL: task state는 `state.json` 하나에만 저장한다.
- CRITICAL: user validation 기록 없이 `completed`로 전이하지 않는다.

## Architecture Boundaries

- `git-ranker-workflow`: SDD harness, task artifact, CLI state transition, verification 기록, review closeout
- `git-ranker`: backend/source-of-truth for server behavior, domain logic, backend tests
- `git-ranker-client`: frontend/source-of-truth for UI behavior, client tests

ALWAYS: 앱 계약을 바꾸는 변경은 해당 앱 저장소의 문서와 테스트를 함께 갱신한다.
ALWAYS: 이 저장소에는 앱 동작을 복제한 prose 문서를 두지 않는다.
NEVER: control plane 문서를 앱 source-of-truth보다 우선시하지 않는다.

## Workflow Contract

1. SPEC: `new`가 `spec.md`와 `state.json` skeleton을 만든다. AI는 소크라테스 질문으로 Request, Problem, Goals, Non-goals, Constraints, Acceptance, Implementation Scopes를 채운다.
2. LOCK/PLAN: 사용자가 spec 확인 요약에 동의하면 `approve`가 `state.json.spec_lock.spec_sha256`으로 spec을 잠그고, `plan`이 `IMP-*`를 `state.json.implementation_scopes`로 초기화한다.
3. IMPLEMENT: `run --start`가 다음 pending `IMP-*`를 시작하고, `run --complete`가 변경 경로와 scope delta를 `state.json`에 기록한다.
4. VERIFY: `verify`가 IMP별 acceptance command를 실행하고 결과를 같은 `state.json`에 compact하게 기록한다.
5. REVIEW: 모든 IMP가 completed + verification passed이면 `review`로 사용자 검증을 요청하고, `review --close --user-validation-note ...`만 최종 완료를 닫는다.

## Socratic Spec Contract

- 질문은 `Socratic Clarification Log`에 `Q:`, 선택적 `A:`, `Decision:`, `Status:` 순서로 기록한다.
- `open` clarification은 `Decision:`을 가질 수 없다.
- `resolved` clarification은 `A:`와 `Decision:`을 가져야 한다.
- 승인 전 AI는 목표/비목표 요약, 확정된 `IMP-*`, 변경 범위와 정책을 사용자에게 확인한다.

## Command Contract

```bash
python3 scripts/workflow.py init
python3 scripts/workflow.py doctor
python3 scripts/workflow.py new <task-id> --title "..." --primary-repo <repo>
python3 scripts/workflow.py approve <task-id> --note "..."
python3 scripts/workflow.py plan <task-id>
python3 scripts/workflow.py run <task-id> --start [--imp-id IMP-01]
python3 scripts/workflow.py run <task-id> --complete [--imp-id IMP-01] --changed-path ...
python3 scripts/workflow.py verify <task-id> [--imp-id IMP-01] [--verify-command "..."]
python3 scripts/workflow.py review <task-id> --note "..."
python3 scripts/workflow.py review <task-id> --close --user-validation-note "..."
python3 scripts/workflow.py reopen <task-id> --note "..." [--imp-id IMP-01]
python3 scripts/workflow.py status <task-id>
python3 scripts/workflow.py status --all --check
python3 scripts/workflow.py hook pre_command --command-text "..."
python3 scripts/workflow.py hook pre_push --command-text "..."
```

- `scripts/workflow.py`는 영구적인 CLI entrypoint다.
- `phases.json`, 별도 `status.json`, `runs/*.json`, `kickoff`는 사용하지 않는다.
- `.githooks/pre-push`는 위험한 push 명령만 검사한다. pre-commit hard gate는 없다.

## Source Of Truth Order

1. `AGENTS.md`: 헌법과 강제 규칙
2. `workflows/tasks/<task-id>/spec.md`: 사람용 SDD source of truth
3. `workflows/tasks/<task-id>/state.json`: 단일 mutable task state
4. `docs/`: artifact, runtime, hooks, runbook 설명
5. 대상 앱 저장소의 문서, 코드, 테스트: 실제 앱 동작

## Forbidden Actions

NEVER: 승인되지 않은 spec으로 구현하지 않는다.
NEVER: `state.json` 외 다른 파일을 task state source로 만들지 않는다.
NEVER: `phases.json`, `runs/*.json`, prose TODO, PR 본문, 채팅 로그를 canonical 계획으로 쓰지 않는다.
NEVER: user validation 없이 task를 `completed`로 닫지 않는다.

## Change Discipline

ALWAYS: workflow 계약이 바뀌면 `AGENTS.md`, 관련 `docs/`, `scripts/`, `tests/`를 함께 갱신한다.
ALWAYS: 새 동작은 tests로 검증한다.
ALWAYS: 구현 범위를 벗어난 변경이 생기면 `state.json`의 scope delta로 드러내고 필요하면 spec을 다시 잠근다.
