# Simplify harness into single-state Socratic SDD

- Task ID: `task-harness-single-state-sdd`
- Primary Repo: `git-ranker-workflow`
- Status: `draft`

## Request

- Harness를 소크라테스식 SDD(Spec-Driven Development)에 맞게 단순화한다.
- 하나의 `spec.md`에는 하나의 상태 파일만 대응되도록 하고, 현재 분산된 `task.json`, `phases.json`, `status.json`, `runs/*.json` 역할을 `state.json` 하나로 통합한다.
- spec authoring은 소크라테스 문답으로 불확실성을 제거한 뒤 `Implementation Scopes`의 `IMP-*` 항목을 확정하고, 승인된 spec 방향대로만 구현이 진행되게 한다.
- 중복 관리 포인트, 불필요한 파일, 과한 guard/ceremony를 제거해 AI가 더 적은 컨텍스트로 안전하게 이어서 작업할 수 있게 만든다.

## Problem

- 현재 Harness는 spec 기반 구현을 돕기보다 Harness 자체의 lifecycle ceremony를 관리하는 비중이 크다.
- `task.json`, `phases.json`, `runs/*.json`에 상태, 실행 계획, evidence가 분산되어 spec 하나를 이해하려면 여러 파일을 따라가야 한다.
- `runs/*.json`은 실행마다 파일이 늘어나 장기적으로 관리 비용과 컨텍스트 노이즈를 만든다.
- `phase`, `kickoff`, bootstrap metadata, circuit breaker, heavy git hook, strict `allowed_write_paths` 같은 요소가 실제 SDD 목표보다 과하게 복잡하다.
- AI가 다음 세션에서 재개할 때 필요한 정보는 `spec.md`와 현재 진행 상태인데, 현재 구조는 이를 간결하게 제공하지 못한다.

## Goals

- task artifact를 `spec.md` + `state.json` 2개 중심으로 단순화한다.
- `phases.json`, 별도 `status.json`, `runs/` 디렉터리, 기존 `task.json` 역할을 제거하거나 `state.json`으로 흡수한다.
- `IMP-*` Implementation Scope를 spec의 구현 단위이자 실행 단위로 삼고, 별도 phase abstraction을 제거한다.
- `state.json`이 승인 상태, spec lock, current focus, IMP별 진행률, 검증 결과, 최근 이벤트, next action, blockers, user validation을 한 곳에서 표현하게 한다.
- `approve`는 spec 전체 복제 대신 `spec_sha256`과 approval metadata를 `state.json`에 잠근다.
- `plan`은 외부 JSON 입력 없이 승인된 `IMP-*`에서 `state.json.implementation_scopes`를 초기화하거나 동기화한다.
- `run`, `verify`, `review`, `reopen`, `status` 명령을 `state.json` 기준으로 재구성한다.
- 중복 문서와 local ceremony를 줄이고, AI 효율을 떨어뜨리는 hard gate를 최소한의 SDD guard로 바꾼다.

## Non-goals

- `git-ranker` 또는 `git-ranker-client`의 앱 동작, API, UI를 변경하지 않는다.
- 기존 `runs/*.json` history를 장기 보존하거나 새 모델로 완전 migration하지 않는다.
- 외부 workflow engine, database, JSON schema framework를 새로 도입하지 않는다.
- GitHub Actions 기반 운영 정책을 새로 강화하지 않는다.
- 완전한 backwards compatibility를 유지하기 위해 과거 artifact format을 계속 지원하지 않는다.

## Constraints

- 구현 전 이 spec의 열린 clarification이 없어야 하며, 사용자가 최종 승인해야 한다.
- 기존 Harness의 실제 enforcement owner는 `scripts/workflow_runtime/*.py`와 `tests/`이므로 문서 변경과 런타임/테스트 변경을 함께 수행한다.
- 새 구조에서는 task state를 `state.json` 하나로만 전이하며, `spec.md`는 사람용 SDD source of truth로 남긴다.
- `state.json`은 사람이 긴 설명을 읽는 문서가 아니라 AI 재개와 CLI 검증을 위한 compact machine-readable state여야 한다.
- `state.json.events`는 별도 run file 대체용이지만 무한히 커지지 않도록 최근 이벤트만 보존하거나 compact summary 중심으로 관리한다.
- 위험 명령 방지, user validation 없는 완료 차단, 승인되지 않은 spec 실행 차단은 유지한다.
- commit/push 단계에서 개발 흐름을 막는 guard는 제거하거나 위험 명령 방지 수준으로 축소한다.

## Acceptance

- 새 task 생성 결과가 `workflows/tasks/<task-id>/spec.md`와 `workflows/tasks/<task-id>/state.json` 중심으로 동작한다.
- 신규 flow에서 `phases.json`, 별도 `status.json`, `runs/` 디렉터리가 생성되지 않는다.
- `spec.md`에 `Implementation Scopes`가 필수 섹션으로 추가되고, `IMP-*` 항목이 machine-readable 하게 파싱된다.
- `approve`가 열린 clarification이 없는 spec만 승인하고, `state.json.spec_lock.spec_sha256`으로 승인된 spec을 잠근다.
- `plan <task-id>`가 외부 phase JSON 없이 `IMP-*`에서 실행 상태를 초기화한다.
- `run --start`, `run --complete`, `verify`, `review`, `reopen`, `status`가 `state.json`만 읽고 쓰도록 동작한다.
- `kickoff`, circuit breaker, `blocked` state, phase bootstrap metadata, `allowed_write_paths` hard failure, pre-commit hook, docs/AGENTS marker doctor 검증이 제거되거나 단순화된다.
- 테스트는 새 SDD artifact model과 command flow를 기준으로 갱신되고 통과한다.
- docs와 AGENTS는 5단계 `SPEC -> LOCK/PLAN -> IMPLEMENT -> VERIFY -> REVIEW` 흐름으로 정리된다.

## Implementation Scopes

- IMP-01: SDD contract와 문서 구조 재정의
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `AGENTS.md`, `docs/README.md`, `docs/artifact-model.md`, `docs/runtime.md`, `docs/hooks.md`, `docs/runbook.md`
  - 정책: `spec.md + state.json`을 canonical artifact로 선언하고, `phases.json`, `runs/`, `kickoff`, circuit breaker, `blocked` state, heavy git hooks 설명을 제거한다.

- IMP-02: Spec parser에 `Implementation Scopes`와 `IMP-*` intake 추가
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `scripts/workflow_runtime/constants.py`, `scripts/workflow_runtime/models.py`, `scripts/workflow_runtime/templates.py`, `tests/test_workflow_cli.py`
  - 정책: `IMP-*`는 id, title, target repo, change paths, policy를 파싱해야 하며, approval readiness는 열린 clarification 0개와 implementation scope 1개 이상을 요구한다.

- IMP-03: 단일 `state.json` artifact 모델 구현
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `scripts/workflow_runtime/models.py`, `scripts/workflow_runtime/templates.py`, `scripts/workflow_runtime/engine.py`, `tests/test_workflow_cli.py`
  - 정책: 기존 `task.json`, `phases.json`, `status.json`, `runs/*.json` 역할을 `state.json`으로 통합하고, 새 task에서는 `runs/` 디렉터리를 만들지 않는다.

- IMP-04: CLI lifecycle을 `state.json` + `IMP-*` 기준으로 재작성
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `scripts/workflow_runtime/cli.py`, `scripts/workflow_runtime/engine.py`, `scripts/workflow_runtime/models.py`, `scripts/workflow.py`, `tests/test_workflow_cli.py`
  - 정책: `plan --from`, `plan --stdin`, `kickoff`, `run --block`, phase-id 중심 흐름을 제거하고, `run --start/--complete`, `verify`, `review`, `reopen`, `status`가 active IMP를 기준으로 동작한다.

- IMP-05: 과한 guard와 중복 관리 포인트 제거
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `.githooks/`, `workflows/system/hooks.json`, `scripts/workflow_runtime/guards.py`, `scripts/workflow_runtime/doctor.py`, `scripts/workflow_runtime/constants.py`, `tests/test_workflow_cli.py`
  - 정책: pre-commit hook, circuit breaker, docs marker doctor, AGENTS constitution doctor, strict `allowed_write_paths` hard failure를 제거하거나 advisory/reporting 중심으로 낮춘다. dangerous command guard와 user validation guard는 유지한다.

- IMP-06: 중복 policy source와 legacy artifact 정리
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `.codex/skills/`, `.github/`, `workflows/tasks/`, `tests/test_workflow_cli.py`
  - 정책: project-local skill 중복 문서를 제거하고, `.github/`는 SDD local harness에 필요 없으면 제거한다. 기존 task history는 새 모델 구현 검증 뒤 정리한다.

- IMP-07: Verification command 실행 경로와 결과 기록 단순화
  - 대상 저장소: `git-ranker-workflow`
  - 변경 경로: `scripts/workflow_runtime/engine.py`, `scripts/workflow_runtime/models.py`, `tests/test_workflow_cli.py`
  - 정책: `verify`는 IMP별 command와 optional `cwd`를 지원하고, 결과는 `state.json.implementation_scopes[].verification`과 compact `events`에 기록한다.

## Socratic Clarification Log

- Q: 이번 Harness 개편의 최종 목적은 무엇인가?
- A: 소크라테스 문답으로 spec을 고정하고, spec의 `IMP-*` 구현 범위대로만 구현이 진행되는 SDD workflow를 만드는 것이다.
- Decision: Harness의 중심은 phase ceremony가 아니라 `spec.md`와 `Implementation Scopes` 기반 실행이어야 한다.
- Status: resolved

- Q: 하나의 spec 문서에 대응하는 상태 artifact는 몇 개여야 하는가?
- A: 하나의 spec 문서에는 하나의 상태 JSON만 대응되는 것이 관리하기 좋다.
- Decision: `task.json`, `phases.json`, 별도 `status.json`, `runs/*.json`을 `state.json` 하나로 통합한다.
- Status: resolved

- Q: 기존 `runs/*.json` evidence 파일들은 계속 유지해야 하는가?
- A: 아니다. 파일이 너무 많이 생기고 spec 하나의 현재 상태를 파악하는 데 노이즈가 된다.
- Decision: 별도 run file은 제거하고, 필요한 최근 event와 verification summary만 `state.json` 안에 compact하게 기록한다.
- Status: resolved

- Q: phase abstraction은 유지해야 하는가?
- A: `IMP-*`가 이미 구현 범위를 나타내므로 phase를 별도로 관리하면 중복이 된다.
- Decision: `IMP-*`를 실행 단위로 삼고 `phases.json`과 phase bootstrap metadata를 제거한다.
- Status: resolved

- Q: approval 시 spec 내용을 JSON state에 중복 저장해야 하는가?
- A: 중복 저장은 관리 포인트를 늘리므로 피하는 편이 좋다.
- Decision: `state.json`에는 approval metadata와 `spec_sha256`을 저장하고, 실제 요구사항 source of truth는 `spec.md`로 둔다.
- Status: resolved

- Q: AI 효율을 떨어뜨리는 과한 제약은 어떻게 다뤄야 하는가?
- A: commit/push나 phase boundary에서 과하게 차단하는 guard는 줄이고, SDD에 필수적인 승인/검증/위험 명령/user validation guard만 남긴다.
- Decision: pre-commit hard gate, kickoff, circuit breaker, docs marker doctor, strict write scope hard failure를 제거하거나 advisory/reporting으로 낮춘다.
- Status: resolved

- Q: `allowed_write_paths`는 완전히 제거해야 하는가?
- A: 구현 범위 파악에는 여전히 유용하지만 hard failure로 AI 작업을 막으면 효율을 떨어뜨릴 수 있다.
- Decision: `IMP-*`의 target repo와 change paths는 scope intent로 유지하되, out-of-scope 변경은 `state.json.scope_delta` 또는 event로 기록하고 필요 시 spec 재승인 판단에 사용한다.
- Status: resolved

- Q: 테스트 정책은 어디서 강제해야 하는가?
- A: git hook이 아니라 IMP completion 또는 verification 단계에서 확인하는 것이 SDD 흐름에 맞다.
- Decision: TDD guard는 pre-commit에서 제거하고, `run --complete`/`verify` 단계의 evidence 또는 command 결과로 판단한다.
- Status: resolved

- Q: 이 작업에서 기존 history와 project-local skills는 어떻게 다뤄야 하는가?
- A: 최종 SDD 방식에 맞지 않는 history와 중복 policy source는 유지할 이유가 없다.
- Decision: 구현 검증 후 `.codex/skills/`, legacy task artifact, 필요 없는 `.github/` 파일을 제거 대상으로 둔다.
- Status: resolved

## Approval

- Actor: `user`
- Timestamp: `2026-05-03T16:40:22+00:00`
- Note: single-state Socratic SDD spec reapproved under state.json model
