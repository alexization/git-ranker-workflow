# 2026-04-14-grw-socratic-skill-policy-alignment

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

Harness workflow가 SDD와 소크라테스식 spec 정의를 중심으로 동작하도록, 기존 policy 문서와 project-local skill 사이의 역할 중복과 충돌을 검토하고 Socratic spec authoring을 약화시키는 내용을 제거한다.

## Problem

현재 workflow는 큰 방향에서 `request-intake -> ambiguity-interview -> socratic-spec-authoring` 흐름을 갖고 있지만, policy와 skill이 같은 규칙을 여러 번 재서술하고 있어 drift 여지가 있다.

## Goals

- workflow policy에서 route 결정, ambiguity 축소, Socratic spec authoring의 canonical owner를 더 분명히 적는다.
- project-local skill을 thin-layer 원칙에 맞게 줄여 policy 재서술을 최소화한다.
- `api-contract-sync`를 spec authoring 단계와 분리된 implementation/contract-sync stage로 명확히 둔다.

## Non-goals

- `request-intake`, `ambiguity-interview`, `socratic-spec-authoring` 세 stage 자체를 제거하거나 합치기
- backend/frontend sibling repo 코드나 문서 수정
- global `~/.codex/skills/` 자산 자체 수정
- verification/review/publish lane 전체를 재설계

## Socratic Clarification Log

### Round 1
- Prompted gap: 중복을 줄일 때 skill stage를 합칠지, thin-layer로 남길지를 먼저 잠가야 했다.
- Why it mattered: stage 삭제까지 들어가면 request routing과 spec authoring state machine 자체를 다시 설계해야 해서 작업 범위가 달라진다.
- User answer / evidence:
  - 사용자 요청은 `ambiguity-interview`, `api-contract-sync`, `request-intake` 등 기존 skill과 policy의 겹침이나 방해 요소를 검토하고 제거해 달라는 것이었다.
  - 현재 canonical docs와 completed spec을 읽은 결과, stage 분리 자체보다 policy/skill의 중복 서술이 더 직접적인 문제였다.
- Closed gap: 이번 작업은 stage 유지, canonical ownership 명확화, thin-layer skill 정리, Socratic 방해 문구 제거로 한정한다.
- Remaining blocker: 없음

## Assumptions And Constraints

- user request 자체를 범위 승인 신호로 보고, 별도 parent issue 없이 docs/skills 정리까지 한 번의 workflow-docs loop로 닫는다.
- project-local skill은 policy를 대체하지 않고 stage handoff와 최소 workflow만 설명해야 한다.
- global skill conflict가 보이더라도 이번 변경은 workflow repo 안의 source of truth와 project-local skill에서 먼저 방어선을 세운다.

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
  - `docs/operations/`
  - `docs/specs/active/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `.codex/skills/README.md`
  - `.codex/skills/request-intake/`
  - `.codex/skills/ambiguity-interview/`
  - `.codex/skills/socratic-spec-authoring/`
  - `.codex/skills/api-contract-sync/`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
- Explicitly forbidden:
  - sibling app repo code or docs changes
  - global `~/.codex/skills/` edits
  - unrelated workflow/runtime rewrites outside skill-policy alignment
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- workflow policy가 route 결정, ambiguity interview, Socratic spec authoring의 경계를 분명히 설명한다.
- `request-intake`, `ambiguity-interview`, `socratic-spec-authoring`가 thin-layer 원칙에 맞게 policy 재서술을 줄인다.
- `api-contract-sync`가 intake/spec authoring 단계와 겹치지 않는 implementation-side contract sync skill로 설명된다.
- skill registry 또는 related README가 위 경계와 ownership을 반영한다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,260p' docs/operations/request-routing-policy.md`
  - `sed -n '1,280p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,320p' docs/operations/workflow-governance.md`
  - `sed -n '1,240p' .codex/skills/README.md`
  - `sed -n '1,220p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,220p' .codex/skills/ambiguity-interview/SKILL.md`
  - `sed -n '1,260p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,220p' .codex/skills/api-contract-sync/SKILL.md`
  - `rg -n "thin-layer|canonical owner|canonical source|request-intake|ambiguity-interview|socratic-spec-authoring|api-contract-sync" docs/operations .codex/skills -g '*.md'`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `default lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `policy-boundary-alignment`
  - Target repo: `git-ranker-workflow`
  - Goal: route, ambiguity, Socratic spec authoring 경계를 canonical policy에 명시한다.
  - In-scope: `docs/operations/`
  - Done when: workflow policy가 각 stage의 canonical owner와 forbidden overlap을 설명한다.
  - Verification hook: policy `sed` review and grep
  - Tracking needed: `no`
- `skill-thin-layer-refactor`
  - Target repo: `git-ranker-workflow`
  - Goal: intake-related skill과 contract sync skill 설명을 thin-layer 원칙에 맞게 정리한다.
  - In-scope: `.codex/skills/README.md`, selected SKILL.md files
  - Done when: skill이 policy를 길게 복제하지 않고 stage goal, inputs, outputs, handoff만 남긴다.
  - Verification hook: skill `sed` review and grep
  - Tracking needed: `no`

## Risks Or Open Questions

- skill을 너무 짧게 줄이면 trigger 품질이 떨어질 수 있으므로 description은 유지하고 본문만 lean하게 줄여야 한다.

## Approval
- Harness judgment: current problem은 stage model 자체보다 canonical policy와 skill 간 중복에 가깝다.
- User approval: 사용자가 overlap과 Socratic 방해 요소를 검토하고 제거해 달라고 직접 요청했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/operations/request-routing-policy.md`
  - `sed -n '1,280p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,320p' docs/operations/workflow-governance.md`
  - `sed -n '1,240p' .codex/skills/README.md`
  - `sed -n '1,220p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,220p' .codex/skills/ambiguity-interview/SKILL.md`
  - `sed -n '1,260p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,220p' .codex/skills/api-contract-sync/SKILL.md`
  - `rg -n "thin-layer|canonical owner|canonical source|request-intake|ambiguity-interview|socratic-spec-authoring|api-contract-sync" docs/operations .codex/skills -g '*.md'`
  - `git diff --check`
- Evidence:
  - `request-routing-policy.md`가 route/handoff 전용 canonical owner 범위를 명시하고, ambiguity 단계에서 spec-level detail을 미리 잠그지 못하게 했다.
  - `.codex/skills/README.md`가 policy ownership과 thin-layer rule을 더 구체적으로 적었다.
  - `request-intake`, `ambiguity-interview`, `socratic-spec-authoring`는 policy 재서술을 줄이고 stage goal, handoff, anti-pattern 중심으로 정리됐다.
  - `api-contract-sync`는 approved spec 이후의 contract sync skill로 경계가 고정됐다.
- Failure or skipped summary:
  - global `~/.codex/skills/`는 non-goal이라 직접 수정하지 않았다.
- Next action: user validation

## Final Change Summary

- workflow policy에 route 결정, Socratic spec contract, runtime governance의 canonical owner를 분리해서 적었다.
- repo-local skill registry와 intake/spec-authoring skill을 thin-layer 원칙에 맞게 줄였다.
- `api-contract-sync`를 intake/spec authoring과 겹치지 않는 후행 contract-sync skill로 재정의했다.

## Final User Validation

- 사용자 요청은 role overlap과 Socratic 방해 요소를 검토하고 제거하라는 직접적인 실행 요청이었다.
- 이번 결과는 stage 자체를 없애지 않고, policy를 canonical source로 두고 skill을 thin-layer handoff로 줄이는 방향으로 그 요청을 반영했다.

## Docs Updated

- `docs/operations/request-routing-policy.md`
- `docs/operations/sdd-spec-policy.md`
- `docs/operations/workflow-governance.md`
- `.codex/skills/README.md`
- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `.codex/skills/socratic-spec-authoring/SKILL.md`
- `.codex/skills/api-contract-sync/SKILL.md`
