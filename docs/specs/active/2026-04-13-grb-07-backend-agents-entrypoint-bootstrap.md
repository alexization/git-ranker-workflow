# 2026-04-13-grb-07-backend-agents-entrypoint-bootstrap

- Status: `Draft`
- Primary Repo: `git-ranker`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

backend repo가 `AGENTS.md` entrypoint와 backend-only knowledge bootstrap surface를 repo-local canonical source로 노출하도록 정리한다.

## Problem

workflow가 federated handoff를 하더라도 backend repo 자체의 entrypoint와 backend-only skill/bootstrap surface가 부족하면 구현 단계의 first source가 여전히 workflow로 역류할 수 있다.

## Goals

- backend repo의 `AGENTS.md` entrypoint requirement를 충족시킨다.
- backend-only knowledge bootstrap surface를 repo-local로 내린다.
- verification entry docs와의 연결을 정리한다.

## Non-goals

- workflow repo의 control-plane 정책 재설계
- backend production feature 변경
- frontend repo 수정

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRB-07`을 spec-first requirement로 남길 방법
- Why it mattered: backend repo-local ownership bootstrap이 사라지면 `GRW-27` 이후 실제 handoff destination이 비게 된다
- User answer / evidence:
  - current user request는 product의 task를 새 요구사항으로 남기라고 한다
  - former catalog entry는 backend entry docs, `.codex/skills/`, verification entry docs를 권장 write scope로 제시했다
- Closed gap: `GRB-07`은 backend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 actual backend entry docs 범위와 bootstrap minimum을 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: `GRB-04`, `GRW-27`
- backend-only implementation knowledge는 workflow가 아니라 `git-ranker`가 소유한다.
- repo-local bootstrap은 verification contract와 충돌하지 않아야 한다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `actual backend entry docs`, `bootstrap minimum`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker`
- Allowed write paths:
  - `AGENTS.md`
  - `README.md`
  - `.codex/skills/`
  - verification entry docs directly referenced by the approved slice
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grb-07-backend-agents-entrypoint-bootstrap.md`
- Explicitly forbidden:
  - frontend repo edits
  - unrelated backend production code changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- backend repo가 `AGENTS.md` entrypoint를 canonical source로 노출한다.
- backend-only knowledge bootstrap surface가 workflow 밖으로 이동한다.
- verification entry docs와 bootstrap linkage가 문서화된다.

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
- `backend-entrypoint-definition`
  - Target repo: `git-ranker`
  - Goal: backend repo의 `AGENTS.md`와 entry docs requirement를 정의하고 적용한다.
  - In-scope: entrypoint wording, backend-only source list
  - Done when: workflow handoff가 backend repo entrypoint를 first source로 가리킨다.
  - Verification hook: entry doc review
  - Tracking needed: `conditional`
- `backend-bootstrap-surface-alignment`
  - Target repo: `git-ranker`
  - Goal: backend-only skill/bootstrap surface를 repo-local ownership에 맞춰 정리한다.
  - In-scope: `.codex/skills/`, verification entry docs alignment
  - Done when: workflow repo가 backend implementation knowledge를 다시 들고 있지 않다.
  - Verification hook: doc/skill review + declared verification commands
  - Tracking needed: `no`

## Risks Or Open Questions

- repo-local bootstrap을 너무 넓게 잡으면 thin-layer handoff contract와 경계가 다시 흐려질 수 있다.

## Approval
- Harness judgment: draft seed는 적절하지만, backend repo entry docs 실사를 거친 뒤에만 승인할 수 있다.
- User approval: `not yet requested for execution`
