# 2026-04-14-grw-skill-policy-alignment-publish

- Status: `In Progress`
- Primary Repo: `git-ranker-workflow`
- Related Issue: `없음`
- Related PR: `not created in this session`

## Request Summary

현재 worktree에 쌓여 있는 workflow policy/skill 정리와 stale reference cleanup 변경을 의도적으로 커밋하고 GitHub에 publish한다.

## Problem

workflow policy/skill alignment와 stale reference cleanup 변경은 로컬 worktree에만 있고 아직 commit, push, PR로 공개되지 않았다. 이 저장소 운영 규칙상 publish가 필요한 결과는 latest verification 뒤 open PR surface로 공개해야 한다.

## Goals

- 현재 worktree 변경 범위를 하나의 intentional commit으로 고정한다.
- feature branch를 만들어 remote에 push한다.
- latest verification evidence를 확인한 뒤 open PR을 생성한다.

## Non-goals

- 현재 diff의 요구사항 재설계
- unrelated local change 포함
- sibling repo 변경

## Socratic Clarification Log

### Round 1
- Prompted gap: 현재 worktree 전체를 이번 publish 범위로 봐도 되는지 먼저 잠가야 했다.
- Why it mattered: mixed worktree면 staging 범위를 따로 분리해야 하고, 잘못 stage하면 unrelated change를 같이 publish하게 된다.
- User answer / evidence:
  - 사용자 요청은 `commit/publish 작업을 수행해주세요.`였다.
  - 현재 `git status --short`에는 workflow docs/skill 정리와 그 close-out spec만 있어 같은 변경 묶음으로 볼 수 있다.
- Closed gap: 현재 worktree 전체를 같은 publish 범위로 본다.
- Remaining blocker: 없음

## Assumptions And Constraints

- base branch는 현재 `develop`이다.
- 사용자는 draft가 아니라 일반 open PR publish를 요청한 것으로 본다.
- commit message는 `.gitmessage.ko.txt` 형식을 따른다.

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
  - `.git/`
  - `docs/specs/active/2026-04-14-grw-skill-policy-alignment-publish.md`
  - `docs/specs/completed/2026-04-14-grw-skill-policy-alignment-publish.md`
  - `/tmp/`
- Control-plane artifacts:
  - `docs/specs/active/2026-04-14-grw-skill-policy-alignment-publish.md`
- Explicitly forbidden:
  - sibling repo changes
  - current diff requirement 변경
- Network / external systems:
  - GitHub remote push
  - GitHub PR creation
- Escalation triggers:
  - `git push`가 sandbox/network 제한에 막히는 경우

## Acceptance Criteria

- current worktree가 intended commit 하나로 기록된다.
- remote branch가 생성되거나 갱신된다.
- current diff와 맞는 latest verification evidence가 남아 있다.
- open PR link가 생성된다.

## Verification
- Contract profile: `workflow-publish`
- Commands:
  - `git status --short`
  - `git diff --check`
  - `sed -n '1,220p' docs/operations/request-routing-policy.md`
  - `sed -n '1,220p' docs/operations/workflow-governance.md`
  - `sed -n '1,220p' .codex/skills/README.md`
  - `sed -n '1,180p' .codex/skills/request-intake/SKILL.md`
  - `sed -n '1,180p' .codex/skills/socratic-spec-authoring/SKILL.md`
  - `sed -n '1,240p' docs/specs/completed/2026-04-14-grw-socratic-skill-policy-alignment.md`
  - `sed -n '1,240p' docs/specs/completed/2026-04-14-grw-stale-skill-reference-cleanup.md`

## Delivery And Tracking Plan
- Lane: `default lane`
- Parent issue needed: `no`
- PR needed: `yes`

## Detailed Subtasks
- 없음

## Risks Or Open Questions

- remote push는 sandbox/network 정책에 따라 escalation이 필요할 수 있다.

## Approval
- Harness judgment: 현재 worktree는 하나의 publish unit으로 충분히 묶인다.
- User approval: 사용자가 commit/publish 실행을 직접 요청했다.
