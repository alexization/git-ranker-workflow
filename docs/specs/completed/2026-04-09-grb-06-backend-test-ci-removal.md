# 2026-04-09-grb-06-backend-test-ci-removal

- Status: `Completed`
- Primary Repo: `git-ranker`
- Related Issue: `alexization/git-ranker#82`
- Related PR: `alexization/git-ranker#83`

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
- current `src/test/` tree는 이미 비어 있으므로, 이번 slice의 실질 변경은 residual Gradle dependency/task surface와 workflow test execution code path 제거에 집중된다.

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
  - `.github/workflows/ci.yml`
  - `.github/workflows/deploy.yml`
  - `src/test/`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-09-grb-06-backend-test-ci-removal.md`
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

## Verification Summary

- Contract profile: `backend-change`
- Overall status: `passed`
- Ran:
  - `./gradlew test`
  - `./gradlew build`
  - `git diff --check` in `git-ranker`
  - `git diff --check` in `git-ranker-workflow`
- Evidence:
  - current `src/test/` tree는 계속 비어 있고, legacy test source/resource tree가 다시 도입되지 않았다.
  - `git-ranker/build.gradle`에서 legacy test dependency와 custom `integrationTest` task를 제거해 residual test/integration surface를 baseline reset 수준으로 걷어냈다.
  - `git-ranker/.github/workflows/ci.yml`과 `git-ranker/.github/workflows/deploy.yml`은 workflow 파일을 유지한 채 test execution code path를 제거하고 `./gradlew build`만 실행하도록 줄였다.
  - reset 뒤에도 `./gradlew test`와 `./gradlew build`가 모두 성공했고, 두 저장소에서 `git diff --check`가 통과했다.
- Failure or skipped summary:
  - `./gradlew test`는 current baseline 특성상 `NO-SOURCE`로 종료된다.
- Next action: completed

## Final Change Summary

- backend repo의 legacy test lane은 이미 비어 있는 `src/test/` tree 위에 남아 있던 Gradle dependency/task 선언과 workflow execution path까지 함께 제거하며 닫았다.
- workflow 파일 자체는 유지해 deploy/build orchestration은 남기되, reset 대상이었던 unit/integration execution lane만 없앴다.
- 후속 test/CI rebuild는 repo-local baseline을 다시 정의하는 별도 follow-up으로 남긴다.

## Final User Validation

- 사용자는 `GRB-05, GRB-06을 진행해주세요.`라고 요청해 legacy test/CI surface reset continuation을 직접 승인했다.
- 이번 close-out은 existing tracked work item의 reset 목적을 유지하면서 residual build/workflow cleanup까지 포함해 마무리했다.

## Docs Updated

- `git-ranker/build.gradle`
- `git-ranker/.github/workflows/ci.yml`
- `git-ranker/.github/workflows/deploy.yml`
- `docs/specs/completed/2026-04-09-grb-06-backend-test-ci-removal.md`
