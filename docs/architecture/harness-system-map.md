# Harness System Map

이 문서는 `git-ranker-workflow` 하네스의 architecture-level source of truth다. task별 요구사항과 sequencing은 `docs/specs/`의 draft/approved spec이 맡고, 이 문서는 각 단계의 책임과 입력/출력과 상태 전이를 정의한다.

## Control Objectives

하네스는 아래 축을 순서대로 고정하는 것을 목표로 한다.

1. 요청 라우팅을 빠르게 끝낸다
2. 즉시 실행 가능한 작업은 모두 소크라테스 기반 spec으로 먼저 정의한다
3. spec 안에서 하위 작업, write scope, tracking 결정을 잠근다
4. 한 번에 한 하위 작업만 구현하고 결정론적 검증을 끝낸다
5. publish가 필요한 결과는 open PR로 공개한다
6. review와 feedback은 위험 신호가 있을 때만 올린다
7. 마지막 완료 판정은 사용자 최종 검증까지 포함한다

## Planning Boundary

- 현재 planning source of truth는 [docs/specs/](../specs/README.md)다.
- remaining work와 sequencing은 `docs/specs/active/`의 draft/approved spec과 prerequisite note로 표현한다.
- 별도 roadmap/catalog 문서는 유지하지 않는다.
- 현재 control plane은 별도 history/reference 트리를 유지하지 않는다. 앱 동작의 canonical source는 각 앱 저장소 문서와 코드/테스트다.

## Federated Thin-Layer Invariants

- workflow-local docs, skills, handoff artifact는 thin layer다. route, stage responsibility, boundary, minimum handoff만 정의한다.
- state transition은 repo entrypoint에서 멈춘다. backend/frontend implementation procedure, file-level bootstrap, repo-local verification command는 sibling repo canonical source가 소유한다.
- control plane 단계가 더 많은 app-specific detail을 필요로 하면 workflow stable doc을 두껍게 늘리지 말고 target repo entrypoint 또는 repo-local follow-up spec으로 handoff한다.

## System Components

| Component | Responsibility | Primary Input | Primary Output |
| --- | --- | --- | --- |
| Router | 사용자 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다. | 사용자 요청, 운영 규칙 | route decision |
| Spec Writer | 소크라테스 질문으로 문제, 목표, 제약, 전제, framing, 하위 작업, 검증 기준을 정리한다. | routed request, source docs, user answers | draft spec, approved spec |
| Tracker | spec에 따라 parent issue, subtask issue, pre-implementation tracking artifact가 필요한지 결정하고 만든다. | approved spec | optional issue set, tracking decision |
| Context Pack | approved spec 기준으로 최소 문서와 읽기 경계를 고정한다. | approved spec, task type, source docs | bounded context pack |
| Implementer | 승인된 spec의 현재 하위 작업을 허용 범위 안에서 구현한다. | approved spec, selected subtask, context | diff, change notes |
| Verification | 명시된 verification contract를 실행하고 pass/fail을 기록한다. | diff, verification contract | verification report or summary |
| Publisher | latest verification을 반영한 open PR을 만든다. | diff, verification evidence, PR body | open PR |
| Reviewer | 필요할 때만 open PR 또는 latest diff를 검토하고 verdict를 남긴다. | open PR, verification evidence, approved spec | optional review verdict |
| Feedback | blocker, 반복 실패, quality drift가 있을 때만 guardrail 후보 또는 cleanup candidate를 남긴다. | failure notes, review verdict, quality sweep signal | optional feedback entry, next follow-up |
| User Validator | 최종 결과가 승인된 spec과 맞는지 사용자 관점에서 닫는다. | latest diff or PR, verification summary, approved spec | final approval or follow-up request |

## Canonical Artifacts

| Artifact | Description | Canonical Location |
| --- | --- | --- |
| Request record | 사용자 요청과 초기 분류 결과 | Issue 본문 또는 작업 대화 |
| Spec | 승인된 요구사항, 하위 작업, write scope, verification, tracking 결정을 모은 단일 문서 | `docs/specs/` |
| Context pack | approved spec에서 허용된 최소 문서와 읽기 경계 | spec과 후속 policy |
| Verification evidence | compact verification summary 또는 detailed report로 latest verification 상태를 남긴다 | spec, verification artifact, PR summary |
| Open PR | 검증된 결과를 공개하는 기본 협업 surface | GitHub PR |
| Review verdict | optional independent review 결과 | review comment, PR comment, spec summary |
| Feedback entry | optional guardrail 승격 또는 후속 분류 결과 | spec, follow-up policy, ledger |
| Quality sweep report | non-blocking quality signal과 cleanup handoff | spec, sweep artifact, 후속 issue/PR |
| User validation note | 사용자가 승인된 spec과 최종 결과를 대조해 남긴 완료 판정 | spec, PR comment, 작업 대화 |

## Canonical State Machine

### Default Happy Path

`Received -> Routed -> Spec Drafting -> Spec Approved -> Context Ready -> Implementing -> Verifying -> User Validating -> Completed`

### Tracked Path

`Received -> Routed -> Spec Drafting -> Spec Approved -> Tracking -> Context Ready -> Implementing -> Verifying -> Publishing -> Reviewing -> User Validating -> Completed`

### Ambiguity Path

`Received -> Routed -> Interviewing -> Spec Drafting`

### Repair Path

`Verifying -> Repairing -> Implementing`

`Reviewing -> Repairing -> Verifying -> Publishing`

### Spec Reopen Path

`Verifying -> Spec Drafting`

`Reviewing -> Spec Drafting`

`Repairing -> Spec Drafting`

`User Validating -> Spec Drafting`

### Optional Feedback Path

`Reviewing -> Feedback Pending -> Completed`

`Verifying -> Feedback Pending -> Completed`

### Terminal Non-execution Path

`Routed -> Rejected`

### Canonical States

| State | Entry Criteria | Exit Condition | Next State |
| --- | --- | --- | --- |
| `Received` | 사용자 요청이 들어왔다. | Router가 요청 유형을 분류했다. | `Routed` |
| `Routed` | 요청이 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류됐다. | 대화/거절이면 종료, 모호하면 인터뷰 시작, 실행 가능하면 spec drafting을 시작한다. | `Rejected`, `Interviewing`, `Spec Drafting` |
| `Interviewing` | 요청은 실행 후보지만 single requirement, primary repo, 기본 완료 조건이 아직 모호하다. | ambiguity가 줄어 spec drafting으로 넘어가거나, 더 이상 줄일 수 없다고 판단한다. | `Spec Drafting`, `Blocked`, `Rejected` |
| `Spec Drafting` | 소크라테스 질문과 초안 정리로 spec을 작성 중이다. | Harness가 approval gate를 통과했다고 판단하고 사용자가 승인했거나, 더 진행할 수 없다고 판단한다. | `Spec Approved`, `Blocked`, `Rejected` |
| `Spec Approved` | 승인된 spec이 존재하고 목표, 하위 작업, write scope, verification, tracking 결정이 잠겼다. | tracking이 필요하면 tracking을 시작하고, 아니면 context pack을 준비한다. | `Tracking`, `Context Ready`, `Blocked` |
| `Tracking` | approved spec이 issue/PR 또는 subtask issue로 투영돼야 한다. | 필요한 tracking artifact 생성이 끝나거나, tracking 불가 사유가 정리됐다. | `Context Ready`, `Blocked` |
| `Context Ready` | 현재 하위 작업에 필요한 최소 문서와 write scope가 승인된 spec 기준으로 고정됐다. | Implementer가 변경을 시작하거나, 필요한 source of truth가 부족하다고 판단한다. | `Implementing`, `Interviewing`, `Blocked` |
| `Implementing` | Implementer가 허용된 범위 안에서 변경을 만든다. | 검증 가능한 diff가 준비되거나, scope drift 또는 외부 blocker가 드러난다. | `Verifying`, `Blocked`, `Spec Drafting` |
| `Verifying` | 결정론적 검증 명령을 실행한다. | 모든 필수 명령이 통과하거나, 수리 가능한 diff defect, spec defect, 환경 blocker가 분류된다. | `Publishing`, `Repairing`, `Spec Drafting`, `Blocked`, `Feedback Pending` |
| `Publishing` | latest verification이 current diff 기준으로 준비됐고 PR body가 채워졌다. | open PR이 publish되거나, publish를 못 할 이유가 확인된다. | `Reviewing`, `User Validating`, `Blocked` |
| `Reviewing` | open PR 또는 latest diff에 대해 independent review가 실제로 시작됐다. | 승인하거나, 수정 요청을 남기거나, spec defect 또는 검토 불가능한 blocker를 선언한다. | `User Validating`, `Repairing`, `Spec Drafting`, `Blocked`, `Feedback Pending` |
| `Repairing` | verification 실패나 review 요청으로 재작업이 필요하다. | 재시도 가능한 수정이 준비되거나, root cause가 spec defect라고 확인되거나, 계속 진행할 근거가 사라진다. | `Implementing`, `Spec Drafting`, `Blocked`, `Rejected` |
| `Feedback Pending` | blocker, 반복 실패, systemic gap, quality handoff를 정리해야 한다. | feedback이 기록되고 다음 follow-up 여부가 결정됐다. | `User Validating`, `Completed` |
| `User Validating` | latest verification과 결과 공유가 끝났고, 최종 수용 여부를 사용자 기준으로 닫아야 한다. | 사용자가 spec 대비 결과를 승인하거나, 구현 follow-up 또는 spec defect reopen을 요청한다. | `Completed`, `Repairing`, `Spec Drafting`, `Blocked` |
| `Completed` | 검증된 결과가 승인된 spec과 맞게 닫혔고, trigger된 review나 feedback이 있다면 그것도 정리됐다. | 없음 | terminal |
| `Blocked` | 선행조건 미충족, 외부 의존성, write scope 충돌, source 부족으로 더 진행할 수 없다. | blocker 해소 후 다시 진입하거나 작업을 종료한다. | `Interviewing`, `Spec Drafting`, `Spec Approved`, `Context Ready`, terminal |
| `Rejected` | 대화성 요청, 작업 취소, 범위 밖 요청처럼 실행을 계속하지 않기로 했다. | 없음 | terminal |

## Pass / Fail Semantics

| Stage | Pass | Fail | Required Consequence |
| --- | --- | --- | --- |
| Router | 정확히 하나의 route가 선택됐고 다음 소유자가 명확하다. | route가 중복되거나 비어 있다. | 편집 작업을 시작하지 않고 intake로 되돌린다. |
| Spec Writer | 질문, why, 전제 점검, framing 점검, 요약으로 approval gate를 닫는다. | 즉답, 숨은 가정 추가, approval gate 누락, 승인 전 구현 착수가 발생한다. | `Interviewing`, `Spec Drafting`, 또는 `Blocked`로 되돌린다. |
| Context Pack | 최소 문서와 금지 범위가 함께 고정됐다. | source of truth가 부족하거나 불필요한 컨텍스트를 과다 공개했다. | `Interviewing` 또는 `Blocked`로 되돌린다. |
| Implementer | 승인된 spec의 현재 하위 작업을 허용 write scope 안에서 구현한다. | scope drift, 무단 cross-repo 변경, spec 밖 요구사항 추가가 발생한다. | `Blocked` 또는 spec 수정 승인 단계로 되돌린다. |
| Verification | 모든 필수 검증 명령이 통과하고 증거가 남는다. | 명령 실패, 환경 부족, 증거 누락, spec defect가 있다. | `Repairing`, `Spec Drafting`, 또는 `Blocked`로 전환한다. |
| Publishing | latest verification을 반영한 open PR이 생성됐다. | 검증 전 publish를 시도하거나, publish 이유가 불명확하다. | `Blocked` 또는 `Verifying`로 되돌린다. |
| Reviewer | reviewer가 diff, verification evidence, approved spec을 기준으로 판단한다. | blocking finding, self-approval 시도, 검증과 diff 불일치, late-discovered spec defect가 있다. | `Repairing`, `Spec Drafting`, 또는 `Blocked`로 되돌린다. |
| Feedback | 정말 필요한 failure나 follow-up만 기록됐다. | close-out과 후속 guardrail/cleanup 판단이 필요한데 비어 있다. | `Feedback Pending`에 머문다. |
| User Validator | 사용자가 spec 대비 결과를 승인한다. | spec과 결과가 어긋나거나, spec lock 자체가 잘못됐거나, follow-up이 필요하다고 판단한다. | `Repairing`, `Spec Drafting`, 또는 `Blocked`로 되돌린다. |

## Stop Conditions

- `Rejected`: 대화성 요청, 범위 밖 요청, 사용자 취소처럼 작업 자체를 진행하지 않는 경우다.
- `Blocked`: 선행조건 부족, 외부 의존성, 권한 문제, canonical source 부재로 현재 작업 안에서 더 진행할 수 없는 경우다.
- `Completed`: latest verification을 반영한 결과가 승인된 spec과 맞게 닫혔고, trigger된 review/feedback/user validation까지 정리된 경우다.
- `Completed`는 terminal state지만, post-closeout quality sweep이 필요하면 새 `Received` work item을 시작할 수 있다.
- `Repairing`은 terminal state가 아니다. 반복 실패가 누적되면 verification contract registry와 feedback policy의 retry budget 기준에 따라 `Blocked` 또는 후속 planning으로 넘긴다.

## Role Separation Invariants

- Implementer는 자기 결과를 independent review evidence로 승인할 수 없다.
- review를 수행할 때만 reviewer separation invariant가 적용된다.
- reviewer는 diff만이 아니라 verification evidence와 approved spec을 함께 읽어야 한다.
- 구현 전 승인되지 않은 spec은 canonical source로 간주하지 않는다.
- 늦게 드러난 spec defect는 current diff patch만으로 흡수하지 않고 spec reopen과 재승인으로 되돌린다.
- verification이 끝나기 전에는 publish하지 않는다.
- publish는 review보다 앞설 수 있다. open PR은 검증된 결과를 공유하는 기본 surface다.
- feedback 단계는 optional이다. blocker, 반복 실패, systemic gap이 있을 때만 들어간다.
- non-blocking quality drift는 original task의 completion verdict를 뒤집지 않고, separate cleanup issue/PR candidate로 분리한다.

## Issue / PR Projection

- approved spec은 모든 즉시 실행 가능한 작업의 공식 기록이다.
- issue는 approved spec이 추적 surface를 요구할 때만 만든다.
- 하위 작업이 생기면 spec 안에서 먼저 분해하고, tracking 필요 여부를 각 하위 작업에 대해 별도로 판단한다.
- PR은 기본적으로 latest verification을 반영한 결과를 공유하는 컨테이너다. review는 그 다음 optional stage다.
- review/repair loop가 열리면 open PR의 current diff와 latest verification evidence를 기준으로 닫는다.
- feedback이나 quality sweep이 필요하면 PR 완료 여부와 분리해 별도 artifact나 follow-up으로 남긴다.
- 완료된 spec은 `docs/specs/completed/`로 옮기고, 후속 작업이 있으면 이 문서를 전제조건으로 참조한다.
- completed spec은 historical close-out record이며 full transcript는 아니다. 현재 canonical runtime과 정책은 stable source of truth 문서에서 해석한다.

## Detailed Policy Surfaces

- [../operations/request-routing-policy.md](../operations/request-routing-policy.md)는 `Router`, `Interviewing`, `Spec Drafting`, `Rejected` semantics를 세분화한다.
- [../operations/sdd-spec-policy.md](../operations/sdd-spec-policy.md)는 소크라테스 질문 루프와 spec 승인 기준을 고정한다.
- [context-pack-registry.md](context-pack-registry.md)는 승인된 spec에서 `Context Ready`로 가는 규칙을 registry 형태로 고정한다.
- [../operations/tool-boundary-matrix.md](../operations/tool-boundary-matrix.md)는 `Context Ready`와 `Implementing` 단계의 허용 도구와 write scope 경계를 상세화한다.
- [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md)는 `Verifying`, `Repairing`, `Blocked` semantics와 retry budget을 명시한다.
- [../operations/dual-agent-review-policy.md](../operations/dual-agent-review-policy.md)는 optional `Reviewing` 단계의 reviewer input, verdict, repair loop, evidence rule을 구체화한다.
- [../operations/failure-to-guardrail-feedback-loop.md](../operations/failure-to-guardrail-feedback-loop.md)는 optional `Feedback Pending` close-out과 guardrail 승격 규칙을 고정한다.
- [../operations/continuous-quality-feedback-loop.md](../operations/continuous-quality-feedback-loop.md)는 recurring quality sweep, cleanup candidate, quality sweep report handoff를 고정한다.
