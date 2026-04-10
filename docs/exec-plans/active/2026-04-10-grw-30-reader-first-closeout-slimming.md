# 2026-04-10-grw-30-reader-first-closeout-slimming

- Issue ID: `GRW-30`
- GitHub Issue: `#79`
- GitHub PR: `not created`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-30-reader-first-closeout-slimming`
- Task Slug: `2026-04-10-grw-30-reader-first-closeout-slimming`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

Harness source of truth는 이미 Issue/PR 본문을 사람이 빠르게 읽는 reader-first 문서로 제한하지만, 실제 최근 workflow Issue/PR 본문에는 exec plan 경로, raw verification command 이름, reviewer runtime, body render 확인 같은 운영 상세가 섞여 있다.

completed exec plan도 historical record라는 목적 자체는 맞지만, 한 문서 안에 planning summary, context/boundary summary, command-by-command verification report, close-out reconciliation이 반복되면서 후속 작업자가 읽어야 할 핵심 판단보다 운영 로그 비중이 커졌다.

## Why Now

이 상태를 지금 바로 줄이지 않으면 current workflow runtime simplification 이후에도 사람이 읽는 surface와 운영 artifact 사이 경계가 다시 흐려진다.

특히 completed exec plan이 계속 누적되는 구조에서는 디렉터리를 없애는 것보다, future completed 문서 한 건당 남기는 정보량을 줄이는 규칙을 먼저 잠가야 historical record와 가독성을 동시에 유지할 수 있다.

## Scope

- Issue/PR 본문에 남길 내용과 별도 artifact로 내려야 할 내용을 governance에 더 직접적으로 적는다.
- workflow Issue/PR 템플릿과 issue body asset을 더 짧은 사람 중심 형식으로 정렬한다.
- exec plan guidance와 관련 skill에서 future completed exec plan의 기본 섹션을 더 작게 만든다.
- current request routing -> lane selection -> implement -> verify -> publish flow 설명이 reader-first 관점에서 읽히도록 필요한 wording만 보강한다.

## Non-scope

- 기존 completed exec plan 일괄 축약 또는 rewrite
- backend/frontend repo 문서나 코드 변경
- GitHub automation, CI, review runtime 구현 변경

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/exec-plans/`
  - `docs/product/`
  - `.github/`
  - `.codex/skills/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-10-grw-30-reader-first-closeout-slimming.md`
  - `/tmp/grw-30-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - 기존 completed exec plan mass rewrite
  - unrelated roadmap/catalog reshaping
- Network / external systems:
  - GitHub issue create/view for `alexization/git-ranker-workflow`
- Escalation triggers:
  - 없음

## Outputs

- updated reader-first body rules
- slimmer workflow Issue/PR templates and issue body asset
- slimmer future completed exec plan guidance
- aligned skill wording for body authoring and close-out density
- `GRW-30` active exec plan and GitHub Issue `#79`

## Verification

- `sed -n '1,260p' docs/operations/workflow-governance.md`
- `sed -n '1,220p' docs/operations/request-routing-policy.md`
- `sed -n '1,220p' docs/architecture/harness-system-map.md`
- `sed -n '1,160p' docs/exec-plans/README.md`
- `sed -n '1,220p' .github/ISSUE_TEMPLATE/engineering_task.yml`
- `sed -n '1,220p' .github/PULL_REQUEST_TEMPLATE.md`
- `sed -n '1,240p' .codex/skills/issue-to-exec-plan/SKILL.md`
- `sed -n '1,220p' .codex/skills/publish-after-review/SKILL.md`
- `rg -n "reader-first|operational evidence|completed exec plan|historical record|Verification Report|Review Guide|Validation" docs .github .codex/skills`
- `git diff --check`

## Evidence

- governance와 template가 같은 reader-first 기준으로 정렬된 diff
- future completed exec plan minimum guidance
- skill wording이 body 과다 작성을 줄이도록 바뀐 근거

## Verification Summary

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `sed -n '1,320p' docs/operations/verification-contract-registry.md`
  - `sed -n '1,220p' docs/architecture/harness-system-map.md`
  - `sed -n '1,220p' docs/exec-plans/README.md`
  - `sed -n '1,220p' .github/ISSUE_TEMPLATE/engineering_task.yml`
  - `sed -n '1,220p' .github/PULL_REQUEST_TEMPLATE.md`
  - `sed -n '1,240p' .codex/skills/issue-to-exec-plan/SKILL.md`
  - `sed -n '1,220p' .codex/skills/publish-after-review/SKILL.md`
  - `sed -n '1,220p' .codex/skills/verification-contract-runner/SKILL.md`
  - `sed -n '1,220p' .codex/skills/reviewer-handoff/SKILL.md`
  - `rg -n "reader-first|verification evidence|Verification Summary|full transcript|1~3개 bullet|exec plan 경로|raw command literal" docs .github .codex/skills`
  - `gh issue view 79 --repo alexization/git-ranker-workflow --json number,title,state,body`
  - `git diff --check`
- Evidence:
  - governance, verification registry, exec plan guidance가 human-facing body와 operational artifact를 더 명확히 분리한다.
  - workflow Issue/PR template와 issue body asset이 짧은 reader-first 형식으로 정렬됐다.
  - skill wording이 `latest verification evidence`, compact `Verification Summary`, PR body density 제한을 같은 vocabulary로 사용한다.
  - GitHub Issue `#79` body render는 예상한 multiline 섹션을 유지한다.
- Failure or skipped summary: 없음
- Next action: 사용자가 publish를 원하면 PR body를 만들고 open PR publish를 수행한다.

## Risks or Blockers

- 템플릿만 줄이고 skill wording이 그대로면 실제 작성 습관이 다시 장문화될 수 있다.
- completed exec plan minimum을 너무 공격적으로 줄이면 guarded lane에서 필요한 verification traceability가 약해질 수 있다.

## Next Preconditions

- 변경 후에는 새 workflow Issue/PR과 completed exec plan이 짧아졌는지 실제 작성 예시에서 다시 확인해야 한다.
- publish를 진행하려면 latest diff 기준 PR body를 만들고 open PR을 생성해야 한다.

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

## Skill Consideration

- 새 skill을 만드는 범위는 아니다.
- 대신 `issue-to-exec-plan`, `publish-after-review`, 필요 시 review-related skill wording이 future body density를 낮추도록 함께 정렬해야 한다.
