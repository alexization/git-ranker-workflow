# Request Routing Policy

이 문서는 사용자 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류하는 intake 규칙을 고정한다.

## Routing Decision Order

1. 요청이 응답만으로 끝나는지 판단한다.
2. 실행 의도가 있으면 single executable requirement로 줄일 수 있는지 본다.
3. 줄일 수 있으면 `즉시 실행 가능한 작업`으로 분류하고 spec authoring으로 넘긴다.
4. 아직 줄일 수 없으면 `모호한 요청`으로 분류하고 blocker 질문을 시작한다.
5. 대화 전환, 취소, 범위 밖 요청, canonical source 부재는 `Rejected`로 닫는다.

## Route Categories

| Route | 선택 기준 | 즉시 해야 할 일 | 상태 전이 |
| --- | --- | --- | --- |
| `대화` | 설명, 요약, 번역, 코드 리뷰 의견처럼 응답만으로 끝난다 | 답변만 제공한다 | `Received -> Routed -> Rejected` |
| `모호한 요청` | 실행 의도는 있지만 single requirement, primary repo, 기본 완료 조건이 아직 하나로 잠기지 않는다 | source of truth를 먼저 확인하고 blocker 질문으로 줄인다 | `Received -> Routed -> Interviewing` |
| `즉시 실행 가능한 작업` | 하나의 spec으로 정의할 수 있고 source of truth로 첫 spec drafting을 시작할 수 있다 | 소크라테스 spec loop를 시작한다 | `Received -> Routed -> Spec Drafting` |

`Rejected`는 route가 아니라 terminal close-out이다.

## Ambiguity Signals

아래 중 하나라도 남아 있으면 `모호한 요청`이다.

- 대상 저장소가 둘 이상으로 해석된다.
- 하나의 요청 안에 둘 이상의 목표가 섞여 있다.
- 완료 조건이나 산출물 형태가 없다.
- 어떤 요구사항을 하나의 spec으로 고정할지 판단할 수 없다.
- canonical source 없이 새 정책을 발명해야 한다.

아래는 ambiguity signal로 보지 않는다.

- spec 안에서 소크라테스 질문으로 더 구체화해야 하는 일반적인 세부사항
- tracking issue가 필요한지 여부처럼 spec authoring 단계에서 결정할 수 있는 사항
- tool approval이나 네트워크 승인만 남아 있는 경우

## Immediate Execution Criteria

아래를 만족하면 `즉시 실행 가능한 작업`이다.

1. 지금 턴에서 답변이 아니라 실행을 원하는 것이 분명하다.
2. 하나의 spec으로 묶을 primary requirement가 있다.
3. primary repo 또는 planning repo를 하나로 고를 수 있다.
4. spec authoring을 시작할 최소한의 source of truth가 있다.
5. 추가 질문이 필요하더라도, 그 질문은 spec 안을 채우는 질문이지 "무슨 작업인지"를 새로 고르는 질문이 아니다.

## Ambiguity Interview Policy

### Interview Objectives

interview 목적은 아래 다섯 가지를 잠그는 것이다.

- single requirement
- primary repo
- expected outcome
- 실행 가능한 범위
- spec authoring을 시작할 수 있는 최소 source

### Interview Rules

- 질문 전에 source of truth를 먼저 읽는다.
- 기본은 한 번에 하나의 blocker 질문이다.
- 여러 목표가 섞여 있으면 무엇을 먼저 한 spec으로 고정할지 묻는다.
- 여러 저장소가 섞여 있으면 이번 턴의 primary repo를 먼저 고정한다.
- ambiguity가 줄어들면 바로 spec authoring 단계로 넘긴다.

### Interview Exit Conditions

| 종료 상태 | 기준 | 다음 행동 |
| --- | --- | --- |
| `Spec Drafting` | single requirement와 primary repo가 잠겨 spec을 쓸 수 있다 | `socratic-spec-authoring`으로 넘긴다 |
| `Blocked` | 실행 의도는 유지되지만 외부 입력이나 canonical source가 없어 더 줄일 수 없다 | blocker를 남기고 멈춘다 |
| `Rejected` | 대화 전환, 취소, 범위 밖 요청, 새 정책 발명이 필요하다 | 실행을 종료한다 |

## Rejected Semantics

canonical close-out reason은 아래를 사용한다.

- `conversation-only`
- `cancelled`
- `out-of-scope`
- `missing-canonical-source`
- `non-executable-after-interview`

## Example Classification

| 요청 | 판정 | 이유 | 다음 행동 |
| --- | --- | --- | --- |
| "`docs/README.md` 구조를 설명해줘" | `대화` | 응답만으로 끝난다 | 답변만 제공 |
| "하네스에 SDD workflow를 도입해줘" | `즉시 실행 가능한 작업` | 하나의 workflow policy 변경 spec으로 정의할 수 있다 | 소크라테스 spec loop 시작 |
| "랭킹 화면 좀 개선해줘" | `모호한 요청` | 어떤 화면과 어떤 완료 조건인지 없다 | blocker 질문 |
| "backend랑 client 인증 흐름 다 정리하고 필요한 것들 한 번에 고쳐줘" | `모호한 요청` | 여러 저장소와 여러 목표가 섞여 있다 | primary spec 후보를 먼저 고르도록 질문 |

## Governance Hooks

- `즉시 실행 가능한 작업`은 구현 전에 항상 spec authoring으로 들어간다.
- `모호한 요청` 단계에서는 spec, issue, PR, 파일 편집을 시작하지 않는다.
- `대화`와 `Rejected` close-out은 문서 변경 없이 종료한다.
