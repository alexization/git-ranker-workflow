# 2026-04-07-grw-17-failure-to-guardrail-feedback-loop

- Issue ID: `GRW-17`
- GitHub Issue: `#43`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-17-failure-to-guardrail-feedback-loop`
- Task Slug: `2026-04-07-grw-17-failure-to-guardrail-feedback-loop`

## Problem

`Feedback Pending` 상태와 "실패를 guardrail 후보로 승격한다"는 상위 원칙은 이미 source of truth에 있다. 하지만 실제 작업에서 어떤 failure taxonomy를 써야 하는지, 어떤 입력을 feedback ledger에 남겨야 하는지, 어떤 경우에 `문서 규칙`, `skill`, `테스트`, `CI`, `template` 중 하나로 승격해야 하는지, 언제 `no new guardrail`로 닫아도 되는지는 아직 canonical policy로 잠겨 있지 않다.

이 공백이 남아 있으면 verification failure와 review finding이 close-out마다 다른 형식으로 남고, 같은 종류의 실패가 반복돼도 어떤 guardrail을 추가해야 하는지 일관되게 판단할 수 없다. 후속 `guardrail-hardening` skill pack과 pilot issue가 재사용할 feedback loop를 먼저 고정해야 한다.

## Why Now

`GRW-15`와 `GRW-16`까지 완료되면서 verification과 review 단계의 입력과 verdict는 잠겼다. 이제 `Feedback Pending -> Completed` 구간의 close-out 기준을 정리해야 하네스의 happy path와 repair path가 모두 닫힌다.

또한 같은 failure class가 반복될 때 문서, skill, 테스트, CI, template 중 어디로 승격할지를 결정론적으로 남겨야 `GRW-S09`와 `GRW-18`이 공통 입력을 사용할 수 있다.

## Scope

- `docs/operations/`에 failure-to-guardrail feedback loop source of truth를 추가한다.
- failure taxonomy, feedback ledger field, 승격 대상, `no new guardrail` 기준을 정의한다.
- `Feedback Pending -> Completed` 단계에서 필요한 implementer/reviewer input과 close-out 규칙을 문서화한다.
- guardrail ledger template를 별도 문서로 추가한다.
- 관련 architecture/operations/product hook과 exec plan을 갱신한다.

## Non-scope

- 자동 PR 생성, 자동 복구, 자동 CI 생성
- backend/frontend 앱 코드 변경
- `GRW-S09` skill pack 구현
- `.github/` template 구조 변경
- sibling repo inspection을 넘어서는 cross-repo planning 확장

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/` 필요 시
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-07-grw-17-failure-to-guardrail-feedback-loop.md`
  - `docs/exec-plans/completed/2026-04-07-grw-17-failure-to-guardrail-feedback-loop.md`
- Explicitly forbidden:
  - sibling app repo code write
  - `.github/` template 구조 변경
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue body render 확인
- Escalation triggers:
  - 없음. 문서 작업 범위에서 처리한다.

## Outputs

- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- feedback taxonomy, promotion rule, `no new guardrail` close-out rule
- 관련 hook 문서 갱신
- `docs/exec-plans/completed/2026-04-07-grw-17-failure-to-guardrail-feedback-loop.md`

## Working Decisions

- 이번 작업의 primary context pack은 `workflow-docs`다.
- feedback 단계의 canonical source는 `docs/operations/failure-to-guardrail-feedback-loop.md`에 둔다.
- guardrail ledger는 PR/exec plan close-out에서 재사용 가능한 entry template를 별도 문서로 분리한다.
- 승격 대상은 work item catalog의 기본 결정대로 `문서 규칙`, `skill`, `테스트`, `CI`, `template` 다섯 가지로 고정한다.
- 같은 root cause의 반복 여부와 현재 issue 내부 수리 가능성은 `GRW-15`의 repair loop semantics와 `GRW-16`의 review verdict 규칙을 재사용해 판정한다.
- stable source of truth 문서에는 task ID를 follow-up 설명용으로 남기지 않는다.

## Verification

- `sed -n '1,320p' docs/operations/failure-to-guardrail-feedback-loop.md`
  - 결과: failure taxonomy, ledger flow, 승격 규칙, `no new guardrail` 기준, close-out minimum이 한 문서에 정리된 것을 확인했다.
- `sed -n '1,220p' docs/operations/guardrail-ledger-template.md`
  - 결과: ledger entry 최소 필드, status vocabulary, 예시 형식이 reviewer/implementer handoff에 재사용 가능한 것을 확인했다.
- `rg -n "feedback|guardrail|ledger|no new guardrail|failure taxonomy|Feedback Pending" docs/operations docs/architecture docs/product docs/exec-plans`
  - 결과: 새 policy와 인접 hook이 operations/architecture/product/exec plan에서 함께 grep되는 것을 확인했다.
- 과거 failure 사례 2~3개 수동 분류
  - 결과: 아래 `Representative Past Failure Classification`에 기록한 세 사례 모두 taxonomy와 ledger template로 승격 대상을 분류할 수 있음을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- GitHub Issue `#43` body render 확인
  - 결과: issue 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- feedback loop policy 본문
- ledger template 본문
- 과거 failure 사례 분류 결과
- 관련 hook 문서 갱신 결과
- `git diff --check` 결과
- GitHub Issue `#43` body 검증 결과

## Independent Review

- Not run
- Reason: GitHub PR `#44` merge 시점에 reviewer pool evidence가 이 plan에 남지 않았고, `GRW-18`에서는 historical snapshot을 retroactive reviewer output으로 다시 쓰지 않는다.

## Representative Past Failure Classification

| Source | Failure class | Promotion decision | Why |
| --- | --- | --- | --- |
| `docs/exec-plans/completed/2026-04-06-grw-19-harness-issue-pr-template-alignment.md` | `evidence-closeout` | `template` | Issue/PR close-out에서 verification, review, feedback 필드가 부족해 structured input 누락이 반복될 수 있었기 때문이다. |
| `docs/exec-plans/completed/2026-04-07-grw-15-verification-contract-registry-repair-loop-policy.md` | `verification-contract` | `docs-rule` | 저장소별 verification entrypoint와 report shape를 잠그는 canonical registry가 없어서 completion semantics가 흔들렸기 때문이다. |
| `docs/exec-plans/completed/2026-04-07-grw-16-dual-agent-review-policy.md` | `review-handoff` | `docs-rule` | implementer/reviewer 분리, reviewer input, verdict 기준 자체가 source of truth로 고정되지 않아 self-approval과 review drift 위험이 있었기 때문이다. |

## Risks or Blockers

- failure taxonomy를 너무 세분화하면 implementer/reviewer가 실제 close-out에서 일관되게 적용하기 어려워질 수 있다.
- 승격 규칙이 review/verification retry semantics와 충돌하면 같은 failure가 repair 대상인지, follow-up guardrail 대상인지 구분이 흐려질 수 있다.
- template와 skill을 지금 같이 구현하면 `GRW-S09` 범위를 잠식하므로, 이번 작업은 policy와 ledger template까지만 잠근다.
- 독립 reviewer evidence는 merge 당시 이 plan에 남지 않았고, 이 completed snapshot은 그 historical gap을 그대로 보존한다.

## Next Preconditions

- `GRW-S09`: guardrail-hardening skill pack
- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증

## Docs Updated

- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- `docs/operations/README.md`
- `docs/operations/workflow-governance.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/exec-plans/completed/2026-04-07-grw-17-failure-to-guardrail-feedback-loop.md`

## Close-out Reconciliation

- GitHub Issue `#43`는 `2026-04-07`에 `closed` (`state_reason=completed`) 상태가 됐다.
- GitHub PR `#44`는 `2026-04-07`에 `merged` 됐다.
- source-of-truth 산출물은 이미 merge된 상태였지만 exec plan 파일이 `active/`에 남아 있어, `GRW-18` pilot에서 stale active record를 `completed/` historical record로 정리했다.
- 이 reconciliation은 policy 본문이나 당시 verification evidence를 다시 쓰지 않고, 상태와 보관 위치만 현재 GitHub state에 맞췄다.

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 대신 후속 `guardrail-ledger-update`, `failure-to-policy` skill이 그대로 재사용할 수 있도록 failure taxonomy, ledger field, 승격 규칙, `no new guardrail` close-out을 source of truth로 먼저 고정한다.
