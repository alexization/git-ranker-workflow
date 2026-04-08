# 2026-04-08-grw-25-pre-pr-review-cycle-hardening

- Issue ID: `GRW-25`
- GitHub Issue: `#71`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-25-review-before-pr-publish`
- Task Slug: `2026-04-08-grw-25-pre-pr-review-cycle-hardening`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

stable source of truth는 이미 `independent review -> feedback close-out -> PR publish` 흐름을 가리키고 있다. 하지만 실제 운영에서는 여전히 draft PR을 먼저 만들고 그 위에서 review/repair를 반복하는 drift가 남아 있다.

이 drift의 핵심은 policy의 방향 자체보다, implementer가 publish 직전까지 따라야 할 operational hook이 약하다는 점이다. local skill registry에는 reviewer-handoff 이후 PR publish를 고정하는 thin-layer skill이 없고, governance/review policy도 "PR은 review workspace가 아니라 publish container"라는 메시지를 반복 surface마다 충분히 직접적으로 표현하지 않는다.

## Why Now

사용자가 원하는 기본 검증 사이클은 `implement -> verification -> sub-agent review -> repair loop -> approved -> feedback close-out -> PR publish`다. 이 순서를 기본 동작으로 만들려면, current governance와 review policy를 더 직접적으로 정리하고, local skill layer에도 publish step을 명시해야 한다.

또한 `GRW-20`이 pre-PR review ordering을 source of truth에 반영했는데도 drift가 반복된다는 것은 문서만으로는 implementer handoff가 충분히 operationalize되지 않았다는 뜻이다. 지금 `publish-after-review` thin-layer skill과 관련 registry hook을 추가해야 이후 세션이 draft-first로 다시 흐르지 않는다.

## Scope

- `docs/operations/workflow-governance.md`에 pre-PR review / repair loop / publish ordering을 더 직접적으로 명시한다.
- `docs/operations/dual-agent-review-policy.md`에 PR이 review workspace가 아니며, review/repair loop가 승인 전까지 반복된다는 점을 더 명확히 반영한다.
- 필요 시 `docs/architecture/harness-system-map.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`의 hook을 정렬한다.
- `.codex/skills/publish-after-review/SKILL.md`를 추가하고 `.codex/skills/README.md` registry와 recommended use를 갱신한다.
- `GRW-25` exec plan과 close-out evidence를 남긴다.

## Non-scope

- backend/frontend 앱 코드 변경
- GitHub Actions, branch protection, reviewer auto-assignment 구현
- external reviewer runtime 추가
- merge policy나 post-merge CI gate 재설계
- plugin cache 안 외부 skill 수정

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/`
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`
  - `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`
  - `/tmp/grw-25-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `.github/workflows/`, branch protection, runtime automation 추가
  - plugin cache 또는 repo 밖 skill 수정
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - worktree/branch 분리를 위한 `git worktree add`만 허용

## Outputs

- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `docs/architecture/harness-system-map.md` 필요 시
- `docs/product/harness-roadmap.md` 필요 시
- `docs/product/work-item-catalog.md` 필요 시
- `.codex/skills/publish-after-review/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`

## Working Decisions

- canonical direction 자체는 바꾸지 않고, current policy의 뜻을 더 명확하게 드러내는 hardening으로 제한한다.
- `publish-after-review` skill은 새 policy를 발명하지 않고, `approved review verdict`와 `fixed feedback outcome` 뒤에 open PR을 publish하는 thin layer만 담당한다.
- draft PR은 canonical review surface가 아니라 user request 또는 blocker-sharing exception이라는 점을 문서와 skill에서 같은 vocabulary로 맞춘다.
- plugin cache의 외부 skill은 source of truth가 아니므로 이번 작업에서 직접 수정하지 않는다.

## Verification

- `sed -n '116,180p' docs/operations/workflow-governance.md`
- `sed -n '10,210p' docs/operations/dual-agent-review-policy.md`
- `sed -n '114,121p' docs/architecture/harness-system-map.md`
- `sed -n '20,26p' docs/product/harness-roadmap.md`
- `sed -n '1,260p' docs/product/work-item-catalog.md`
- `sed -n '1,260p' .codex/skills/publish-after-review/SKILL.md`
- `sed -n '1,120p' .codex/skills/reviewer-handoff/SKILL.md`
- `sed -n '1,240p' .codex/skills/README.md`
- `rg -n "publish-after-review|draft PR|review workspace|publish container|independent review를 먼저|approved.*PR|PR 존재 여부|feedback close-out" docs .codex/skills`
- `gh issue view --repo alexization/git-ranker-workflow 71 --json body,title,number`
- `git diff --check`

## Evidence

- governance/review policy wording 정렬 결과
- new publish skill 본문
- registry / roadmap / catalog hook 정렬 결과
- grep 기반 vocabulary consistency
- issue body render 확인 결과

## Risks or Blockers

- feedback close-out과 PR publish의 상대 순서를 잘못 압축하면 기존 `Feedback Pending` semantics와 충돌할 수 있다.
- skill이 policy를 재서술하는 mini policy가 되면 source of truth drift가 생긴다.
- product/architecture hook까지 과도하게 건드리면 단순 hardening 범위를 넘어설 수 있다.

## Next Preconditions

- 없음

## Skill Consideration

이번 이슈의 핵심은 publish 단계 thin-layer skill을 추가해 current policy를 operationalize하는 것이다. 따라서 새 skill은 policy 재정의가 아니라, reviewer-handoff 이후 PR publish를 canonical 순서로 고정하는 최소 surface에 머문다.

## Verification Report

- Overall Status: `passed`
- Verification Time: `2026-04-08`
- Notes:
  - workflow-docs profile 기준 본문/registry/skill hook 정렬을 확인했다.
  - first review에서 나온 `feedback close-out ordering shorthand`와 `verification coverage` finding을 반영해 workflow-governance, `publish-after-review`, exec plan wording을 수리한 뒤 affected command를 다시 실행했다.
  - GitHub issue `#71` body render와 local diff whitespace check를 함께 확인했다.

### Commands

1. `sed -n '116,190p' docs/operations/workflow-governance.md`
   - 결과: PR을 review workspace가 아니라 publish container로 정의하고, `verification -> review -> repair loop -> approved -> feedback close-out -> PR publish` 순서를 명시한 것을 확인했다.
2. `sed -n '10,230p' docs/operations/dual-agent-review-policy.md`
   - 결과: PR 존재 여부가 review 선행조건이 아니고, draft/open PR 생성이 review start signal이 아니며, repair loop를 local artifact 기준으로 닫는 규칙이 반영된 것을 확인했다.
3. `sed -n '114,125p' docs/architecture/harness-system-map.md`
   - 결과: PR projection이 local review/repair close-out 이후 publish container라는 설명으로 정렬된 것을 확인했다.
4. `sed -n '20,40p' docs/product/harness-roadmap.md`
   - 결과: open PR publish 기본값과 draft exception wording, `GRW-25` roadmap entry를 확인했다.
5. `sed -n '1,260p' docs/product/work-item-catalog.md`
   - 결과: `GRW-25` catalog entry와 기본 결정, write scope, verification surface가 추가된 것을 확인했다.
6. `sed -n '1,260p' .codex/skills/publish-after-review/SKILL.md`
   - 결과: `approved` verdict와 feedback close-out 뒤 publish하는 thin-layer skill 본문이 추가된 것을 확인했다.
7. `sed -n '1,120p' .codex/skills/reviewer-handoff/SKILL.md`
   - 결과: `approved` verdict 뒤에는 feedback close-out을 먼저 정리하고, publish는 `publish-after-review` 단계로 넘긴다는 handoff note를 직접 확인했다.
8. `sed -n '1,240p' .codex/skills/README.md`
   - 결과: skill registry와 close-out 추천 순서에 `publish-after-review` hook이 추가된 것을 확인했다.
9. `rg -n "publish-after-review|draft PR|review workspace|publish container|independent review를 먼저|approved.*PR|PR 존재 여부|feedback close-out" docs .codex/skills`
   - 결과: governance, review policy, roadmap, catalog, local skill surface에서 `feedback close-out`을 포함한 같은 vocabulary가 반복되어 draft-first drift를 줄이는 방향으로 정렬된 것을 확인했다.
10. `gh issue view --repo alexization/git-ranker-workflow 71 --json body,title,number`
   - 결과: issue `#71` body render가 의도한 섹션과 줄바꿈을 유지하는 것을 확인했다.
11. `git diff --check`
    - 결과: whitespace error 없음.

## Reviewer Handoff Input

- Exec plan: `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`
- Latest verification report: `passed`
- Diff summary:
  - governance/review policy wording을 pre-PR review cycle과 local repair loop 기준으로 강화했다.
  - architecture/product hook에 publish container / draft exception wording을 정렬했다.
  - local skill registry와 `reviewer-handoff` handoff note를 갱신하고, `publish-after-review` thin-layer skill을 추가했다.
  - `GRW-25` work-item catalog entry와 exec plan close-out을 추가했다.
- Touched files:
  - `docs/operations/workflow-governance.md`
  - `docs/operations/dual-agent-review-policy.md`
  - `docs/architecture/harness-system-map.md`
  - `docs/product/harness-roadmap.md`
  - `docs/product/work-item-catalog.md`
  - `.codex/skills/README.md`
  - `.codex/skills/reviewer-handoff/SKILL.md`
  - `.codex/skills/publish-after-review/SKILL.md`
  - `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`
- Source-of-truth update:
  - `docs/operations/workflow-governance.md`
  - `docs/operations/dual-agent-review-policy.md`
  - `docs/architecture/harness-system-map.md`
  - `docs/product/harness-roadmap.md`
  - `docs/product/work-item-catalog.md`
  - `.codex/skills/README.md`
  - `.codex/skills/reviewer-handoff/SKILL.md`
  - `.codex/skills/publish-after-review/SKILL.md`
- Remaining risks / skipped checks:
  - 이번 이슈는 workflow-docs hardening이라 runtime CI나 GitHub PR publish는 아직 실행하지 않았다.
  - reviewer는 새 skill이 policy를 재정의하지 않고 thin layer에 머무는지, close-out 순서가 `Feedback Pending` semantics와 충돌하지 않는지 확인해야 한다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `reviewer-coordinator` (`Bernoulli`)
- Additional Reviewers:
  - `scope-and-governance`: `Mencius`
  - `verification-and-regression`: `Ohm`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan / linked issue / PR: `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`, `#71`, PR 없음
  - Latest verification report: `passed`
  - Diff summary: governance/review policy wording hardening, roadmap/catalog hook update, local skill registry update, `publish-after-review` thin-layer skill 추가, exec plan verification/report close-out 정리
  - Source-of-truth update: `docs/operations/workflow-governance.md`, `docs/operations/dual-agent-review-policy.md`, `docs/architecture/harness-system-map.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, `.codex/skills/README.md`, `.codex/skills/reviewer-handoff/SKILL.md`, `.codex/skills/publish-after-review/SKILL.md`
  - Remaining risks / skipped checks: docs-only 범위라 runtime CI와 실제 PR publish는 미실행, roadmap의 `feedback evidence` 표현은 다소 약하지만 blocker는 아님
- Review Verdict: `approved`
- Findings / Change Requests:
  - `scope-and-governance`: blocking finding 없음
  - `verification-and-regression`: blocking finding 없음
- Evidence:
  - `scope-and-governance` reviewer인 `Mencius`는 governance shorthand, `publish-after-review` precondition, exec plan flow shorthand가 모두 `approved -> feedback close-out -> PR publish` 순서로 정렬됐다고 확인했다.
  - `verification-and-regression` reviewer인 `Ohm`은 `reviewer-handoff` direct check가 latest verification report에 추가됐고, rerun note가 now-current diff를 충분히 덮는다고 확인했다.
  - reviewer-coordinator인 `Bernoulli`는 필수 reviewer 역할 두 개가 모두 `approved`이고 blocking finding이 없으므로 aggregation rule에 따라 overall verdict를 `approved`로 잠갔다.
- Review repair:
  - 초기 reviewer pass에서는 exec plan과 governance의 ordering shorthand가 `feedback close-out` 단계를 건너뛰고, `publish-after-review`가 feedback outcome 고정 전 publish를 허용하며, latest verification report가 `.codex/skills/reviewer-handoff/SKILL.md` direct check를 직접 덮지 않는다고 지적됐다.
  - repair에서 workflow-governance 공통 지시, `publish-after-review` precondition/step 2, exec plan canonical flow shorthand를 보정하고 `reviewer-handoff` direct verification을 추가한 뒤 reviewer pool을 다시 실행해 최종 `approved`를 받았다.

## Feedback / Guardrail Follow-up

- Latest verification status: `passed`
- Latest review verdict: `approved`
- Failure class: `review-handoff`
- Root cause: reviewer-handoff 이후 publish ordering과 feedback close-out precondition을 강제하는 operational hook이 약해 draft-first drift가 다시 열릴 수 있었다.
- Promotion decision: `no-new-guardrail`
- Decision rationale: 이번 issue 자체에서 governance wording hardening과 `publish-after-review` skill/registry hook을 함께 추가해 필요한 guardrail을 current diff 안에서 이미 반영했다. 별도의 추가 guardrail asset을 더 만들 필요는 없다.
- Follow-up asset or issue: 없음

## Docs Updated

- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `.codex/skills/README.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/publish-after-review/SKILL.md`
- `docs/exec-plans/completed/2026-04-08-grw-25-pre-pr-review-cycle-hardening.md`
