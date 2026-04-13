# 2026-04-13-grw-27-federated-repo-handoff-contract

- Status: `Draft`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

workflow가 target repo에 넘겨야 하는 최소 handoff contract를 정의하고, 각 repo의 `AGENTS.md` entrypoint requirement를 고정한다.

## Problem

federated ownership model을 실제 runtime handoff로 연결하려면 workflow가 무엇을 넘기고 무엇을 넘기지 않는지, 그리고 각 repo가 어떤 entrypoint를 반드시 노출해야 하는지가 필요하다. 이 contract가 없으면 cross-repo planning 뒤 구현 단계의 first source가 흔들린다.

## Goals

- target repo `AGENTS.md` requirement를 정의한다.
- handoff summary shape와 local skill discovery order를 고정한다.
- repo bootstrap checklist를 정리한다.

## Non-goals

- backend/frontend repo에서 실제 bootstrap 수행
- app repo 코드 변경
- workflow 밖 새로운 orchestration surface 추가

## Socratic Clarification Log

### Round 1
- Prompted gap: removed product catalog의 `GRW-27`을 실행 가능한 spec seed로 보존할 방법
- Why it mattered: `GRW-26` 뒤에 이어질 concrete handoff requirement가 사라지면 federation transition이 중간에서 끊긴다
- User answer / evidence:
  - current user request는 product의 남은 작업을 spec 정의부터 시작할 수 있게 남기라고 요구한다
  - former catalog entry는 `AGENTS.md` requirement, handoff summary shape, local skill discovery order, repo bootstrap checklist를 기본 결정으로 담고 있었다
- Closed gap: `GRW-27`을 workflow-docs draft spec으로 승격한다
- Remaining blocker: approval 시점에 handoff artifact shape와 repo bootstrap checklist의 exact minimum을 더 좁혀야 한다

## Assumptions And Constraints

- Prerequisites before approval: `GRW-26`
- workflow는 target repo에 필요한 최소 handoff만 남긴다.
- target repo bootstrap 실제 적용은 repo-local spec에서 닫는다.

## Approval Gate
- Problem and goal locked: `seeded`
- Non-goals explicit: `seeded`
- Primary repo and write scope locked: `partial`
- Verification method locked: `partial`
- Subtask split decided: `seeded`
- Tracking decision locked: `not yet`
- Remaining blockers: `minimum handoff artifact`, `repo bootstrap checklist depth`, `tracking 여부`

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/architecture/`
  - `docs/operations/`
  - `docs/specs/`
  - `.codex/skills/`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grw-27-federated-repo-handoff-contract.md`
- Explicitly forbidden:
  - sibling app repo bootstrap execution
  - repo-local implementation guide를 workflow에서 복제하는 것
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- target repo `AGENTS.md` requirement와 handoff summary shape가 문서화된다.
- local skill discovery order가 control-plane 기준으로 정렬된다.
- repo bootstrap checklist가 follow-up repo-local work와 연결된다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `rg -n "handoff|AGENTS.md|bootstrap|entrypoint|local skill" docs .codex/skills`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `conditional`
- PR needed: `conditional`

## Detailed Subtasks
- `handoff-contract-definition`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow-to-repo handoff summary의 minimum shape를 고정한다.
  - In-scope: handoff summary fields, local skill discovery order
  - Done when: Implementer가 target repo entrypoint로 안전하게 넘겨질 수 있다.
  - Verification hook: architecture/operations doc review
  - Tracking needed: `conditional`
- `repo-bootstrap-requirement-definition`
  - Target repo: `git-ranker-workflow`
  - Goal: repo가 노출해야 하는 `AGENTS.md`와 bootstrap checklist requirement를 정리한다.
  - In-scope: checklist wording, repo-local follow-up linkage
  - Done when: backend/frontend follow-up spec이 같은 contract를 참조할 수 있다.
  - Verification hook: `AGENTS.md` + related doc review
  - Tracking needed: `no`

## Risks Or Open Questions

- handoff contract를 너무 두껍게 정의하면 `GRW-26`의 thin-layer 원칙과 충돌할 수 있다.

## Approval
- Harness judgment: requirement seed는 확보됐지만, approval 전에 exact checklist와 field shape를 더 잠가야 한다.
- User approval: `not yet requested for execution`
