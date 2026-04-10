# Failure-To-Guardrail Feedback Loop

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 optional `Feedback Pending` semantics를 실제 close-out 규칙으로 고정한다. [verification-contract-registry.md](verification-contract-registry.md)가 verification의 pass/fail과 repair budget을 잠그고, [dual-agent-review-policy.md](dual-agent-review-policy.md)가 review verdict와 reviewer evidence를 잠근다면, 이 문서는 "언제 feedback close-out이 필요한가"와 "이 failure를 어떤 guardrail로 승격할 것인가"를 잠근다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md)를 따른다.

## Policy Invariants

- feedback close-out은 모든 성공 경로의 공통 의무가 아니다.
- latest verification이 통과했고 blocker, 반복 실패, systemic gap이 없으면 feedback 단계 없이 완료할 수 있다.
- feedback close-out은 verification과 review를 대체하지 않는다. in-scope repair가 아직 남아 있으면 feedback으로 우회 종료하지 않는다.
- ledger entry는 root cause 하나당 하나씩 남긴다. 서로 다른 failure class를 한 entry에 섞지 않는다.
- 같은 root cause가 반복되면 다음 턴에는 guardrail 승격 여부가 반드시 결정돼야 한다.
- 승격 대상은 `docs-rule`, `skill`, `test`, `ci`, `template`, `no-new-guardrail` 여섯 가지로 고정한다.
- deterministic check로 막을 수 있는 regression은 가능하면 `test` 또는 `ci`로 올린다.

## Feedback Trigger Rules

아래 중 하나라도 해당하면 feedback close-out을 남긴다.

- verification이 `failed` 또는 `blocked`로 끝났다
- independent review가 `changes-requested` 또는 `blocked`를 남겼다
- 같은 root cause가 한 작업 안에서 반복됐다
- 이번 작업 중 guardrail promotion, cleanup candidate, follow-up policy asset이 필요하다고 판단했다
- 사용자가 회고, postmortem, guardrail 정리를 명시적으로 요청했다

아래는 기본적으로 feedback close-out 없이 끝낼 수 있다.

- latest verification이 통과한 low-risk 작업
- non-blocking note만 남은 docs/editorial change
- current diff 안에서 필요한 guardrail이 이미 자연스럽게 같이 해결됐고 추가 기록 가치가 낮은 one-off note

## Feedback Entry Preconditions

feedback close-out을 시작할 때 최소한 아래 입력이 있어야 한다.

- task brief 또는 exec plan
- latest verification report 또는 `Blocked` 이유
- latest review verdict 또는 review를 생략한 이유
- repair attempt 요약 필요 시
- 남은 리스크, skipped check, failure note

추가 규칙:

- `Rejected`와 `conversation-only` close-out은 feedback ledger 대상이 아니다.
- review를 수행하지 않은 작업이라면 `latest review verdict` 대신 `review skipped` 이유를 적을 수 있다.
- 현재 issue 안에서 이미 guardrail을 함께 추가했다면, 그 사실도 feedback entry에 남긴다.

## Root Cause Normalization Rule

feedback entry를 쓰기 전 failure를 아래 순서로 정리한다.

1. 가장 최근의 verification failure, review finding, blocked reason을 모은다.
2. 원인이 다른 항목은 분리한다.
3. "무엇이 실패했는가"보다 "왜 같은 실수가 다시 생길 수 있는가"를 root cause로 적는다.
4. 현재 issue 안에서 이미 해결된 구현 버그와, 다음 guardrail로 남겨야 할 시스템 문제를 구분한다.

예시:

- `git diff --check` 실패와 reviewer input 누락은 서로 다른 root cause이므로 entry를 나눈다.
- 동일한 verification command를 두 번 빠뜨린 문제는 command 이름이 아니라 "verification handoff shape 미고정"으로 묶는다.

## Failure Taxonomy

| Failure class | Typical signal | Primary stage | Default question |
| --- | --- | --- | --- |
| `intake-scope` | request가 한 issue나 task brief로 고정되지 않음, write scope drift, non-scope 누락 | `Routed`, `Interviewing`, `Scoped`, `Planned` | intake rule이나 planning template가 failure를 더 일찍 막았어야 하는가 |
| `context-boundary` | 잘못된 context pack 선택, sibling repo eager load, boundary 위반, scope 밖 수정 시도 | `Context Ready`, `Implementing` | boundary rule을 문서나 skill로 더 좁혀야 하는가 |
| `verification-contract` | latest report 누락, command 불일치, precondition 미기록, retry budget 해석 drift | `Verifying`, `Repairing` | verification registry, runner skill, template 중 무엇이 비어 있었는가 |
| `review-handoff` | self-approval, reviewer input 누락, diff/report mismatch, finding 분류 drift | `Reviewing` | review policy만으로 충분한가, handoff shape를 template나 skill로 더 강제해야 하는가 |
| `behavior-regression` | correctness, contract, reliability regression이 늦게 발견됨 | `Implementing`, `Verifying`, `Reviewing` | deterministic test나 CI check가 있어야 했는가 |
| `evidence-closeout` | source-of-truth update 누락, artifact/evidence 위치 불명확 | `Publishing`, `Completed` | close-out template나 docs rule이 더 강해야 하는가 |
| `external-dependency` | Docker, port, credential, remote outage, missing worktree처럼 현재 scope 밖 환경 문제가 막음 | `Scoped` 이후 어느 단계든 | harness 내부 guardrail로 줄일 수 있는 부분이 있는가 |

## Guardrail Promotion Decision

### Decision Targets

| Decision | Choose when | Typical output |
| --- | --- | --- |
| `docs-rule` | canonical rule, vocabulary, stop condition, evidence minimum이 비어 있거나 서로 충돌한다 | policy, registry, runbook, README hook |
| `skill` | canonical rule은 있지만 같은 순서의 실행, triage, handoff가 반복적으로 흔들린다 | skill, checklist, handoff recipe |
| `test` | product or contract regression을 저장소 안에서 결정론적으로 재현하고 막을 수 있다 | unit, integration, e2e, contract test |
| `ci` | 로컬 deterministic check는 있는데 PR/runtime에서 일관되게 실행되지 않는다 | CI job, required check, automation gate |
| `template` | issue, PR, exec plan, review body처럼 structured input 자체가 비어 있어 정보 누락이 반복된다 | template field, body section, form change |
| `no-new-guardrail` | 기존 guardrail이 이미 충분하고 이번 case가 one-off 외부 이슈이거나, 현재 issue 안에서 필요한 guardrail이 이미 추가됐다 | explicit rationale only |

### Selection Rules

1. 같은 failure를 가장 이른 단계에서 막을 수 있는 자산을 먼저 고른다.
2. 여러 자산이 가능하면 가장 작은 변경으로 반복을 끊는 쪽을 고른다.
3. rule 자체가 비어 있으면 `skill`, `template`, `test`, `ci`보다 먼저 `docs-rule`을 본다.
4. rule은 있는데 실행 순서가 빠지는 문제면 `skill` 또는 `template`을 본다.
5. behavior regression이라면 문서 설명보다 `test`를 우선한다.
6. local test가 이미 있는데 "실행 안 됨"이 root cause면 `ci`를 우선한다.
7. `template`은 입력 누락 문제에만 쓴다.

## Recurrence Rule

- 첫 발생이어도 blast radius가 크거나 필수 close-out field가 비어 있으면 즉시 승격할 수 있다.
- 같은 root cause가 두 번 관측되면 `no-new-guardrail`은 예외 사유가 있어야만 가능하다.
- 같은 root cause가 세 번 이상 반복되거나 둘 이상의 task type에 걸치면, automation이 가능한 경우 `docs-rule`만으로 닫지 않는다.
- 현재 issue 안에서 안전하게 만들 수 없는 guardrail이면 follow-up asset 또는 issue를 남기고 `follow-up-needed`로 닫는다.

## `No New Guardrail` Criteria

아래 중 하나면 `no-new-guardrail`을 선택할 수 있다.

- 기존 policy, template, test, CI가 이미 있었고 이번 failure는 단순 미준수이지만, 현재 issue에서 그 미준수를 다시 막는 추가 guardrail이 합리적으로 늘지 않는다.
- 외부 서비스 장애, credential 부재, worktree 부재처럼 현재 control plane이 직접 줄일 수 없는 one-off blocker다.
- 현재 issue diff 안에서 필요한 guardrail이 이미 추가됐다.
- editorial wording, non-blocking note처럼 반복 방지용 시스템 자산까지 만들 가치가 낮다.

## Feedback Ledger Flow

1. latest verification 상태와 review verdict 또는 review skipped reason을 기준으로 현재 작업의 최종 상태를 고정한다.
2. guardrail 후보가 되는 root cause를 하나씩 분리한다.
3. `Failure Taxonomy`에서 class를 고른다.
4. 기존 guardrail이 이미 있는지와 recurrence를 확인한다.
5. `Guardrail Promotion Decision`으로 승격 대상 또는 `no-new-guardrail`을 고른다.
6. ledger entry에 follow-up asset, issue, 현재 issue 적용 여부를 남긴다.
7. PR 본문 또는 exec plan close-out에 이번 판단을 요약한다.

## Feedback Close-Out Minimum

`Feedback Pending`을 `Completed`로 넘길 때는 exec plan close-out, review note, follow-up artifact 중 최소 한 곳에 아래가 있어야 한다.

- latest verification 상태 또는 `Blocked` 이유
- latest review verdict 또는 review skipped reason
- ledger entry 하나 이상 또는 `no new guardrail` entry
- promotion decision 근거
- follow-up asset, issue, 또는 "없음" 사유

feedback close-out artifact가 비어 있으면 해당 작업을 feedback 완료로 보지 않는다.

## Relationship To Other Policies

- verification 재시도, budget, `Blocked` 전환은 계속 [verification-contract-registry.md](verification-contract-registry.md)가 canonical source다.
- reviewer verdict vocabulary와 blocking finding 기준은 계속 [dual-agent-review-policy.md](dual-agent-review-policy.md)가 canonical source다.
- 이 문서는 feedback이 실제로 trigger됐을 때만 verification과 review의 최신 결과를 다음 guardrail 자산으로 연결하는 close-out 규칙을 맡는다.
- recurring lint drift, duplication, unused code sweep과 cleanup candidate handoff는 [continuous-quality-feedback-loop.md](continuous-quality-feedback-loop.md)가 맡는다.
