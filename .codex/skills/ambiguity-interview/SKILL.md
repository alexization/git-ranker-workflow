---
name: ambiguity-interview
description: "`request-intake` 결과가 `모호한 요청`일 때, 남아 있는 blocker를 줄여 single executable spec 후보, `Blocked`, 또는 `Rejected`로 수렴시킨다."
---

# Ambiguity Interview

이 skill은 질문을 늘리는 용도가 아니라 질문을 줄이는 용도다.

## 언제 사용하나

- `request-intake`가 `모호한 요청`으로 끝났다.
- source of truth를 읽고도 single requirement나 primary repo가 잠기지 않는다.

## 먼저 확인할 것

- 최신 사용자 요청
- `docs/operations/request-routing-policy.md`
- 관련 product 문서와 저장소 entry 문서

## 작업 방식

1. 남아 있는 ambiguity signal을 짧게 적는다.
2. 그중 하나를 가장 많이 줄일 수 있는 blocker 질문 한 개를 고른다.
3. 질문에는 왜 지금 이 답이 필요한지 짧게 붙인다.
4. 질문을 고를 때는 single requirement, primary repo, expected outcome, 숨은 다중 목표 여부 중 무엇을 잠그는지 먼저 분명히 한다.
5. spec authoring 단계에서 닫아도 되는 세부사항까지 여기서 미리 캐묻지 않는다.
6. 답을 받은 뒤에는 무엇이 잠겼고 무엇이 아직 안 잠겼는지 짧게 요약한다.
7. single requirement와 primary repo가 잠기면 `Spec Drafting`으로 넘기고, 그렇지 않으면 다음 blocker 또는 `Blocked`/`Rejected`를 정리한다.

## 결과

- `Spec Drafting`
  - 무엇이 잠겼는지와 남은 spec-level 질문 후보를 함께 남긴다.
  - 다음 단계는 `socratic-spec-authoring`이다.
- `Blocked`
  - 현재 spec 안에서 더 줄일 수 없는 blocker와 필요한 외부 입력을 남긴다.
- `Rejected`
  - canonical close-out reason을 남기고 실행을 종료한다.

## 피해야 할 것

- 한 번에 여러 blocker 질문을 쏟아내는 것
- spec authoring 단계에서 닫아야 할 write scope, verification detail까지 ambiguity 단계에서 미리 확정하려는 것
- 답을 받은 뒤에도 무엇이 잠겼는지 요약 없이 바로 다음 질문으로 넘어가는 것
