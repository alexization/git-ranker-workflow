# Failure-To-Guardrail Feedback Loop

이 문서는 언제 feedback close-out이 필요한가와 이 failure를 어떤 guardrail로 승격할 것인가를 고정한다.

## Policy Invariants

- feedback close-out은 모든 성공 경로의 공통 의무가 아니다.
- latest verification이 통과했고 blocker, 반복 실패, systemic gap이 없으면 feedback 단계 없이 완료할 수 있다.
- feedback close-out은 verification과 review를 대체하지 않는다.
- ledger entry는 root cause 하나당 하나씩 남긴다.
- 승격 대상은 `docs-rule`, `skill`, `test`, `ci`, `template`, `no-new-guardrail` 여섯 가지로 고정한다.

## Feedback Trigger Rules

아래 중 하나라도 해당하면 feedback close-out을 남긴다.

- verification이 `failed` 또는 `blocked`로 끝났다
- independent review가 `changes-requested` 또는 `blocked`를 남겼다
- 같은 root cause가 한 작업 안에서 반복됐다
- 이번 작업 중 guardrail promotion, cleanup candidate, follow-up policy asset이 필요하다고 판단했다
- 사용자가 회고, postmortem, guardrail 정리를 명시적으로 요청했다

## Feedback Entry Preconditions

- approved spec
- latest verification evidence 또는 `Blocked` 이유
- latest review verdict 또는 review skipped reason
- repair attempt 요약 필요 시
- 남은 리스크, skipped check, failure note

## Failure Taxonomy

| Failure class | Typical signal | Primary stage |
| --- | --- | --- |
| `intake-scope` | request가 single spec으로 고정되지 않음, non-goal 누락, subtask split 미정 | `Routed`, `Interviewing`, `Spec Drafting` |
| `context-boundary` | 잘못된 context pack, sibling repo eager load, boundary 위반 | `Context Ready`, `Implementing` |
| `verification-contract` | latest report 누락, command 불일치, precondition 미기록 | `Verifying`, `Repairing` |
| `review-handoff` | reviewer input 누락, diff/report mismatch, finding 분류 drift | `Reviewing` |
| `behavior-regression` | correctness, contract, reliability regression이 늦게 발견됨 | `Implementing`, `Verifying`, `Reviewing` |
| `evidence-closeout` | source-of-truth update 누락, artifact 위치 불명확 | `Publishing`, `User Validating`, `Completed` |
| `external-dependency` | Docker, port, credential, remote outage, missing worktree | 어느 단계든 |

## Guardrail Promotion Decision

| Decision | Choose when |
| --- | --- |
| `docs-rule` | canonical rule, vocabulary, evidence minimum이 비어 있거나 충돌한다 |
| `skill` | canonical rule은 있지만 같은 실행 순서나 handoff가 반복적으로 흔들린다 |
| `test` | regression을 결정론적으로 재현하고 막을 수 있다 |
| `ci` | 로컬 deterministic check는 있는데 PR/runtime에서 일관되게 실행되지 않는다 |
| `template` | spec, issue, PR, review body처럼 structured input 자체가 비어 있어 정보 누락이 반복된다 |
| `no-new-guardrail` | 기존 guardrail이 이미 충분하거나 one-off 외부 이슈다 |

## Feedback Close-Out Minimum

`Feedback Pending`을 닫을 때는 spec close-out, review note, follow-up artifact 중 최소 한 곳에 아래가 있어야 한다.

- latest verification 상태 또는 `Blocked` 이유
- latest review verdict 또는 review skipped reason
- ledger entry 하나 이상 또는 `no new guardrail` entry
- promotion decision 근거
- follow-up asset, issue, 또는 `없음` 사유
