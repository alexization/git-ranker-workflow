# 2026-04-13-grb-05-backend-gc-baseline-alignment

- Status: `Completed`
- Primary Repo: `git-ranker`
- Related Issue: `alexization/git-ranker#82`
- Related PR: `alexization/git-ranker#83`

## Request Summary

backend GC baseline을 workflow repo가 아니라 backend repo의 Gradle task와 GitHub Actions ownership으로 정렬한다.

## Problem

backend guardrail and GC baseline이 repo-local Gradle/CI ownership으로 충분히 정렬되지 않으면 workflow control plane이 quality gate까지 소유하는 것처럼 보일 수 있다. 이는 federated ownership model과 충돌한다.

## Goals

- backend GC baseline ownership을 repo-local Gradle task와 GitHub Actions로 고정한다.
- static analysis config와 verification entry docs의 연결을 정리한다.
- workflow repo가 상위 semantics만 소유한다는 경계를 재확인한다.

## Non-goals

- backend feature 변경
- frontend repo 수정
- workflow repo에서 backend GC를 대신 실행하는 새 surface 추가

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRB-05`를 product 제거 이후에도 canonical requirement로 남길 방법
- Why it mattered: backend quality baseline alignment가 사라지면 repo-local guardrail ownership migration이 미완으로 남는다
- User answer / evidence:
  - current user request는 product task를 새로운 요구사항으로 전환하라고 명시한다
  - former catalog entry는 `build.gradle`, backend static analysis config, `.github/workflows/`, backend README 또는 verification entry docs`를 권장 write scope로 제시했다
- Closed gap: `GRB-05`는 backend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact GC surface와 retained workflow scope를 더 좁혀야 한다

### Round 2
- Prompted gap: exact GC surface, retained CI scope, tracking 여부
- Why it mattered: repo-local baseline을 어떤 Gradle/workflow/doc surface가 소유하는지 잠기지 않으면 `GRB-06`의 legacy lane reset 뒤에도 backend guardrail ownership이 다시 흐려진다
- User answer / evidence:
  - current `git-ranker/src/test/` tree는 이미 비어 있고, `./gradlew test`, `./gradlew integrationTest`, `./gradlew build`는 모두 성공하지만 test lane은 `NO-SOURCE` baseline이다
  - `git-ranker/build.gradle`은 여전히 `testImplementation`, `testRuntimeOnly`, `tasks.named('test')`, `integrationTest`를 선언하고 `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`도 같은 legacy trio를 실행한다
  - `git-ranker/AGENTS.md`는 repo-local verification baseline을 여전히 `test -> integrationTest -> build`로 설명하고, 별도 backend static analysis config 파일은 현재 repo에 없다
- Closed gap: 이번 slice의 exact GC surface는 `build.gradle`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `AGENTS.md`로 잠그고, retained CI scope는 `./gradlew build` 단일 baseline으로 고정한다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: `GRB-04`, `GRB-07`
- backend GC baseline ownership은 repo-local이다.
- workflow repo는 상위 semantics와 evidence 규칙만 유지한다.
- current repo에는 standalone backend static analysis config가 없으므로, 이번 slice의 baseline semantics는 Gradle build surface와 GitHub Actions, `AGENTS.md`가 함께 소유한다.
- root `README.md`는 overview-only surface로 유지하고 GC baseline detail은 repo entry docs와 workflow가 소유한다.

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
  - `AGENTS.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grb-05-backend-gc-baseline-alignment.md`
- Explicitly forbidden:
  - frontend repo edits
  - unrelated backend production code changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- backend GC baseline ownership이 repo-local Gradle/CI surface로 설명된다.
- `build.gradle`, workflow, `AGENTS.md`가 같은 baseline semantics를 따른다.
- standalone backend static analysis config가 없는 current state를 새 surface 없이 설명한다.
- workflow repo가 backend GC implementation detail을 소유하지 않는다.

## Verification
- Contract profile: `backend-change`
- Commands:
  - `./gradlew build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `backend-gc-surface-inventory`
  - Target repo: `git-ranker`
  - Goal: current GC/static analysis/CI surface를 inventory하고 repo-local ownership 범위를 잠근다.
  - In-scope: build task, static analysis config, workflow references
  - Done when: retained baseline surface가 설명 가능하다.
  - Verification hook: config and workflow review
  - Tracking needed: `no`
- `repo-local-baseline-alignment`
  - Target repo: `git-ranker`
  - Goal: backend GC baseline을 repo-local entry docs와 함께 정렬한다.
  - In-scope: verification docs, CI wording, retained tasks
  - Done when: workflow repo 없이도 backend GC baseline을 해석할 수 있다.
  - Verification hook: declared commands + doc review
  - Tracking needed: `conditional`

## Risks Or Open Questions

- current backend repo의 GC surface가 legacy lane과 섞여 있으면 baseline reset 또는 split spec이 더 필요할 수 있다.

## Approval
- Harness judgment: actual Gradle/workflow/doc surface, retained CI scope, tracking decision이 잠겨 repo-local baseline alignment slice로 바로 실행 가능하다.
- User approval: current user request가 `GRB-05`, `GRB-06` sequenced backend continuation을 직접 요청했다.

## Verification Summary

- Contract profile: `backend-change`
- Overall status: `passed`
- Ran:
  - `./gradlew build`
  - `git diff --check` in `git-ranker`
  - `git diff --check` in `git-ranker-workflow`
- Evidence:
  - `git-ranker/build.gradle`은 legacy test dependency와 custom `integrationTest` surface를 제거하고 current build-only baseline만 남겼다.
  - `git-ranker/.github/workflows/ci.yml`과 `git-ranker/.github/workflows/deploy.yml`은 같은 baseline을 `./gradlew build` 단일 step으로 실행하도록 정렬됐다.
  - `git-ranker/AGENTS.md`는 current repo-local baseline이 dedicated test/integration lane 없이 build-only라는 점과 follow-up rebuild contract를 직접 설명한다.
  - backend repo와 workflow repo 모두 `git diff --check`를 통과했다.
- Failure or skipped summary:
  - 없음
- Next action: completed

## Final Change Summary

- backend GC baseline ownership을 `build.gradle`, GitHub Actions workflow, `AGENTS.md`가 공유하는 build-only semantics로 다시 잠갔다.
- standalone backend static analysis config가 없는 current state를 새 surface 없이 설명하고, workflow repo가 backend GC implementation detail을 대신 소유하지 않게 정리했다.
- `GRB-06`의 legacy lane reset 이후 남는 repo-local guardrail baseline을 같은 change set에서 바로 문서화해 downstream handoff ambiguity를 없앴다.

## Final User Validation

- 사용자는 `GRB-05, GRB-06을 진행해주세요.`라고 요청해 backend baseline reset과 repo-local baseline alignment를 같은 continuation 범위로 직접 승인했다.
- 이번 close-out으로 backend repo는 current contract 기준에서 build/workflow/entry-doc surface만으로 baseline을 해석할 수 있게 됐다.

## Docs Updated

- `git-ranker/build.gradle`
- `git-ranker/.github/workflows/ci.yml`
- `git-ranker/.github/workflows/deploy.yml`
- `git-ranker/AGENTS.md`
- `docs/specs/completed/2026-04-13-grb-05-backend-gc-baseline-alignment.md`
