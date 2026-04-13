# 2026-04-13-grw-product-to-spec-migration

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

`docs/product`에 남아 있는 로드맵과 작업 카탈로그를 제거하고, 그 안의 남은 work item을 `docs/specs/active/`의 draft spec으로 승격해 SDD 기준의 단일 요구사항 surface로 정렬한다.

## Problem

현재 Harness에는 `docs/product/`와 `docs/specs/`가 동시에 남아 있어 pending work의 source of truth가 둘로 갈라져 있다. 이 상태에서는 작업이 spec authoring이 아니라 roadmap/catalog에서 출발하는 것처럼 읽힐 수 있다.

## Goals

- `docs/product`의 pending work를 개별 draft spec으로 투영한다.
- 상위 workflow 목표와 문서 경계를 architecture/operations/spec docs에 흡수한다.
- `docs/product`를 제거하고 spec-first 구조만 남긴다.
- 기존 active spec과 새 draft spec이 함께 remaining work를 설명하도록 정렬한다.

## Non-goals

- 새로 생성하는 draft spec을 이번 turn에서 바로 `Approved`로 올리거나 구현까지 진행하는 것
- sibling app repo 코드나 문서를 실제로 수정하는 것
- `docs/specs/` 밖에 별도 backlog/roadmap/catalog surface를 새로 만드는 것

## Socratic Clarification Log

### Round 1
- Prompted gap: `docs/product`를 없앤 뒤 남은 work item을 어떤 canonical surface로 보존할지
- Why it mattered: 단순 삭제만 하면 remaining requirement와 dependency 정보가 함께 사라진다
- User answer / evidence:
  - 사용자는 `product에 명시되어있는 작업들을 새로운 요구사항으로 두고 스펙 정의부터 시작해서 작업을 수행할 수 있도록` 정리해 달라고 요청했다
  - existing policy는 spec 하나를 canonical working artifact로 두고 별도 planning 문서 중복을 금지한다
- Closed gap: 남은 work item은 개별 draft spec으로 승격하고, 별도 roadmap/catalog은 남기지 않는다

### Round 2
- Prompted gap: roadmap에 있던 상위 목표와 순서를 어디에 남길지
- Why it mattered: product 제거 후에도 control-plane 목적과 sequencing semantics는 stable source of truth에서 읽을 수 있어야 한다
- User answer / evidence:
  - `docs/architecture/`와 `docs/operations/`는 이미 control-plane 책임과 runtime rule을 소유한다
  - sequencing은 각 draft spec의 prerequisite와 상태로 표현할 수 있다
- Closed gap: 상위 목표는 architecture/operations/spec docs로 흡수하고, 남은 순서는 draft spec dependency로 남긴다
- Remaining blocker: seeded draft spec의 초기 상태와 approval semantics를 explicit하게 잠가야 한다

### Round 3
- Prompted gap: actual Socratic question loop 없이 이 spec을 `Approved`/`Completed`로 닫아도 되는지
- Why it mattered: user validation에서 드러난 process defect는 current policy상 `Draft` 재오픈과 재승인을 요구한다
- User answer / evidence:
  - 사용자는 `이 작업을 하면서 단 한번도 소크라테스 프롬프트를 돌리지 않은것 같은데 맞아 ?`라고 지적했다
  - 이어서 `그러면 진행해줘.`라고 답해 reopen loop를 실제로 진행하라고 요청했다
- Closed gap: 이 spec은 user validation에서 process defect가 확인돼 `Draft`로 재오픈한다
- Remaining blocker: pending item을 seed draft로 두는 semantics를 explicit하게 승인받아야 한다

### Round 4
- Prompted gap: `docs/product`에서 옮긴 7개 남은 항목을 모두 future execution용 seeded `Draft` spec으로만 유지해도 되는지
- Why it mattered: 이 결정이 잠겨야 `docs/product` 제거 뒤 남는 canonical planning surface와 approval semantics를 닫을 수 있다
- User answer / evidence:
  - 사용자는 `네`라고 답해 7개 pending item을 seeded `Draft` spec queue로 두는 방향을 승인했다
- Closed gap: remaining item은 모두 seeded `Draft` spec으로 유지하고, 실제 착수 시 각 spec을 다시 소크라테스 loop로 `Approved`까지 올린다
- Remaining blocker: 없음

## Assumptions And Constraints

- 기존 active spec `GRB-04`, `GRB-06`, `GRW-PR82-review-feedback`는 그대로 유지한다.
- 새로 추가하는 spec은 requirement seed이므로 `Draft` 상태로 남기고, future execution 시 별도의 Socratic clarification과 사용자 승인으로 `Approved`로 올린다.
- 이번 작업의 primary context pack은 `workflow-docs`다.

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
  - `AGENTS.md`
  - `docs/README.md`
  - `docs/architecture/`
  - `docs/operations/`
  - `docs/specs/`
  - `.codex/skills/README.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-product-to-spec-migration.md`
- Explicitly forbidden:
  - sibling app repo code or docs edits
  - `docs/specs/` 밖 새 planning/backlog surface 추가
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- `docs/product`의 pending work가 existing active spec 또는 new draft spec으로 모두 투영된다.
- stable source of truth가 `docs/product` 없이 spec-first planning surface를 설명한다.
- `docs/specs/README.md`와 `docs/specs/active/README.md`가 draft spec이 remaining requirement를 대체한다는 점을 설명한다.
- `docs/product/` 디렉터리가 제거된다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `test ! -d docs/product && echo removed`
  - `find docs/specs -maxdepth 2 -type f | sort`
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,220p' docs/README.md`
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' docs/specs/README.md`
  - `sed -n '1,220p' docs/specs/active/README.md`
  - `sed -n '1,220p' .codex/skills/README.md`
  - `rg -n "docs/product|harness-roadmap|work-item-catalog" AGENTS.md docs/README.md docs/architecture docs/operations docs/specs/README.md docs/specs/active/README.md .codex/skills/README.md`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `seed-draft-specs`
  - Target repo: `git-ranker-workflow`
  - Goal: former `docs/product/work-item-catalog.md`의 pending item을 개별 draft spec으로 승격한다.
  - In-scope: draft spec 생성, prerequisite와 provisional write scope 이관
  - Done when: remaining pending item마다 active draft spec이 존재한다.
  - Verification hook: `find docs/specs -maxdepth 2 -type f | sort`
  - Tracking needed: `no`
- `source-of-truth-realignment`
  - Target repo: `git-ranker-workflow`
  - Goal: root/architecture/operations/spec 문서에서 planning surface를 spec-first로 재정렬한다.
  - In-scope: `docs/product` 참조 제거, spec registry semantics 추가
  - Done when: stable source of truth가 `docs/product` 없이도 same intent를 설명한다.
  - Verification hook: `sed` review, negative `rg`
  - Tracking needed: `no`
- `product-surface-removal`
  - Target repo: `git-ranker-workflow`
  - Goal: obsolete `docs/product/` tree를 제거한다.
  - In-scope: directory file deletion
  - Done when: `docs/product/`가 더 이상 존재하지 않는다.
  - Verification hook: negative `rg`, `find docs -maxdepth 2 -type f | sort`
  - Tracking needed: `no`

## Risks Or Open Questions

- draft spec을 seed로만 남기기 때문에 각 작업의 final write scope와 verification contract는 future approval loop에서 더 좁혀질 수 있다.

## Approval
- Harness judgment: `docs/product` 제거는 remaining work를 seeded `Draft` spec으로 먼저 투영할 때 안전하게 닫을 수 있다.
- User approval: 사용자가 `네`라고 답해 7개 pending item을 seeded `Draft` spec queue로 유지하는 semantics를 승인했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `test ! -d docs/product && echo removed`
  - `find docs/specs -maxdepth 2 -type f | sort`
  - `sed -n '1,220p' AGENTS.md`
  - `sed -n '1,220p' docs/README.md`
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' docs/specs/README.md`
  - `sed -n '1,220p' docs/specs/active/README.md`
  - `sed -n '1,220p' .codex/skills/README.md`
  - `rg -n "docs/product|harness-roadmap|work-item-catalog" AGENTS.md docs/README.md docs/architecture docs/operations docs/specs/README.md docs/specs/active/README.md .codex/skills/README.md`
  - `git diff --check`
- Evidence:
  - `docs/product/` directory가 제거됐다.
  - `docs/specs/active/`에 pending work를 대체하는 seeded draft spec 7건이 추가됐다.
  - root/architecture/operations/spec/skill docs가 `docs/specs/active/`의 draft/approved spec을 remaining work surface로 설명한다.
  - stable source of truth 경로에서는 `docs/product`, `harness-roadmap`, `work-item-catalog` 참조가 남지 않았다.
- Failure or skipped summary: 없음
- Next action: completed

## Final Change Summary

- `docs/product`의 roadmap/catalog 내용을 개별 draft spec으로 승격했다.
- `AGENTS.md`, `docs/README.md`, architecture/governance/spec/skill docs를 spec-first planning surface 기준으로 재정렬했다.
- `docs/product/` 디렉터리를 제거했다.
- user validation에서 드러난 process defect를 반영해 spec을 재오픈했고, seeded draft semantics에 대한 explicit approval 뒤 다시 close-out 했다.

## Final User Validation

- 사용자는 process defect 지적 뒤 reopen loop를 요청했고, 마지막 blocker 질문에 `네`라고 답해 seeded draft semantics를 승인했다.
- 이번 결과는 그 승인에 맞춰 remaining work를 `docs/specs/active/`의 draft spec queue로 유지하고 별도 product surface를 제거한 상태로 닫혔다.

## Docs Updated

- `AGENTS.md`
- `docs/README.md`
- `docs/architecture/control-plane-map.md`
- `docs/architecture/harness-system-map.md`
- `docs/operations/workflow-governance.md`
- `docs/specs/README.md`
- `docs/specs/active/README.md`
- `.codex/skills/README.md`
- `docs/specs/active/2026-04-13-grw-26-federated-ownership-model-alignment.md`
- `docs/specs/active/2026-04-13-grw-27-federated-repo-handoff-contract.md`
- `docs/specs/active/2026-04-13-grc-05-frontend-verification-contract-normalization.md`
- `docs/specs/active/2026-04-13-grb-07-backend-agents-entrypoint-bootstrap.md`
- `docs/specs/active/2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap.md`
- `docs/specs/active/2026-04-13-grb-05-backend-gc-baseline-alignment.md`
- `docs/specs/active/2026-04-13-grc-06-frontend-gc-baseline-alignment.md`
- `docs/specs/completed/2026-04-13-grw-product-to-spec-migration.md`
