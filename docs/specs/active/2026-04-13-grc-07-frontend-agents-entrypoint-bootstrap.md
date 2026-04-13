# 2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap

- Status: `Draft`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend repo가 `AGENTS.md` entrypoint와 frontend-only knowledge bootstrap surface를 repo-local canonical source로 노출하도록 정리한다.

## Problem

frontend repo가 자체 entrypoint와 bootstrap surface를 충분히 갖추지 못하면 workflow에서 내려보낸 handoff가 다시 workflow 문서 의존으로 되돌아간다. 이러면 federated ownership model이 frontend track에서 실제로 작동하지 않는다.

## Goals

- frontend repo의 `AGENTS.md` entrypoint requirement를 충족시킨다.
- frontend-only knowledge surface를 repo-local로 내린다.
- verification entry docs와 bootstrap linkage를 정리한다.

## Non-goals

- backend repo 수정
- frontend feature 구현
- workflow control-plane 정책 재설계

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-07`을 spec-first requirement로 보존할 방법
- Why it mattered: `GRC-05`와 `GRW-27` 뒤에 이어질 frontend bootstrap task가 product 제거와 함께 사라지면 안 된다
- User answer / evidence:
  - current user request는 product의 task를 새 요구사항으로 남기라고 요구한다
  - former catalog entry는 frontend entry docs, `.codex/skills/`, verification entry docs를 권장 write scope로 제시했다
- Closed gap: `GRC-07`은 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 actual frontend entry docs와 bootstrap minimum을 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: `GRC-05`, `GRW-27`
- frontend-only knowledge surface는 `git-ranker-client`가 소유한다.
- repo-local bootstrap은 frontend verification contract와 일관돼야 한다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `actual frontend entry docs`, `bootstrap minimum`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker-client`
- Allowed write paths:
  - `AGENTS.md`
  - `README.md`
  - `.codex/skills/`
  - verification entry docs directly referenced by the approved slice
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap.md`
- Explicitly forbidden:
  - backend repo edits
  - unrelated frontend route or UI changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- frontend repo가 `AGENTS.md` entrypoint를 canonical source로 노출한다.
- frontend-only knowledge bootstrap surface가 workflow 밖으로 이동한다.
- verification entry docs와 bootstrap linkage가 문서화된다.

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
- `frontend-entrypoint-definition`
  - Target repo: `git-ranker-client`
  - Goal: frontend repo의 `AGENTS.md`와 entry docs requirement를 정의하고 적용한다.
  - In-scope: entrypoint wording, frontend-only source list
  - Done when: workflow handoff가 frontend repo entrypoint를 first source로 가리킨다.
  - Verification hook: entry doc review
  - Tracking needed: `conditional`
- `frontend-bootstrap-surface-alignment`
  - Target repo: `git-ranker-client`
  - Goal: frontend-only bootstrap surface를 repo-local ownership에 맞춰 정리한다.
  - In-scope: `.codex/skills/`, verification entry docs alignment
  - Done when: workflow repo가 frontend implementation knowledge를 다시 들고 있지 않다.
  - Verification hook: doc/skill review + declared verification commands
  - Tracking needed: `no`

## Risks Or Open Questions

- frontend repo entrypoint가 실제 codebase 구조와 맞지 않으면 approval 단계에서 subtask split이 더 필요할 수 있다.

## Approval
- Harness judgment: draft seed는 확보됐지만, frontend repo entrypoint 실사 전에는 approval gate를 닫지 않는다.
- User approval: `not yet requested for execution`
