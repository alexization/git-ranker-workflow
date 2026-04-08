---
name: green
description: TDD의 green 단계에서 이미 잠긴 failing test를 최소한의 production-side 변경으로 통과시킨다. test file을 건드리지 않고 현재 behavior slice만 green으로 만들어야 할 때 이 skill을 사용한다.
---

# Green Implementation Turn

이 턴의 목적은 설계 정리가 아니라 pass를 만드는 것이다. 필요한 범위의 production 파일만 바꾸고, test file은 그대로 둔다.

## 언제 사용하나

- red turn이 끝났고 failing test가 재현된다.
- 실패 원인이 구현 부재 또는 구현 불일치다.
- 이제 behavior를 통과시키는 최소 구현이 필요하다.

## 작업 방식

1. red를 다시 재현한다.
2. failing reason을 이해한다.
3. test file은 건드리지 않고 production-side 변경만 한다.
4. targeted test를 green으로 만든다.
5. 필요한 경우에만 인접한 작은 범위의 suite를 추가 확인한다.

## 빠른 점검 명령

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

## 피해야 할 것

- test file을 수정하지 않는다.
- passing을 위해 assertion, fixture, mock을 뒤로 숨겨 바꾸지 않는다.
- refactor 성격의 cleanup을 이 턴에 섞지 않는다.
- 현재 failing test와 무관한 새 동작을 같이 구현하지 않는다.
- 필요 이상으로 넓은 구조 변경을 하지 않는다.
