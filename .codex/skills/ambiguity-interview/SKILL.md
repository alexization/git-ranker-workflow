---
name: ambiguity-interview
description: `request-intake` 결과가 `모호한 요청`일 때, 남아 있는 blocker를 줄여 single executable spec 후보, `Blocked`, 또는 `Rejected`로 수렴시킨다.
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
2. 그중 하나를 닫을 수 있는 질문 한 개를 고른다.
3. single requirement, primary repo, expected outcome처럼 scope를 가장 많이 줄이는 질문부터 묻는다.
4. 답을 받은 뒤 `Spec Drafting`, `Blocked`, `Rejected` 중 하나로 정리한다.

## 결과

- `Spec Drafting`
  - 다음 단계는 `socratic-spec-authoring`이다.
- `Blocked`
  - 현재 spec 안에서 더 줄일 수 없는 blocker와 필요한 외부 입력을 남긴다.
- `Rejected`
  - canonical close-out reason을 남기고 실행을 종료한다.
