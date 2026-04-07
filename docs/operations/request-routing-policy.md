# Request Routing Policy

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Router`, `Interviewing`, `Rejected` 상태를 실제 intake 운영 규칙으로 구체화한다. 목표는 사용자 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 일관되게 분류하고, ambiguity interview가 요구사항을 늘리지 않고 실행 범위를 줄이도록 고정하는 것이다.

## Routing Decision Order

1. 먼저 요청이 작업 실행을 요구하는지, 아니면 응답만으로 끝나는 `대화`인지 판단한다.
2. 작업 실행 의도가 있으면 ambiguity signal이 남아 있는지 확인한다.
3. ambiguity signal이 없고 단일 목표와 write scope와 verification을 고정할 수 있으면 `즉시 실행 가능한 작업`으로 분류한다.
4. ambiguity signal이 남아 있으면 `모호한 요청`으로 분류하고 interview를 시작한다.
5. `대화`, 사용자 취소, 범위 밖 요청, canonical source 부재처럼 실행을 계속하지 않기로 결정한 경우는 terminal close-out을 `Rejected`로 기록한다.

## Route Categories

| Route | 선택 기준 | 즉시 해야 할 일 | 상태 전이 |
| --- | --- | --- | --- |
| `대화` | 설명, 요약, 번역, 브레인스토밍, 코드 리뷰 의견처럼 응답만으로 끝나는 요청이거나, 사용자가 명시적으로 수정하지 말라고 했다. | 답변만 제공하고 issue, exec plan, 파일 편집을 시작하지 않는다. | `Received -> Routed -> Rejected` (`conversation-only`) |
| `모호한 요청` | 작업 실행 의도는 있지만 최소 하나 이상의 ambiguity signal이 남아 있다. | source of truth를 먼저 확인하고, 남는 blocker만 interview 질문으로 줄인다. issue와 exec plan은 아직 만들지 않는다. | `Received -> Routed -> Interviewing` |
| `즉시 실행 가능한 작업` | 단일 목표, 대상 저장소, 예상 산출물, write scope, verification을 현재 문서와 코드에서 고정할 수 있다. | GitHub issue와 active exec plan을 만들고 작업을 시작한다. | `Received -> Routed -> Planned` |

`Rejected`는 네 번째 route가 아니라 terminal non-execution close-out이다. `대화`, 사용자 취소, 범위 밖 요청, interview 실패가 모두 `Rejected`로 닫힐 수 있다.

## Ambiguity Signals

아래 중 하나라도 남아 있으면 `모호한 요청`으로 분류한다.

- 대상 저장소, 파일, 문서 위치가 둘 이상으로 해석되며 source of truth만으로 하나로 줄일 수 없다.
- 하나의 요청 안에 둘 이상의 목표가 섞여 있어 `Issue 1개 = PR 1개` 원칙을 바로 적용할 수 없다.
- 완료 조건이나 산출물 형태가 없다. 예: "좀 개선", "정리", "다 고쳐줘", "알아서 처리".
- write scope가 잠기지 않는다. 예: workflow 문서 변경인지, backend 코드 수정인지, client UI 수정인지가 갈린다.
- 검증 기준을 적을 수 없다. 어떤 명령이나 어떤 문서 검토로 완료를 판정할지 정할 수 없다.
- source of truth가 서로 충돌하거나, 현재 canonical source가 없어서 작업자가 임의 정책을 만들어야 한다.
- 제품/디자인/운영 선호를 새로 결정해야 한다. source of truth에 없는 선택을 작업자가 대신 정하면 scope가 커진다.

아래는 ambiguity signal로 보지 않는다.

- 저장소 안에서 확인 가능한 사실을 아직 읽지 않은 상태
- `docs/product/work-item-catalog.md`나 기존 exec plan이 이미 기본 결정을 제공하는 경우
- 실행 도중 필요한 tool approval이나 네트워크 권한 요청만 남아 있는 경우

## Immediate Execution Criteria

아래 항목을 모두 만족하면 `즉시 실행 가능한 작업`으로 본다.

1. 목표가 하나다.
2. 대상 저장소가 하나로 고정된다.
3. 바꿀 자산 종류가 드러난다. 예: `docs/operations/`, 특정 app 모듈, 특정 test.
4. 산출물과 비범위를 exec plan에 바로 적을 수 있다.
5. 검증 명령 또는 문서 검토 절차를 적을 수 있다.
6. source of truth만으로 남은 선택을 처리할 수 있고, 새 사용자 선호를 물을 필요가 없다.

위 기준을 만족하면 issue와 active exec plan을 먼저 만들고, 그 다음 구현이나 문서 편집을 시작한다.

## Ambiguity Interview Policy

### Interview Objectives

interview의 목적은 요청을 더 크게 정의하는 것이 아니라, 아래 다섯 항목을 잠그는 것이다.

- 문제 정의
- 범위와 비범위
- 대상 저장소와 write scope
- 기대 산출물
- verification 방법

### Interview Rules

- 질문 전에 source of truth와 저장소를 먼저 읽어, 사용자에게 묻지 않아도 되는 사실은 직접 해소한다.
- 질문은 기본적으로 한 번에 하나의 blocker만 겨냥한다.
- 같은 답으로 함께 닫히는 ambiguity가 명확할 때만 한 라운드에 최대 세 가지까지 묶어 묻는다.
- 질문은 구현 아이디어를 늘리지 말고 범위를 줄이는 방향이어야 한다.
- 여러 목표가 섞여 있으면 "무엇을 먼저 한 issue로 고정할지"를 묻는다.
- 여러 저장소가 섞여 있으면 cross-repo 대작업으로 진행하지 말고, 이번 턴의 primary repo를 먼저 고정한다.
- work item catalog나 governance에 기본 결정이 있으면 그 결정을 기본값으로 사용하고, 사용자에게는 예외가 필요한 경우만 묻는다.
- ambiguity가 해소되면 바로 issue와 exec plan 형식으로 요약해 범위를 고정한다.

### Interview Exit Conditions

| 종료 상태 | 기준 | 다음 행동 |
| --- | --- | --- |
| `Planned` | issue의 reader-facing summary와 exec plan의 `Problem`, `Scope`, `Non-scope`, `Write Scope`, `Verification`을 채울 수 있다. | GitHub issue를 만들고 active exec plan을 작성한다. |
| `Blocked` | 실행 의도는 유지되지만, 사용자 응답이나 외부 canonical source가 없어 더 줄일 수 없다. | blocker를 명시하고 작업을 멈춘다. |
| `Rejected` | 사용자가 취소했거나, 대화만 원하거나, 허용된 저장소 밖 요청이거나, 필요한 narrowing이 source of truth 없이 새 정책 발명에 가까워졌다. | 실행을 종료하고 이유를 남긴다. |

같은 ambiguity signal이 두 번의 interview 라운드 뒤에도 그대로 남아 있으면 더 많은 질문으로 밀어붙이지 않는다. 이 경우 `Blocked` 또는 `Rejected`로 정리한다.

## Rejected Semantics

`Rejected`는 실패가 아니라 "이번 턴에서 실행을 계속하지 않음"을 뜻한다. 아래 reason을 canonical close-out reason으로 사용한다.

| Reason | 의미 | 예시 처리 |
| --- | --- | --- |
| `conversation-only` | 응답형 요청으로 끝났다. | 답변만 제공하고 종료 |
| `cancelled` | 사용자가 진행을 취소했다. | 편집 중지 후 종료 |
| `out-of-scope` | 허용 저장소나 현재 작업 경계를 벗어난다. | 범위 밖임을 알리고 종료 |
| `missing-canonical-source` | 작업자가 새 canonical policy를 발명해야만 진행 가능하다. | 후속 planning issue 후보로 남기고 종료 |
| `non-executable-after-interview` | 인터뷰 후에도 한 issue로 고정할 수 없다. | split 또는 후속 issue 제안 후 종료 |

## Example Classification

| 요청 | 판정 | 이유 | 다음 행동 |
| --- | --- | --- | --- |
| "`docs/README.md` 구조를 설명해줘" | `대화` | 응답만으로 끝나는 설명 요청이다. | 답변만 제공하고 종료 |
| "현재 catalog에 있는 request routing policy 작업을 진행해줘" | `즉시 실행 가능한 작업` | work item catalog와 시스템 문서가 이미 범위와 write scope를 제공해 issue와 exec plan을 바로 만들 수 있다. | issue 생성 후 exec plan 작성 |
| "랭킹 화면 좀 개선해줘" | `모호한 요청` | 대상 저장소, 화면 범위, 완료 조건이 없다. | 어떤 화면과 어떤 변경을 원하는지 interview |
| "backend랑 client 인증 흐름 다 정리하고 필요한 것들 한 번에 고쳐줘" | `모호한 요청` | 여러 저장소와 여러 목표가 섞여 있어 한 issue로 고정할 수 없다. | 이번 턴의 primary repo와 첫 issue를 고르도록 interview |
| "이 작업은 취소하고 지금은 정책 방향만 얘기하자" | `Rejected` (`cancelled`) | 실행 요청이 철회됐고 대화로 전환됐다. | 편집하지 않고 대화만 이어감 |

## Governance Hooks

- `즉시 실행 가능한 작업`만 GitHub issue와 active exec plan을 만든다.
- `모호한 요청` 단계에서는 issue, exec plan, 파일 편집을 시작하지 않는다.
- `대화`와 `Rejected` close-out은 문서 변경 없이 응답 또는 종료로 닫는다.
- 후속 intake/ambiguity skill은 이 문서의 route taxonomy와 interview exit condition을 그대로 재사용한다.
