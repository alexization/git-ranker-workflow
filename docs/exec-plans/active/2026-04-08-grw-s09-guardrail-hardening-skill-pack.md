# 2026-04-08-grw-s09-guardrail-hardening-skill-pack

- Issue ID: `GRW-S09`
- GitHub Issue: `#58`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s09-guardrail-hardening-skill-pack`
- Task Slug: `2026-04-08-grw-s09-guardrail-hardening-skill-pack`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`GRW-17`에서 failure taxonomy, promotion decision, recurrence rule, `no-new-guardrail` 기준, guardrail ledger entry 최소 필드가 source of truth로 고정됐다. 하지만 implementer가 feedback close-out에서 이 규칙을 같은 입력과 순서로 적용하게 만드는 project-local skill pack은 아직 없다.

이 상태에서는 verification failure, review finding, blocked reason을 어떤 root cause로 정규화할지와 어떤 guardrail 자산으로 승격할지를 작업자마다 매번 다시 조립해야 한다. 그 결과 ledger entry 품질, promotion decision, follow-up asset 기록이 흔들리고, `GRW-18` pilot도 공통 feedback surface를 재사용하기 어렵다.

## Why Now

`GRW-S08`으로 verification report와 reviewer handoff 절차까지 operationalize됐고, 이제 마지막으로 feedback close-out thin layer를 추가해야 Phase 2 skill pack이 닫힌다. `GRW-S09`는 `guardrail-ledger-update`와 `failure-to-policy`를 통해 root cause normalization, recurrence 확인, promotion decision, `no-new-guardrail` 예외 판단을 같은 입력/출력/증거 형식으로 고정해야 한다.

또한 `GRW-17` exec plan이 policy와 ledger template를 먼저 잠그고 template/skill 구현은 후속 `GRW-S09` 범위로 남겨 두었으므로, 이번 작업이 그 후속 구현 슬롯을 정확히 닫는다.

## Scope

- `.codex/skills/guardrail-ledger-update/SKILL.md` 작성
- `.codex/skills/failure-to-policy/SKILL.md` 작성
- `.codex/skills/guardrail-ledger-update/checklists/feedback-closeout-minimum.md` 추가
- `.codex/skills/README.md`에 새 skill registry와 feedback 단계 hook 반영
- `GRW-S09` exec plan 작성과 close-out 기록 정리

## Non-scope

- `docs/operations/` feedback policy 재설계
- backend/frontend 앱 코드 또는 verification contract 변경
- 자동 CI 생성, GitHub automation, runtime 스크립트 추가
- `GRW-18` pilot 자체 수행
- stable source of truth에 task ID를 설명용으로 추가하는 문서 개편

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-s09-guardrail-hardening-skill-pack.md`
  - `docs/exec-plans/completed/2026-04-08-grw-s09-guardrail-hardening-skill-pack.md`
  - `/tmp/grw-s09-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/`, `docs/product/`의 policy 재설계
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음

## Outputs

- `.codex/skills/guardrail-ledger-update/SKILL.md`
- `.codex/skills/guardrail-ledger-update/checklists/feedback-closeout-minimum.md`
- `.codex/skills/failure-to-policy/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-s09-guardrail-hardening-skill-pack.md`

## Working Decisions

- canonical rule은 계속 `docs/operations/failure-to-guardrail-feedback-loop.md`와 `docs/operations/guardrail-ledger-template.md`가 소유하고, skill은 이를 thin layer로 operationalize한다.
- `guardrail-ledger-update`는 feedback entry precondition 확인, root cause normalization, ledger entry 작성, evidence minimum 점검을 담당한다.
- `failure-to-policy`는 failure taxonomy 분류, recurrence rule 확인, promotion decision 선택, `no-new-guardrail` 예외 판단, follow-up asset 결정 절차를 담당한다.
- checklist는 template 대체가 아니라 feedback close-out 전에 빠뜨리기 쉬운 필수 입력과 금지 누락을 재확인하는 지원 자산으로만 둔다.
- `.codex/skills/README.md`에는 task ID가 아니라 asset 이름과 feedback hook만 반영한다.

## Verification

- `find .codex/skills -maxdepth 3 -type f | sort`
  - 결과: `guardrail-ledger-update`, `failure-to-policy`, checklist, registry 업데이트가 기대 경로에 생성된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/guardrail-ledger-update/SKILL.md`
  - 결과: entry precondition, root cause normalization, output location, required evidence, `failure-to-policy` handoff가 포함된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/failure-to-policy/SKILL.md`
  - 결과: failure taxonomy, recurrence 확인, promotion decision, `no-new-guardrail` 예외, follow-up handoff가 포함된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/guardrail-ledger-update/checklists/feedback-closeout-minimum.md`
  - 결과: feedback close-out 입력, 누락 금지 항목, `no-new-guardrail` 판단 확인 포인트가 checklist로 재사용 가능한 것을 확인했다.
- `sed -n '1,260p' .codex/skills/README.md`
  - 결과: 새 skill registry와 feedback 단계 hook이 반영된 것을 확인했다.
- `rg -n "guardrail-ledger-update|failure-to-policy|guardrail ledger|feedback close-out|Promotion decision|no-new-guardrail" .codex/skills docs/operations`
  - 결과: skill 본문과 canonical source가 같은 vocabulary와 hook을 재사용하는 것을 확인했다.
- representative failure 사례 수동 시뮬레이션 2건
  - 결과: `GRW-19`의 template field 누락 사례는 `evidence-closeout -> template`로, `GRW-S08`의 verification/review handoff 수동 조립 사례는 `evidence-closeout -> skill`로 좁혀져 ledger entry와 promotion decision handoff를 재현할 수 있음을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- `gh issue view --repo alexization/git-ranker-workflow 58 --json body,title,number`
  - 결과: Issue `#58` 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - workflow 저장소의 skill/doc 전용 변경
  - GitHub Issue `#58`, feature branch, active exec plan이 준비됨
- Command: `find .codex/skills -maxdepth 3 -type f | sort`
  - Status: `passed`
  - Evidence: 새 skill 2종과 checklist가 기대 경로에 생성됐다.
- Command: `sed -n '1,260p' .codex/skills/guardrail-ledger-update/SKILL.md`
  - Status: `passed`
  - Evidence: entry precondition, root cause normalization, ledger entry output, `failure-to-policy` handoff가 포함됐다.
- Command: `sed -n '1,260p' .codex/skills/failure-to-policy/SKILL.md`
  - Status: `passed`
  - Evidence: failure taxonomy, recurrence, promotion decision, `no-new-guardrail` 예외가 포함됐다.
- Command: `sed -n '1,220p' .codex/skills/guardrail-ledger-update/checklists/feedback-closeout-minimum.md`
  - Status: `passed`
  - Evidence: feedback close-out 입력, entry quality, decision guard, close-out hook이 checklist로 정리됐다.
- Command: `sed -n '1,260p' .codex/skills/README.md`
  - Status: `passed`
  - Evidence: 새 skill registry와 feedback 단계 hook이 반영됐다.
- Command: `rg -n "guardrail-ledger-update|failure-to-policy|guardrail ledger|feedback close-out|Promotion decision|no-new-guardrail" .codex/skills docs/operations`
  - Status: `passed`
  - Evidence: 새 skill과 canonical source가 같은 vocabulary와 hook을 재사용한다.
- Command: `gh issue view --repo alexization/git-ranker-workflow 58 --json body,title,number`
  - Status: `passed`
  - Evidence: Issue `#58` 본문이 template 섹션과 줄바꿈을 유지한 채 생성됐다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: whitespace 또는 patch formatting 오류가 없다.
- Failure summary: 없음
- Next action: independent review 준비

## Evidence

- skill 본문 2종
- feedback close-out checklist
- registry 업데이트 결과
- representative failure 사례 수동 시뮬레이션 결과
  - `GRW-19`: template field 누락 문제를 `evidence-closeout -> template`로 재현할 수 있었다.
  - `GRW-S08`: verification/review handoff 수동 조립 병목을 `evidence-closeout -> skill`로 재현할 수 있었다.
- GitHub Issue `#58` body 확인 결과
- `git diff --check` 결과

## Risks or Blockers

- skill이 policy 표를 길게 복사하면 source of truth drift가 생길 수 있다.
- checklist가 template처럼 비대해지면 thin-layer skill pack 범위를 벗어날 수 있다.
- recurrence rule과 `no-new-guardrail` 예외를 잘못 압축하면 승격 판단이 느슨해질 수 있다.
- 현재 세션에서는 sub-agent reviewer pool을 아직 실행하지 않았으므로 `Completed` close-out용 independent review evidence는 아직 비어 있다.

## Next Preconditions

- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증

## Docs Updated

- `.codex/skills/guardrail-ledger-update/SKILL.md`
- `.codex/skills/guardrail-ledger-update/checklists/feedback-closeout-minimum.md`
- `.codex/skills/failure-to-policy/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/active/2026-04-08-grw-s09-guardrail-hardening-skill-pack.md`

## Skill Consideration

이번 Issue 자체가 feedback close-out thin-layer skill pack을 추가하는 작업이다. 새 skill은 policy를 대체하지 않고, feedback close-out을 같은 입력/출력/증거 규칙으로 반복 가능하게 만드는 실행 레시피에 집중한다.
