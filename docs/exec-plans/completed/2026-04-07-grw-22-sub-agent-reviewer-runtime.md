# 2026-04-07-grw-22-sub-agent-reviewer-runtime

- Issue ID: `GRW-22`
- GitHub Issue: `#53`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-22-sub-agent-reviewer-runtime`
- Task Slug: `2026-04-07-grw-22-sub-agent-reviewer-runtime`

## Problem

Issue/PR reader-facing 문서에는 사람이 판단하는 데 꼭 필요하지 않은 파일 inventory, raw 검증 명령, 내부 운영 dump가 과도하게 남아 있었고, review 정책 쪽 stable source of truth에는 sub-agent reviewer pool을 단일 canonical path로 읽기 어렵게 만드는 표현이 남아 있었다.

이 상태가 유지되면 사람은 Issue/PR 본문에서 중요한 판단 포인트를 찾기 어려워지고, 구현자는 dual-agent review를 읽고도 외부 reviewer 경로나 단일 reviewer를 허용된 대안으로 오해할 수 있다. reader-first body 규칙과 sub-agent reviewer pool canonical runtime을 stable source of truth에 함께 고정하고, completed exec plan은 현재 정책에 맞춰 rewrite하지 않는다는 경계도 명시해야 한다.

## Why Now

사용자는 사람이 읽기 쉬운 Issue/PR template과, 항상 다른 sub-agent들로 review를 수행하는 정책을 명시적으로 요구했다.

template, governance, review policy, historical record 경계를 한 번에 정리해야 이후 `reviewer-handoff` skill, pilot issue, 실제 PR close-out이 같은 reader-first 및 sub-agent review 경로를 따른다.

## Scope

- reader-first Issue/PR template과 관련 governance/hook 문서를 정리한다.
- dual-agent review, governance, roadmap, catalog, system map, verification handoff 문구를 sub-agent reviewer pool 기준으로 정리한다.
- completed exec plan은 historical record로 보존하고, 현재 canonical runtime은 stable source of truth에서 읽는다는 경계를 추가한다.
- 이번 작업 자체도 session-isolated sub-agent independent review evidence로 close-out한다.

## Non-scope

- backend/frontend 앱 코드 변경
- 외부 reviewer runtime 인프라 수정
- 자동 PR review bot 구현
- repo 밖 자동화나 개인 로컬 설정 수정

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/`
  - `docs/exec-plans/`
  - `.github/`
  - `.codex/skills/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-07-grw-22-sub-agent-reviewer-runtime.md`
  - `/tmp/grw-22-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code write
  - 외부 reviewer runtime 구현 코드 추가
  - scope 밖 stable source of truth mass update

## Outputs

- reader-first issue/PR template 정리본
- sub-agent reviewer pool을 canonical runtime으로 고정한 source of truth
- completed exec plan historical record 규칙
- `GRW-22` 실행 기록

## Working Decisions

- independent review의 canonical runtime은 session-isolated sub-agent reviewer pool이다.
- MCP 기반 외부 reviewer runtime과 외부 모델 호출은 canonical review path로 다루지 않는다.
- completed exec plan은 당시 사실관계와 evidence를 보존하고, 현재 정책은 stable source of truth에서 해석한다.
- reader-facing Issue/PR 본문에는 사람이 판단해야 할 내용만 남기고 operational evidence는 close-out artifact로 내린다.

## Verification

- `gh issue view --repo alexization/git-ranker-workflow 53 --json number,title,body`
  - 결과: Issue `#53` 본문이 reader-first 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- `rg -n "Gemini CLI|gemini-2.5|same-model|single reviewer|단일 reviewer" docs/operations docs/architecture docs/product .codex/skills .github`
  - 결과: stable source of truth와 template 범위에서는 legacy reviewer runtime vocabulary가 남아 있지 않음을 확인했다.
- `rg -n "MCP 기반 외부 reviewer runtime|외부 모델 호출" docs/operations docs/architecture docs/product`
  - 결과: 외부 reviewer 경로가 허용 대안이 아니라 명시적 금지 규칙으로만 남아 있음을 확인했다.
- `rg -n "sub-agent reviewer pool|session-isolated sub-agent|reviewer coordinator|Reviewer Roles / Prompt Focus|scope-and-governance|verification-and-regression|security-and-reliability" docs/operations docs/architecture docs/product`
  - 결과: sub-agent reviewer pool vocabulary와 reviewer 역할 구성이 touched hook 전반에 반영된 것을 확인했다.
- `rg -n "historical record|historical snapshot|stable source of truth" docs/operations/workflow-governance.md docs/architecture/harness-system-map.md docs/exec-plans/completed/README.md`
  - 결과: completed exec plan을 historical record로 보존하고 현재 정책은 stable source of truth에서 읽는 규칙이 추가된 것을 확인했다.
- `sed -n '55,110p' docs/operations/request-routing-policy.md`
  - 결과: ambiguity interview 목적과 `Planned` 종료 기준에 `Why Now`가 다시 포함되어 workflow governance 및 ambiguity-interview skill과 기준이 맞는 것을 확인했다.
- `rg -n "Why Now|왜 지금|Planned" docs/operations/request-routing-policy.md .codex/skills/ambiguity-interview/SKILL.md docs/operations/workflow-governance.md`
  - 결과: request routing policy, ambiguity-interview skill, workflow governance가 모두 `왜 지금 필요한지`를 issue/plan 필수 맥락으로 요구하는 것을 확인했다.
- post-PR review repair
  - 결과: PR review에서 지적된 `request-routing-policy.md`의 `Why Now` 누락을 복원했고, ambiguity-interview skill 요약/evidence도 같은 기준으로 맞췄다.
- `ruby -e 'require "yaml"; YAML.load_file(".github/ISSUE_TEMPLATE/engineering_task.yml"); puts "YAML OK"'`
  - 결과: issue template YAML 파싱이 정상임을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.

## Evidence

- sub-agent reviewer pool 기준으로 갱신된 policy/hook 문서
- reader-first issue/PR template 정리본
- completed exec plan historical-record boundary
- GitHub Issue `#53` body render 확인 결과

## Independent Review

- Implementer: `Codex`
- Reviewer: `Hume | reviewer-coordinator`
- Additional Reviewers:
  - `verification-and-regression`: `Nash`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/completed/2026-04-07-grw-22-sub-agent-reviewer-runtime.md`
  - Latest verification report: `passed`
  - Diff summary: reader-first Issue/PR template 정리, sub-agent reviewer pool canonical runtime 고정, completed exec plan historical-record boundary 추가, `request-routing-policy`와 `ambiguity-interview`의 `Why Now` 정합성 복원
  - Source-of-truth update: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/engineering_task.yml`, `.codex/skills/issue-to-exec-plan/templates/github-issue-body.md`, `.codex/skills/ambiguity-interview/SKILL.md`, `docs/operations/workflow-governance.md`, `docs/operations/dual-agent-review-policy.md`, `docs/operations/verification-contract-registry.md`, `docs/operations/request-routing-policy.md`, `docs/operations/failure-to-guardrail-feedback-loop.md`, `docs/operations/guardrail-ledger-template.md`, `docs/architecture/harness-system-map.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, `docs/exec-plans/completed/README.md`
  - Remaining risks / skipped checks: repo 밖 자동화나 로컬 설정이 MCP reviewer를 별도로 호출하면 이번 저장소 수정만으로는 차단되지 않음
- Review Verdict: `approved`
- Findings / Change Requests:
  - `scope-and-governance`: blocking finding 없음
  - `verification-and-regression`: blocking finding 없음
- Evidence:
  - `Hume`는 reviewer minimum context semantics, canonical runtime wording, historical-record 규칙, `Why Now` 복원 이후의 active exec plan scope가 stable source of truth와 일관된다고 확인했고 `approved` verdict를 남겼다.
  - `Nash`는 verification/handoff semantics, legacy reviewer vocabulary 제거, prohibition-only wording, `request-routing-policy`와 `ambiguity-interview`의 `Why Now` 정합성, completed exec plan 보존 상태가 현재 diff와 맞는다고 확인했고 `approved` verdict를 남겼다.
  - reviewer coordinator인 `Hume`는 두 필수 역할이 모두 `approved`이고 blocking finding이 없으므로 overall verdict를 `approved`로 집계했다.

## Risks or Blockers

- repo 밖 자동화나 로컬 도구 설정이 별도로 MCP reviewer를 호출하고 있다면 이번 저장소 수정만으로는 막지 못한다.
- completed exec plan에는 당시 reviewer/runtime 어휘가 남아 있을 수 있으므로, 현재 정책 해석은 stable source of truth를 우선해야 한다.

## Next Preconditions

- session-isolated sub-agent reviewer들의 independent review verdict 수집
- commit, push, PR publish 전 close-out evidence 확정

## Docs Updated

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/engineering_task.yml`
- `.codex/skills/issue-to-exec-plan/templates/github-issue-body.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `docs/operations/verification-contract-registry.md`
- `docs/operations/request-routing-policy.md`
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/README.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 다만 후속 `reviewer-handoff` skill은 이번 문서가 고정한 sub-agent reviewer pool runtime을 그대로 재사용해야 한다.
