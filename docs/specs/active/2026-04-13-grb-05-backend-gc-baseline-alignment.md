# 2026-04-13-grb-05-backend-gc-baseline-alignment

- Status: `Draft`
- Primary Repo: `git-ranker`
- Related Issue: `not created`
- Related PR: `not created`

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

## Assumptions And Constraints

- Prerequisites before approval: `GRB-04`, `GRB-07`
- backend GC baseline ownership은 repo-local이다.
- workflow repo는 상위 semantics와 evidence 규칙만 유지한다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `exact GC surface`, `retained CI scope`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker`
- Allowed write paths:
  - `build.gradle`
  - backend static analysis config directly tied to the approved slice
  - `.github/workflows/`
  - `README.md` or backend verification entry docs
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grb-05-backend-gc-baseline-alignment.md`
- Explicitly forbidden:
  - frontend repo edits
  - unrelated backend production code changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- backend GC baseline ownership이 repo-local Gradle/CI surface로 설명된다.
- static analysis config, workflow, verification docs가 같은 baseline semantics를 따른다.
- workflow repo가 backend GC implementation detail을 소유하지 않는다.

## Verification
- Contract profile: `backend-change`
- Commands:
  - `./gradlew test`
  - `./gradlew build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `conditional`
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
- Harness judgment: seed spec은 적절하지만, backend repo current GC surface 확인 전에는 승인하지 않는다.
- User approval: `not yet requested for execution`
