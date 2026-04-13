# 2026-04-13-grw-26-federated-ownership-model-alignment

- Status: `Draft`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

workflow control plane과 sibling app repo 사이의 federated ownership model을 stable source of truth로 정렬한다.

## Problem

workflow repo가 orchestration만 소유해야 한다는 원칙은 이미 여러 문서에 흩어져 있지만, ownership matrix와 thin-layer 기준이 완전히 잠겨 있지 않다. 이 간극이 남으면 workflow가 repo-local implementation knowledge를 다시 흡수할 위험이 있다.

## Goals

- workflow vs repo-local ownership 경계를 stable source of truth에 명시한다.
- workflow-local skill이 thin layer만 소유해야 한다는 기준을 잠근다.
- migration exit criteria와 no-duplication rule을 정리한다.

## Non-goals

- backend/frontend repo 실제 파일 생성
- repo-local CI나 guardrail 구현
- app source code 수정

## Socratic Clarification Log

### Round 1
- Prompted gap: removed product catalog의 `GRW-26`을 어떤 spec shape로 보존할지
- Why it mattered: product 제거 후에도 ownership alignment requirement가 canonical artifact로 남아야 한다
- User answer / evidence:
  - current user request는 product의 work item을 새 요구사항으로 전환하라고 명시한다
  - former catalog entry는 `ownership matrix`, `workflow-vs-repo 책임 경계`, `thin-layer 기준`, `migration exit criteria`를 핵심 작업으로 제시했다
- Closed gap: `GRW-26`은 workflow-docs draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact touched doc set과 skill 변경 필요 여부를 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: `GRB-04`, `GRC-05`
- 이 spec은 control-plane 문서와 workflow-local skill만 다룬다.
- app repo 구현은 follow-up spec/PR에서만 다룬다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `exact document set`, `approval-time clarification`, `tracking 필요 여부`

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/architecture/`
  - `docs/operations/`
  - `docs/specs/`
  - `.codex/skills/`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grw-26-federated-ownership-model-alignment.md`
- Explicitly forbidden:
  - sibling app repo code or docs edits
  - workflow가 app canonical source를 복제하는 새 문서 추가
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- ownership matrix가 workflow orchestration과 repo-local implementation knowledge를 분리해 설명한다.
- workflow-local skill의 thin-layer 기준이 문서화된다.
- migration exit criteria와 duplication 금지 원칙이 source of truth에 반영된다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `rg -n "ownership|orchestration|repo-local|thin layer|canonical source" docs .codex/skills`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `conditional`
- PR needed: `conditional`

## Detailed Subtasks
- `ownership-boundary-definition`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow와 app repo 책임 경계를 stable source of truth로 잠근다.
  - In-scope: ownership matrix, no-duplication rule, migration exit criteria
  - Done when: control-plane 문서가 federated ownership model을 일관되게 설명한다.
  - Verification hook: doc review + `rg`
  - Tracking needed: `conditional`
- `workflow-skill-thin-layer-alignment`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow-local skill이 orchestration handoff만 남기도록 기준을 정렬한다.
  - In-scope: affected skill registry or wording updates
  - Done when: skill layer가 repo-local implementation knowledge를 소유하지 않는다.
  - Verification hook: `.codex/skills/README.md` and affected skill review
  - Tracking needed: `no`

## Risks Or Open Questions

- ownership 문구를 과하게 일반화하면 후속 `GRW-27` handoff contract의 concrete requirement가 흐려질 수 있다.

## Approval
- Harness judgment: former product catalog를 대체하는 seeded draft spec으로는 충분하지만, implementation 전에는 재질의응답이 더 필요하다.
- User approval: `not yet requested for execution`
