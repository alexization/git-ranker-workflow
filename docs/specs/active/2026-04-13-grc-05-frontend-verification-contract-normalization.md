# 2026-04-13-grc-05-frontend-verification-contract-normalization

- Status: `Draft`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend repo의 verification surface를 repo-local canonical source 기준으로 정규화한다.

## Problem

workflow의 상위 verification semantics는 고정돼 있지만, frontend repo는 아직 자신의 build/lint/typecheck surface와 환경 전제를 repo-local verification contract로 충분히 잠그지 못했다. 이 상태에서는 workflow와 repo-local validation의 경계가 흐려진다.

## Goals

- frontend verification surface를 repo-local canonical source 기준으로 정리한다.
- build/lint/typecheck entrypoint와 환경 전제를 명시한다.
- 결과 해석 기준과 remaining risk를 기록한다.

## Non-goals

- 새 기능 구현
- frontend route or UI behavior 변경
- frontend CI 전면 재설계

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-05`를 spec-first workflow 안에 보존할 방법
- Why it mattered: frontend track의 prerequisite가 사라지면 후속 `GRC-07`, `GRC-06`의 출발점이 없어진다
- User answer / evidence:
  - current user request는 product의 task를 새로운 요구사항으로 전환하라고 명시한다
  - former catalog entry는 frontend 검증 문서, build/lint/typecheck entrypoint 정리를 핵심 작업으로 남겼다
- Closed gap: `GRC-05`는 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact frontend entrypoint와 environment precondition을 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: 없음
- workflow는 상위 verification semantics만 고정하고, repo-local command surface는 `git-ranker-client`가 소유한다.
- repo-local canonical source 확인 없이는 `Approved`로 올리지 않는다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `exact entrypoints`, `environment assumptions`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker-client`
- Allowed write paths:
  - `README.md`
  - `package.json`
  - `docs/`
  - `.github/workflows/`
  - verification entry docs and config files directly touched by the approved slice
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grc-05-frontend-verification-contract-normalization.md`
- Explicitly forbidden:
  - backend repo changes
  - unrelated frontend feature work
- Network / external systems:
  - package registry or declared verification endpoint only when future verification requires it
- Escalation triggers:
  - sandbox가 frontend verification command를 막을 때만

## Acceptance Criteria

- frontend verification contract가 repo-local canonical source에서 읽힌다.
- build/lint/typecheck command와 환경 전제가 문서화된다.
- verification 결과 해석 기준과 remaining risk가 기록된다.

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
- `frontend-verification-surface-inventory`
  - Target repo: `git-ranker-client`
  - Goal: current build/lint/typecheck surface와 환경 전제를 inventory한다.
  - In-scope: repo-local entry docs, scripts, config surface 확인
  - Done when: verification contract 초안에 필요한 command set이 잠긴다.
  - Verification hook: entry doc and script review
  - Tracking needed: `no`
- `repo-local-contract-normalization`
  - Target repo: `git-ranker-client`
  - Goal: workflow semantics와 충돌하지 않는 frontend verification contract를 repo-local 문서에 정리한다.
  - In-scope: verification doc wording, remaining risk 기록
  - Done when: 후속 frontend spec이 같은 contract를 재사용할 수 있다.
  - Verification hook: declared commands + doc review
  - Tracking needed: `conditional`

## Risks Or Open Questions

- 실제 frontend repo의 current script surface를 읽으면 command set이나 config path가 더 좁아질 수 있다.

## Approval
- Harness judgment: draft seed는 충분하지만, repo-local canonical source 확인 전에는 approval gate를 닫을 수 없다.
- User approval: `not yet requested for execution`
