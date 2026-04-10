# Harness System Map

이 문서는 `git-ranker-workflow` 하네스의 architecture-level source of truth다. [docs/product/harness-roadmap.md](../product/harness-roadmap.md)가 작업 순서와 목표를 설명한다면, 이 문서는 각 단계의 책임과 입력/출력과 상태 전이를 정의한다.

## Control Objectives

하네스는 아래 여섯 축을 순서대로 고정하는 것을 목표로 한다.

1. 요청 라우팅을 빠르게 끝낸다
2. 작업에 맞는 최소 실행 lane만 고른다
3. write scope와 도구 경계를 통제한다
4. publish 전에 결정론적 검증을 끝낸다
5. 검증된 결과를 open PR로 빠르게 공개한다
6. review와 feedback은 위험 신호가 있을 때만 올린다

## Planning Boundary

- 현재 planning source of truth는 [docs/product/harness-roadmap.md](../product/harness-roadmap.md), [docs/product/work-item-catalog.md](../product/work-item-catalog.md), [docs/exec-plans/](../exec-plans/README.md)다.
- 작업 순서와 backlog는 `docs/product/`가, task별 범위와 검증은 `docs/exec-plans/`가 맡는다.
- 현재 control plane은 별도 history/reference 트리를 유지하지 않는다. 앱 동작의 canonical source는 각 앱 저장소 문서와 코드/테스트다.

## System Components

| Component | Responsibility | Primary Input | Primary Output |
| --- | --- | --- | --- |
| Router | 사용자 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류하고 lane을 고른다. | 사용자 요청, 운영 규칙 | route decision, lane decision |
| Planner | guarded lane에서 issue와 exec plan으로 범위를 formal하게 잠근다. | routed request, product docs, source docs | issue, exec plan, write scope |
| Context Pack | guarded lane에서 최소 문서와 write scope를 고정한다. | exec plan, task type, source docs | bounded context pack |
| Implementer | 허용된 저장소와 파일 범위 안에서 변경을 만든다. | task brief 또는 exec plan, context | diff, change notes |
| Verification | 명시된 verification contract를 실행하고 pass/fail을 기록한다. | diff, verification contract | verification report or summary |
| Publisher | latest verification을 반영한 open PR을 만든다. | diff, verification evidence, PR body | open PR |
| Reviewer | 필요할 때만 open PR 또는 latest diff를 검토하고 verdict를 남긴다. | open PR, verification evidence, task brief or exec plan | optional review verdict |
| Feedback | blocker, 반복 실패, quality drift가 있을 때만 guardrail 후보 또는 cleanup candidate를 남긴다. | failure notes, review verdict, quality sweep signal | optional feedback entry, next follow-up |

## Canonical Artifacts

| Artifact | Description | Canonical Location |
| --- | --- | --- |
| Request record | 사용자 요청과 초기 분류 결과 | Issue 본문 또는 작업 대화 |
| Task brief | default lane에서 repo, 목표, write scope, verification을 잠근 짧은 메모 | 작업 대화, PR body 초안 |
| Exec plan | guarded lane의 scope, non-scope, write scope, verification contract | `docs/exec-plans/` |
| Context pack | guarded lane에서 허용된 최소 문서와 write scope | exec plan과 후속 policy |
| Verification report | 실행 명령, 최종 상태, 핵심 evidence, 실패/예외 요약 | exec plan, verification artifact, PR summary |
| Open PR | 검증된 결과를 공개하는 기본 협업 surface | GitHub PR |
| Review verdict | optional independent review 결과 | review comment, PR comment, exec plan 요약 |
| Feedback entry | optional guardrail 승격 또는 후속 분류 결과 | exec plan, follow-up policy, ledger |
| Quality sweep report | non-blocking quality signal과 cleanup handoff | exec plan, sweep artifact, 후속 issue/PR |

## Canonical State Machine

### Default Happy Path

`Received -> Routed -> Scoped -> Implementing -> Verifying -> Publishing -> Completed`

### Guarded Path

`Received -> Routed -> Planned -> Context Ready -> Implementing -> Verifying -> Publishing -> Reviewing -> Completed`

### Ambiguity Path

`Received -> Routed -> Interviewing -> Scoped`

`Received -> Routed -> Interviewing -> Planned`

### Repair Path

`Verifying -> Repairing -> Implementing`

`Reviewing -> Repairing -> Verifying -> Publishing`

### Optional Feedback Path

`Reviewing -> Feedback Pending -> Completed`

`Verifying -> Feedback Pending -> Completed`

### Terminal Non-execution Path

`Routed -> Rejected`

### Canonical States

| State | Entry Criteria | Exit Condition | Next State |
| --- | --- | --- | --- |
| `Received` | 사용자 요청이 들어왔다. | Router가 요청 유형을 분류했다. | `Routed` |
| `Routed` | 요청이 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류됐다. | 대화/거절이면 종료, 모호하면 인터뷰 시작, 실행 가능하면 lane을 고른다. | `Rejected`, `Interviewing`, `Scoped`, `Planned` |
| `Interviewing` | 요청은 실행 후보지만 범위나 완료 조건이 아직 모호하다. | ambiguity가 줄어 task brief 또는 exec plan을 쓸 수 있거나, 더 이상 줄일 수 없다고 판단한다. | `Scoped`, `Planned`, `Blocked`, `Rejected` |
| `Scoped` | default lane task brief가 기록돼 repo, 목표, write scope, verification이 잠겼다. | Implementer가 변경을 시작하거나 guarded lane으로 승격한다. | `Implementing`, `Planned`, `Blocked` |
| `Planned` | guarded lane issue와 exec plan이 생성되어 scope, non-scope, write scope, verification contract 초안이 잠겼다. | task type에 맞는 context pack과 허용 범위가 확정됐다. | `Context Ready`, `Blocked` |
| `Context Ready` | guarded lane의 최소 문서와 write scope가 고정됐다. | Implementer가 변경을 시작하거나, 필요한 source of truth가 부족하다고 판단한다. | `Implementing`, `Interviewing`, `Blocked` |
| `Implementing` | Implementer가 허용된 범위 안에서 변경을 만든다. | 검증 가능한 diff가 준비되거나, scope drift 또는 외부 blocker가 드러난다. | `Verifying`, `Blocked`, `Planned` |
| `Verifying` | 결정론적 검증 명령을 실행한다. | 모든 필수 명령이 통과하거나, 실패/환경 blocker가 발생한다. | `Publishing`, `Repairing`, `Blocked`, `Feedback Pending` |
| `Publishing` | latest verification이 current diff 기준으로 준비됐고 PR body가 채워졌다. | open PR이 publish되거나, publish를 못 할 이유가 확인된다. | `Completed`, `Reviewing`, `Blocked` |
| `Reviewing` | open PR 또는 latest diff에 대해 independent review가 실제로 시작됐다. | 승인하거나, 수정 요청을 남기거나, 검토 불가능한 blocker를 선언한다. | `Completed`, `Repairing`, `Blocked`, `Feedback Pending` |
| `Repairing` | verification 실패나 review 요청으로 재작업이 필요하다. | 재시도 가능한 수정이 준비되거나, 계속 진행할 근거가 사라진다. | `Implementing`, `Blocked`, `Rejected` |
| `Feedback Pending` | blocker, 반복 실패, systemic gap, quality handoff를 정리해야 한다. | feedback이 기록되고 다음 follow-up 여부가 결정됐다. | `Completed` |
| `Completed` | 검증된 결과가 publish됐고, trigger된 review나 feedback이 있다면 그것도 정리됐다. | 없음 | terminal |
| `Blocked` | 선행조건 미충족, 외부 의존성, write scope 충돌, source 부족으로 더 진행할 수 없다. | blocker 해소 후 다시 진입하거나 작업을 종료한다. | `Interviewing`, `Scoped`, `Planned`, `Context Ready`, terminal |
| `Rejected` | 대화성 요청, 작업 취소, 범위 밖 요청처럼 실행을 계속하지 않기로 했다. | 없음 | terminal |

## Pass / Fail Semantics

| Stage | Pass | Fail | Required Consequence |
| --- | --- | --- | --- |
| Router | 정확히 하나의 route와 lane이 선택됐고 다음 소유자가 명확하다. | route가 중복되거나 비어 있다. | 편집 작업을 시작하지 않고 intake로 되돌린다. |
| Planner | issue와 exec plan이 현재 guarded lane scope를 설명한다. | write scope나 verification이 비어 있다. | `Blocked` 또는 `Interviewing`으로 되돌린다. |
| Context Pack | 최소 문서와 금지 범위가 함께 고정됐다. | source of truth가 부족하거나 불필요한 컨텍스트를 과다 공개했다. | `Interviewing` 또는 `Blocked`로 되돌린다. |
| Implementer | 허용 write scope 안에서 목표 산출물을 만든다. | scope drift, 무단 cross-repo 변경, 불명확한 요구사항이 발생한다. | `Blocked` 또는 lane 승격으로 전환한다. |
| Verification | 모든 필수 검증 명령이 통과하고 증거가 남는다. | 명령 실패, 환경 부족, 증거 누락이 있다. | `Repairing` 또는 `Blocked`로 전환한다. |
| Publishing | latest verification을 반영한 open PR이 생성됐다. | 검증 전 publish를 시도하거나, publish 이유가 불명확하다. | `Blocked` 또는 `Verifying`로 되돌린다. |
| Reviewer | reviewer가 diff, verification evidence, scope note를 기준으로 판단한다. | blocking finding, self-approval 시도, 검증과 diff 불일치가 있다. | `Repairing` 또는 `Blocked`로 되돌린다. |
| Feedback | 정말 필요한 failure나 follow-up만 기록됐다. | close-out과 후속 guardrail/cleanup 판단이 필요한데 비어 있다. | `Feedback Pending`에 머문다. |

## Stop Conditions

- `Rejected`: 대화성 요청, 범위 밖 요청, 사용자 취소처럼 작업 자체를 진행하지 않는 경우다.
- `Blocked`: 선행조건 부족, 외부 의존성, 권한 문제, canonical source 부재로 현재 작업 안에서 더 진행할 수 없는 경우다.
- `Completed`: latest verification을 반영한 결과가 publish됐고, trigger된 review/feedback까지 정리된 경우다.
- `Completed`는 terminal state지만, post-closeout quality sweep이 필요하면 새 `Received` work item을 시작할 수 있다.
- `Repairing`은 terminal state가 아니다. 반복 실패가 누적되면 verification contract registry와 feedback policy의 retry budget 기준에 따라 `Blocked` 또는 후속 planning으로 넘긴다.

## Role Separation Invariants

- Implementer는 자기 결과를 independent review evidence로 승인할 수 없다.
- review를 수행할 때만 reviewer separation invariant가 적용된다.
- reviewer는 diff만이 아니라 verification evidence와 task brief 또는 exec plan을 함께 읽어야 한다.
- verification이 끝나기 전에는 publish하지 않는다.
- publish는 review보다 앞설 수 있다. open PR은 검증된 결과를 공유하는 기본 surface다.
- feedback 단계는 optional이다. blocker, 반복 실패, systemic gap이 있을 때만 들어간다.
- non-blocking quality drift는 original task의 completion verdict를 뒤집지 않고, separate cleanup issue/PR candidate로 분리한다.

## Issue / PR Projection

- guarded lane의 Issue는 최소한 `Received`에서 `Planned`까지의 상태를 설명한다.
- default lane은 issue 없이 task brief와 PR body만으로 시작할 수 있다.
- exec plan은 guarded lane의 공식 기록이며, 구현을 시작하기 전에 존재해야 한다.
- PR은 기본적으로 latest verification을 반영한 결과를 공유하는 컨테이너다. review는 그 다음 optional stage다.
- review/repair loop가 열리면 open PR의 current diff와 latest verification evidence를 기준으로 닫는다.
- feedback이나 quality sweep이 필요하면 PR 완료 여부와 분리해 별도 artifact나 follow-up으로 남긴다.
- 완료된 exec plan은 `docs/exec-plans/completed/`로 옮기고, 후속 Issue가 이 문서를 전제조건으로 참조한다.
- completed exec plan은 historical close-out record이며, 현재 canonical runtime과 정책은 stable source of truth 문서에서 해석한다.

## Detailed Policy Surfaces

- request routing and lane selection policy는 `Router`, `Interviewing`, `Scoped`, `Planned`, `Rejected` semantics를 세분화한다.
- [context-pack-registry.md](context-pack-registry.md)는 guarded lane의 `Planned`에서 `Context Ready`로 가는 규칙을 registry 형태로 고정한다.
- [../operations/tool-boundary-matrix.md](../operations/tool-boundary-matrix.md)는 `Context Ready`와 `Implementing` 단계의 허용 도구와 write scope 경계를 상세화한다.
- [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md)는 `Verifying`, `Repairing`, `Blocked` semantics와 retry budget을 명시한다.
- [../operations/dual-agent-review-policy.md](../operations/dual-agent-review-policy.md)는 optional `Reviewing` 단계의 reviewer input, verdict, repair loop, evidence rule을 구체화한다.
- [../operations/failure-to-guardrail-feedback-loop.md](../operations/failure-to-guardrail-feedback-loop.md)는 optional `Feedback Pending` close-out과 guardrail 승격 규칙을 고정한다.
- [../operations/continuous-quality-feedback-loop.md](../operations/continuous-quality-feedback-loop.md)는 recurring quality sweep, cleanup candidate, quality sweep report handoff를 고정한다.
