# Artifact Model

## Core Layout

```text
workflows/
├── system/
│   ├── hooks.json
│   └── circuit-breaker.json
└── tasks/
    └── <task-id>/
        ├── spec.md
        ├── task.json
        ├── phases.json
        └── runs/
            └── <run-id>.json
```

## Artifact Roles

- `workflows/tasks/<task-id>/spec.md`: 사람용 requirement artifact. 요청, 문제, 목표, 비목표, 제약, acceptance, 소크라테스 질문 로그, 승인 기록을 담는다. 새 spec contract에서는 clarification question마다 coverage category를 잠근다.
- `workflows/tasks/<task-id>/task.json`: mutable task state이자 승인 시점의 locked intake source다. approval, active phase, latest run, latest verified run, kickoff requirement, blocked reason, user validation과 `intake`를 담는다.
- `workflows/tasks/<task-id>/phases.json`: 승인 이후 생성된 executable phase 집합이다. phase 목표, write scope, acceptance command, test policy, retry count와 다음 세션 kickoff용 bootstrap metadata를 담는다.
- `workflows/tasks/<task-id>/runs/*.json`: phase completion, phase kickoff, verification, review, reopen evidence다.
- `workflows/system/hooks.json`: 전역 hook/guard/breaker 정책이다.
- `workflows/system/circuit-breaker.json`: 반복 실패 fingerprint 메모리다.

## Spec And Phase Loading Flow

1. `new`가 task 디렉터리와 `spec.md`, `task.json`, `phases.json` skeleton을 만든다.
2. 소크라테스 질문으로 `spec.md`를 채운다. `Socratic Clarification Log`는 `Q:`, `A:`, `Decision:` triplet만 허용하고, 새 contract에서는 `[scope]`, `[goal]`, `[non_goal]`, `[constraint]`, `[acceptance]` coverage를 모두 채운다.
3. 사용자가 현재 spec 초안에 명시적으로 동의하면 `approve`가 같은 `spec.md`에 Approval block을 추가하고, 내용을 `task.json.intake`로 잠근 뒤 `task.json`을 `approved`로 전이한다.
4. 추가 요구사항으로 spec을 다시 잠그면 `approve`를 다시 실행해 `task.json.intake`를 갱신한다.
5. `plan --from` 또는 `plan --stdin`이 외부 phase 초안을 읽어 같은 task 디렉터리의 `phases.json`으로 적재한다.
6. 이후 실행, verification, review, reopen은 같은 task 디렉터리 artifact만 읽고 쓴다.

## Canonical State Fields

`task.json`은 최소한 아래 필드를 가진다.

- `id`
- `title`
- `contract_version`
- `state`
- `primary_repo`
- `created_at`
- `approved_at`
- `approval`
- `active_phase_id`
- `latest_run_id`
- `last_verified_run_id`
- `kickoff_required_for_phase`
- `last_kickoff_run_id`
- `blocked_reason`
- `user_validated`
- `user_validation_note`
- `intake.request_summary`
- `intake.problem_summary`
- `intake.goals`
- `intake.non_goals`
- `intake.constraints`
- `intake.acceptance`
- `intake.clarifications`

`intake.clarifications`의 각 항목은 아래 필드를 가진다.

- `question`
- `category`
- `answer`
- `decision`
- `resolved`

## Phase Fields

`phases.json`의 각 phase는 최소한 아래 필드를 가진다.

- `id`
- `order`
- `title`
- `goal`
- `inputs`
- `required_reads`
- `starting_points`
- `deliverables`
- `completion_signal`
- `allowed_write_paths`
- `acceptance.commands`
- `test_policy.mode`
- `test_policy.evidence`
- `status`
- `retry_count`

`test_policy.mode`는 아래 둘 중 하나다.

- `require_tests`: 구현 변경이 있으면 대응 테스트 변경이 필요하다.
- `evidence_only`: 테스트 delta 대신 명시적 evidence 배열을 근거로 허용한다.

`required_reads`, `starting_points`, `deliverables`, `completion_signal`은 다음 phase를 새 세션에서 시작할 때 `task.json`/`phases.json`/`spec.md`만으로 bootstrap할 수 있게 만드는 canonical metadata다.

## Validation Ownership

- JSON schema 파일은 사용하지 않는다.
- artifact validation과 상태 전이는 `scripts/workflow_runtime/models.py`와 `engine.py`가 소유한다.
- 문서는 구조를 설명하지만 enforcement owner는 코드와 테스트다.
