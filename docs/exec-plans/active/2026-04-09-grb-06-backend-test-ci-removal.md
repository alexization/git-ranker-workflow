# 2026-04-09-grb-06-backend-test-ci-removal

- Issue ID: `GRB-06`
- GitHub Issue: `not created in this session`
- GitHub PR: `not created`
- Status: `In Progress`
- Repository: `git-ranker`
- Branch Name: `feat/grb-06-backend-test-ci-removal`
- Task Slug: `2026-04-09-grb-06-backend-test-ci-removal`
- Primary Context Pack: `backend-change`
- Verification Contract Profile: `backend-change`

## Problem

`git-ranker`에는 현재 과거 방식의 테스트 코드와 CI 검증 레인이 남아 있다. 사용자는 현 Harness 기준과 맞지 않는 이 surface를 일단 전부 제거하고, 이후 보완된 테스트 skill과 새 CI 검증 로직을 기준으로 다시 구축하려고 한다.

## Why Now

현재 남아 있는 테스트 코드와 GitHub Actions 검증 로직은 이후 재구성 대상인데, 지금 상태를 유지하면 legacy 검증 의미와 새 Harness 재구성 방향이 동시에 존재하게 된다. 재작성 전에 baseline을 비워 두어야 후속 test/CI 재구성 범위를 분리할 수 있다.

## Scope

- `git-ranker/src/test/` 아래의 기존 테스트 코드와 테스트 리소스를 제거한다.
- `git-ranker/build.gradle`에서 현재 테스트 코드와 CI 레인을 위해 유지되던 test/integration 관련 의존성과 커스텀 task를 제거한다.
- `git-ranker/.github/workflows/ci.yml`과 `deploy.yml`은 유지하되, 테스트를 실행하는 단계와 연결만 제거한다.
- 이번 변경의 범위, 검증 결과, 후속 재구성 전제조건을 workflow exec plan에 기록한다.

## Non-scope

- 새 테스트 코드 작성
- 새 CI 검증 로직 도입
- `git-ranker/src/main/` production 동작 변경
- frontend 또는 workflow stable source of truth 재설계

## Write Scope

- Primary repo: `git-ranker`
- Allowed write paths:
  - `build.gradle`
  - `.github/workflows/`
  - `src/test/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-09-grb-06-backend-test-ci-removal.md`
- Explicitly forbidden:
  - `git-ranker/src/main/`
  - `git-ranker-client/`
  - workflow stable docs mass update
- Network / external systems:
  - 없음
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Outputs

- backend test source/resource tree removed
- `build.gradle`에서 current test suite 전용 dependency/task surface removed
- `.github/workflows/ci.yml` retained without test execution steps
- `.github/workflows/deploy.yml` retained without pre-deploy test verification lane
- active exec plan with latest verification report

## Working Decisions

- 이번 작업의 primary repo와 task type은 `git-ranker` / `backend 수정`으로 고정한다.
- baseline reset이 목적이므로 replacement test/CI는 같은 issue에 넣지 않는다.
- production source 변경 없이 test/verification ownership surface만 비운다.
- workflow 파일 자체는 남기되, 테스트를 실제로 호출하는 code path만 제거한다.

## Execution Note

- initial removal plan은 `ci.yml` 삭제까지 포함했지만, user가 중간에 범위를 좁혀 workflow 파일은 유지하고 test execution code만 제거하도록 조정했다.
- 최종 diff는 narrowed scope를 따라 `ci.yml` placeholder 유지, `deploy.yml` deploy lane 유지, backend test source 제거로 수렴했다.

## Context Selection Summary

- Task type: `backend 수정`
- Primary context pack: `backend-change`
- Required docs:
  - `AGENTS.md`
  - `docs/README.md`
  - `PLANS.md`
  - `docs/operations/workflow-governance.md`
  - `docs/architecture/context-pack-registry.md`
  - `docs/operations/tool-boundary-matrix.md`
  - `docs/operations/verification-contract-registry.md`
  - `git-ranker/README.md`
  - `git-ranker/build.gradle`
  - `git-ranker/.github/workflows/ci.yml`
  - `git-ranker/.github/workflows/deploy.yml`
- Optional docs trigger:
  - 기존 backend verification cleanup 이력이 필요하면 `2026-04-09-grb-04-backend-verification-contract-reset.md`
- Forbidden context:
  - frontend repo code tree
  - unrelated workflow stable docs eager load
  - `src/main/` production feature 탐색 확장

## Boundary Check Summary

- Read boundary:
  - backend verification surface와 현재 exec plan 근처까지만 읽는다.
- Write boundary:
  - `git-ranker/build.gradle`
  - `git-ranker/.github/workflows/`
  - `git-ranker/src/test/`
  - current workflow exec plan
- Control-plane artifact:
  - current active exec plan
- Explicitly forbidden path:
  - `git-ranker/src/main/`
  - sibling frontend repo
- Network:
  - 없음
- Escalation:
  - declared verification command가 sandbox 제약으로 막힐 때만

## Verification

- `./gradlew test`
- `./gradlew build`
- `git diff --check`

## Evidence

- removed backend test inventory
- removed Gradle test/integration surface inventory
- removed CI/deploy test execution inventory
- latest `test`, `build`, `git diff --check` result
- follow-up rebuild preconditions for future test/CI reintroduction

## Risks or Blockers

- `build`는 Java plugin 기본 lifecycle 때문에 empty `test` task를 계속 통과시킬 수 있다. 이는 current explicit test suite removal의 결과이지 replacement verification 도입이 아니다.
- CI/deploy workflow 파일은 남지만 automated test verification은 후속 test/CI 재구성 전까지 비어 있게 된다.
- 후속 작업이 시작되기 전까지 backend repo는 automated regression surface가 거의 없는 상태가 된다.

## Docs Updated

- stable source of truth update는 이번 issue 범위가 아니다.
- control-plane artifact인 current exec plan만 갱신한다.

## Skill Consideration

- 이번 작업은 기존 `request-intake`, `issue-to-exec-plan`, `context-pack-selection`, `boundary-check` 흐름으로 닫는다.
- 후속 test/CI 재구성 단계에서 repo-specific test bootstrap 또는 CI template가 반복되면 별도 skill 후보로 검토한다.

## Verification Report

- Contract profile: `backend-change`
- Overall status: `passed`
- Preconditions:
  - branch: `feat/grb-06-backend-test-ci-removal`
  - `src/test/` tree removed
  - `.github/workflows/ci.yml` and `.github/workflows/deploy.yml` retained, but test execution code removed
- Command: `./gradlew test`
  - Status: `passed`
  - Evidence: empty test baseline에서 task가 성공했고 build graph는 유지됐다.
- Command: `./gradlew build`
  - Status: `passed`
  - Evidence: `compileTestJava NO-SOURCE`, `test NO-SOURCE` 상태로 전체 build가 성공했다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: backend repo diff와 workflow control-plane diff 모두 formatting 오류가 없다.
- Failure summary: 없음
- Next action:
  - future test skill 보강 이후 backend test suite와 CI verification lane를 새 contract 기준으로 재구성한다.
