# 2026-04-08-grw-s11-skills-best-practice-refactor

- Issue ID: `GRW-S11`
- GitHub Issue: `#65`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s11-skills-best-practice-refactor`
- Task Slug: `2026-04-08-grw-s11-skills-best-practice-refactor`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`.codex/skills` 아래의 기존 project-local skill들은 공통 section template과 영문 위주의 단일 trigger 문구에 크게 의존하고 있다. 이 구조는 Anthropic `skill-creator`와 `best-practices.md`가 강조하는 discoverability, description quality, progressive disclosure, resource selection 기준을 skill별로 충분히 반영하지 못한다.

`skill-creator`는 이미 authoring entrypoint로 추가됐지만, 실제 registry 아래 skill들은 아직 이전 작성 방식에 남아 있다. 따라서 `skill-creator`를 기준으로 전체 skill을 다시 읽고, 부족한 authoring guidance가 드러나면 `skill-creator` 자체를 먼저 보강한 뒤 나머지 skill들을 순차 리팩터링해야 한다.

## Why Now

사용자는 `.codex/skills` 아래의 기존 skill들을 모두 `best-practices`와 Anthropic `skill-creator`에 맞춰 다시 만들고, refactor 과정에서 `skill-creator`도 같이 보완하길 요청했다. 개별 skill을 하나씩 손보는 대신 authoring 기준과 skill 본문을 한 번에 정렬해야 이후 local skill pack 전체가 같은 규칙으로 유지된다.

## Scope

- `.codex/skills/skill-creator/SKILL.md` 재보강
- `.codex/skills/*/SKILL.md` 전체 refactor
- 기존 support file 경로와 역할 재정렬
- `.codex/skills/README.md` registry 및 authoring guidance 갱신
- `GRW-S11` exec plan close-out 기록 정리

## Non-scope

- backend/frontend 저장소 코드 변경
- Anthropic eval/viewer/script 전체 이식
- `.codex/skills` 밖 stable source of truth 대규모 재설계
- PR publish 또는 reviewer handoff

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-s11-skills-best-practice-refactor.md`
  - `docs/exec-plans/completed/2026-04-08-grw-s11-skills-best-practice-refactor.md`
  - `/tmp/grw-s11-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/`, `docs/product/` 정책 재설계
  - Anthropic runtime wholesale import
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음

## Outputs

- `.codex/skills/skill-creator/SKILL.md`
- `.codex/skills/README.md`
- refactor된 `.codex/skills/*/SKILL.md`
- 필요 시 재배치된 support files
- `docs/exec-plans/completed/2026-04-08-grw-s11-skills-best-practice-refactor.md`

## Working Decisions

- `skill-creator`를 authoring 기준으로 실제 적용하면서, 부족한 guidance는 먼저 `skill-creator`에 되먹임한다.
- 각 skill은 고정 section template을 유지하는 대신, 실제 workflow에 맞는 구조를 택한다.
- frontmatter `description`은 무엇을 하는지와 언제 써야 하는지를 함께 담는 한국어 trigger surface로 다시 쓴다.
- bundled resource는 실제로 필요한 경우에만 유지하거나 추가하고, 기존 support file도 `references/`, `assets/`, `scripts/` 관점에서 다시 분류한다.
- canonical source를 길게 복제하는 문단은 줄이고, 실제 execution quality를 바꾸는 workflow와 heuristics만 남긴다.

## Verification

- `find .codex/skills -maxdepth 3 -type f | sort`
- `find .codex/skills -maxdepth 2 -name SKILL.md | sort | xargs wc -l`
- `rg -n "^description:" .codex/skills/*/SKILL.md`
- representative `sed -n` checks on refactored skills
- `git diff --check`
- `gh issue view --repo alexization/git-ranker-workflow 65 --json body,title,number`

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Command: `find .codex/skills -maxdepth 3 -type f | sort`
  - Status: `passed`
  - Evidence: `skill-creator` 포함 전체 skill tree가 정리됐고, support file 경로가 `issue-to-exec-plan/assets/github-issue-body.md`, `guardrail-ledger-update/references/feedback-closeout-minimum.md`로 재배치됐다.
- Command: `find .codex/skills -maxdepth 2 -name SKILL.md | sort | xargs wc -l`
  - Status: `passed`
  - Evidence: 기존 1800줄대 skill pack이 1000줄 안팎의 더 lean한 pack으로 정리됐고, 모든 SKILL.md가 240줄 이하로 유지됐다.
- Command: `rg -n "^description:" .codex/skills/*/SKILL.md`
  - Status: `passed`
  - Evidence: 모든 skill frontmatter에 한국어 trigger description이 들어가고, 기존 `Use this skill when...` 패턴은 제거됐다.
- Command: representative `sed -n` checks on refactored skills
  - Status: `passed`
  - Evidence:
    - `request-intake`는 route 분류와 handoff만 남기는 구조로 줄었다.
    - `issue-to-exec-plan`은 exec plan 잠금과 issue body asset 사용을 직접 가리킨다.
    - `reviewer-handoff`는 reviewer minimum context fan-out과 evidence block에 집중한다.
    - `guardrail-ledger-update`는 root-cause-per-entry 원칙과 reference checklist 연결을 유지한다.
    - `skill-creator`는 레거시 resource 재분류, pack-wide refactor loop, 상대경로 링크 규칙까지 포함하게 보강됐다.
- Check: manual prompt simulation 4건
  - Status: `passed`
  - Evidence:
    - "새 요청을 먼저 분류해줘"는 `request-intake` description과 바로 맞닿는다.
    - "이 이슈를 exec plan으로 바꿔줘"는 `issue-to-exec-plan` description이 직접 잡는다.
    - "review 전에 verification report부터 써줘"는 `verification-contract-runner` description이 직접 잡는다.
    - "feedback close-out ledger entry를 정리해줘"는 `guardrail-ledger-update` description이 직접 잡는다.
- Command: `gh issue view --repo alexization/git-ranker-workflow 65 --json body,title,number`
  - Status: `passed`
  - Evidence: Issue `#65` 본문이 현재 scope와 support file 구조 재정렬 목표를 유지한다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: whitespace 또는 patch formatting 오류가 없다.
- Failure summary: 없음
- Next action: refactored skill pack을 기준으로 이후 신규 skill과 후속 보완을 진행

## Evidence

- pre-refactor audit notes
- updated `skill-creator`
- refactored skill set
- support file migration notes
- manual prompt simulation notes
- verification results

## Independent Review

- Not run
- Reason: 이번 턴은 로컬 skill pack authoring refactor와 registry 정렬까지 범위에 포함했고, PR publish 또는 reviewer pool handoff는 요청되지 않았다.

## Risks or Blockers

- skill 수가 많아서 refactor 중 description tone과 구조 일관성이 흔들릴 수 있다.
- support file 이동 시 기존 참조 경로가 깨질 수 있다.
- `skill-creator` 자체 guidance가 부족하면 refactor 결과도 부분 최적화에 머물 수 있다.

## Next Preconditions

- refactor 완료 후 representative prompt 기준으로 추가 보완 여부 확인

## Docs Updated

- `.codex/skills/README.md`
- `.codex/skills/skill-creator/SKILL.md`
- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/issue-to-exec-plan/assets/github-issue-body.md`
- `.codex/skills/parallel-work-split/SKILL.md`
- `.codex/skills/api-contract-sync/SKILL.md`
- `.codex/skills/verification-contract-runner/SKILL.md`
- `.codex/skills/repair-loop-triage/SKILL.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/guardrail-ledger-update/SKILL.md`
- `.codex/skills/guardrail-ledger-update/references/feedback-closeout-minimum.md`
- `.codex/skills/failure-to-policy/SKILL.md`
- `.codex/skills/quality-sweep-triage/SKILL.md`
- `.codex/skills/red/SKILL.md`
- `.codex/skills/green/SKILL.md`
- `.codex/skills/refactor/SKILL.md`
- `docs/exec-plans/completed/2026-04-08-grw-s11-skills-best-practice-refactor.md`

## Skill Consideration

이번 Issue는 기존 skill pack 전체를 `skill-creator` 기준으로 재작성하는 작업이다. 결과물은 개별 skill 정리뿐 아니라, 이후 새 skill을 만들 때 재사용할 authoring 기준까지 함께 안정화해야 한다.
