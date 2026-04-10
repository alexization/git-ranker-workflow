# 2026-04-10-grw-24-product-federation-roadmap

- Issue ID: `GRW-24`
- GitHub Issue: `#75`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-24-product-federation-roadmap`
- Task Slug: `2026-04-10-grw-24-product-federation-roadmap`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`docs/product/`에는 이미 완료된 foundation work와 남아 있는 transition work가 함께 섞여 있었고, workflow가 orchestration을 맡고 app repo가 implementation knowledge를 소유하는 federation 구조도 product surface에 충분히 드러나지 않았다.

또한 target repo entrypoint를 `README.md` fallback처럼 다루는 표현과, `GRW-18`이 current active exec plan queue를 어떻게 정리해야 하는지에 대한 기준이 product planning과 active exec plan 사이에서 일관되지 않았다.

## Why Now

현재 active queue에는 `GRW-24`, `GRW-18`, `GRB-04`, `GRB-06`이 남아 있고, 이후 작업은 `GRW-26`, `GRW-27`, `GRB-07`, `GRC-07`처럼 federation ownership과 repo-local bootstrap으로 이어진다. product 문서가 completed backlog와 target ownership을 계속 섞어 보여주면 후속 issue 분해와 handoff 기준이 흔들린다.

지금 단계에서 product 문서를 남은 backlog만 보이게 정리하고, target repo canonical entrypoint를 `AGENTS.md`로 잠가 두어야 이후 app repo bootstrap과 repo-local skill ownership을 같은 기준으로 진행할 수 있다.

## Scope

- `docs/product/README.md`를 active/pending backlog 중심으로 정리한다.
- `docs/product/harness-roadmap.md`를 federation 구조와 `AGENTS.md` entrypoint 기준에 맞게 갱신한다.
- `docs/product/work-item-catalog.md`에서 completed 항목을 제거하고 남은 workflow/backend/frontend backlog만 유지한다.
- `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`에 active queue reconciliation 범위를 반영한다.

## Non-scope

- backend/frontend 앱 코드 변경
- `git-ranker`, `git-ranker-client`에 실제 `AGENTS.md` 생성
- backend/frontend verification contract 구현 완료
- 새 GitHub Actions, quality detector, runtime 추가

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/product/`
  - `docs/exec-plans/active/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-10-grw-24-product-federation-roadmap.md`
  - `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - `/tmp/grw-24-issue-body.md`
  - `/tmp/grw-24-pr-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/` policy 본문 대량 재설계
- Network / external systems:
  - GitHub issue / PR metadata 확인 및 게시
- Escalation triggers:
  - 없음

## Outputs

- `docs/product/README.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `docs/exec-plans/active/2026-04-10-grw-24-product-federation-roadmap.md`

## Working Decisions

- 이 작업의 primary repo와 task type은 `git-ranker-workflow` / `workflow 문서 수정`으로 고정한다.
- completed task는 product 문서에서 제거하고, historical 근거는 `docs/exec-plans/completed/`에 남긴다.
- target repo의 canonical entrypoint는 `AGENTS.md`로 계획에 명시한다.
- `GRW-18`은 active queue reconciliation을 포함하지만 app repo 미완료 구현을 흡수하지는 않는다.

## Context Selection Summary

- Task type: `workflow 문서 수정`
- Primary context pack: `workflow-docs`
- Required docs:
  - `AGENTS.md`
  - `docs/README.md`
  - `PLANS.md`
  - `docs/operations/workflow-governance.md`
  - `docs/architecture/context-pack-registry.md`
  - `docs/product/README.md`
  - `docs/product/harness-roadmap.md`
  - `docs/product/work-item-catalog.md`
  - `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- Optional docs trigger:
  - completed task reference 제거 여부를 확인할 때 completed exec plan inventory를 참고한다.
- Forbidden context:
  - sibling app repo code tree eager load
  - unrelated stable docs mass rewrite
- First-ring hot file cue:
  - `GRW-24`, `GRW-18`, `AGENTS.md`, `active/pending`, `completed`

## Boundary Check Summary

- Read boundary:
  - `workflow-docs` pack required docs와 current active/completed exec plan inventory까지만 읽는다.
- Write boundary:
  - `docs/product/`, `docs/exec-plans/active/`, body file
- Control-plane artifact:
  - current `GRW-24` active exec plan, `GRW-18` active exec plan, GitHub issue/pr metadata
- Explicitly forbidden path:
  - sibling app repo code, unrelated stable source of truth mass update
- Network:
  - GitHub issue/pr publish와 body verification만 허용
- Escalation:
  - 없음

## Verification

- `! rg -n "GRW-10|GRW-11|GRW-12|GRW-13|GRW-14|GRW-15|GRW-16|GRW-17|GRW-19|GRW-20|GRW-21|GRW-22|GRW-23|GRW-25|GRW-S|GRB-01|GRB-02|GRC-01|GRC-02|GRC-03|GRW-01|GRW-02|GRW-03|GRW-04|GRW-05" docs/product`
- `rg -n "GRB-06" docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
- `rg -n "AGENTS.md|GRW-27|GRB-07|GRC-07|active queue" docs/product/harness-roadmap.md docs/product/work-item-catalog.md docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `gh pr view 76 --repo alexization/git-ranker-workflow --json number,state,isDraft,headRefName,baseRefName,headRefOid`
- `git diff --check`

## Evidence

- completed task reference 제거 결과
- federation ownership / `AGENTS.md` entrypoint wording 정렬 결과
- `GRW-18` active queue reconciliation 범위 반영 결과
- GitHub Issue `#75`
- GitHub PR `#76`

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - scope is limited to `docs/product/` 정리와 `GRW-18` active exec plan wording alignment
  - target repo `AGENTS.md` bootstrap은 planning만 반영하고 실제 app repo 생성 작업은 포함하지 않는다
- Command: `! rg -n "GRW-10|GRW-11|GRW-12|GRW-13|GRW-14|GRW-15|GRW-16|GRW-17|GRW-19|GRW-20|GRW-21|GRW-22|GRW-23|GRW-25|GRW-S|GRB-01|GRB-02|GRC-01|GRC-02|GRC-03|GRW-01|GRW-02|GRW-03|GRW-04|GRW-05" docs/product`
  - Status: `passed`
  - Evidence: completed foundation work item ID가 `docs/product/` 본문에 남지 않고, no-match 결과를 success로 취급하는 replayable command다.
- Command: `rg -n "GRB-06" docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
  - Status: `passed`
  - Evidence: active queue에 남아 있는 `GRB-06`이 roadmap과 catalog에도 다시 반영된다.
- Command: `rg -n "AGENTS.md|GRW-27|GRB-07|GRC-07|active queue" docs/product/harness-roadmap.md docs/product/work-item-catalog.md docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - Status: `passed`
  - Evidence: federation ownership, `AGENTS.md` entrypoint, `GRW-18` active queue reconciliation wording이 roadmap, catalog, active exec plan에 함께 반영된다.
- Command: `gh pr view 76 --repo alexization/git-ranker-workflow --json number,state,isDraft,headRefName,baseRefName,headRefOid`
  - Status: `passed`
  - Evidence: live PR `#76`은 `OPEN`, `isDraft=true` 상태이고 current head branch가 `feat/grw-24-product-federation-roadmap`임을 확인했다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: current workflow docs diff와 active exec plan patch에 formatting 오류가 없다.
- Failure summary: 없음
- Next action:
  - repaired tree에 대한 verification은 다시 `passed`로 잠겼다.
  - current repaired tree 기준 refreshed reviewer aggregation verdict를 잠근다.
  - reviewer pool verdict가 `approved`면 open publish readiness를 다시 판정한다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `Franklin | reviewer-coordinator`
- Additional Reviewers:
  - `scope-and-governance`: `Franklin`
  - `verification-and-regression`: `Hume`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/active/2026-04-10-grw-24-product-federation-roadmap.md`
  - Latest verification report: `passed`
  - Diff summary: product backlog를 active/pending 기준으로 정리하고, workflow orchestration / app-repo implementation ownership, `AGENTS.md` entrypoint, `GRW-18` active queue reconciliation 범위를 source of truth에 반영했다.
  - Source-of-truth update (cumulative issue diff): `docs/product/README.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - Remaining risks / skipped checks: target repo `AGENTS.md` bootstrap은 후속 issue로 남아 있다.
- Review Verdict: `approved`
- Findings / Change Requests:
  - No blocking findings.
- Evidence:
  - `scope-and-governance` reviewer `Franklin`은 scope, ownership boundary, active backlog alignment, draft blocker-sharing handling에서 blocking finding이 없음을 확인했다.
  - `verification-and-regression` reviewer `Hume`은 final metadata sync 이후 `Next action`, `Next Preconditions`, verification report, live PR body가 current repaired tree와 일치한다고 확인했다.
  - reviewer-coordinator `Franklin`이 두 필수 reviewer role의 latest verdict가 모두 `approved`이고 blocking finding이 없음을 확인해 overall verdict를 `approved`로 잠갔다.

## Publish Result

- Initial publish path: `draft blocker-sharing exception`
- GitHub PR: `#76`
- PR URL: `https://github.com/alexization/git-ranker-workflow/pull/76`
- Branch: `feat/grw-24-product-federation-roadmap`
- Current promotion status:
  - latest independent review verdict는 `approved`다.
  - PR `#76`은 approved review 뒤 open 상태로 promote됐다.
- Body render check:
  - `gh pr view 76 --repo alexization/git-ranker-workflow --json number,title,body,state,isDraft,url,headRefName,baseRefName`
  - Result: `OPEN`, `isDraft=false`, expected sections/body preserved

## Risks or Blockers

- `GRW-18` 범위를 과하게 넓히면 one-issue/one-goal, primary-repo boundary를 깰 수 있다.
- target repo `AGENTS.md` 생성은 아직 planning만 반영됐고 실제 bootstrap은 후속 repo task로 남아 있다.

## Next Preconditions

- 후속 작업은 `GRW-26`, `GRW-27`, `GRB-07`, `GRC-07` 순서로 federation ownership과 repo-local bootstrap을 진행한다.

## Docs Updated

- `docs/product/README.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `docs/exec-plans/active/2026-04-10-grw-24-product-federation-roadmap.md`

## Repair Note

- `2026-04-10`: reviewer pool (`Nietzsche`, `Anscombe`)이 `changes-requested`를 반환했다.
- trigger:
  - product backlog에서 `GRB-06` 누락
  - no-match `rg` command의 non-replayable verification 기록
  - `GRW-18` active queue evidence와 publish result commit SHA stale state
- Decision: current issue 안에서 `repair`
- Root cause: active queue reconciliation과 publish artifact를 업데이트하면서 current branch에 새 active exec plan과 추가 backend active item을 product source of truth에 끝까지 반영하지 못했다.
- Budget remaining: same-issue repair 1회 가능
- Rerun targets:
  - `! rg -n "GRW-10|GRW-11|GRW-12|GRW-13|GRW-14|GRW-15|GRW-16|GRW-17|GRW-19|GRW-20|GRW-21|GRW-22|GRW-23|GRW-25|GRW-S|GRB-01|GRB-02|GRC-01|GRC-02|GRC-03|GRW-01|GRW-02|GRW-03|GRW-04|GRW-05" docs/product`
  - `rg -n "GRB-06" docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
  - `rg -n "AGENTS.md|GRW-27|GRB-07|GRC-07|active queue" docs/product/harness-roadmap.md docs/product/work-item-catalog.md docs/exec-plans/active/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - `gh pr view 76 --repo alexization/git-ranker-workflow --json number,state,isDraft,headRefName,baseRefName,headRefOid`
  - `git diff --check`
- Next owner: `Codex`
- `2026-04-10`: follow-up reviewer pass에서 live PR body와 exec plan의 publish-state wording drift가 추가로 지적됐다.
- same-issue repair로 live PR body를 current draft review-in-progress 상태에 맞게 갱신했고, `Independent Review` 섹션을 refreshed reviewer aggregation pending 상태로 다시 잠갔다.
