# 2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync

- Issue ID: `GRW-28`
- GitHub Issue: `#77`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-28-workflow-post-merge-closeout-publish-sync`
- Task Slug: `2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`GRW-18`의 terminal-state correction은 로컬에서 이미 정리됐지만, 아직 원격 기본 브랜치에는 publish되지 않았다. 이 상태가 남아 있으면 GitHub에서 읽는 completed exec plan historical record와 product backlog가 current GitHub state와 어긋나고, `GRW-18`이 여전히 active queue처럼 보일 수 있다.

이미 닫힌 Issue `#70`과 merged PR `#73`을 다시 publish container로 쓰기보다, 이 후행 sync는 별도 workflow-docs issue/PR로 분리해 publish해야 lineage와 historical snapshot을 모두 보존할 수 있다.

## Why Now

workflow repo의 source of truth는 local branch가 아니라 원격 기본 브랜치 기준으로 읽힌다. `GRW-18` completed historical record와 product backlog sync가 publish되지 않으면 후속 작업자는 stale active queue를 기준으로 읽게 되고, close-out drift가 remote source에서는 계속 남는다.

또한 이 follow-up은 새 policy 작업이 아니라 이미 정리된 terminal-state correction을 publish하는 운영성 close-out sync이므로, 범위를 좁게 잠그고 빠르게 publish path를 정리해야 한다.

## Scope

- local branch에 있는 `GRW-18` terminal-state sync diff를 publish 가능한 workflow-docs issue/exec plan/PR artifact로 정리한다.
- `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md` publish 범위를 고정한다.
- `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md` active queue sync publish 범위를 고정한다.
- GitHub Issue `#77` body render, verification 결과, publish result를 active exec plan에 기록한다.
- canonical review runtime이 없는 경우 blocker-sharing draft exception path를 명시하고 publish artifact에 남긴다.

## Non-scope

- `GRW-18` historical record 의미 재설계
- backend/frontend app repo 구현
- 새 workflow policy, skill, template 추가
- `GRB-04`, `GRB-06`, `GRC-05`의 내용 변경

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/exec-plans/active/`
  - `docs/exec-plans/completed/`
  - `docs/product/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
  - `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - `docs/product/harness-roadmap.md`
  - `docs/product/work-item-catalog.md`
  - `/tmp/grw-28-issue-body.md`
  - `/tmp/grw-28-pr-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/` policy 재설계
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue `#77` create/view
  - GitHub PR create/view for `alexization/git-ranker-workflow`
- Escalation triggers:
  - sandbox가 git index write 또는 push를 막을 때만

## Outputs

- `docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
- `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- GitHub Issue `#77`
- follow-up publish PR

## Working Decisions

- 이번 follow-up의 primary repo와 task type은 `git-ranker-workflow` / `workflow 문서 수정`으로 고정한다.
- 범위는 이미 local branch에 있는 terminal-state correction diff publish에 한정한다.
- `GRW-18` Issue `#70`과 PR `#73`은 historical state를 유지하고 reopen하지 않는다.
- canonical reviewer sub-agent runtime을 현재 세션에서 실행하지 못하면 blocker-sharing draft exception으로 publish한다.
- detailed verification/review evidence는 exec plan에 남기고, PR body에는 reader-first 요약만 싣는다.

## Context Selection Summary

- Task type: `workflow 문서 수정`
- Primary context pack: `workflow-docs`
- Required docs:
  - `AGENTS.md`
  - `docs/README.md`
  - `PLANS.md`
  - `docs/operations/workflow-governance.md`
  - `docs/architecture/context-pack-registry.md`
  - `docs/operations/tool-boundary-matrix.md`
  - `docs/operations/verification-contract-registry.md`
  - `docs/operations/dual-agent-review-policy.md`
  - `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - `docs/product/harness-roadmap.md`
  - `docs/product/work-item-catalog.md`
- Optional docs trigger:
  - blocker-sharing draft exception wording을 검토할 때 `.github/PULL_REQUEST_TEMPLATE.md`
- Forbidden context:
  - sibling app repo code tree eager load
  - unrelated stable source of truth 확장
- First-ring hot file cue:
  - `GRW-18`
  - `GRW-28`
  - `Publish`
  - `Feedback / Guardrail Follow-up`
  - `GRB-04`
  - `GRB-06`

## Boundary Check Summary

- Read boundary:
  - `workflow-docs` pack required docs, touched exec plan/product docs, GitHub issue/PR metadata까지만 읽는다.
- Write boundary:
  - `docs/exec-plans/active/`, `docs/exec-plans/completed/`, `docs/product/`
- Control-plane artifact:
  - current active exec plan, completed `GRW-18` historical record, product backlog docs, publish body files
- Explicitly forbidden path:
  - sibling app repo code, unrelated stable source of truth
- Network:
  - GitHub issue/pr create/view만 허용
- Escalation:
  - git staging/commit/push에 필요한 최소 범위만 허용

## Verification

- `sed -n '1,420p' docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `sed -n '1,220p' docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
- `sed -n '1,120p' docs/product/harness-roadmap.md`
- `sed -n '1,120p' docs/product/work-item-catalog.md`
- `rg -n 'GRB-04|GRB-06|GRC-05|GRW-26|GRW-27|GRW-18' docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
- `GitHub PR #78 comments fetch`
- `gh issue view 77 --repo alexization/git-ranker-workflow --json number,title,body,state`
- `git diff --check`
- conditional: publish 후 `gh pr view --json number,title,body,state,isDraft,url,headRefName,baseRefName`

## Evidence

- current local diff summary
- `GRW-18` completed historical record
- product backlog sync 결과
- GitHub Issue `#77` body render 결과
- GitHub PR `#78` automated review comment
- latest verification report
- publish result 또는 blocker disclosure

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - local branch `feat/grw-28-workflow-post-merge-closeout-publish-sync`는 `develop` 대비 `GRW-18` terminal-state sync diff commit `2a1a1a0`를 포함한다.
  - GitHub Issue `#77`은 `OPEN` 상태로 생성됐고 body render를 확인했다.
  - PR `#78` automated review response가 stale active-queue evidence 1건을 남겼고, current local diff는 그 finding을 직접 수리한다.
- Command: `sed -n '1,420p' docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
  - Status: `passed`
  - Evidence: `GRW-18` completed historical record가 post-merge close-out sync, feedback close-out, active queue terminal state를 함께 기록하고, current branch의 active exec plan queue `GRB-04`, `GRB-06`, `GRW-28`과 일치하도록 stale wording을 제거한다.
- Command: `sed -n '1,220p' docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
  - Status: `passed`
  - Evidence: `GRW-28` active exec plan이 issue `#77`, write scope, verification, blocker-sharing publish path와 automated review feedback repair 상태를 현재 diff 기준으로 고정한다.
- Command: `sed -n '1,120p' docs/product/harness-roadmap.md`
  - Status: `passed`
  - Evidence: roadmap는 다음 queue를 `GRB-04`, `GRB-06`, `GRC-05`, `GRW-26`, `GRW-27`로 유지하고 `GRW-18` active wording을 제거한다.
- Command: `sed -n '1,120p' docs/product/work-item-catalog.md`
  - Status: `passed`
  - Evidence: catalog는 `GRW-18` active section 없이 남은 workflow/backend/client backlog만 유지한다.
- Command: `rg -n 'GRB-04|GRB-06|GRC-05|GRW-26|GRW-27|GRW-18' docs/product/harness-roadmap.md docs/product/work-item-catalog.md`
  - Status: `passed`
  - Evidence: product docs에는 `GRW-18` active item section이 없고, 남은 queue와 선행조건 훅만 남아 있다.
- Command: `GitHub PR #78 comments fetch`
  - Status: `passed`
  - Evidence: automated review는 completed `GRW-18` record의 stale active-queue evidence 1건만 지적했고, current local diff는 그 표현을 `GRB-04`, `GRB-06`, `GRW-28` 기준으로 갱신해 branch state와 다시 맞춘다.
- Command: `gh issue view 77 --repo alexization/git-ranker-workflow --json number,title,body,state`
  - Status: `passed`
  - Evidence: Issue `#77`은 `OPEN` 상태이며 body의 줄바꿈과 섹션이 예상대로 유지된다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: formatting 오류가 없다.
- Command: `gh pr view 78 --repo alexization/git-ranker-workflow --json number,title,body,state,isDraft,url,headRefName,baseRefName`
  - Status: `passed`
  - Evidence: draft PR `#78`이 `OPEN`, `isDraft=true`, expected body sections 유지 상태로 생성됐다.
- Failure summary: 없음
- Next action: draft blocker-sharing exception 상태를 유지하고, reviewer runtime 확보 뒤 same issue에서 reviewer handoff를 이어간다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `not run`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
  - Latest verification report: `passed`
  - Diff summary: `GRW-18` completed historical record publish, roadmap/catalog active queue sync publish, `GRW-28` active exec plan 추가
  - Source-of-truth update: `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, current active exec plan
  - Remaining risks / skipped checks: canonical reviewer sub-agent runtime unavailable in current turn
- Review Verdict: `blocked`
- Findings / Change Requests:
  - latest verification report는 준비됐지만 session-isolated reviewer pool을 현재 세션에서 실행하지 못했다.
  - open PR publish path에 필요한 canonical `approved` verdict가 아직 없다.
- Evidence:
  - current workflow governance는 independent review evidence 없이 open PR publish를 기본값으로 허용하지 않는다.
  - 현재 세션에서는 reviewer sub-agent runtime을 호출하지 않아 reviewer minimum context를 fan-out한 canonical review evidence를 만들지 못했다.

## Feedback / Guardrail Follow-up

- Stage: `Reviewing`
- Failure class: `review-handoff`
- Promotion decision: `pending`
- Rationale:
  - blocker의 원인은 current diff 자체가 아니라 canonical reviewer runtime 부재다.
  - 이번 턴에서는 blocker-sharing draft exception으로 publish surface를 열고, review 가능 runtime이 확보되면 same issue에서 verdict를 갱신한다.
- Core evidence:
  - latest verification report는 `passed`다.
  - independent review verdict는 reviewer runtime unavailable로 `blocked`다.
- Follow-up asset:
  - draft PR blocker disclosure와 후속 reviewer handoff

## Publish Result

- Publish decision: `draft blocker-sharing exception`
- GitHub PR: `#78`
- PR URL: `https://github.com/alexization/git-ranker-workflow/pull/78`
- GitHub Issue: `#77`
- Branch: `feat/grw-28-workflow-post-merge-closeout-publish-sync`
- Current publish status:
  - latest verification report는 `passed`다.
  - latest independent review verdict는 reviewer runtime unavailable로 `blocked`다.
  - PR `#78`은 `OPEN`, `isDraft=true` 상태로 blocker disclosure를 공유한다.
  - PR thread의 automated review response는 stale active-queue evidence 1건을 남겼고, current local diff가 그 finding을 반영한다.
- Body render check:
  - `gh pr view 78 --repo alexization/git-ranker-workflow --json number,title,body,state,isDraft,url,headRefName,baseRefName`
  - Result: expected sections/body preserved

## Risks or Blockers

- canonical reviewer sub-agent runtime이 현재 세션에서 승인되지 않으면 open PR publish path 대신 blocker-sharing draft exception이 필요하다.
- local diff는 `GRW-18` historical record를 고치지 않고 publish만 목표로 하므로, 범위를 넓혀 새 policy 작업으로 번지면 안 된다.
- 이미 닫힌 `#70`/`#73`을 reopen하면 historical snapshot이 다시 흔들린다.

## Next Preconditions

- reviewer runtime이 가능한 세션에서 canonical reviewer handoff를 다시 실행한다.
- PR `#78`의 latest pushed diff가 stale active-queue repair를 포함하는지 확인한다.
- blocking finding이 없으면 draft PR `#78`의 ready/open promote 여부를 판단한다.
- `GRW-28` close-out은 latest review verdict와 feedback decision이 고정된 뒤 진행한다.

## Docs Updated

- `docs/exec-plans/active/2026-04-10-grw-28-workflow-post-merge-closeout-publish-sync.md`
- `docs/exec-plans/completed/2026-04-08-grw-18-workflow-pilot-closeout-reconciliation.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`

## Skill Consideration

이번 작업은 새 skill을 만드는 범위가 아니다. 기존 `issue-to-exec-plan`, `verification-contract-runner`, `publish-after-review` 절차를 workflow-docs publish follow-up에 재사용한다.
