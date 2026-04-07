# 2026-04-07-grw-s08-verification-review-loop-skill-pack

- Issue ID: `GRW-S08`
- GitHub Issue: `#56`
- Status: `In Progress`
- Repository: `git-ranker-workflow`
- Branch Name: `feat-grw-s08-verification-review-loop-skill-pack`
- Task Slug: `2026-04-07-grw-s08-verification-review-loop-skill-pack`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`GRW-15`, `GRW-16`, `GRW-21`, `GRW-22`까지 source of truth에는 verification contract, repair loop, reviewer minimum context, sub-agent reviewer pool, verdict aggregation 규칙이 고정됐다. 하지만 implementer가 이 규칙을 실제 작업에서 반복 가능한 절차로 실행하게 만드는 project-local skill pack은 아직 없다.

이 공백이 남아 있으면 verification report 작성, repair triage, reviewer pool handoff가 매번 수동으로 조립되고, reviewer들이 같은 minimum context를 다시 읽으면서도 같은 aggregation 근거를 매번 새로 정리해야 한다. 그 결과 independent review는 느려지고, issue마다 verification/review close-out 품질도 흔들릴 수 있다.

## Why Now

사용자는 sub-agent 기반 검증 시간이 너무 오래 걸리는 이유를 먼저 검토해 달라고 요청했고, 원인 분석 결과 현재 병목은 policy 부재보다 `reviewer-handoff`와 verification close-out을 얇게 operationalize하는 skill 부재에 더 가깝다는 점이 드러났다.

`GRW-S08`은 `verification-contract-runner`, `repair-loop-triage`, `reviewer-handoff`를 source of truth의 thin layer로 추가해 implementer와 reviewer가 같은 입력/출력/증거 surface를 재사용하게 만들어야 한다. 그래야 이후 `GRW-18` pilot에서 verification/review 시간이 실제로 줄었는지 비교할 수 있다.

## Scope

- `.codex/skills/verification-contract-runner/SKILL.md` 작성
- `.codex/skills/repair-loop-triage/SKILL.md` 작성
- `.codex/skills/reviewer-handoff/SKILL.md` 작성
- `.codex/skills/README.md`에 새 skill registry와 recommended use 반영
- 필요 시 `.codex/skills/authoring-rules.md` 또는 기존 skill 문서의 최소 hook 정리
- `GRW-S08` active exec plan 작성과 close-out 기록 정리

## Non-scope

- backend/frontend 앱 코드 변경
- 테스트 프레임워크, CI, 외부 reviewer runtime 인프라 추가
- `docs/operations/` policy 재설계
- `GRW-18` pilot 자체 수행
- formal benchmark automation 구현

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-07-grw-s08-verification-review-loop-skill-pack.md`
  - `docs/exec-plans/completed/2026-04-07-grw-s08-verification-review-loop-skill-pack.md`
  - `/tmp/grw-s08-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/`, `docs/product/`의 범위 밖 stable source of truth mass update
  - sub-agent runtime implementation code 추가
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - branch 생성 또는 GitHub issue 확인에 필요한 git/gh command

## Outputs

- `.codex/skills/verification-contract-runner/SKILL.md`
- `.codex/skills/repair-loop-triage/SKILL.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-07-grw-s08-verification-review-loop-skill-pack.md`

## Working Decisions

- canonical rule은 계속 `docs/operations/verification-contract-registry.md`와 `docs/operations/dual-agent-review-policy.md`가 소유하고, skill은 이를 thin layer로 operationalize한다.
- `reviewer-handoff`는 reviewer minimum context 다섯 가지를 한 번에 fan-out하고, role prompt와 aggregation evidence만 얇게 추가한다.
- `verification-contract-runner`는 실제 명령을 새로 발명하지 않고 contract selection, required/conditional command, verification report shape를 재사용한다.
- `repair-loop-triage`는 retry budget과 `failed`/`blocked`/follow-up split 기준을 요약하는 절차만 맡는다.
- representative handoff 입력을 기준으로 간단한 timing breakdown을 evidence에 남겨, 이후 pilot의 전후 비교 기준으로 재사용한다.

## Verification

- `find .codex/skills -maxdepth 2 -type f | sort`
  - 결과: `.codex/skills/verification-contract-runner/SKILL.md`, `.codex/skills/repair-loop-triage/SKILL.md`, `.codex/skills/reviewer-handoff/SKILL.md`가 registry 문서와 함께 기대 경로에 생성된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/verification-contract-runner/SKILL.md`
  - 결과: contract selection, required/conditional command, verification report shape, reviewer handoff input이 포함된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/repair-loop-triage/SKILL.md`
  - 결과: verification failure와 review finding을 current issue repair, `Blocked`, follow-up split으로 좁히는 triage 절차와 retry budget 규칙이 포함된 것을 확인했다.
- `sed -n '1,300p' .codex/skills/reviewer-handoff/SKILL.md`
  - 결과: reviewer minimum context 다섯 가지, reviewer role focus, fan-out, aggregation evidence가 포함된 것을 확인했다.
- `sed -n '1,240p' .codex/skills/README.md`
  - 결과: 새 skill registry와 구현 뒤 close-out hook 순서가 현재 source of truth와 충돌하지 않는 것을 확인했다.
- `rg -n "verification-contract-runner|repair-loop-triage|reviewer-handoff|Reviewer Minimum Context|verification report|retry budget|role prompt|aggregation" .codex/skills docs/operations`
  - 결과: skill 본문이 canonical source의 용어와 hook을 재사용하고, `reviewer-handoff` thin-layer hook이 policy 문서와 함께 grep되는 것을 확인했다.
- representative input 수동 시뮬레이션
  - 결과: sample exec plan, sample verification report, sample diff summary 기준으로 `verification-contract-runner`가 latest report를 만들고, `repair-loop-triage`가 failed/blocked 여부를 좁히며, `reviewer-handoff`가 passed report 이후 minimum context를 reviewer pool에 fan-out하는 순서를 재현할 수 있음을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류 없이 통과했다.
- GitHub Issue `#56` body render 확인
  - 결과: Issue `#56` 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Evidence

- skill 본문 3종
- registry 업데이트 결과
- representative input 시뮬레이션 결과
- timing breakdown 메모
  - 구현 전 반복 병목은 verification report 수동 조립, reviewer minimum context fan-out, aggregation evidence 수동 정리에 있었다.
  - 이번 skill pack은 이 세 단계를 문서형 handoff로 고정해 이후 pilot에서 전후 시간을 비교할 기준을 만든다.
- GitHub Issue `#56` body 확인 결과
- `git diff --check` 결과

## Risks or Blockers

- skill이 policy 표를 길게 복사하면 source of truth drift가 생길 수 있다.
- reviewer-handoff가 minimum context를 과도하게 축약하면 canonical review path를 훼손할 수 있다.
- timing breakdown은 first-pass 메모 수준이므로, 실제 개선 폭은 `GRW-18` pilot에서 다시 확인해야 한다.
- independent review evidence는 아직 작성되지 않았다. 이 exec plan은 구현과 local verification까지 진행했고 review close-out은 다음 단계로 남아 있다.

## Next Preconditions

- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증
- `GRW-S09`: 반복 failure를 guardrail 승격 규칙으로 연결

## Docs Updated

- `.codex/skills/verification-contract-runner/SKILL.md`
- `.codex/skills/repair-loop-triage/SKILL.md`
- `.codex/skills/reviewer-handoff/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/active/2026-04-07-grw-s08-verification-review-loop-skill-pack.md`

## Skill Consideration

이번 Issue 자체가 verification/review-loop skill pack을 추가하는 작업이다. 새 skill은 policy 문서를 대체하지 않고, verification, repair, reviewer handoff를 같은 입력/출력/증거 규칙으로 반복 가능하게 만드는 실행 레시피에 집중한다.
