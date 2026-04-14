---
name: refactor
description: TDD의 refactor 단계에서 green을 유지한 채 구조만 정리한다. 새 behavior를 추가하지 않고 중복 제거, 이름 개선, helper 추출 같은 정리를 해야 할 때 이 skill을 사용한다.
---

# Refactor Pass Turn

refactor는 의미를 바꾸지 않는 정리다. assertion 의미나 contract가 달라질 것 같으면 refactor를 멈추고 다시 범위를 좁힌다.

## 언제 사용하나

- targeted test가 이미 green이다.
- 구현이나 테스트에 중복, 잡음, 구조적 냄새가 남아 있다.
- 새 behavior 추가가 아니라 existing behavior 정리가 목적이다.

## 작업 방식

1. 어떤 냄새를 줄일지 먼저 짧게 정한다.
2. green을 깨지 않는 범위에서 production code와 test code를 정리한다.
3. test file을 건드린다면 의미 변경 없는 cleanup에만 한정한다.
4. 같은 테스트 기준으로 다시 green을 확인한다.
5. 남은 개선 포인트가 있으면 다음 slice로 넘긴다.

## 빠른 점검 명령

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

필요하면 targeted test 외에 인접한 작은 suite를 추가로 확인한다. refactor는 항상 green으로 끝나야 한다.

## 피해야 할 것

- 새 behavior를 추가하지 않는다.
- failing test를 통과시키기 위해 기대 결과를 완화하지 않는다.
- assertion 의미, 시나리오 범위, contract 자체를 바꾸지 않는다.
- bug fix를 refactor로 위장하지 않는다.
- 테스트를 red 상태로 둔 채 끝내지 않는다.
