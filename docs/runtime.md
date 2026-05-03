# Runtime

## Canonical Order

1. SPEC: `new`로 task skeleton을 만들고, 소크라테스 문답으로 `spec.md`를 채운다.
2. LOCK/PLAN: 사용자가 spec 확인 요약에 동의하면 `approve`로 spec hash를 잠그고, `plan`으로 `IMP-*` 진행 상태를 초기화한다.
3. IMPLEMENT: `run --start`와 `run --complete`로 active `IMP-*`를 진행한다.
4. VERIFY: `verify`가 command를 실행하고 결과를 `state.json`에 기록한다.
5. REVIEW: 모든 IMP가 verified이면 `review`와 `review --close`로 사용자 validation을 남긴다.

## Task States

- `draft`
- `approved`
- `in_progress`
- `failed`
- `review_ready`
- `completed`

## Implementation States

- `pending`
- `in_progress`
- `completed`
- `failed`

## Runtime Rules

- 승인 전에는 `plan`, `run`, `verify`, `review`를 허용하지 않는다.
- `approve`는 `spec.md`의 필수 section, placeholder 제거 여부, 열린 clarification 0개, `IMP-*` 1개 이상을 검증한다.
- `approve`는 spec 내용을 JSON에 복제하지 않고 `state.json.spec_lock.spec_sha256`으로 잠근다.
- 승인 뒤 `spec.md`가 바뀌면 `plan`, `run`, `verify`는 실패하고 재승인을 요구한다.
- `plan`은 외부 JSON을 받지 않는다. 승인된 `Implementation Scopes`에서 `state.json.implementation_scopes`를 만든다.
- `run --complete`는 변경 경로와 scope delta를 기록한다. scope delta는 차단이 아니라 재승인 필요 여부를 판단하기 위한 signal이다.
- `verify`는 IMP별 command를 실행한다. command는 `{cmd, cwd}` 형태로 저장된다.
- `events`는 `runs/*.json` 대체용 compact log이며 최근 이벤트만 보존한다.
- `review --close`는 user validation note 없이는 실패한다.

## Internal Runtime Structure

- `scripts/workflow.py`: 안정적인 CLI entrypoint
- `scripts/workflow_runtime/cli.py`: command parsing과 dispatch
- `scripts/workflow_runtime/engine.py`: state transition과 command execution
- `scripts/workflow_runtime/models.py`: spec parser, state validation, artifact helpers
- `scripts/workflow_runtime/guards.py`: dangerous command와 user validation guard
- `scripts/workflow_runtime/doctor.py`: hook config와 task artifact consistency 점검
- `scripts/workflow_runtime/git_ops.py`: staged/unpushed path 조회

## Removed Concepts

- `phases.json`
- 별도 `status.json`
- `runs/*.json`
- `kickoff`
- circuit breaker
- `blocked` state
- pre-commit hard gate
- docs/AGENTS marker doctor validation
