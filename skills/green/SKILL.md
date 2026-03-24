---
name: green
description: Use this skill for the green phase of TDD when a failing test already exists and the goal is to make it pass by changing only production-side code.
---

# Green Implementation Turn

## Purpose

이미 잠근 failing test를 통과시키는 최소 구현을 만든다. 이 턴의 목적은 설계 정리가 아니라 pass를 만드는 것이다.

## Trigger

- 직전 red turn이 끝나 있고 failing test가 재현 가능하다.
- 실패 원인이 구현 부재 또는 구현 불일치로 확인됐다.
- 이제 behavior를 통과시키는 최소 구현이 필요하다.

## Inputs and Preconditions

- red turn에서 만든 failing test file과 명령이 있어야 한다.
- 테스트가 왜 실패하는지 이해하고 있어야 한다.
- 현재 작업의 exec plan과 직전 red turn 결과를 이미 확인한 상태여야 한다.
- 구현 범위가 애매하면 코드를 늘리기 전에 사용자에게 질문한다.
- 이 턴에서는 test file을 수정하지 않는다.

## Output and Artifact Location

- 산출물은 failing test를 green으로 바꾸는 production-side 변경이다.
- test file은 수정하지 않는다.
- 필요한 범위의 production 파일만 바꾼다.
- 작업 기록에는 어떤 구현 파일이 바뀌었는지와 어떤 명령으로 green을 확인했는지 남긴다.

## Standard Commands

먼저 red를 다시 재현한 뒤, 가장 작은 구현으로 targeted test를 green으로 만든다.

예시:

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

targeted test가 green이 되면, 필요할 때만 인접한 작은 범위의 suite를 추가로 확인한다.

## Required Evidence

- green을 확인한 명령
- 변경한 production file 목록
- test file을 수정하지 않았다는 확인
- 구현이 red에서 잠근 동작만 해결했다는 요약

## Forbidden Shortcuts

- test file을 수정하지 않는다.
- passing을 위해 assertion, fixture, mock을 뒤로 숨겨 바꾸지 않는다.
- refactor 성격의 cleanup을 이 턴에 섞지 않는다.
- 현재 failing test와 무관한 새 동작을 같이 구현하지 않는다.
- 필요 이상으로 넓은 구조 변경을 하지 않는다.

## Parallel Ownership Rule

- 한 agent는 한 behavior slice의 production 파일 집합만 소유한다.
- 같은 slice의 red/refactor와 파일 ownership이 겹치면 순서를 나눈다.
- shared core module을 건드려야 하면 다른 green 작업과 충돌하지 않게 범위를 먼저 고정한다.

## Handoff

refactor 턴으로 넘길 때는 아래를 함께 전달한다.

- green이 된 targeted test 명령
- 변경한 production file 목록
- 아직 남아 있는 중복, 냄새, 구조 개선 포인트
