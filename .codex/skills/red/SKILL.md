---
name: red
description: TDD의 red 단계에서 한 개의 behavior slice를 failing test 하나로 고정한다. 구현보다 기대 동작을 먼저 잠가야 하고, 이 턴을 production code 변경 없이 끝내야 할 때 이 skill을 사용한다.
---

# Red Test Turn

이 턴의 목적은 명세를 잠그는 것이다. 실패 원인은 구현 공백이어야 하고, 잡음 때문에 실패하면 red로 간주하지 않는다.

## 언제 사용하나

- TDD로 시작한다.
- 현재 slice를 설명하는 failing test가 아직 없다.
- 구현보다 기대 동작을 먼저 고정해야 한다.

## 작업 방식

1. behavior slice를 하나로 줄인다.
2. test file 하나만 만들거나 수정한다.
3. 가장 좁은 테스트 명령으로 red를 확인한다.
4. 실패 원인이 구현 부재나 불일치인지 확인한다.
5. failing command와 이유를 기록하고 green으로 넘긴다.

## 빠른 점검 명령

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

## 피해야 할 것

- production code를 수정하지 않는다.
- test file을 둘 이상 수정하지 않는다.
- helper, fixture, mock, config 파일을 추가하지 않는다.
- green을 쉽게 만들기 위해 assertion을 약하게 쓰지 않는다.
- 여러 행동 조각을 한 red turn에 묶지 않는다.
