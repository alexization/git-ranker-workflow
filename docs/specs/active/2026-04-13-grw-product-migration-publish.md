# 2026-04-13-grw-product-migration-publish

- Status: `Approved`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `alexization/git-ranker-workflow#83`
- Related PR: `not created`

## Request Summary

현재 workflow 문서 변경과 seeded draft spec 추가 내용을 기준으로 umbrella issue와 open PR을 생성한다.

## Problem

`docs/product` 제거와 spec-first queue 전환은 로컬 diff로만 남아 있고, 현재 이를 추적하고 리뷰할 GitHub surface가 없다.

## Goals

- 현재 docs-only 변경을 설명하는 umbrella issue를 만든다.
- 같은 변경을 publish하는 open PR을 만든다.
- issue/PR 본문이 reader-first 규칙과 repo template을 따른다.

## Non-goals

- sibling app repo 변경 publish
- seeded draft spec 자체의 구현 시작
- current docs diff와 무관한 cleanup 포함

## Socratic Clarification Log

### Round 1
- Prompted gap: current worktree에 섞여 있는 변경 중 무엇을 이번 umbrella issue/PR 범위에 포함할지
- Why it mattered: PR은 목표 1개만 가져야 하므로 publish scope를 먼저 잠가야 한다
- User answer / evidence:
  - 사용자는 `일단 이 작업들에 대해서 크게 이슈와 PR을 작성해줘.`라고 요청했다
  - 추가 질문에 `포함해줘.`라고 답해 함께 잡혀 있던 spec 삭제 signal도 같은 publish 범위에 포함해도 된다고 승인했다
- Closed gap: 이번 publish는 현재 workflow docs diff 전체를 하나의 umbrella artifact로 묶는다
- Remaining blocker: 없음

## Assumptions And Constraints

- PR은 repo policy에 따라 draft가 아니라 open PR로 생성한다.
- publish 대상은 `git-ranker-workflow`의 docs/spec/skill 변경만 포함한다.
- issue/PR 본문에는 raw command dump 대신 문제, 접근, 영향, 리스크만 요약한다.

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
  - `docs/specs/active/2026-04-13-grw-product-migration-publish.md`
  - temporary issue/PR body file under `/tmp`
  - git metadata for branch/commit on current repo
- Control-plane artifacts:
  - `docs/specs/active/2026-04-13-grw-product-migration-publish.md`
- Explicitly forbidden:
  - sibling app repo changes
  - current diff와 무관한 추가 문서 수정
- Network / external systems:
  - GitHub issue/PR publish for `alexization/git-ranker-workflow`
- Escalation triggers:
  - `git push`
  - GitHub issue/PR creation if sandbox/network blocks

## Acceptance Criteria

- umbrella issue가 현재 docs migration과 seeded draft queue를 설명한다.
- open PR이 현재 diff를 publish하고 linked issue를 포함한다.
- branch, commit, issue, PR metadata가 current spec과 모순되지 않는다.

## Verification
- Contract profile: `workflow-docs`
- Commands:
  - `git status --short`
  - `git diff --stat`
  - `git diff --check`
  - `gh issue view <issue-number>`
  - `gh pr view <pr-number>`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `yes`
- PR needed: `yes`

## Detailed Subtasks
- `tracking-body-authoring`
  - Target repo: `git-ranker-workflow`
  - Goal: template에 맞는 umbrella issue/PR body를 준비한다.
  - In-scope: title, summary, scope, risk, linkage
  - Done when: issue/PR body file이 reader-first 규칙을 만족한다.
  - Verification hook: body file review
  - Tracking needed: `yes`
- `publish-current-diff`
  - Target repo: `git-ranker-workflow`
  - Goal: current docs diff를 branch/commit/issue/PR로 publish한다.
  - In-scope: branch creation, commit, push, GitHub issue/PR creation
  - Done when: open PR과 linked issue가 존재한다.
  - Verification hook: `gh issue view`, `gh pr view`
  - Tracking needed: `yes`

## Risks Or Open Questions

- untracked draft spec 파일을 빠뜨리면 issue/PR 설명과 actual diff가 어긋날 수 있다.

## Approval
- Harness judgment: 현재 publish 범위는 workflow docs migration과 seeded draft spec queue를 설명하는 하나의 umbrella artifact로 닫을 수 있다.
- User approval: 사용자가 umbrella issue/PR 생성을 요청했고, publish scope에 current mixed diff를 포함하는 데 동의했다.
