# 2026-04-07-grw-21-same-model-reviewer-pool

- Issue ID: `GRW-21`
- GitHub Issue: `#50`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-21-same-model-reviewer-pool`
- Task Slug: `2026-04-07-grw-21-same-model-reviewer-pool`

## Problem

현재 `dual-agent review` 정책은 implementer와 reviewer를 분리해야 한다는 원칙까지는 고정했지만, 외부 reviewer runtime이 MCP timeout에 취약할 때 어떤 구조를 기본값으로 써야 하는지는 잠겨 있지 않았다.

이 공백이 남아 있으면 independent review가 환경 실패에 묶여 실행되지 않거나, implementer가 임시로 reviewer 역할까지 겸하는 self-approval drift가 생길 수 있다. 같은 base model을 쓰더라도 세션, 컨텍스트, 역할 프롬프트, output ownership을 분리한 reviewer pool을 공식 runtime으로 인정해야 review stage가 실제로 운영된다.

## Why Now

사용자는 이미 implementer와 reviewer를 worker로 분리하려 했고, 현재 병목은 review quality 기준이 아니라 외부 reviewer runtime의 timeout 실패였다. 따라서 하네스는 "다른 모델"보다 "독립된 세션과 컨텍스트를 가진 reviewer"를 핵심 통제로 다시 정의해야 했다.

현재 Codex 환경은 sub-agent 세션을 제공하므로, 같은 모델을 쓰더라도 세션 격리와 역할 프롬프트 분리만 지키면 reviewer pool을 바로 운영할 수 있다. 이 구조를 source of truth에 반영해야 이후 review handoff와 pilot issue도 같은 기본값을 따른다.

## Scope

- same-model multi-agent reviewer pool 허용 조건을 정의한다.
- reviewer role taxonomy와 prompt/input boundary를 정의한다.
- multi-reviewer verdict aggregation과 close-out 규칙을 정의한다.
- 관련 architecture/operations/product hook을 같은 의미로 정렬한다.
- 이번 작업 자체를 Codex sub-agent independent review evidence로 close-out한다.

## Non-scope

- 외부 MCP timeout 인프라 자체의 수정
- backend/frontend 앱 코드 변경
- 완전 자동 PR review bot 구현
- verification contract 전면 재설계
- `.codex/skills/` 신규 skill 작성

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-07-grw-21-same-model-reviewer-pool.md`
  - `.artifacts/2026-04-07-grw-21-same-model-reviewer-pool/` 필요 시
- Explicitly forbidden:
  - sibling app repo code write
  - 외부 reviewer runtime 구현 코드 추가
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음. 문서 작업 범위에서 처리했다.

## Outputs

- same-model reviewer pool semantics를 반영한 review policy
- reviewer role prompt / input boundary / verdict aggregation rule
- architecture/product/governance hook 갱신
- `GRW-21` 실행 기록

## Working Decisions

- 이번 작업의 primary context pack은 `workflow-docs`다.
- stable source of truth에는 특정 vendor명을 박지 않고 `same-model`, `session-isolated`, `role-prompted reviewer pool` vocabulary로 일반화한다.
- review isolation의 핵심은 모델 종류가 아니라 세션, 컨텍스트, 역할 프롬프트, output ownership 분리다.
- reviewer는 read-only 분석과 verdict만 담당하고, implementer는 findings를 받아 repair를 수행한다.
- reviewer pool을 쓰더라도 최종 verdict vocabulary는 기존 `approved`, `changes-requested`, `blocked`를 유지한다.

## Verification

- `gh issue view --repo alexization/git-ranker-workflow 50 --json body,title,number`
  - 결과: Issue `#50` 본문이 줄바꿈과 섹션을 유지한 채 생성된 것을 확인했다.
- `sed -n '1,240p' docs/operations/dual-agent-review-policy.md`
  - 결과: same-model reviewer pool 허용 조건, reviewer isolation model, reviewer pool mode, verdict aggregation, review evidence rule이 한 문서에 정리된 것을 확인했다.
- `sed -n '70,170p' docs/operations/workflow-governance.md`
  - 결과: evidence minimum, reviewer pool canonical verdict, reviewer handoff fan-out, same-model reviewer guardrail이 반영된 것을 확인했다.
- `sed -n '287,310p' docs/operations/verification-contract-registry.md`
  - 결과: reviewer handoff surface가 single reviewer와 reviewer pool 모두에 동일하게 적용되고, final verdict owner의 revision alignment 책임이 반영된 것을 확인했다.
- `sed -n '20,120p' docs/architecture/harness-system-map.md`
  - 결과: reviewer component와 role separation invariant가 reviewer pool aggregation과 output ownership 분리를 반영하는 것을 확인했다.
- `sed -n '1,180p' docs/product/harness-roadmap.md`
  - 결과: roadmap 목표, 고정 결정, phase order가 same-model reviewer pool 기본값을 반영하는 것을 확인했다.
- `sed -n '100,180p' docs/product/work-item-catalog.md`
  - 결과: `GRW-21` work item과 `GRW-S08`의 reviewer-handoff 기본 결정이 현재 정책과 일치하는 것을 확인했다.
- `rg -n "same-model|session-isolated|reviewer pool|role-prompted|role prompt|verdict aggregation|output ownership|reviewer-coordinator" docs/operations/dual-agent-review-policy.md docs/operations/workflow-governance.md docs/operations/verification-contract-registry.md docs/architecture/harness-system-map.md docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
  - 결과: same-model reviewer pool, role-prompted reviewer, output ownership, aggregation vocabulary가 touched hook 전반에 일관되게 grep되는 것을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- independent review
  - 결과: Codex sub-agent reviewer 둘이 각각 `scope-and-governance`, `verification-and-regression` role prompt로 diff와 exec plan을 검토했고 둘 다 `approved` verdict를 남겼다. blocking finding은 없었다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- same-model reviewer pool policy 본문
- architecture/product/governance hook 정렬 결과
- GitHub Issue `#50` body render 확인 결과
- Codex sub-agent independent review evidence

## Independent Review

- Implementer: `Codex`
- Reviewer: `Pascal`
- Additional Reviewers:
  - `verification-and-regression`: `Volta`
- Reviewer Roles / Prompt Focus: `scope-and-governance`, `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/completed/2026-04-07-grw-21-same-model-reviewer-pool.md`
  - Latest verification report: `passed`
  - Diff summary: review policy, governance, verification handoff, architecture, roadmap, catalog에 same-model session-isolated reviewer pool semantics 반영
  - Source-of-truth update: `docs/operations/dual-agent-review-policy.md`, `docs/operations/workflow-governance.md`, `docs/operations/verification-contract-registry.md`, `docs/architecture/harness-system-map.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`
  - Remaining risks / skipped checks: reviewer-handoff skill은 아직 별도 구현되지 않았고, 이번 작업은 policy/source-of-truth 정렬까지만 수행
- Review Verdict: `approved`
- Findings / Change Requests:
  - blocking finding 없음
- Evidence:
  - `Pascal`은 scope/governance 관점에서 scope/write-scope alignment가 유지되고, same-model reviewer pool wording이 self-approval drift를 허용하지 않는다고 확인했다.
  - `Volta`는 verification/regression 관점에서 reviewer minimum context, handoff surface, aggregation rule이 기존 `approved | changes-requested | blocked` semantics를 깨지 않는다고 확인했다.

## Risks or Blockers

- same-model reviewer pool을 허용하더라도 실제 skill이나 운영 습관이 implementer/reviewer 세션을 섞어 쓰면 문서만으로 drift를 완전히 막을 수는 없다.
- reviewer 수와 역할을 과도하게 고정하면 문서 작업처럼 위험 표면이 작은 이슈에도 review cost가 과도해질 수 있다.
- future `reviewer-handoff` skill이 이번 policy를 thin layer로 재사용하지 않으면 runtime semantics가 다시 분기될 수 있다.

## Next Preconditions

- `GRW-S08`은 same-model reviewer pool fan-out과 aggregation을 thin layer skill로 재현해야 한다.
- `GRW-18` pilot issue는 이번 policy와 evidence rule을 실제 close-out에 적용해야 한다.

## Docs Updated

- `docs/operations/dual-agent-review-policy.md`
- `docs/operations/workflow-governance.md`
- `docs/operations/verification-contract-registry.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/2026-04-07-grw-21-same-model-reviewer-pool.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 대신 후속 `reviewer-handoff` 또는 review-loop skill이 그대로 재사용할 수 있도록 same-model reviewer pool의 최소 규칙과 evidence를 source of truth로 먼저 고정했다.
