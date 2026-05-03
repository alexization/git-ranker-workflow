# Artifact Model

## Core Layout

```text
workflows/
├── system/
│   └── hooks.json
└── tasks/
    └── <task-id>/
        ├── spec.md
        └── state.json
```

## Artifact Roles

- `spec.md`: 사람용 SDD source of truth다. Request, Problem, Goals, Non-goals, Constraints, Acceptance, Implementation Scopes, Socratic Clarification Log, Approval block을 담는다.
- `state.json`: 단일 mutable task state다. approval lock, current focus, IMP별 진행률, verification result, recent events, next action, blockers, user validation을 담는다.
- `hooks.json`: 최소 guard 정책이다. 위험 명령과 user validation closeout만 전역 정책으로 둔다.

`task.json`, `phases.json`, 별도 `status.json`, `runs/*.json`은 새 모델에서 생성하지 않는다.

## Spec Sections

`spec.md`는 아래 section을 가져야 한다.

- `Request`
- `Problem`
- `Goals`
- `Non-goals`
- `Constraints`
- `Acceptance`
- `Implementation Scopes`
- `Socratic Clarification Log`

`Implementation Scopes`는 `IMP-*` 항목을 사용한다.

```markdown
- IMP-01: 문서 계약 정리
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `AGENTS.md`, `docs/`
  - 정책: SDD 5단계와 state.json 단일 상태 모델을 설명한다.
```

## State Fields

`state.json`은 최소한 아래 필드를 가진다.

- `task_id`
- `title`
- `contract_version`
- `state`
- `primary_repo`
- `created_at`
- `updated_at`
- `spec_lock.approved`
- `spec_lock.approved_at`
- `spec_lock.approved_by`
- `spec_lock.approval_note`
- `spec_lock.spec_sha256`
- `current_focus.imp_id`
- `current_focus.status`
- `implementation_scopes[]`
- `events[]`
- `next_action`
- `blockers[]`
- `user_validation.validated`
- `user_validation.note`
- `user_validation.validated_at`

## Implementation Scope State

각 `implementation_scopes[]` 항목은 아래 필드를 가진다.

- `imp_id`
- `title`
- `target_repos`
- `change_paths`
- `policy`
- `status`
- `changed_paths`
- `scope_delta`
- `started_at`
- `completed_at`
- `note`
- `verification.status`
- `verification.commands[]`
- `verification.last_run_at`
- `verification.results[]`

`scope_delta`는 hard failure가 아니라 spec 범위 밖 변경을 드러내기 위한 signal이다.
