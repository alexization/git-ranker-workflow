# harness-spec-approval-gate

- Status: `In Progress`
- Primary Repo: `git-ranker-workflow`
- Related Issue: None
- Related PR: None

## Request Summary

Harness workflow 문서와 관련 skill에 spec 작성과 승인 순서를 더 명시적으로 고정한다. 특히, 소크라테스식 질의응답 루프를 돌며 spec을 세부화하고, Harness가 더 이상 질문이 없다고 판단한 뒤에만 사용자에게 승인 요청을 할 수 있으며, 그때 사용자가 spec에 명시적으로 동의했을 때만 `Approved`로 고정된다는 점을 stable source of truth와 relevant skill handoff에 함께 반영한다.

## Problem

현재 `docs/operations/sdd-spec-policy.md`, `docs/operations/workflow-governance.md`, `.codex/skills/request-intake/SKILL.md`, `.codex/skills/socratic-spec-authoring/SKILL.md`에는 pre-implementation 흐름의 일부가 적혀 있지만, 아래 순서가 policy와 skill 모두에 충분히 직접적으로 반영되어 있지 않다.

- 소크라테스식 질의응답 루프로 spec을 세부화한다.
- Harness가 더 이상 blocker 질문이 없다고 판단할 때까지 loop를 계속한다.
- 그 다음에만 사용자에게 spec approval을 요청한다.
- 사용자가 spec 초안에 명시적으로 동의했을 때만 `Approved`로 고정한다.

이 공백 때문에 작업 요청, spec drafting loop, Harness readiness 판단, approval request, 사용자 명시적 승인 사이의 단계가 실제 실행에서 흐려질 수 있다.

## Goals

- 소크라테스식 질문 루프가 approval request보다 먼저 온다는 순서를 policy에 명시한다.
- Harness가 질문이 더 없다고 판단한 뒤에만 approval request를 할 수 있다는 규칙을 추가한다.
- spec approval은 사용자의 명시적 동의가 있어야만 성립한다는 규칙을 Harness workflow 문서에 직접 추가한다.
- 관련 skill이 같은 순서를 handoff와 anti-pattern에 맞춰 따르도록 갱신한다.
- 작업 요청, spec 초안 작성, Harness readiness 판단, 사용자 approval의 차이를 문서상으로 구분한다.
- 승인 전에는 구현이나 publish로 진행할 수 없다는 runtime rule을 더 분명히 적는다.

## Non-goals

- request routing category를 새로 정의하지 않는다.
- repo-local AGENTS나 backend/frontend app-specific skill은 이번 작업에서 바꾸지 않는다.
- 승인 방식에 새로운 UI, tooling, automation requirement를 추가하지 않는다.

## Socratic Clarification Log

### Round 1
- Prompted gap: 이번 요청이 stable source of truth 문서 수정 작업으로 바로 좁혀지는지 확인해야 했다.
- Why it mattered: session-level 메모로 끝낼지, Harness workflow 문서까지 바꿀지에 따라 primary repo와 write scope가 달라진다.
- User answer / evidence: 사용자가 "이 기준을 이번 세션에서만 유지하는게 아니라, Harness 워크플로우에 명시해줘"라고 명시했다.
- Closed gap: primary repo는 `git-ranker-workflow`이고, 목표는 Harness workflow policy 문서 수정이다.
- Remaining blocker: 없음

### Round 2
- Prompted gap: 질문이 없어도 spec drafting을 시작할 수 있는지, 아니면 요구사항 ambiguity가 남아 있는지 확인해야 했다.
- Why it mattered: blocker가 없으면 draft spec을 쓸 수 있지만, 사용자 approval 전 구현은 금지되어야 한다.
- User answer / evidence: 관련 source of truth인 `docs/operations/sdd-spec-policy.md`와 `docs/operations/workflow-governance.md`를 읽은 결과, 보강할 규칙의 위치와 대상 문서가 이미 보인다.
- Closed gap: draft spec 작성까지는 추가 질문 없이 진행 가능하다.
- Remaining blocker: 사용자 명시적 spec 승인

### Round 3
- Prompted gap: approval gate만이 아니라, 소크라테스식 질의응답 루프를 끝내고 approval request로 넘어가는 정확한 순서를 문서에 넣어야 했다.
- Why it mattered: "사용자 승인 필요"만 적으면 approval request를 언제 해도 되는지 모호해져, 질문 루프가 충분히 닫히기 전에 승인부터 받으려는 잘못된 흐름이 남을 수 있다.
- User answer / evidence: 사용자가 "소크라테스식 질문법을 통해 질의응답을 계속해서 루프를 돌면서 스펙문서를 세부화해나가고 Harness가 판단했을 때 더 이상 질문이 없을 때 승인 요청을 사용자에게 하고, 그때 사용자가 스펙 문서를 동의했을 때 고정"해야 한다고 명시했다.
- Closed gap: policy change는 approval semantics뿐 아니라 `question loop -> Harness no-more-questions judgment -> approval request -> user explicit approval -> Approved` 순서까지 고정해야 한다.
- Remaining blocker: 사용자 명시적 spec 승인

### Round 4
- Prompted gap: 이 핵심 순서를 stable policy 문서에만 둘지, 관련 skill에도 함께 반영할지 범위를 잠가야 했다.
- Why it mattered: policy만 고치고 skill handoff가 예전 표현을 유지하면 실제 실행 단계에서 다시 드리프트가 생길 수 있다.
- User answer / evidence: 사용자가 "이 핵심 순서가 Harness 정책문서, 스킬에 모두 반영되어야합니다."라고 명시했다.
- Closed gap: 이번 작업의 범위는 policy 문서와 관련 workflow-local skill까지 포함한다.
- Remaining blocker: 사용자 명시적 spec 승인

### Round 5
- Prompted gap: draft spec을 실제 문서/skill 수정 단계로 올릴 수 있는지, 즉 사용자 명시적 approval이 확보됐는지 반영해야 했다.
- Why it mattered: approval 전에는 stable source of truth와 relevant skill 수정에 들어가면 안 된다.
- User answer / evidence: 사용자가 "진행해주세요."라고 명시적으로 승인했다.
- Closed gap: 현재 draft spec에 대한 사용자 명시적 approval이 확보됐다.
- Remaining blocker: 없음

## Assumptions And Constraints

- stable source of truth 수정은 `docs/operations/` 문서와 relevant workflow-local skill로 닫는다.
- spec approval에 필요한 사용자 동의는 작업 요청 자체와 구분해서 명시해야 한다.
- 구현 전 approval gate를 지키는 runtime rule과 approval exit condition을 함께 보강하는 것이 필요하다.
- 질문 루프는 blocker 질문이 없어질 때까지 반복될 수 있으며, approval request는 그 이후 단계여야 한다.
- skill은 policy를 대체하지 않고, 동일한 순서를 trigger/handoff/anti-pattern에 맞춰 얇게 반영해야 한다.

## Approval Gate

- Problem and goal locked: Yes
- Non-goals explicit: Yes
- Primary repo and write scope locked: Yes
- Verification method locked: Yes
- Subtask split decided: Yes
- Tracking decision locked: Yes
- Remaining blockers: None

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/sdd-spec-policy.md`
  - `docs/operations/workflow-governance.md`
  - `.codex/skills/request-intake/SKILL.md`
  - `.codex/skills/socratic-spec-authoring/SKILL.md`
  - `.codex/skills/README.md`
  - `docs/specs/active/2026-04-14-harness-spec-approval-gate.md`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-14-harness-spec-approval-gate.md`
- Explicitly forbidden:
  - `docs/architecture/**`
  - `git-ranker/**`
  - `git-ranker-client/**`
- Network / external systems: 없음
- Escalation triggers: 없음

## Acceptance Criteria

- `docs/operations/sdd-spec-policy.md`가 소크라테스식 질의응답 루프를 통해 spec을 세부화하고, Harness가 더 이상 질문이 없다고 판단한 뒤에만 approval request를 한다는 순서를 직접 설명한다.
- `docs/operations/sdd-spec-policy.md`가 작업 요청과 사용자 명시적 spec 승인 사이의 차이를 직접적으로 설명한다.
- `docs/operations/workflow-governance.md`가 구현 시작 전에 필요한 approval gate를 runtime rule로 더 분명히 적는다.
- `.codex/skills/socratic-spec-authoring/SKILL.md`가 question loop, Harness no-more-questions judgment, approval request, user explicit approval의 순서를 handoff에 반영한다.
- `.codex/skills/request-intake/SKILL.md`가 작업 요청을 approval로 오해하지 않고 spec authoring stage handoff까지만 담당한다는 경계를 분명히 한다.
- 필요하면 `.codex/skills/README.md`가 pre-implementation 흐름에서 policy와 skill의 역할 경계를 더 분명히 설명한다.
- 문서 표현은 기존 policy/skill boundary를 깨지 않고 approval semantics만 강화한다.

## Verification

- Contract profile: `docs-policy-diff`
- Commands:
  - `git diff --check -- docs/operations/sdd-spec-policy.md docs/operations/workflow-governance.md .codex/skills/request-intake/SKILL.md .codex/skills/socratic-spec-authoring/SKILL.md .codex/skills/README.md docs/specs/active/2026-04-14-harness-spec-approval-gate.md`
  - `sed -n '1,260p' docs/operations/sdd-spec-policy.md`
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,240p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,260p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,220p' .codex/skills/README.md`
- Latest evidence:
  - `git diff --check -- docs/operations/sdd-spec-policy.md docs/operations/workflow-governance.md .codex/skills/request-intake/SKILL.md .codex/skills/socratic-spec-authoring/SKILL.md .codex/skills/README.md docs/specs/active/2026-04-14-harness-spec-approval-gate.md` -> passed
  - `docs/operations/sdd-spec-policy.md` -> request와 approval 분리, no-more-questions judgment, explicit approval exit condition 반영 확인
  - `docs/operations/workflow-governance.md` -> runtime 순서와 draft-vs-approved execution guard 반영 확인
  - `.codex/skills/request-intake/SKILL.md` -> intake는 approval stage가 아니라는 경계 반영 확인
  - `.codex/skills/socratic-spec-authoring/SKILL.md` -> question loop 후 approval request, explicit approval 후 Approved 고정 순서 반영 확인
  - `.codex/skills/README.md` -> request-intake와 socratic-spec-authoring의 역할 경계 반영 확인

## Delivery And Tracking Plan

- Lane: `default lane`
- Parent issue needed: Yes
- PR needed: Yes

## Detailed Subtasks

1. Draft spec 고정
   - Target repo: `git-ranker-workflow`
   - Goal: 요구사항, write scope, verification을 잠근다.
   - In-scope: active spec 1개
   - Done when: 사용자 approval 대기 상태의 draft spec이 존재한다.
   - Verification hook: spec file 존재와 내용 확인
   - Tracking needed: No

2. Approval semantics 문서 보강
   - Target repo: `git-ranker-workflow`
   - Goal: question loop에서 approval request를 거쳐 `Approved`로 고정되는 순서를 stable source of truth에 더 직접적으로 추가한다.
   - In-scope: `docs/operations/sdd-spec-policy.md`, `docs/operations/workflow-governance.md`
   - Done when: 사용자 승인 후에 문서 수정과 verification이 완료된다.
   - Verification hook: policy diff check
   - Tracking needed: No

3. Relevant skill handoff 보강
   - Target repo: `git-ranker-workflow`
   - Goal: pre-implementation 단계의 workflow-local skill이 같은 순서를 얇게 반영하게 한다.
   - In-scope: `.codex/skills/request-intake/SKILL.md`, `.codex/skills/socratic-spec-authoring/SKILL.md`, 필요 시 `.codex/skills/README.md`
   - Done when: skill 설명이 policy와 충돌하지 않고 같은 gate 순서를 따른다.
   - Verification hook: skill diff check
   - Tracking needed: No

## Risks Or Open Questions

- 사용자 approval 표현을 얼마나 엄격하게 정의할지 문구가 과도하면 작은 직접 요청에서도 운영 마찰이 커질 수 있다.
- request와 approval를 분리하는 표현을 강화하되, blocker 질문이 없는 경우 draft spec 작성까지는 허용된다는 현재 흐름은 유지해야 한다.
- "더 이상 질문이 없다"는 판단이 질문을 영구히 금지하는 뜻이 아니라, 현재 approval gate를 채우기에 충분하다는 뜻임을 문서에서 과도하게 복잡하게 만들지 않고 표현해야 한다.
- skill에 policy 내용을 과하게 복제하면 thin-layer rule을 깨므로, skill은 handoff와 anti-pattern 수준까지만 반영해야 한다.

## Approval

- Harness judgment: 문제, 대상 문서, write scope, verification이 잠겼고 implementation 단계로 진행 가능하다.
- User approval: 2026-04-14 대화에서 현재 draft spec 범위로 진행하라고 명시적으로 승인함
