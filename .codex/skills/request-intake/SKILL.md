---
name: request-intake
description: 새 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류한다. 실행 의도가 보이면 구현 전에 spec authoring으로 갈 수 있는지 먼저 가려야 할 때 사용한다.
---

# Request Intake

새 요청을 받으면 가장 먼저 route를 잠근다. 이 skill은 route를 분류하고 다음 stage로 handoff하는 데만 쓴다.

## 언제 사용하나

- 새 사용자 요청이 들어왔다.
- 아직 spec, issue, PR, 파일 편집을 시작하지 않았다.

## 먼저 확인할 것

- 최신 사용자 요청
- `docs/operations/request-routing-policy.md`
- `docs/operations/workflow-governance.md`

## 작업 방식

1. `request-routing-policy.md` 기준으로 route만 결정한다.
2. `즉시 실행 가능한 작업`이면 problem, primary repo candidate, expected outcome을 한 줄씩 요약해 `socratic-spec-authoring`으로 넘긴다.
3. 이 단계는 spec approval을 받는 단계가 아니다. 사용자의 초기 작업 요청을 spec 승인으로 해석하지 않는다.
4. `모호한 요청`이면 남아 있는 ambiguity signal과 첫 blocker 하나만 적어 `ambiguity-interview`로 넘긴다.
5. `대화`면 사용자 질문에 대한 답변을 제공하고 종료한다.
6. `Rejected`면 close-out reason만 남기고 종료한다.

## 결과

- route
- route reason
- next stage 또는 close-out reason

`대화` route에서는 close-out reason 대신 실제 답변이 결과여야 한다.

## 피해야 할 것

- spec-level 질문, approval gate, write scope를 여기서 잠그려는 것
- 사용자의 작업 요청을 spec approval로 오인하는 것
- route를 정하지 않은 채 바로 구현이나 spec 편집으로 들어가는 것
