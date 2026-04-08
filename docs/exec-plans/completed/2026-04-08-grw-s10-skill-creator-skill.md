# 2026-04-08-grw-s10-skill-creator-skill

- Issue ID: `GRW-S10`
- GitHub Issue: `#64`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s10-skill-creator-skill`
- Task Slug: `2026-04-08-grw-s10-skill-creator-skill`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`.codex/skills`의 새 skill 작성 진입점이 아직 정적 문서와 관성적인 기존 구조에 묶여 있다. 이 상태로는 Anthropic `skill-creator`와 `best-practices.md`에서 제시하는 trigger description, progressive disclosure, bundled resource 판단을 재사용 가능한 authoring flow로 고정하기 어렵다.

프로젝트는 앞으로 기존 skill들을 `skill-creator` 방식으로 순차 리팩터링하려고 하므로, 그 전에 "새 skill을 어떤 기준으로 만들고 어떻게 검토할지"를 안내하는 project-local `skill-creator`를 먼저 세워야 한다.

## Why Now

사용자는 앞으로 `authoring-rules.md`를 더 이상 쓰지 않고 `skill-creator`로만 skill을 제작하겠다고 명시했다. 이 전환이 먼저 고정되어야 이후 skill 재구성 작업이 같은 기준과 같은 vocabulary를 재사용할 수 있다.

Anthropic의 `skill-creator` 번들과 `best-practices.md`는 강한 참조점이지만, 현재 턴의 목표는 그 전체 런타임을 옮기는 것이 아니라 authoring surface 자체를 바꾸는 것이다. 따라서 먼저 한국어 `SKILL.md` 중심의 local `skill-creator`를 두고, 필요한 자산이 보이면 후속 리팩터링에서 확장한다.

## Scope

- `.codex/skills/skill-creator/SKILL.md` 작성
- `.codex/skills/README.md`에 `skill-creator` registry 및 사용 순서 반영
- `.codex/skills/authoring-rules.md` 삭제
- `GRW-S10` exec plan 작성 및 close-out 기록 정리

## Non-scope

- 기존 project-local skill 전체 일괄 rewrite
- Anthropic `skill-creator`의 eval/viewer/script 전체 이식
- `.codex/skills` 바깥 source of truth 재설계
- backend/frontend 저장소 변경

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-s10-skill-creator-skill.md`
  - `docs/exec-plans/completed/2026-04-08-grw-s10-skill-creator-skill.md`
  - `/tmp/grw-s10-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/`, `docs/product/` policy 재설계
  - Anthropic eval runtime wholesale import
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음

## Outputs

- `.codex/skills/skill-creator/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-s10-skill-creator-skill.md`

## Working Decisions

- external best practice는 `best-practices.md`와 Anthropic `skill-creator/SKILL.md`를 직접 기준으로 삼고, 불필요한 로컬 보조 규칙 문서는 두지 않는다.
- 새 `skill-creator`는 한국어 `SKILL.md` 하나로 시작하고, bundled resource는 반복 사용에서 실제 이득이 보일 때만 후속 리팩터링에서 추가한다.
- `.codex/skills/README.md`에는 authoring entrypoint가 `skill-creator`로 바뀌었다는 사실과 필요한 registry 변경만 반영한다.

## Verification

- `find .codex/skills -maxdepth 3 -type f | sort`
- `sed -n '1,260p' .codex/skills/skill-creator/SKILL.md`
- `sed -n '1,260p' .codex/skills/README.md`
- `test ! -e .codex/skills/authoring-rules.md`
- `rg -n "skill-creator|progressive disclosure|description" .codex/skills`
- `git diff --check`
- `gh issue view --repo alexization/git-ranker-workflow 64 --json body,title,number`

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Command: `find .codex/skills -maxdepth 3 -type f | sort`
  - Status: `passed`
  - Evidence: `.codex/skills/skill-creator/SKILL.md`가 추가됐고 `authoring-rules.md`는 목록에서 사라졌으며 기존 skill tree는 유지됐다.
- Command: `sed -n '1,260p' .codex/skills/skill-creator/SKILL.md`
  - Status: `passed`
  - Evidence: 한국어 본문으로 trigger, description quality, progressive disclosure, bundled resource 판단, refactoring 기준, `SKILL.md` 단독 시작 조건이 모두 포함됐다.
- Command: `sed -n '1,260p' .codex/skills/README.md`
  - Status: `passed`
  - Evidence: `skill-creator`가 registry와 authoring entrypoint에 반영됐고, support directory 예시가 `references/`, `scripts/`, `assets/` 기준으로 갱신됐다.
- Command: `test ! -e .codex/skills/authoring-rules.md`
  - Status: `passed`
  - Evidence: `authoring-rules.md`가 제거됐다.
- Command: `rg -n "skill-creator|progressive disclosure|description" .codex/skills`
  - Status: `passed`
  - Evidence: 새 `skill-creator`와 registry가 기대 vocabulary를 포함하고, stable source of truth 범위에서 `authoring-rules` 잔존 참조가 제거됐다.
- Command: `gh issue view --repo alexization/git-ranker-workflow 64 --json body,title,number`
  - Status: `passed`
  - Evidence: Issue `#64` 본문이 삭제된 `authoring-rules` 대신 `skill-creator` 중심 authoring 전환과 현재 scope를 반영한다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: whitespace 또는 patch formatting 오류가 없다.
- Failure summary: 없음
- Next action: 이후 기존 skill 리팩터링을 `skill-creator` 기준으로 진행

## Evidence

- external references comparison notes
- new `skill-creator` skill text
- registry / authoring entrypoint update
- `authoring-rules.md` 삭제 결과
- `SKILL.md` 단독 시작 판단 근거
- GitHub Issue `#64` body 확인 결과

## Independent Review

- Not run
- Reason: 이번 턴은 로컬 skill authoring과 source-of-truth 갱신까지만 범위에 포함했고, PR publish 또는 reviewer handoff는 요청되지 않았다.

## Risks or Blockers

- `skill-creator`가 외부 best practice를 요약 없이 길게 복제하면 SKILL.md 자체가 비대해질 수 있다.
- 현재는 `SKILL.md` 하나로 시작했기 때문에, 후속 skill 리팩터링에서 반복되는 예시나 deterministic helper가 보이면 resource 추가 판단이 다시 필요할 수 있다.
- 기존 skill pack registry와 새 authoring entrypoint가 동시에 유지되면 후속 작성자가 어느 쪽을 우선해야 하는지 혼동할 수 있다.

## Next Preconditions

- 이후 `.codex/skills` 재구성 작업은 새 `skill-creator`를 기준으로 개별 skill을 순차 정렬한다.

## Docs Updated

- `.codex/skills/skill-creator/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-s10-skill-creator-skill.md`

## Skill Consideration

이번 Issue 자체가 앞으로의 skill 작성 절차를 담당하는 project-local `skill-creator`를 추가하는 작업이다. 새 skill은 Anthropic `skill-creator`와 `best-practices.md`를 직접 참고해 작성하고, 이후 기존 skill 리팩터링의 출발점이 된다.
