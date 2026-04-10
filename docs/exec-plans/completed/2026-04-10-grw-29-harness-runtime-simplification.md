# 2026-04-10-grw-29-harness-runtime-simplification

- Issue ID: `GRW-29`
- GitHub Issue: `not created in this session`
- GitHub PR: `not created`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `develop`
- Task Slug: `2026-04-10-grw-29-harness-runtime-simplification`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

현재 Harness workflow source of truth는 간단한 작업에도 issue, exec plan, context pack, boundary check, sub-agent review, feedback close-out을 거의 공통 게이트처럼 요구하고 있었다.

이 상태에서는 실제 변경이 작아도 implementer가 무엇을 왜 하는지보다 절차를 채우는 시간이 더 길어지고, 특히 pre-PR sub-agent review와 draft PR 기본 흐름이 runtime을 과도하게 늘렸다. 사용자가 원하는 것은 critical path에 직접 기여하지 않는 단계를 줄이고, 기본 happy path를 `spec/구현 -> 검증 -> open PR`로 단순화하는 것이다.

## Why Now

기존 정책은 `GRW-20`, `GRW-21`, `GRW-22`, `GRW-25`를 거치며 review/publish discipline을 강화했지만, 그 결과 non-critical 문서 작업과 작은 수정에도 같은 무게의 절차가 붙는 drift가 생겼다.

지금 이 단계를 정리하지 않으면 이후 workflow 작업마다 review runtime, draft 공유, feedback close-out이 계속 기본값으로 남고, 사용자가 요구한 "빠르게 구현하고 검증한 뒤 open PR publish" 운영 방식으로 수렴하지 못한다.

## Scope

- 현재 workflow source of truth에서 runtime을 무겁게 만드는 단계를 재분석하고 기본 happy path를 단순화한다.
- `default lane`과 `guarded lane`을 분리해 non-critical 작업의 기본 진입 비용을 낮춘다.
- `implement -> verify -> open PR`를 canonical publish order로 고정한다.
- independent review, reviewer pool, feedback close-out을 trigger-based optional step으로 재정의한다.
- 관련 operations, architecture, product, skill 문서와 historical snapshot을 갱신한다.

## Non-scope

- GitHub issue 생성 또는 backlog 재분해
- backend/frontend app repo 코드 변경
- reviewer runtime 또는 CI 구현 추가
- 기존 active exec plan을 소급해서 새 policy로 rewrite

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/`
  - `.codex/skills/`
  - `docs/exec-plans/completed/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-10-grw-29-harness-runtime-simplification.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - unrelated backlog reshaping
  - GitHub publish metadata rewrite
- Network / external systems:
  - 없음
- Escalation triggers:
  - 없음

## Outputs

- runtime simplification과 lane split를 반영한 workflow governance
- post-verification open PR publish order
- optional review / optional feedback semantics
- 관련 skill과 architecture/product hook 정렬
- `GRW-29` completed historical snapshot

## Working Decisions

- 이번 작업의 primary repo와 task type은 `git-ranker-workflow` / `workflow 문서 수정`으로 고정한다.
- simple scoped work는 issue + exec plan을 universal prerequisite로 두지 않고 `task brief` 기반 `default lane`으로 바로 실행할 수 있게 한다.
- higher-risk work만 `guarded lane`에서 issue, exec plan, context pack, boundary check를 강하게 요구한다.
- canonical publish order는 `implement -> verify -> open PR`로 고정하고, draft PR은 사용자 명시 요청일 때만 허용한다.
- independent review와 feedback close-out은 기본 happy path가 아니라 risk signal, failure, user request가 있을 때만 실행한다.

## Verification

- `sed -n '1,260p' docs/operations/workflow-governance.md`
  - 결과: `Runtime Simplification Principles`, lane split, `implement -> verify -> open PR publish`, draft PR 예외 규칙이 반영된 것을 확인했다.
- `sed -n '1,240p' docs/operations/request-routing-policy.md`
  - 결과: immediate executable task가 `default lane`과 `guarded lane`으로 분기되고 `task brief` 종료 shape가 추가된 것을 확인했다.
- `sed -n '1,260p' docs/operations/dual-agent-review-policy.md`
  - 결과: review가 open PR 이후 필요할 때만 실행되는 optional path로 재정의되고 reviewer pool이 high-risk trigger로 한정된 것을 확인했다.
- `sed -n '1,240p' docs/operations/failure-to-guardrail-feedback-loop.md`
  - 결과: feedback close-out이 failure-driven optional step으로 축소된 것을 확인했다.
- `sed -n '1,240p' docs/architecture/harness-system-map.md`
  - 결과: state machine이 `default happy path`와 `guarded path`를 분리해 표현하는 것을 확인했다.
- `sed -n '1,220p' docs/product/harness-roadmap.md`
  - 결과: fixed decisions와 roadmap wording이 simplified runtime과 publish order에 맞게 정렬된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/README.md`
  - 결과: skill registry가 `review when needed`, `publish after verification` 기준으로 갱신된 것을 확인했다.
- `sed -n '1,200p' .codex/skills/request-intake/SKILL.md`
  - 결과: request intake가 `default`/`guarded` lane 선택을 직접 잠그도록 갱신된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/reviewer-handoff/SKILL.md`
  - 결과: reviewer handoff가 open PR 이후 필요 시점에만 사용되는 thin step으로 축소된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/publish-after-review/SKILL.md`
  - 결과: legacy skill name과 무관하게 canonical timing이 `verification -> open PR publish -> optional review`로 설명되는 것을 확인했다.
- `rg -n "default lane|guarded lane|task brief|open PR|draft PR|optional review|optional feedback" docs/operations docs/architecture docs/product .codex/skills`
  - 결과: simplification 핵심 용어가 touched source-of-truth와 skill 문서 전반에서 함께 grep되는 것을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.

## Evidence

- workflow governance의 lane split와 publish order 변경
- request routing, review policy, feedback policy의 optional-step 정렬
- architecture/product/skill hook 일관성
- `git diff --check` 결과

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - scope는 workflow source-of-truth simplification과 skill/hook alignment에 한정한다.
  - GitHub issue, PR, independent reviewer runtime은 이번 턴의 required output이 아니다.
- Command: `sed -n '1,260p' docs/operations/workflow-governance.md`
  - Status: `passed`
  - Evidence: runtime simplification 원칙과 `implement -> verify -> open PR` 순서가 문서 상단 기본 규칙으로 고정됐다.
- Command: `sed -n '1,240p' docs/operations/request-routing-policy.md`
  - Status: `passed`
  - Evidence: immediate execution path가 `task brief` 기반 `default lane`을 허용한다.
- Command: `sed -n '1,260p' docs/operations/dual-agent-review-policy.md`
  - Status: `passed`
  - Evidence: independent review는 universal gate가 아니라 risk-based optional step으로 정리됐다.
- Command: `sed -n '1,240p' docs/operations/failure-to-guardrail-feedback-loop.md`
  - Status: `passed`
  - Evidence: feedback close-out이 failure-driven trigger로 축소됐다.
- Command: `sed -n '1,240p' docs/architecture/harness-system-map.md`
  - Status: `passed`
  - Evidence: default happy path와 guarded path state machine이 새 운영 규칙과 일치한다.
- Command: `sed -n '1,220p' docs/product/harness-roadmap.md`
  - Status: `passed`
  - Evidence: roadmap fixed decisions가 simplified publish/runtime 기준으로 갱신됐다.
- Command: `sed -n '1,220p' .codex/skills/README.md`
  - Status: `passed`
  - Evidence: skill registry 설명이 optional review와 post-verification publish를 따른다.
- Command: `sed -n '1,200p' .codex/skills/request-intake/SKILL.md`
  - Status: `passed`
  - Evidence: intake skill이 default/guarded lane 결정을 직접 수행한다.
- Command: `sed -n '1,220p' .codex/skills/reviewer-handoff/SKILL.md`
  - Status: `passed`
  - Evidence: reviewer handoff가 "review가 실제로 필요할 때"만 쓰이는 최소 handoff로 정리됐다.
- Command: `sed -n '1,220p' .codex/skills/publish-after-review/SKILL.md`
  - Status: `passed`
  - Evidence: legacy naming에도 불구하고 open PR publish가 verification 직후 canonical step으로 정렬됐다.
- Command: `rg -n "default lane|guarded lane|task brief|open PR|draft PR|optional review|optional feedback" docs/operations docs/architecture docs/product .codex/skills`
  - Status: `passed`
  - Evidence: simplification vocabulary가 source-of-truth와 skill layer에 일관되게 반영됐다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: formatting 오류가 없다.
- Failure summary: 없음
- Next action:
  - 이후 workflow 변경은 `default lane`을 기본으로 사용하고, high-risk case만 `guarded lane`으로 승격한다.

## Independent Review

- Not run
- Reason:
  - 이번 작업의 목적 자체가 non-critical 기본 경로에서 universal review tax를 제거하는 것이었고, 현재 diff는 그 기본값 변경을 source of truth에 반영하는 workflow-docs 수정이다.
  - verification과 cross-doc consistency check로 close-out 가능한 범위로 판단했다.

## Risks or Blockers

- 기존 active exec plan이나 open/draft PR은 이 변경으로 자동 재정렬되지 않으므로, 이미 진행 중인 항목에는 과거 규칙 흔적이 남아 있을 수 있다.
- reviewer runtime을 optional로 낮춘 뒤에도 high-risk 작업에서 lane classification이 느슨해지면 review 누락 drift가 생길 수 있다.
- `publish-after-review` 같은 legacy naming은 유지되므로, skill 이름만 보고 옛 순서를 추정하는 오해가 남을 수 있다.

## Next Preconditions

- 새 workflow task를 시작할 때 `request-intake`에서 `default lane`과 `guarded lane`을 먼저 고정한다.
- open PR publish와 review timing이 다시 흔들리는 사례가 나오면 lane classification 또는 publish skill wording만 추가로 보정한다.

## Docs Updated

- `docs/operations/workflow-governance.md`
- `docs/operations/request-routing-policy.md`
- `docs/operations/dual-agent-review-policy.md`
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/verification-contract-registry.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `.codex/skills/README.md`
- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/publish-after-review/SKILL.md`
- `docs/exec-plans/completed/2026-04-10-grw-29-harness-runtime-simplification.md`

## Skill Consideration

- 이번 작업은 새 skill 작성이 아니라 기존 workflow skill의 trigger와 설명을 runtime simplification 기준으로 재정렬하는 범위였다.
- 후속으로 필요한 것은 새 skill 추가보다 lane misclassification이나 publish wording drift가 실제로 다시 발생하는지 관찰하는 것이다.
