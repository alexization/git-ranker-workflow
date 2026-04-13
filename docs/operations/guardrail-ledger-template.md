# Guardrail Ledger Template

이 문서는 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)의 canonical ledger entry 형식을 제공한다. PR 본문에는 요약만 둘 수 있고, canonical entry는 spec close-out, review note, follow-up artifact 중 하나에 아래 최소 필드로 남긴다.

## Entry Template

```md
## Guardrail Ledger Entry
- Date:
- Task / Spec:
- Stage:
  - `Interviewing | Spec Drafting | Spec Approved | Context Ready | Implementing | Verifying | Reviewing | Feedback Pending | User Validating | Blocked`
- Failure class:
  - `intake-scope | context-boundary | verification-contract | review-handoff | behavior-regression | evidence-closeout | external-dependency`
- Trigger signal:
- Root cause:
- Existing guardrail:
- Recurrence:
  - `first-seen | repeated | systemic`
- Current issue disposition:
  - `repaired-in-scope | approved-with-note | blocked | follow-up-needed`
- Promotion decision:
  - `docs-rule | skill | test | ci | template | no-new-guardrail`
- Guardrail status:
  - `applied-now | follow-up-created | deferred | no-new-guardrail`
- Decision rationale:
- Guardrail change or follow-up asset:
- Owner / next action:
- Evidence:
- Notes:
```

## Writing Rules

- 한 entry에는 root cause 하나만 적는다.
- `Trigger signal`은 symptom이고, `Root cause`는 반복될 이유다.
- `Existing guardrail`에는 이미 있던 policy, template, test, CI, skill이 있으면 적고, 없으면 `없음`이라고 적는다.
- `Promotion decision`과 `Guardrail status`를 함께 적어 무엇으로 승격할지와 이번 작업에서 적용됐는지를 분리한다.
- `no-new-guardrail`을 고르면 `Decision rationale`에 왜 추가 guardrail이 필요 없는지 반드시 적는다.

## Minimal Example

```md
## Guardrail Ledger Entry
- Date: `2026-04-07`
- Task / Spec: `docs/specs/completed/2026-04-07-sample.md`
- Stage:
  - `Reviewing`
- Failure class:
  - `review-handoff`
- Trigger signal: reviewer input에 latest verification evidence 요약이 비어 있었다.
- Root cause: review handoff minimum이 close-out 형식에서 강제되지 않았다.
- Existing guardrail: `docs/operations/dual-agent-review-policy.md`
- Recurrence:
  - `repeated`
- Current issue disposition:
  - `follow-up-needed`
- Promotion decision:
  - `template`
- Guardrail status:
  - `follow-up-created`
- Decision rationale: structured field가 비어도 PR close-out이 진행돼 handoff 누락이 반복됐다.
- Guardrail change or follow-up asset: `.github/PULL_REQUEST_TEMPLATE.md` follow-up
- Owner / next action: template 정렬 작업에서 reviewer input block을 강화한다.
- Evidence: PR close-out draft와 review note
- Notes: policy는 이미 있었고, 입력 강제가 부족했다.
```
