# 2026-04-08-grw-23-continuous-quality-feedback-loop

- Issue ID: `GRW-23`
- GitHub Issue: `#60`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-23-continuous-quality-feedback-loop`
- Task Slug: `2026-04-08-grw-23-continuous-quality-feedback-loop`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

현재 Harness workflow에는 verification, independent review, failure-to-guardrail feedback close-out까지의 기본 통제는 있다. 하지만 "AI가 만든 코드를 주기적으로 점검하고 품질 저하를 자동 감지해 정리 PR까지 이어지는 지속적 피드백 루프"는 source of truth와 project-local skill로 아직 고정돼 있지 않다.

그 결과 현재 하네스는 개별 구현 작업의 완료 여부는 통제할 수 있지만, 시간이 지나며 누적되는 lint drift, duplication, unused code 같은 비차단 품질 저하를 어떤 trigger로 스캔하고, 어떤 evidence 형식으로 기록하며, 언제 cleanup PR 또는 guardrail follow-up으로 보내야 하는지는 작업자마다 매번 다시 정해야 한다.

## Why Now

`verification-contract-registry`, `dual-agent-review-policy`, `failure-to-guardrail-feedback-loop`, `guardrail-hardening` skill pack까지 갖춰지면서 "한 번의 구현 작업을 닫는 루프"는 거의 정리됐다. 이제 사용자가 기대하는 "지속적으로 품질 저하를 다시 끌어올리는 루프"를 같은 control plane 안에 붙여야 feedback system이 사후 close-out에만 머물지 않는다.

또한 중복 코드, 미사용 코드, coding rule drift는 correctness regression과 달리 즉시 repair loop로 되돌리기보다는 별도 cleanup 작업이나 guardrail 승격으로 다뤄야 하는 경우가 많다. 이 경계를 canonical policy와 thin-layer skill로 먼저 잠가야 후속 repo 작업이 흔들리지 않는다.

## Scope

- 현재 하네스가 이미 커버하는 feedback/guardrail 범위와 비어 있는 continuous quality sweep 범위를 문서로 구분한다.
- `docs/operations/`에 continuous quality feedback loop source of truth와 report template를 추가한다.
- coding-rule drift, duplication, unused code를 quality sweep signal class와 cleanup candidate로 정의한다.
- quality sweep 결과를 cleanup issue/PR handoff 또는 guardrail promotion으로 보내는 규칙을 architecture/product/governance hook에 연결한다.
- implementer가 quality sweep 결과를 반복 가능한 형식으로 정리할 수 있도록 project-local skill을 추가한다.
- `GRW-23` exec plan과 close-out 근거를 남긴다.

## Non-scope

- backend/frontend 저장소의 실제 코드 정리
- GitHub Actions, cron, bot account 같은 runtime automation 직접 구현
- 외부 정적 분석 도구 신규 도입
- 기존 verification/review/failure policy 전체 재설계
- sibling repo code write 또는 cross-repo runtime orchestration 추가

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/`
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-23-continuous-quality-feedback-loop.md`
  - `docs/exec-plans/completed/2026-04-08-grw-23-continuous-quality-feedback-loop.md`
  - `/tmp/grw-23-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code write
  - `.github/workflows/` 등 runtime automation 추가
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음

## Outputs

- `docs/operations/continuous-quality-feedback-loop.md`
- `docs/operations/quality-sweep-report-template.md`
- `.codex/skills/quality-sweep-triage/SKILL.md`
- 관련 architecture/product/operations/skills registry hook
- `docs/exec-plans/active/2026-04-08-grw-23-continuous-quality-feedback-loop.md`

## Working Decisions

- 현재 하네스에 있는 `failure-to-guardrail`은 "작업 close-out feedback loop"로 유지하고, 새 문서는 이를 대체하지 않는 "continuous quality sweep loop"로 분리한다.
- quality sweep은 state machine에 새 terminal stage를 추가하지 않고, `Feedback` 단계에서 후속 cleanup issue/PR 또는 guardrail follow-up을 생성하는 recurring surface로 정의한다.
- non-blocking quality drift는 기존 작업의 완료 판정을 자동으로 뒤집지 않는다. 대신 새 cleanup work item 또는 guardrail follow-up으로 분리한다.
- quality signal class는 우선 `coding-rule-drift`, `duplication-drift`, `unused-code-drift` 세 가지로 고정하고, 저장소별 detector 구현은 각 repo contract가 소유한다.
- project-local skill은 canonical policy를 thin layer로 operationalize하는 수준에 머문다.
- enterprise-grade rollout은 `workflow = policy/triage`, `repo = detector/CI/runtime` 분리 원칙을 따른다.
- PR blocking lane에는 fast/deterministic/low-noise signal만 넣고, duplication과 wide dead code scan은 scheduled sweep lane으로 분리한다.
- auto-generated cleanup PR은 autofixable low-risk surface에만 허용하고, duplication refactor와 backend dead code removal은 issue-first를 기본으로 한다.

## Enterprise Review

- 현재 `workflow`에 넣은 방식은 enterprise harness의 control-plane 역할로는 적절하다. policy, taxonomy, evidence, handoff를 중앙에서 고정하고, detector runtime은 각 repo가 소유하는 분리가 맞다.
- 비효율적인 방식은 `workflow` 저장소가 backend/frontend 코드를 직접 스캔하거나, 모든 GC를 중앙 스케줄러 하나로 몰아넣는 것이다. 현재 control-plane map과 context pack registry 기준에도 이 방식은 boundary를 깨뜨린다.
- 우리 구조에서는 backend와 frontend가 이미 각자 CI/workflow surface를 갖고 있으므로, GC도 각 repo의 PR gate와 scheduled workflow에 붙이는 것이 가장 적절하다.
- 가장 중요한 수정점은 "자동 PR 생성"의 범위를 줄이는 것이다. enterprise 방식에서는 auto-PR을 전면 허용하지 않고, deterministic autofix가 가능한 low-risk surface만 허용한다.

## Recommended Rollout

1. `workflow`는 지금처럼 policy, report template, skill, cleanup handoff만 유지한다.
2. backend는 existing Gradle + `quality-gate.yml` 위에 repo-local GC lane을 추가한다.
   - PR blocking lane: low-noise static analysis만 추가
   - scheduled sweep lane: duplication/wide dead code scan
   - auto-PR: 기본적으로 끄고, 안전한 import/format 계열만 추후 검토
3. frontend는 existing npm scripts + `ci.yml` 위에 repo-local GC lane을 추가한다.
   - PR blocking lane: `lint` 기반 coding-rule drift와 high-confidence unused detector 일부
   - scheduled sweep lane: duplication, wide unused file/export/dependency scan
   - auto-PR: lint autofix나 high-confidence unused cleanup처럼 bounded surface만 허용
4. repo-local sweep 결과는 `quality sweep report` 형식으로 다시 workflow policy에 handoff한다.

## Verification

- `sed -n '1,260p' docs/operations/continuous-quality-feedback-loop.md`
  - 결과: trigger mode, signal taxonomy, detection surface, disposition vocabulary, cleanup handoff minimum이 한 문서에 정리된 것을 확인했다.
- `sed -n '1,220p' docs/operations/quality-sweep-report-template.md`
  - 결과: quality sweep report 필수 필드, disposition vocabulary, minimal example이 canonical artifact로 재사용 가능한 것을 확인했다.
- `sed -n '1,260p' .codex/skills/quality-sweep-triage/SKILL.md`
  - 결과: quality sweep trigger, required evidence, disposition handoff, `request-intake -> issue-to-exec-plan` 연결이 thin-layer skill에 포함된 것을 확인했다.
- `rg -n "continuous quality|quality sweep|coding-rule-drift|duplication-drift|unused-code-drift|quality-sweep-triage" docs .codex`
  - 결과: operations, architecture, product, skill registry, active exec plan이 같은 vocabulary와 hook을 공유하는 것을 확인했다.
- representative quality signal simulation 2건
  - 결과: `GRC-02`의 lint warning debt는 `coding-rule-drift -> cleanup-pr-candidate`로, `GRW-04`의 unused ranking prefetch 경로는 `unused-code-drift -> cleanup-pr-candidate`로 현재 policy에 대입 가능함을 확인했다.
- current repo structure review
  - 결과: backend는 local Gradle project와 existing `quality-gate.yml`을 이미 갖고 있어 repo-local GC lane 확장에 적합했다.
  - 결과: frontend는 remote `README.md`, `package.json`, existing `ci.yml` 기준으로 repo-local npm script + GitHub Actions 확장이 가장 자연스러웠고, 현재 workflow worktree에는 local frontend checkout이 없으므로 implementation 전 worktree 준비가 필요함을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- `gh issue view --repo alexization/git-ranker-workflow 60 --json body,title,number`
  - 결과: Issue `#60` 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - workflow 저장소 문서/skill 전용 변경
  - GitHub Issue `#60`
  - feature branch `feat/grw-23-continuous-quality-feedback-loop`
- Command: `sed -n '1,260p' docs/operations/continuous-quality-feedback-loop.md`
  - Status: `passed`
  - Evidence: trigger mode, signal taxonomy, detection surface, disposition, cleanup handoff minimum이 포함됐다.
- Command: `sed -n '1,220p' docs/operations/quality-sweep-report-template.md`
  - Status: `passed`
  - Evidence: quality sweep report 필수 필드와 example이 canonical template로 정리됐다.
- Command: `sed -n '1,260p' .codex/skills/quality-sweep-triage/SKILL.md`
  - Status: `passed`
  - Evidence: cleanup candidate, guardrail follow-up, repair-now triage와 handoff가 skill에 반영됐다.
- Command: `rg -n "continuous quality|quality sweep|coding-rule-drift|duplication-drift|unused-code-drift|quality-sweep-triage" docs .codex`
  - Status: `passed`
  - Evidence: architecture, operations, product, skills registry, exec plan이 같은 hook을 참조한다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: formatting 오류가 없다.
- Command: `gh issue view --repo alexization/git-ranker-workflow 60 --json body,title,number`
  - Status: `passed`
  - Evidence: issue body render가 깨지지 않았다.
- Failure summary: 없음
- Next action: 사용자 검토 또는 후속 independent review handoff

## Evidence

- current harness coverage와 gap 검토 결과
- continuous quality feedback policy 본문
- quality sweep report template 본문
- quality sweep triage skill 본문
- 관련 hook 문서 grep 결과
- representative quality signal simulation 2건
  - `docs/exec-plans/completed/2026-03-26-grc-02-frontend-lint-debt.md`: `coding-rule-drift -> cleanup-pr-candidate`
  - `docs/exec-plans/completed/2026-03-25-grw-04-frontend-routes-data-flow-docs.md`: `unused-code-drift -> cleanup-pr-candidate`
- current repo structure review
  - backend local `build.gradle`, `.github/workflows/quality-gate.yml`
  - frontend remote `README.md`, `package.json`, `.github/workflows/ci.yml`
- `git diff --check` 결과
- GitHub Issue `#60` body render 확인 결과

## Risks or Blockers

- quality sweep을 verification completion gate처럼 오해하게 쓰면 기존 완료 semantics가 흔들릴 수 있다.
- runtime automation이 없는 상태에서 "자동 PR 생성"을 과장하면 source of truth와 실제 구현이 어긋날 수 있다.
- duplication/unused code detector는 repo별 도구 의존성이 달라 workflow 문서가 구현 세부를 과도하게 소유하면 boundary가 무너진다.

## Next Preconditions

- `GRB-05`: backend repo-local GC baseline 정렬
- `GRC-06`: frontend repo-local GC baseline 정렬
- frontend 구현 전 local worktree 준비 또는 remote canonical source 기반 planning 고정
- cleanup PR publish automation은 low-risk autofix surface가 검증된 뒤 별도 runtime/CI work item으로 분리

## Docs Updated

- `.codex/skills/README.md`
- `.codex/skills/quality-sweep-triage/SKILL.md`
- `docs/architecture/harness-system-map.md`
- `docs/operations/README.md`
- `docs/operations/continuous-quality-feedback-loop.md`
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/quality-sweep-report-template.md`
- `docs/operations/workflow-governance.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/active/2026-04-08-grw-23-continuous-quality-feedback-loop.md`

## Independent Review

- 이번 턴에서는 session-isolated reviewer pool을 실행하지 않았다.
- 따라서 canonical independent review evidence와 `Completed` close-out은 아직 남아 있다.

## Skill Consideration

이번 작업은 canonical policy와 thin-layer skill을 함께 추가해 continuous quality feedback loop를 workflow control plane에 반영하는 일이다. skill은 policy를 대체하지 않고, quality sweep 결과를 cleanup candidate 또는 guardrail follow-up으로 분류하는 반복 절차만 담당한다.
