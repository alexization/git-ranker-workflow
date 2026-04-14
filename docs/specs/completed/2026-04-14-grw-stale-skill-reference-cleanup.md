# 2026-04-14-grw-stale-skill-reference-cleanup

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

최근 제거된 local skill을 전제로 남아 있던 stale skill-specific reference를 workflow policy, project-local skill, recent spec artifact에서 제거한다.

## Problem

직전 docs/skill 정리에서 특정 local skill 존재를 전제로 한 explicit reference가 여러 문서에 남아 있다. 현재 repo-local skill registry에는 해당 skill이 없으므로, 그 문구가 source of truth와 맞지 않는 stale reference가 됐다.

## Goals

- workflow policy와 local skill에서 제거된 skill을 전제로 쓴 direct reference를 제거한다.
- spec-first, thin-layer, canonical ownership 같은 일반 규칙은 유지한다.
- 직전 completed spec artifact에서도 stale reference를 걷어낸다.

## Non-goals

- request-routing / Socratic SDD stage 구조 자체 재설계
- repo 밖 global skill 또는 다른 저장소 수정
- 일반적인 planning/spec-first 원칙 삭제

## Socratic Clarification Log

### Round 1
- Prompted gap: 사용자가 지우라고 한 범위가 전체 alignment 변경인지, stale skill reference cleanup인지 먼저 잠겨야 했다.
- Why it mattered: 전체 alignment를 되돌리면 canonical owner, thin-layer 정리까지 같이 사라져 범위가 과도하게 커진다.
- User answer / evidence:
  - 사용자 요청은 제거된 local skill을 전제로 남아 있는 명시 문구를 지워 달라는 것이었다.
  - 현재 grep 결과는 skill-specific direct reference가 policy, skill, recent spec artifact에만 남아 있고, thin-layer / canonical owner 정리는 별도 축으로 남아 있다.
- Closed gap: 이번 작업은 stale skill-specific reference cleanup으로 한정한다.
- Remaining blocker: 없음

## Assumptions And Constraints

- 해당 local skill removal은 이미 완료된 사실로 본다.
- skill 삭제와 무관한 `spec-first`, `Approved spec`, `thin-layer` 규칙은 유지한다.
- stale reference 제거 대상에는 직전 untracked completed spec도 포함한다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `no`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `.codex/skills/README.md`
  - `.codex/skills/request-intake/`
  - `.codex/skills/socratic-spec-authoring/`
  - `docs/specs/active/2026-04-14-grw-stale-skill-reference-cleanup.md`
  - `docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `docs/specs/completed/2026-04-14-grw-stale-skill-reference-cleanup.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-14-grw-stale-skill-reference-cleanup.md`
- Explicitly forbidden:
  - sibling app repo changes
  - repo 밖 global skill edits
  - removed skill cleanup과 무관한 workflow rule rollback
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- repo-local docs/skills에서 제거된 skill을 직접 지칭한 stale reference가 제거된다.
- thin-layer, canonical owner, spec-first 같은 일반 규칙은 유지된다.
- recent completed spec artifact가 현재 cleanup 결과와 모순되지 않게 정리된다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - targeted stale-reference negative grep over workflow policy, selected local skills, and the recent completed spec
  - `sed -n '1,220p' docs/operations/request-routing-policy.md`
  - `sed -n '1,220p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,220p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' .codex/skills/README.md`
  - `sed -n '1,220p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,240p' docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `default lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- 없음

## Risks Or Open Questions

- 다른 historical artifact에 남아 있는 제거된 skill reference까지 전부 정리할지 여부는 이번 범위 밖이다.

## Approval
- Harness judgment: stale reference cleanup으로 범위를 좁혀도 사용자 요청을 충분히 충족한다.
- User approval: 사용자가 제거된 skill을 근거로 명시 문구 제거를 직접 요청했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - targeted stale-reference negative grep over workflow policy, selected local skills, and the recent completed spec
  - `sed -n '1,220p' docs/operations/request-routing-policy.md`
  - `sed -n '1,220p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,220p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' .codex/skills/README.md`
  - `sed -n '1,220p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,240p' docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `git diff --check`
- Evidence:
  - targeted workflow policy와 local skill에서 removed skill을 직접 지칭하던 stale 문구가 제거됐다.
  - `spec-first`, `Approved spec`, `thin-layer`, canonical owner 정리는 유지됐다.
  - 직전 completed spec도 cleanup 결과와 모순되지 않도록 같이 정리됐다.
- Failure or skipped summary:
  - unrelated historical artifact와 `tool-boundary-matrix.md`의 일반 planning vocabulary는 이번 범위 밖이라 건드리지 않았다.
- Next action: completed

## Final Change Summary

- workflow policy와 selected local skill에서 removed skill-specific direct reference를 제거했다.
- spec-first와 thin-layer 정리는 유지하고, stale direct mention만 걷어냈다.
- recent completed spec artifact도 현재 상태와 맞게 업데이트했다.

## Final User Validation

- 사용자가 제거된 skill을 전제로 명시 문구 삭제를 직접 요청했고, 이번 결과는 그 cleanup 범위만 반영했다.
- 결과적으로 repo-local source of truth와 skill layer에서는 해당 removed skill을 전제로 한 direct reference가 남지 않게 정리됐다.

## Docs Updated

- `docs/operations/request-routing-policy.md`
- `docs/operations/sdd-spec-policy.md`
- `docs/operations/workflow-governance.md`
- `.codex/skills/README.md`
- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/socratic-spec-authoring/SKILL.md`
- `docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
