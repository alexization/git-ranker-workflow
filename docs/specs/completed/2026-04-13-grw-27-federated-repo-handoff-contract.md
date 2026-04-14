# 2026-04-13-grw-27-federated-repo-handoff-contract

- Status: `Completed`
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

### Round 2
- Prompted gap: exact minimum handoff artifact, repo bootstrap checklist depth, tracking 여부
- Why it mattered: 이 셋이 잠기지 않으면 workflow가 repo-local knowledge를 다시 복제하거나, 반대로 handoff가 너무 얇아서 다음 source가 비게 된다
- User answer / evidence:
  - `docs/architecture/control-plane-map.md`는 runtime entrypoint and knowledge를 workflow ownership surface로 정의하고, target repo discovery order와 handoff minimum을 workflow가 소유한다고 적는다
  - `docs/architecture/harness-system-map.md`는 state transition이 repo entrypoint에서 멈추고, repo-local verification/bootstrap은 sibling repo가 소유한다고 고정한다
  - `docs/architecture/context-pack-registry.md`와 `docs/operations/verification-contract-registry.md`는 impacted repo entry doc 또는 공식 remote source 확인이 planning verification의 일부임을 고정한다
  - local `../git-ranker/README.md`와 remote `alexization/git-ranker-client` source를 확인한 결과, 두 repo 모두 `AGENTS.md`는 아직 없고 frontend `README.md`는 기본 템플릿 상태라서 contract는 current implementation guide가 아니라 repo-local bootstrap minimum이어야 한다
- Closed gap: handoff summary minimum, discovery order, target repo `AGENTS.md` requirement, bootstrap gap handling, tracking 불필요 결정이 architecture source로 잠겼다
- Remaining blocker: `none`

### Round 3
- Prompted gap: target repo root `README.md`가 bootstrap checklist에서 concrete entry surface까지 책임져야 하는지 여부
- Why it mattered: root `README.md`에 entrypoint responsibility를 실으면 repo-local ownership 경계가 다시 흐려지고, 실제 repo bootstrap 방향과도 어긋난다
- User answer / evidence:
  - target repo의 root `README.md`에는 단순한 프로젝트 설명만 둔다
- Closed gap: root `README.md`는 overview-only surface로 두고, concrete entrypoint responsibility는 `AGENTS.md`와 named entry docs가 소유한다고 contract를 수정한다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: `GRW-26`
- workflow는 target repo에 필요한 최소 handoff만 남긴다.
- target repo bootstrap 실제 적용은 repo-local spec에서 닫는다.
- local worktree가 없는 impacted repo는 official remote source로 entrypoint 상태를 확인할 수 있다.
- target repo root `README.md`는 overview-only surface일 수 있고, entrypoint detail은 `AGENTS.md` 또는 named entry docs가 소유한다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `yes`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/architecture/README.md`
  - `docs/architecture/control-plane-map.md`
  - `docs/architecture/context-pack-registry.md`
  - `docs/architecture/harness-system-map.md`
  - `docs/architecture/repo-handoff-contract.md`
  - `docs/specs/`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-27-federated-repo-handoff-contract.md`
- Explicitly forbidden:
  - sibling app repo bootstrap execution
  - sibling app repo code or docs edits
  - repo-local implementation guide나 command inventory를 workflow에서 복제하는 것
- Network / external systems:
  - impacted repo entrypoint 상태 확인을 위한 GitHub remote source read-only inspection
- Escalation triggers:
  - 없음

## Acceptance Criteria

- target repo `AGENTS.md` requirement와 handoff summary shape가 문서화된다.
- local skill discovery order가 control-plane 기준으로 정렬된다.
- repo bootstrap checklist가 follow-up repo-local work와 연결되고, root `README.md`는 overview-only requirement로 유지된다.

## Verification
- Contract profile: `cross-repo-planning`
- Commands:
  - `sed -n '1,260p' docs/architecture/repo-handoff-contract.md`
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/architecture/context-pack-registry.md`
  - impacted repo entry doc 또는 official remote source 확인
  - `rg -n "handoff|AGENTS.md|bootstrap|entrypoint|local skill|repo-handoff-contract" docs/architecture docs/specs`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `no`

## Detailed Subtasks
- `handoff-contract-definition`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow-to-repo handoff summary의 minimum shape를 고정한다.
  - In-scope: handoff summary fields, local skill discovery order
  - Done when: Implementer가 target repo entrypoint로 안전하게 넘겨질 수 있다.
  - Verification hook: architecture/operations doc review
  - Tracking needed: `no`
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
- Harness judgment: handoff summary minimum, bootstrap checklist depth, contract profile, tracking decision이 모두 잠겨 cross-repo planning slice로 바로 실행 가능하다.
- User approval: current user request가 이 spec의 실행을 직접 요청했다.

## Verification Summary

- Contract profile: `cross-repo-planning`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/architecture/repo-handoff-contract.md`
  - `sed -n '1,220p' docs/architecture/control-plane-map.md`
  - `sed -n '1,220p' docs/architecture/harness-system-map.md`
  - `sed -n '1,220p' docs/architecture/context-pack-registry.md`
  - `test -f ../git-ranker/AGENTS.md && echo present || echo missing`
  - `sed -n '1,80p' ../git-ranker/README.md`
  - GitHub fetch `alexization/git-ranker-client:README.md`
  - GitHub fetch `alexization/git-ranker-client:AGENTS.md`
  - GitHub fetch `alexization/git-ranker-client:package.json`
  - `rg -n "handoff|AGENTS.md|bootstrap|entrypoint|local skill|repo-handoff-contract" docs/architecture docs/specs`
  - `git diff --check`
- Evidence:
  - `docs/architecture/repo-handoff-contract.md`가 handoff summary minimum, discovery order, local skill order, target repo `AGENTS.md` requirement, bootstrap gap handling을 stable source로 고정했다.
  - root `README.md`는 overview-only이고 concrete entrypoint는 `AGENTS.md`와 named entry docs가 소유한다는 correction을 반영했다.
  - `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`, `docs/architecture/context-pack-registry.md`, `docs/architecture/README.md`가 새 contract 문서를 existing architecture surface에서 발견 가능하게 연결했다.
  - local backend worktree 기준 `../git-ranker/AGENTS.md`는 아직 없고 `README.md`만 존재해 `GRB-07`이 bootstrap gap close-out을 계속 소유한다는 점이 확인됐다.
  - remote `alexization/git-ranker-client` 기준 `AGENTS.md`는 404이고 `README.md`는 기본 Next.js 템플릿, `package.json`은 verification entry surface로 존재해 `GRC-07`이 entrypoint/bootstrap 정렬을 계속 소유한다는 점이 확인됐다.
  - `git diff --check`가 통과해 formatting issue는 없었다.
- Failure or skipped summary: 없음
- Next action: completed

## Final Change Summary

- `docs/architecture/repo-handoff-contract.md`를 추가해 workflow-to-repo handoff minimum을 전용 stable source로 분리했다.
- 같은 문서에 handoff summary field, target repo discovery order, local skill discovery rule, target repo `AGENTS.md` requirement, bootstrap gap handling을 고정했고 root `README.md`를 overview-only로 낮췄다.
- `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`, `docs/architecture/context-pack-registry.md`, `docs/architecture/README.md`에서 새 contract 문서를 canonical hook으로 연결했다.
- current spec의 blocker를 source evidence로 닫고 `cross-repo-planning` verification contract, tracking `no`, network boundary를 명시했다.

## Final User Validation

- 사용자는 `GRW-27를 진행해주세요.`라고 요청해 현재 docs-only planning slice의 실행과 close-out continuation을 직접 승인했다.
- 이후 `target repo에 root README.md 에는 단순히 프로젝트 설명밖에 없을거야.`라고 clarification을 남겨 README expectation correction을 직접 닫았다.
- 이번 결과는 workflow stable source 정렬 작업이라 추가 runtime validation surface가 없고, repo-local follow-up은 `GRB-07`, `GRC-07`에서 이어서 닫는다.

## Docs Updated

- `docs/architecture/README.md`
- `docs/architecture/control-plane-map.md`
- `docs/architecture/context-pack-registry.md`
- `docs/architecture/harness-system-map.md`
- `docs/architecture/repo-handoff-contract.md`
- `docs/specs/completed/2026-04-13-grw-27-federated-repo-handoff-contract.md`
