# 2026-04-09-grb-06-backend-test-ci-removal

- Status: `In Progress`
- Primary Repo: `git-ranker`
- Related Issue: `not created in this session`
- Related PR: `not created`

## Request Summary

현 Harness 기준과 맞지 않는 backend legacy test/CI surface를 baseline reset 대상으로 제거한다.

## Problem

`git-ranker`에는 과거 방식의 테스트 코드와 CI 검증 레인이 남아 있다. 이 surface를 유지하면 legacy 검증 의미와 후속 재구성 방향이 동시에 존재하게 된다.

## Goals

- `src/test/` 아래 기존 테스트 코드와 테스트 리소스를 제거한다.
- `build.gradle`의 current test/integration surface를 baseline reset 수준으로 제거한다.
- workflow 파일은 남기되 test execution code path만 제거한다.

## Non-goals

- 새 테스트 코드 작성
- 새 CI 검증 로직 도입
- `src/main/` production 동작 변경

## Socratic Clarification Summary

- 사용자는 workflow 파일 자체 삭제가 아니라 test execution lane 제거를 원한다.
- replacement test/CI는 같은 작업에 넣지 않고 follow-up으로 남긴다.

## Assumptions And Constraints

- baseline reset이 목적이다.
- current active work를 새 spec 체계로 이관한다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `yes`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker`
- Allowed write paths:
  - `build.gradle`
  - `.github/workflows/`
  - `src/test/`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-09-grb-06-backend-test-ci-removal.md`
- Explicitly forbidden:
  - `git-ranker/src/main/`
  - `git-ranker-client/`
  - workflow stable docs mass update
- Network / external systems:
  - 없음
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- backend test source/resource tree가 제거된다.
- workflow 파일은 남지만 test execution code는 제거된다.
- 후속 test/CI rebuild 전제조건이 기록된다.

## Verification
- Contract profile: `backend-change`
- Commands:
  - `./gradlew test`
  - `./gradlew build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `optional`
- PR needed: `yes when published`

## Detailed Subtasks
- `test-tree-removal`
  - Target repo: `git-ranker`
  - Goal: legacy test source/resource tree를 제거한다.
  - Done when: `src/test/` baseline이 비워진다.
  - Verification hook: `./gradlew test`
  - Tracking needed: `no`
- `workflow-lane-reset`
  - Target repo: `git-ranker`
  - Goal: CI/deploy workflow는 유지하되 test execution code path만 제거한다.
  - Done when: retained workflow와 removed test lane이 함께 설명 가능하다.
  - Verification hook: `./gradlew build`, `git diff --check`
  - Tracking needed: `no`

## Risks Or Open Questions

- automated regression surface가 follow-up rebuild 전까지 거의 비게 된다.

## Approval
- Harness judgment: 기존 active work item을 새 spec 체계로 이관해 계속 실행 가능하다고 판단한다.
- User approval: pre-existing active tracked work를 migration 대상으로 유지한다.
