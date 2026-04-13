# 2026-04-13-grc-06-frontend-gc-baseline-alignment

- Status: `Draft`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend GC baseline을 repo-local npm script와 GitHub Actions ownership으로 정렬한다.

## Problem

frontend quality baseline이 workflow repo가 아니라 frontend repo의 script/CI surface로 고정되지 않으면 federated ownership model 아래에서 guardrail 위치가 계속 흔들린다.

## Goals

- frontend GC baseline ownership을 repo-local npm script와 GitHub Actions로 고정한다.
- static analysis config와 verification entry docs의 연결을 정리한다.
- workflow repo는 상위 semantics만 남긴다.

## Non-goals

- frontend feature 구현
- backend repo 수정
- workflow repo에 frontend GC implementation guide를 추가하는 것

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-06`을 product 제거 후에도 남길 canonical surface
- Why it mattered: frontend track의 repo-local guardrail baseline alignment가 future work로 계속 남아 있어야 한다
- User answer / evidence:
  - current user request는 product task를 새로운 요구사항으로 전환하라고 한다
  - former catalog entry는 `package.json`, frontend static analysis config, `.github/workflows/`, frontend README 또는 repo entry docs`를 권장 write scope로 제시했다
- Closed gap: `GRC-06`은 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact frontend GC surface와 retained CI scope를 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: `GRC-05`, `GRC-07`
- frontend GC baseline ownership은 repo-local이다.
- workflow repo는 상위 semantics와 evidence rule만 유지한다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `exact GC surface`, `retained CI scope`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker-client`
- Allowed write paths:
  - `package.json`
  - frontend static analysis config directly tied to the approved slice
  - `.github/workflows/`
  - `README.md` or frontend entry docs
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grc-06-frontend-gc-baseline-alignment.md`
- Explicitly forbidden:
  - backend repo edits
  - unrelated frontend route or UI changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- frontend GC baseline ownership이 repo-local npm script/CI surface로 설명된다.
- static analysis config, workflow, verification docs가 같은 baseline semantics를 따른다.
- workflow repo가 frontend GC implementation detail을 소유하지 않는다.

## Verification
- Contract profile: `frontend-change`
- Commands:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `conditional`
- PR needed: `conditional`

## Detailed Subtasks
- `frontend-gc-surface-inventory`
  - Target repo: `git-ranker-client`
  - Goal: current GC/static analysis/CI surface를 inventory하고 repo-local ownership 범위를 잠근다.
  - In-scope: script, config, workflow references
  - Done when: retained baseline surface가 설명 가능하다.
  - Verification hook: config and workflow review
  - Tracking needed: `no`
- `repo-local-baseline-alignment`
  - Target repo: `git-ranker-client`
  - Goal: frontend GC baseline을 repo-local entry docs와 함께 정렬한다.
  - In-scope: verification docs, CI wording, retained scripts
  - Done when: workflow repo 없이도 frontend GC baseline을 해석할 수 있다.
  - Verification hook: declared commands + doc review
  - Tracking needed: `conditional`

## Risks Or Open Questions

- current frontend repo의 GC surface가 실제 script/config 상태와 다르면 approval 단계에서 더 좁은 split이 필요할 수 있다.

## Approval
- Harness judgment: seed spec은 적절하지만, frontend repo current GC surface 확인 전에는 승인할 수 없다.
- User approval: `not yet requested for execution`
