# Runtime

## Canonical Order

1. 요청 수신
2. 소크라테스 질문으로 `spec.md` 정의
3. 사용자가 현재 spec 초안에 명시적으로 동의하면 `approve`로 승인 고정
4. `approve`가 `spec.md`를 `task.json.intake`로 잠금
5. `plan`으로 `phases.json` 적재
6. active phase 실행
7. `run --complete`로 phase closure
8. `verify`로 completed phase의 acceptance command 실행
9. 모든 phase 완료 후 `review`
10. `review --close`로 user validation과 완료 고정
11. 필요하면 `reopen`으로 repair loop 재개

## Task States

- `draft`
- `approved`
- `in_progress`
- `failed`
- `blocked`
- `review_ready`
- `completed`

## Phase States

- `pending`
- `in_progress`
- `completed`
- `failed`
- `blocked`

## Runtime Rules

- `approve` 전에는 `plan`, `run`, `verify`, `review`를 허용하지 않는다.
- `approve`는 `spec.md`의 필수 section, placeholder 제거 여부, `Socratic Clarification Log`의 `Q/A/Decision` triplet 형식을 검증한다.
- `approve`는 승인된 spec을 `task.json.intake`로 잠그며, 이후 `spec.md`를 수정했으면 `approve`를 다시 실행해 intake를 재잠가야 한다.
- `plan`은 명시적 phase 입력 없이는 실행되지 않는다.
- `plan`은 `task.json.intake`와 현재 `spec.md`가 일치할 때만 허용한다.
- `status`는 `spec.md`를 읽어 `ready_for_approval`, `clarification_count`, `unresolved_clarifications`를 JSON으로 노출한다.
- `run --complete`는 `allowed_write_paths`와 `workflows/tasks/<task-id>/` 밖 변경을 차단한다.
- `verify`는 completed active phase 또는 지정된 completed phase의 `acceptance.commands`를 실행해 run evidence를 남긴다.
- phase completion 뒤 verification이 통과하기 전까지 `last_verified_run_id`는 비어 있어야 한다.
- `review`는 `last_verified_run_id`가 active phase와 일치하는 passed verification일 때만 허용한다.
- task-level review는 모든 phase가 `completed`일 때만 연다.
- `review --close --user-validation-note ...`만 최종 완료를 닫을 수 있다.

## Internal Runtime Structure

- `scripts/workflow.py`: 안정적인 CLI entrypoint
- `scripts/workflow_runtime/cli.py`: command parsing과 dispatch
- `scripts/workflow_runtime/engine.py`: 상태 전이와 실행 엔진
- `scripts/workflow_runtime/models.py`: artifact validation과 공통 model helper
- `scripts/workflow_runtime/guards.py`: TDD, write scope, dangerous command, verification freshness guard
- `scripts/workflow_runtime/doctor.py`: repository health와 stale reference 점검
- `scripts/workflow_runtime/git_ops.py`: staged/unpushed path 조회

`workflow.py`를 유지하는 이유는 사람과 AI가 단일 고정 명령 surface를 기억하는 편이 가장 효율적이기 때문이다.
`init`는 로컬 git 저장소의 `core.hooksPath`를 `.githooks`로 맞추고, `.githooks/*`와 `workflows/system/hooks.json`을 source 기준으로 다시 동기화한다.
`doctor`는 이 설정이 어긋나거나 runtime surface가 source와 drift하면 실패한다.

## Retry / Blocked Semantics

- phase 실패 시 `retry_count`를 증가시킨다.
- verification 실패도 retry에 포함한다.
- 동일한 `error_fingerprint`가 짧은 시간 안에 반복되면 Circuit Breaker가 `blocked`로 전이한다.
- `blocked`는 외부 입력, spec 재정의, phase 재계획이 필요한 상태다.
- `reopen`은 `failed`, `blocked`, `review_ready`, `completed` task를 다시 `approved`로 되돌리고 target phase를 `pending`으로 복구한 뒤 repair loop를 재시작한다.
- 추가 요구사항이면 `reopen` 뒤 `spec.md`를 다시 잠그고 `approve`를 재실행한 뒤 `plan`으로 phase를 다시 적재한다.
