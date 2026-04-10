# 2026-04-10-grw-30-reader-first-closeout-slimming

- Issue ID: `GRW-30`
- GitHub Issue: `#79`
- GitHub PR: `#80`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Task Slug: `2026-04-10-grw-30-reader-first-closeout-slimming`
- Verification Contract Profile: `workflow-docs`

## Problem

Harness source of truth는 이미 Issue/PR 본문을 reader-first 문서로 제한하지만, 실제 최근 workflow Issue/PR 본문에는 exec plan 경로, raw verification command 이름, reviewer runtime 같은 운영 상세가 계속 섞여 있었다.

completed exec plan도 historical record라는 목적 자체는 맞지만, planning, context, boundary, verification 상세가 반복되면서 후속 작업자가 읽어야 할 핵심 판단보다 운영 로그 비중이 커지는 drift가 남아 있었다.

## Final Change Summary

- Issue/PR 본문에 남길 내용과 exec plan 또는 verification artifact로 내릴 내용을 governance에 더 명확히 구분했다.
- workflow Issue/PR template와 issue body asset을 더 짧은 reader-first 형식으로 줄였다.
- future completed exec plan이 historical close-out record에 집중하도록 기본 섹션과 optional 섹션 규칙을 다시 정리했다.
- verification, review, feedback 관련 skill wording을 `verification evidence`와 compact `Verification Summary` 기준으로 정렬했다.

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/exec-plans/`
  - `.github/`
  - `.codex/skills/`
- Explicitly forbidden:
  - sibling app repo code tree
  - 기존 completed exec plan mass rewrite
  - unrelated roadmap/catalog reshaping

## Outputs

- updated reader-first body rules
- slimmer workflow Issue/PR templates and issue body asset
- slimmer future completed exec plan guidance
- aligned skill wording for body authoring and close-out density
- GitHub Issue `#79`
- open PR `#80`

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n` review for governance, verification registry, harness system map, exec plan guidance, workflow templates, related skills
  - `rg -n "reader-first|verification evidence|Verification Summary|full transcript|1~3개 bullet|exec plan 경로|raw command literal" docs .github .codex/skills`
  - `find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort`
  - `gh issue view 79 --repo alexization/git-ranker-workflow --json number,title,state,body`
  - `gh pr view 80 --repo alexization/git-ranker-workflow --json number,title,state,isDraft,url,body`
  - `git diff --check`
- Evidence:
  - governance, verification registry, exec plan guidance가 human-facing body와 operational artifact를 더 명확히 분리한다.
  - workflow Issue/PR template와 issue body asset이 짧은 reader-first 형식으로 정렬됐다.
  - skill wording이 `latest verification evidence`, compact `Verification Summary`, PR body density 제한을 같은 vocabulary로 사용한다.
  - `GRW-30` exec plan은 active queue에서 빠지고 completed historical record로만 남는다.
  - GitHub Issue `#79`, PR `#80` body render는 예상한 multiline 섹션을 유지한다.
- Failure or skipped summary: 없음
- Next action: 없음

## Risks or Follow-up

- 실제 다음 workflow 작업에서 body가 다시 길어지면 template보다 skill 또는 close-out 습관 쪽을 추가로 조정해야 한다.
- compact `Verification Summary`와 detailed `Verification Report` 경계가 실제 작업에서 충분한지 후속 예시로 한 번 더 확인할 필요가 있다.

## Docs Updated

- `docs/operations/workflow-governance.md`
- `docs/operations/verification-contract-registry.md`
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- `docs/architecture/harness-system-map.md`
- `docs/exec-plans/README.md`
- `docs/exec-plans/completed/README.md`
- `.github/ISSUE_TEMPLATE/engineering_task.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.codex/skills/README.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/issue-to-exec-plan/assets/github-issue-body.md`
- `.codex/skills/publish-after-review/SKILL.md`
- `.codex/skills/verification-contract-runner/SKILL.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/guardrail-ledger-update/SKILL.md`
- `.codex/skills/guardrail-ledger-update/references/feedback-closeout-minimum.md`
- `docs/exec-plans/completed/2026-04-10-grw-30-reader-first-closeout-slimming.md`
