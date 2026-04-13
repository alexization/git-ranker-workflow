# 2026-04-09-grb-04-backend-verification-contract-reset

- Status: `In Progress`
- Primary Repo: `git-ranker`
- Related Issue: `alexization/git-ranker#77`
- Related PR: `alexization/git-ranker#78`

## Request Summary

legacy verification surface를 backend repo 기준의 repo-local verification contract로 다시 정렬한다.

## Problem

`git-ranker`에는 harness 기준으로 재사용하기 어려운 legacy verification surface가 남아 있고, cleanup 이후 review에서 orphan integration lane과 pre-deploy verification gap이 드러났다.

## Goals

- backend verification surface를 repo-local canonical source 기준으로 정리한다.
- minimal `integrationTest` lane과 pre-deploy verification gate를 복구한다.
- legacy verification surface 제거와 current repair 범위를 함께 기록한다.

## Non-goals

- 새 기능 구현
- backend production behavior 변경
- legacy coverage/OpenAPI/Docker preflight surface 복구

## Socratic Clarification Summary

- 현재 active work item을 새 spec 체계로 이관하는 작업이므로, 요구사항은 기존 issue와 active work 범위를 그대로 유지한다.
- 이번 subtask의 핵심은 legacy surface reset 자체보다 review에서 드러난 minimum verification gap repair다.

## Assumptions And Constraints

- primary repo와 task type은 `git-ranker` / `backend 수정`으로 고정한다.
- local Docker daemon이 없을 수 있으므로 integration lane 최종 확인은 remote CI evidence를 사용할 수 있다.

## Write Scope
- Primary repo: `git-ranker`
- Allowed write paths:
  - `README.md`
  - `build.gradle`
  - `.github/workflows/`
  - `docs/openapi/`
  - `src/test/java/com/gitranker/api/architecture/`
  - `src/test/java/com/gitranker/api/docs/`
  - `src/test/java/com/gitranker/api/testsupport/`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
- Explicitly forbidden:
  - `git-ranker-client` code tree
  - `src/main/` production feature change
  - workflow stable source of truth mass update
- Network / external systems:
  - GitHub issue/PR metadata for `alexization/git-ranker`
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- minimal `integrationTest` lane이 다시 executable하다.
- deploy workflow 앞단에 verification gate가 복구된다.
- legacy verification surface 제거 범위와 remaining risk가 기록된다.

## Verification
- Contract profile: `backend-change`
- Commands:
  - `./gradlew test`
  - `./gradlew integrationTest`
  - `./gradlew build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `yes`
- PR needed: `yes`

## Detailed Subtasks
- `legacy-verification-surface-reset`
  - Target repo: `git-ranker`
  - Goal: obsolete verification task, workflow, doc surface를 제거하거나 neutralize한다.
  - Done when: cleanup 범위가 고정되고 repo-local baseline이 남는다.
  - Verification hook: `./gradlew test`, `./gradlew build`
  - Tracking needed: `yes`
- `minimum-verification-gap-repair`
  - Target repo: `git-ranker`
  - Goal: orphan integration lane과 pre-deploy verification gap을 복구한다.
  - Done when: `integrationTest` lane과 deploy gate가 current diff 기준으로 설명 가능하다.
  - Verification hook: `./gradlew integrationTest`, CI evidence 필요 시
  - Tracking needed: `no`

## Risks Or Open Questions

- local Docker 부재 때문에 integration lane은 remote CI evidence 의존이 남을 수 있다.
- coverage/OpenAPI/Docker preflight surface는 follow-up으로 남는다.

## Approval
- Harness judgment: 기존 active work item을 새 spec 체계로 이관해 계속 실행 가능하다고 판단한다.
- User approval: pre-existing active tracked work를 migration 대상으로 유지한다.
