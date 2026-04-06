# Harness System Map

이 문서는 `git-ranker-workflow` 하네스의 architecture-level source of truth다. [docs/product/harness-roadmap.md](../product/harness-roadmap.md)가 작업 순서와 목표를 설명한다면, 이 문서는 각 단계의 책임과 입력/출력과 상태 전이를 정의한다.

## Control Objectives

하네스는 아래 여섯 축을 순서대로 고정하는 것을 목표로 한다.

1. 요청 라우팅
2. 컨텍스트 최소 공개
3. 도구 경계와 write scope 통제
4. 결정론적 검증
5. 구현 Agent와 review Agent 분리
6. 실패의 가드레일화

## Planning Boundary

- 현재 planning source of truth는 [docs/product/harness-roadmap.md](../product/harness-roadmap.md), [docs/product/work-item-catalog.md](../product/work-item-catalog.md), [docs/exec-plans/](../exec-plans/README.md)다.
- 작업 순서와 backlog는 `docs/product/`가, task별 범위와 검증은 `docs/exec-plans/`가 맡는다.
- 이관 전 전체 분해 문서와 초기 아이디어는 `docs/references/`에 둔다. 역사 문서는 현재 작업 지시를 내리는 planning source가 아니다.

## System Components

| Component | Responsibility | Primary Input | Primary Output |
| --- | --- | --- | --- |
| Router | 사용자 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다. | 사용자 요청, 상위 운영 규칙 | route decision |
| Interview | 모호한 요청을 줄여 exec plan으로 고정 가능한 작업으로 만든다. | ambiguous request, source of truth | clarified scope, close-out decision |
| Context Pack | task type에 맞는 최소 문서와 write scope를 고정한다. | exec plan, task type, source docs | bounded context pack |
| Implementer | 허용된 저장소와 파일 범위 안에서 변경을 만든다. | context pack, exec plan | diff, change notes |
| Verification | 명시된 verification contract를 실행하고 pass/fail을 기록한다. | diff, verification contract | verification report |
| Reviewer | 구현과 분리된 관점으로 diff와 검증 결과를 검토한다. | diff, verification report, exec plan | review verdict |
| Feedback | 실패와 취약 지점을 guardrail 후보로 분류하고 close-out을 남긴다. | review verdict, failure notes, exec plan | feedback entry, next follow-up |

## Canonical Artifacts

| Artifact | Description | Canonical Location |
| --- | --- | --- |
| Request record | 사용자 요청과 초기 분류 결과 | Issue 본문 또는 작업 대화 |
| Exec plan | scope, non-scope, write scope, verification contract | `docs/exec-plans/` |
| Context pack | 이번 작업에 허용된 최소 문서와 write scope | exec plan과 후속 policy |
| Verification report | 실행 명령, 최종 상태, 핵심 evidence, 실패/예외 요약 | exec plan, PR 본문, `.artifacts/` 필요 시 |
| Review verdict | reviewer 승인 또는 수정 요청 | PR 본문, review comment, exec plan 요약 |
| Feedback entry | 반복 실패와 guardrail 승격 여부 | exec plan, 후속 policy 또는 ledger |

## Canonical State Machine

### Happy Path

`Received -> Routed -> Planned -> Context Ready -> Implementing -> Verifying -> Reviewing -> Feedback Pending -> Completed`

### Ambiguity Path

`Received -> Routed -> Interviewing -> Planned`

### Repair Path

`Verifying -> Repairing -> Implementing`

`Reviewing -> Repairing -> Implementing`

### Terminal Non-execution Path

`Routed -> Rejected`

### Canonical States

| State | Entry Criteria | Exit Condition | Next State |
| --- | --- | --- | --- |
| `Received` | 사용자 요청이 들어왔다. | Router가 요청 유형을 분류했다. | `Routed` |
| `Routed` | 요청이 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류됐다. | 대화/거절이면 종료, 모호하면 인터뷰 시작, 실행 가능하면 Issue와 exec plan을 만든다. | `Rejected`, `Interviewing`, `Planned` |
| `Interviewing` | 요청은 실행 후보지만 범위나 완료 조건이 아직 모호하다. | ambiguity가 줄어 exec plan을 쓸 수 있거나, 더 이상 줄일 수 없다고 판단한다. | `Planned`, `Blocked`, `Rejected` |
| `Planned` | Issue와 exec plan이 생성되어 scope, non-scope, write scope, verification contract 초안이 잠겼다. | task type에 맞는 context pack과 허용 범위가 확정됐다. | `Context Ready`, `Blocked` |
| `Context Ready` | 필요한 최소 문서와 write scope가 고정됐다. | Implementer가 변경을 시작하거나, 필요한 source of truth가 부족하다고 판단한다. | `Implementing`, `Interviewing`, `Blocked` |
| `Implementing` | Implementer가 허용된 범위 안에서 변경을 만든다. | 검증 가능한 diff가 준비되거나, scope drift 또는 외부 blocker가 드러난다. | `Verifying`, `Blocked` |
| `Verifying` | 결정론적 검증 명령을 실행한다. | 모든 필수 명령이 통과하거나, 실패/환경 blocker가 발생한다. | `Reviewing`, `Repairing`, `Blocked` |
| `Reviewing` | Reviewer가 diff와 검증 결과를 함께 평가한다. | 승인하거나, 수정 요청을 남기거나, 검토 불가능한 blocker를 선언한다. | `Feedback Pending`, `Repairing`, `Blocked` |
| `Repairing` | verification 실패나 review 요청으로 재작업이 필요하다. | 재시도 가능한 수정이 준비되거나, 계속 진행할 근거가 사라진다. | `Implementing`, `Blocked`, `Rejected` |
| `Feedback Pending` | 최종 close-out 전 실패 원인과 guardrail 후보를 정리해야 한다. | feedback이 기록되고 다음 follow-up 여부가 결정됐다. | `Completed` |
| `Completed` | verification 통과, reviewer 승인, feedback close-out이 모두 끝났다. | 없음 | terminal |
| `Blocked` | 선행조건 미충족, 외부 의존성, write scope 충돌, source 부족으로 더 진행할 수 없다. | blocker 해소 후 다시 진입하거나 작업을 종료한다. | `Interviewing`, `Planned`, `Context Ready`, terminal |
| `Rejected` | 대화성 요청, 작업 취소, 범위 밖 요청처럼 실행을 계속하지 않기로 했다. | 없음 | terminal |

## Pass / Fail Semantics

| Stage | Pass | Fail | Required Consequence |
| --- | --- | --- | --- |
| Router | 정확히 하나의 route를 선택했고 다음 소유자가 명확하다. | route가 중복되거나 비어 있다. | 편집 작업을 시작하지 않고 intake로 되돌린다. |
| Interview | scope, non-scope, write scope, 완료 조건을 exec plan에 적을 수 있다. | ambiguity가 남아 실행 조건을 잠글 수 없다. | `Blocked` 또는 `Rejected`로 종료한다. |
| Context Pack | 최소 문서와 금지 범위가 함께 고정됐다. | source of truth가 부족하거나 불필요한 컨텍스트를 과다 공개했다. | `Interviewing` 또는 `Blocked`로 되돌린다. |
| Implementer | 허용 write scope 안에서 목표 산출물을 만든다. | scope drift, 무단 cross-repo 변경, 불명확한 요구사항이 발생한다. | `Blocked`로 전환하고 범위를 재정의한다. |
| Verification | 모든 필수 검증 명령이 통과하고 증거가 남는다. | 명령 실패, 환경 부족, 증거 누락이 있다. | `Repairing` 또는 `Blocked`로 전환한다. |
| Reviewer | reviewer가 diff, verification report, 남은 리스크를 기준으로 승인한다. | blocking finding, self-approval 시도, 검증과 diff 불일치가 있다. | `Repairing`으로 되돌린다. |
| Feedback | 실패 분류 또는 `no new guardrail` 판단이 기록됐다. | close-out과 후속 guardrail 판단이 비어 있다. | `Feedback Pending`에 머문다. |

## Stop Conditions

- `Rejected`: 대화성 요청, 범위 밖 요청, 사용자 취소처럼 작업 자체를 진행하지 않는 경우다.
- `Blocked`: 선행조건 부족, 외부 의존성, 권한 문제, canonical source 부재로 현재 이슈 안에서 더 진행할 수 없는 경우다.
- `Completed`: verification 통과, reviewer 승인, feedback close-out이 모두 끝난 경우다.
- `Repairing`은 terminal state가 아니다. 반복 실패가 누적되면 `GRW-15`, `GRW-17`에서 정의할 retry budget과 guardrail 정책에 따라 `Blocked` 또는 후속 Issue로 넘긴다.

## Role Separation Invariants

- Implementer는 자기 결과를 최종 승인할 수 없다.
- Reviewer는 diff만이 아니라 verification report와 exec plan을 함께 읽어야 한다.
- verification이 끝나기 전에는 review verdict를 final로 선언할 수 없다.
- feedback 단계는 성공 경로와 실패 경로 모두에 필요하다. 성공 시에는 `no new guardrail`도 하나의 명시적 판단으로 남긴다.
- task type별 세부 정책은 후속 Issue가 확장하더라도, `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback` 순서는 바꾸지 않는다.

## Issue / PR Projection

- Issue는 최소한 `Received`에서 `Planned`까지의 상태를 설명해야 한다.
- exec plan은 `Planned` 상태의 공식 기록이며, 구현을 시작하기 전에 존재해야 한다.
- PR은 `Implementing` 이후의 산출물과 `Verifying`, `Reviewing`, `Feedback Pending` 증거를 담는 컨테이너다.
- `Completed` 판정은 PR의 verification 결과와 reviewer verdict, exec plan의 close-out이 함께 있어야 성립한다.
- 완료된 exec plan은 `docs/exec-plans/completed/`로 옮기고, 후속 Issue가 이 문서를 전제조건으로 참조한다.

## Follow-up Ownership

- `GRW-12`는 `Router`, `Interviewing`, `Rejected` semantics를 세분화한다.
- `GRW-13`은 `Planned`에서 `Context Ready`로 가는 규칙을 registry로 고정한다.
- `GRW-14`는 `Context Ready`와 `Implementing` 단계의 tool boundary를 상세화한다.
- `GRW-15`는 `Verifying`, `Repairing`, `Blocked` semantics와 retry budget을 명시한다.
- `GRW-16`은 `Reviewing` 단계의 reviewer input과 verdict 규칙을 구체화한다.
- `GRW-17`은 `Feedback Pending`과 guardrail 승격 규칙을 ledger 형태로 정의한다.
