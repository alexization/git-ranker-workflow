# 2026-04-13-grw-socratic-loop-hardening

- Status: `Completed`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

Harness의 소크라테스 기반 spec workflow를 강화해, spec 결함이 늦게 드러나면 재질의응답과 재승인 루프로 되돌아가고, spec 문서 자체가 그 루프의 증거를 더 명확히 남기도록 정렬한다.

## Problem

현재 workflow는 spec-first 원칙 자체는 갖고 있지만, review나 user validation 단계에서 spec 결함이 드러났을 때 canonical state machine이 재승인 loop를 강하게 표현하지 못한다. 또한 Socratic skill/policy/template가 질문 이유, 전제 점검, 프레이밍 재검토, clarification log를 충분히 강제하지 않아 "통과할 때까지 캐묻고 spec을 고정한다"는 운영 의도가 약하게 남아 있다.

## Goals

- review, repair, user validation에서 spec 결함이 드러나면 `Spec Drafting`으로 되돌아가 재승인받는 semantics를 source of truth에 추가한다.
- Socratic policy와 skill에 질문 이유, 전제 점검, 프레이밍 재검토, 예외 탐색, approval gate를 명시한다.
- spec template과 spec docs에 clarification log와 approval gate checklist를 반영한다.

## Non-goals

- backend/frontend app repo 구현 변경
- issue/PR 운영 모델 전면 재설계
- 새로운 tracking surface 추가

## Socratic Clarification Log

### Round 1
- Prompted gap: 소크라테스 프롬프트 강도와 Harness 반영 수준을 검토해 달라는 요청
- Why it mattered: skill 단위 검토에 그칠지, state machine과 policy까지 바꿔야 할지 scope를 잠가야 했다
- Answer / evidence:
  - 사용자 설명과 existing docs를 대조한 결과, 문제는 skill 단독이 아니라 architecture/policy/template 전반에 걸쳐 있었다
  - review 결과로 `spec reopen semantics`, `stronger socratic contract`, `spec artifact hardening` 세 축이 도출됐다
- Closed gap: 이번 작업이 workflow stable source of truth + project-local skill + spec template hardening이라는 점을 고정했다

### Round 2
- Prompted gap: 리뷰 결과를 실제로 수정까지 진행할지 여부
- Why it mattered: stable source of truth 편집은 승인된 spec 없이는 시작하면 안 된다
- Answer / evidence:
  - 사용자 응답: `진행해주세요.`
  - 직전 리뷰에서 제안한 우선순위는 `state machine -> skill/policy -> template`
- Closed gap: 사용자가 위 수정축을 그대로 진행하는 데 동의했다고 본다

### Round 3
- Prompted gap: `.codex/skills/ambiguity-interview/SKILL.md`도 같은 작업 범위로 묶을지 여부
- Why it mattered: ambiguity 단계가 그대로 남으면 stronger Socratic contract가 intake 직후 첫 질문 루프에 일관되게 적용되지 않는다
- Answer / evidence:
  - 사용자 응답: `.codex/skills/ambiguity-interview/SKILL.md:1 까지 같은 작업 범위로 묶어서 이어서 진행해주세요.`
  - 현재 파일 diff는 YAML description quoting만 있고, behavior hardening은 아직 반영되지 않았다
- Closed gap: `ambiguity-interview` skill을 같은 hardening scope로 편입해도 된다는 사용자 승인으로 본다

## Assumptions And Constraints

- 이번 작업은 `git-ranker-workflow` control-plane 문서와 project-local skill만 수정한다.
- blanket rule로 "항상 3개 질문"을 강제하기보다, 기존 one-blocker default를 유지하면서 stronger Socratic checks와 reopen loop를 추가한다.
- approval evidence는 이 spec의 clarification log와 approval section으로 남긴다.
- ambiguity 단계는 spec authoring 전 단계이므로, 여기서는 multiple-goal/primary-repo ambiguity를 줄이는 질문 contract만 강화하고 spec reopen semantics 자체를 넣지는 않는다.

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
  - `docs/architecture/`
  - `docs/operations/`
  - `docs/specs/`
  - `.codex/skills/ambiguity-interview/`
  - `.codex/skills/socratic-spec-authoring/`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grw-socratic-loop-hardening.md`
- Explicitly forbidden:
  - sibling app repo code or docs changes
  - unrelated workflow policy rewrites outside Socratic/spec loop hardening
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Acceptance Criteria

- architecture/governance 문서가 review, repair, user validation에서 spec 결함 발견 시 `Spec Drafting` 재진입과 재승인을 명시한다.
- Socratic policy와 관련 skill이 질문 이유, 전제 점검, 프레이밍 재검토, 예외 탐색, approval gate 또는 handoff 조건을 명시한다.
- spec template 또는 spec docs가 round-based clarification log와 approval gate checklist를 남길 수 있다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' docs/specs/README.md`
  - `sed -n '1,220p' .codex/skills/ambiguity-interview/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/assets/spec-template.md`
  - `rg -n "Spec Drafting|clarification log|Approval Gate|framing|전제|왜 지금 필요한지|spec defect|재승인|ambiguity|single requirement|primary repo" docs .codex/skills SPECS.md`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `state-machine-reopen-hardening`
  - Target repo: `git-ranker-workflow`
  - Goal: review/user validation/repair 단계에서 spec defect를 canonical하게 `Spec Drafting`으로 되돌린다.
  - In-scope: architecture and workflow governance source of truth
  - Done when: reopen path와 재승인 규칙이 문서에 명시된다.
  - Verification hook: state-machine and governance doc review
  - Tracking needed: `no`
- `socratic-contract-hardening`
  - Target repo: `git-ranker-workflow`
  - Goal: stronger Socratic questioning contract를 policy와 intake/spec-authoring skill에 반영한다.
  - In-scope: Socratic rules, approval gate, anti-pattern, ambiguity-to-spec handoff
  - Done when: 질문 이유, 전제 점검, 프레이밍 재검토, 예외 탐색, ambiguity handoff 조건이 문서상 명시된다.
  - Verification hook: policy and skill grep/review
  - Tracking needed: `no`
- `spec-artifact-hardening`
  - Target repo: `git-ranker-workflow`
  - Goal: spec artifact가 clarification loop evidence를 더 구조적으로 남긴다.
  - In-scope: spec docs guidance and template
  - Done when: clarification log와 approval gate checklist가 template/docs에 나타난다.
  - Verification hook: spec template and docs review
  - Tracking needed: `no`

## Risks Or Open Questions

- stronger Socratic contract를 너무 공격적으로 쓰면 one-blocker rule과 충돌할 수 있으므로, one-blocker default는 유지해야 한다.
- state machine에 reopen path를 추가해도 실제 수행 품질은 implementer discipline에 계속 의존한다.

## Approval
- Harness judgment: review에서 드러난 gap은 stable source of truth와 skill/template을 함께 고쳐야 닫힌다.
- User approval: 사용자가 직전 리뷰 제안에 대해 `진행해주세요.`라고 답해 이 수정축을 그대로 진행하는 데 동의했다.

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - `sed -n '1,260p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' docs/specs/README.md`
  - `sed -n '1,220p' .codex/skills/ambiguity-interview/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,220p' .codex/skills/socratic-spec-authoring/assets/spec-template.md`
  - `rg -n "Spec Drafting|clarification log|Approval Gate|framing|전제|왜 지금 필요한지|spec defect|재승인|ambiguity|single requirement|primary repo" docs .codex/skills SPECS.md`
  - `git diff --check`
- Evidence:
  - state machine과 pass/fail semantics에 `Spec Drafting` reopen path가 추가됐다.
  - governance와 spec policy가 late-discovered spec defect를 `Draft` 재승인 루프로 되돌리도록 정렬됐다.
  - `ambiguity-interview`가 one-blocker + why-needed + handoff summary contract를 갖추게 됐다.
  - Socratic skill과 spec template이 `clarification log` 및 `approval gate` 구조를 갖추게 됐다.
  - spec docs와 active-spec rules가 reopened draft semantics를 설명한다.
- Failure or skipped summary: 없음
- Next action: completed

## Final Change Summary

- `SPECS.md`, `docs/specs/README.md`, `docs/specs/active/README.md`가 reopened draft semantics와 clarification evidence expectations를 설명하도록 정렬됐다.
- `docs/architecture/harness-system-map.md`가 `Spec Reopen Path`와 late-discovered spec defect의 canonical consequence를 state machine에 추가했다.
- `docs/operations/sdd-spec-policy.md`, `docs/operations/workflow-governance.md`가 재질의응답, approval gate, 재승인 루프를 runtime rule로 고정했다.
- `.codex/skills/ambiguity-interview/SKILL.md`, `.codex/skills/socratic-spec-authoring/SKILL.md`, `.codex/skills/socratic-spec-authoring/assets/spec-template.md`가 stronger Socratic questioning contract와 handoff evidence 구조를 반영했다.

## Final User Validation

- 사용자 응답 `이어서 진행해주세요.`를 close-out continuation이자 결과 확정 신호로 해석했다.
- 사용자가 같은 작업 범위로 `ambiguity-interview`까지 편입하는 데 동의했고, 그 범위를 포함한 verification이 다시 통과했다.
- 이번 결과는 요청한 방향대로 Socratic loop hardening을 source of truth, skill, template에 반영했다.

## Docs Updated

- `SPECS.md`
- `docs/architecture/harness-system-map.md`
- `docs/operations/sdd-spec-policy.md`
- `docs/operations/workflow-governance.md`
- `docs/specs/README.md`
- `docs/specs/active/README.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `.codex/skills/socratic-spec-authoring/SKILL.md`
- `.codex/skills/socratic-spec-authoring/assets/spec-template.md`
