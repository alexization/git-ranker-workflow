# 2026-04-13-grw-sdd-socratic-harness-workflow

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

Harness 시스템에서 `exec plan` 개념을 완전히 제거하고, SDD와 소크라테스 프롬프트를 적용한 새로운 workflow를 구축한다.

## Problem

기존 Harness는 request routing, exec plan, context pack, verification artifact가 분리되어 있었고, 사용자가 원하는 `답 내놓기 금지, 먼저 캐물어라` 기반 spec-first workflow와 맞지 않았다.

## Goals

- `exec plan` 개념과 `docs/exec-plans/` 트리를 제거한다.
- 모든 즉시 실행 가능한 작업이 소크라테스 기반 approved spec을 먼저 갖도록 바꾼다.
- spec 하나가 요구사항, 하위 작업, write scope, verification, tracking 결정을 함께 소유하도록 재설계한다.
- issue 생성은 conditional로 두고, publish가 필요한 결과만 PR로 공개하는 흐름을 유지한다.
- current active work는 새 `docs/specs/active/`로 이관한다.

## Non-goals

- backend/frontend repo 구현 작업 자체 수행
- old completed exec plan historical record 보존
- repo-local app source of truth 재설계

## Socratic Clarification Summary

- 모든 즉시 실행 가능한 작업에 소크라테스 기반 spec을 필수 적용한다.
- spec 고정 조건은 `Harness 판단 + 사용자 승인`이다.
- issue 생성은 추적이 필요할 때만 한다.
- `exec plan`은 완전히 제거하고, 하위 작업 정의도 spec 안에서 처리한다.
- 기존 `docs/exec-plans/`는 archive 없이 제거한다.

## Assumptions And Constraints

- workflow는 control plane만 소유한다.
- tracking issue와 implementation PR은 spec이 요구할 때만 만든다.
- 기존 active backend 작업 2건은 새 active spec으로 이관해 canonical working artifact 공백을 막는다.

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `AGENTS.md`
  - `SPECS.md`
  - `docs/`
  - `.github/`
  - `.codex/skills/`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-sdd-socratic-harness-workflow.md`
  - `docs/specs/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - `docs/specs/active/2026-04-09-grb-06-backend-test-ci-removal.md`
- Explicitly forbidden:
  - sibling app repo code change
  - app repo implementation start
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- source of truth 문서가 `exec plan` 없이 spec-first workflow를 설명한다.
- `docs/exec-plans/`가 제거된다.
- project-local skill registry가 `socratic-spec-authoring` 중심 순서로 재정렬된다.
- active backend work 2건이 `docs/specs/active/`로 이관된다.
- old `exec plan` 용어가 stable source of truth와 skill layer에서 제거된다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,220p' SPECS.md`
  - `sed -n '1,260p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,240p' .codex/skills/README.md`
  - `find docs/specs -maxdepth 2 -type f | sort`
  - `rg -n "Socratic|소크라테스|approved spec|docs/specs|user final|user validation|Detailed Subtasks|verification contract profile" AGENTS.md SPECS.md docs .codex .github`
  - `rg -n "exec plan|docs/exec-plans|issue-to-exec-plan|PLANS.md|task brief" AGENTS.md SPECS.md docs/architecture docs/operations docs/product .codex .github`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `source-of-truth-migration`
  - Target repo: `git-ranker-workflow`
  - Goal: architecture, operations, product, root entry docs를 spec-first workflow로 재작성한다.
  - Done when: stable source of truth가 approved spec 중심 흐름을 설명한다.
  - Verification hook: workflow-docs grep and `sed` review
  - Tracking needed: `no`
- `skill-layer-migration`
  - Target repo: `git-ranker-workflow`
  - Goal: `issue-to-exec-plan`을 제거하고 `socratic-spec-authoring`을 새 기본 진입점으로 추가한다.
  - Done when: skill registry와 핵심 skill이 새 순서를 따른다.
  - Verification hook: skill README and skill file review
  - Tracking needed: `no`
- `active-work-migration`
  - Target repo: `git-ranker-workflow`
  - Goal: 기존 active backend work 2건을 새 active spec으로 이관한다.
  - Done when: `docs/specs/active/`에 대응 spec이 존재한다.
  - Verification hook: `find docs/specs -maxdepth 2 -type f | sort`
  - Tracking needed: `no`
- `exec-plan-removal`
  - Target repo: `git-ranker-workflow`
  - Goal: old `docs/exec-plans/` tree와 obsolete skill asset을 제거한다.
  - Done when: old terminology grep이 비어 있다.
  - Verification hook: negative `rg`
  - Tracking needed: `no`

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,220p' SPECS.md`
  - `sed -n '1,260p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,240p' .codex/skills/README.md`
  - `find docs/specs -maxdepth 2 -type f | sort`
  - `rg -n "Socratic|소크라테스|approved spec|docs/specs|user final|user validation|Detailed Subtasks|verification contract profile" AGENTS.md SPECS.md docs .codex .github`
  - `rg -n "exec plan|docs/exec-plans|issue-to-exec-plan|PLANS.md|task brief" AGENTS.md SPECS.md docs/architecture docs/operations docs/product .codex .github`
  - `git diff --check`
- Evidence:
  - root entrypoint가 `SPECS.md`와 `docs/specs/` 기준으로 바뀌었다.
  - workflow governance, state machine, verification/review/feedback policy가 모두 approved spec vocabulary를 사용한다.
  - skill registry가 `request-intake -> ambiguity-interview -> socratic-spec-authoring` 순서로 바뀌었다.
  - `docs/specs/active/`에 현재 active backend 작업 2건이 이관됐다.
  - stable source of truth와 skill/template layer에서 old `exec plan` terminology grep은 결과가 없었고, completed migration spec만 제거 대상을 설명하기 위해 예외적으로 해당 용어를 포함한다.
- Failure or skipped summary: 없음
- Next action: user validation

## Final Change Summary

- `SPECS.md`와 `docs/specs/` 구조를 추가했다.
- `docs/operations/sdd-spec-policy.md`를 추가하고 runtime governance를 spec-first로 재작성했다.
- `docs/architecture/`, `docs/product/`, `.github/`, `.codex/skills/`를 approved spec 기준으로 정렬했다.
- `issue-to-exec-plan` skill과 `docs/exec-plans/` tree를 제거했다.

## Final User Validation

- 사용자는 소크라테스 loop에서 아래 결정을 직접 승인했다.
  - 모든 즉시 실행 가능한 작업에 spec 필수
  - spec 고정 조건은 Harness 판단 + 사용자 승인
  - issue 생성은 추적이 필요할 때만
  - `exec plan` 완전 제거
- 이번 turn의 구현 결과는 그 승인된 방향에 맞게 반영되었다.
