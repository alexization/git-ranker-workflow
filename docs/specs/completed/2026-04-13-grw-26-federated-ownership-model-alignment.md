# 2026-04-13-grw-26-federated-ownership-model-alignment

- Status: `Completed`
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

### Round 2
- Prompted gap: workflow-only slice로 바로 실행 가능한지, 그리고 exact touched doc set과 tracking 필요 여부가 무엇인지
- Why it mattered: sibling repo draft spec을 기다리지 않고도 control-plane ownership vocabulary를 먼저 잠글 수 있어야 했다
- User answer / evidence:
  - current user request는 이 spec 작업을 지금 진행하라고 명시한다
  - `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`, `.codex/skills/README.md`가 이미 control-plane boundary와 skill ownership의 stable surface다
  - `docs/specs/active/2026-04-13-grw-27-federated-repo-handoff-contract.md`, `docs/specs/active/2026-04-13-grb-05-backend-gc-baseline-alignment.md`, `docs/specs/active/2026-04-13-grc-06-frontend-gc-baseline-alignment.md`는 federated ownership model을 downstream input으로 참조한다
- Closed gap: exact touched doc set은 두 architecture 문서와 skill README, 그리고 current spec이며, 이 작업은 `workflow 문서 수정`으로 self-contained하게 실행한다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: 없음
- 이 spec은 downstream repo-local spec이 재사용할 stable ownership vocabulary를 먼저 고정한다.
- 이 spec은 control-plane 문서와 workflow-local skill만 다룬다.
- app repo 구현은 follow-up spec/PR에서만 다룬다.

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
  - `docs/architecture/control-plane-map.md`
  - `docs/architecture/harness-system-map.md`
  - `.codex/skills/README.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-26-federated-ownership-model-alignment.md`
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
  - `sed -n '1,240p' .codex/skills/README.md`
  - `rg -ni "federated ownership|ownership matrix|thin layer|thin-layer|no-duplication|canonical source" docs/architecture .codex/skills`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `ownership-boundary-definition`
  - Target repo: `git-ranker-workflow`
  - Goal: workflow와 app repo 책임 경계를 stable source of truth로 잠근다.
  - In-scope: ownership matrix, no-duplication rule, migration exit criteria
  - Done when: control-plane 문서가 federated ownership model을 일관되게 설명한다.
  - Verification hook: doc review + `rg`
  - Tracking needed: `no`
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
- Harness judgment: exact touched doc set, task type, verification contract, tracking decision이 모두 잠겨 workflow-only docs slice로 실행 가능하다.
- User approval: current user request가 이 spec의 실행을 직접 요청했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/architecture/control-plane-map.md`
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,240p' .codex/skills/README.md`
  - `rg -ni "federated ownership|ownership matrix|thin layer|thin-layer|no-duplication|canonical source" docs/architecture .codex/skills`
  - `git diff --check`
- Evidence:
  - `docs/architecture/control-plane-map.md`가 federated ownership matrix, no-duplication rule, migration exit criteria를 명시한다.
  - `docs/architecture/harness-system-map.md`가 workflow thin-layer invariant와 repo entrypoint handoff boundary를 명시한다.
  - `.codex/skills/README.md`가 workflow-local skill을 stage procedure와 handoff 중심 thin layer로 제한한다.
  - diff scope는 spec write scope 안에 머물렀고 formatting issue는 없었다.
- Failure or skipped summary: 없음
- Next action: completed

## Final Change Summary

- `docs/architecture/control-plane-map.md`에 federated ownership matrix를 추가해 workflow control plane ownership, repo-local ownership, 금지 ownership을 한 표로 잠갔다.
- 같은 문서에 no-duplication rule과 migration exit criteria를 추가해 workflow가 sibling repo canonical source를 다시 복제하지 않도록 명시했다.
- `docs/architecture/harness-system-map.md`에 federated thin-layer invariant를 추가해 workflow 문서와 skill이 handoff boundary까지만 소유한다고 고정했다.
- `.codex/skills/README.md`에 thin-layer rule을 추가해 workflow-local skill이 repo-specific implementation knowledge의 stable home이 되지 않도록 정렬했다.
- current spec의 approval gate, write scope, tracking decision, verification evidence를 현재 실행 결과에 맞춰 닫았다.

## Final User Validation

- 사용자는 구현 요약과 verification 결과를 공유받은 뒤 `진행해주세요.`라고 답해 close-out continuation을 요청했다.
- 이번 작업은 workflow 문서 정렬 작업이므로, 추가 수정 요청 없이 close-out을 진행해도 된다는 user validation로 해석한다.

## Docs Updated

- `docs/architecture/control-plane-map.md`
- `docs/architecture/harness-system-map.md`
- `.codex/skills/README.md`
- `docs/specs/completed/2026-04-13-grw-26-federated-ownership-model-alignment.md`
