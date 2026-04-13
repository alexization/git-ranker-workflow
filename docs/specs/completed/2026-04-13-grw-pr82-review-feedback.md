# 2026-04-13-grw-pr82-review-feedback

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `alexization/git-ranker-workflow#82`

## Request Summary

PR `#82`의 코드리뷰 코멘트를 검토하고, 반영할 내용이 있으면 workflow 문서와 active spec을 수정한다.

## Problem

PR `#82` 리뷰에서 두 가지 문서 일관성 문제가 지적됐다. 첫째, `approval gate` requirement가 기존 active spec을 즉시 비호환처럼 보이게 만들 수 있다. 둘째, workflow governance의 실행 순서가 verification 단계의 spec reopen trigger를 누락해 같은 문서 안에서 운영 path가 갈릴 수 있다.

## Goals

- 현재 active spec 두 건이 새 minimum shape와 충돌하지 않도록 호환성을 맞춘다.
- `현재 기준 실행 순서`에 verification-based reopen trigger를 명시한다.
- PR `#82`에 올린 변경이 review feedback 기준으로 설명 가능하게 만든다.

## Non-goals

- PR review thread reply 또는 resolve
- app repo 코드/테스트 변경
- PR `#82`의 나머지 본문/제목 재작성

## Socratic Clarification Log

### Round 1
- Prompted gap: review comment가 실제로 code change가 필요한 actionable feedback인지 여부
- Why it mattered: informational comment까지 섞어 scope를 넓히면 PR repair 범위가 흔들린다
- User answer / evidence:
  - 사용자는 PR `#82` 코드리뷰를 검토하고 반영할 내용이 있으면 반영해 달라고 요청했다
  - connector review comment 두 개는 모두 specific file/line을 가진 actionable doc feedback이었다
- Closed gap: 이번 작업은 두 review comment 반영으로 좁힐 수 있다

## Assumptions And Constraints

- review reply나 thread resolve는 사용자 요청이 없어 수행하지 않는다.
- current PR branch `codex/socratic-loop-hardening` 위에서 docs-only repair commit 하나로 닫는 것이 가장 자연스럽다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `yes`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/workflow-governance.md`
  - `docs/specs/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - `docs/specs/active/2026-04-09-grb-06-backend-test-ci-removal.md`
  - `docs/specs/completed/2026-04-13-grw-pr82-review-feedback.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-pr82-review-feedback.md`
- Explicitly forbidden:
  - sibling app repo changes
  - unrelated policy rewrites outside the two review findings
- Network / external systems:
  - GitHub PR review context for `alexization/git-ranker-workflow#82`
- Escalation triggers:
  - git commit / git push only

## Acceptance Criteria

- active spec 두 건이 `Approval Gate`를 포함해 새 shape와 충돌하지 않는다.
- `docs/operations/workflow-governance.md`의 실행 순서가 verification-based reopen trigger를 포함한다.
- workflow-docs verification evidence가 남는다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,220p' docs/specs/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - `sed -n '1,220p' docs/specs/active/2026-04-09-grb-06-backend-test-ci-removal.md`
  - `sed -n '150,170p' docs/operations/workflow-governance.md`
  - `rg -n "Approval Gate|verification, review, feedback, user validation" docs/specs/active docs/operations/workflow-governance.md`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `default lane`
- Parent issue needed: `no`
- PR needed: `already open`

## Detailed Subtasks
- `active-spec-compatibility`
  - Target repo: `git-ranker-workflow`
  - Goal: 기존 active spec 두 건에 `Approval Gate`를 추가해 minimum shape와 맞춘다.
  - In-scope: review comment 1 관련 active spec 보강
  - Done when: 두 active spec 모두 approval gate를 가진다.
  - Verification hook: active spec review
  - Tracking needed: `no`
- `execution-order-alignment`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow governance 실행 순서가 verification-based reopen trigger를 포함한다.
  - In-scope: review comment 2 관련 wording 정렬
  - Done when: 실행 순서 문장이 runtime principle과 state machine에 맞는다.
  - Verification hook: governance review
  - Tracking needed: `no`

## Risks Or Open Questions

- active spec에 approval gate를 추가해도 older clarification summary wording은 남아 있을 수 있다. 이번 repair는 review comment 범위에 한정한다.

## Approval
- Harness judgment: 두 review comment 모두 명확하고 bounded docs repair로 닫을 수 있다.
- User approval: 사용자가 PR `#82`의 코드리뷰를 검토하고 반영할 내용이 있으면 반영해 달라고 요청했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Review evidence:
  - `gh api graphql`로 PR `#82`의 unresolved review thread를 확인했고, actionable thread는 2건이었다.
  - thread 1은 `docs/operations/sdd-spec-policy.md`의 `Approval Gate` minimum shape가 기존 active spec과 충돌한다는 지적이었다.
  - thread 2는 `docs/operations/workflow-governance.md` 실행 순서가 verification-based reopen trigger를 누락한다는 지적이었다.
- Ran:
  - `sed -n '1,220p' docs/specs/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - `sed -n '1,220p' docs/specs/active/2026-04-09-grb-06-backend-test-ci-removal.md`
  - `sed -n '150,170p' docs/operations/workflow-governance.md`
  - `rg -n "Approval Gate|verification, review, feedback, user validation" docs/specs/active docs/operations/workflow-governance.md`
  - `git diff --check`
- Evidence:
  - 기존 active spec 두 건이 모두 `Approval Gate` section을 가져 current minimum shape와 충돌하지 않는다.
  - workflow governance 실행 순서가 `verification, review, feedback, user validation`을 모두 reopen trigger로 명시한다.
  - 문서 diff에 whitespace 또는 patch formatting 문제는 없다.
- Failure or skipped summary: review reply / thread resolve는 사용자 요청이 없어 수행하지 않았다.
- Next action: merged in PR `#82`

## Final Change Summary

- active spec 두 건에 `Approval Gate`를 보강했다.
- workflow governance 실행 순서에 verification-based reopen trigger를 반영했다.
- review feedback artifact를 completed history로 보존했다.

## Final User Validation

- PR `#82`는 2026-04-13에 merged 되었고, 이 spec은 해당 review repair의 historical close-out record로 보존된다.
