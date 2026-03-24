---
name: refactor
description: Use this skill for the refactor phase of TDD when tests are already green and the goal is to improve code structure without changing behavior.
---

# Refactor Pass Turn

## Purpose

green을 유지한 채로 구조를 정리한다. 중복 제거, 이름 개선, helper 추출, 테스트 정돈은 가능하지만 외부 동작 의미는 바꾸지 않는다.

## Trigger

- targeted test가 이미 green이다.
- 현재 구현이나 테스트에 중복, 잡음, 구조적 냄새가 남아 있다.
- 새 behavior 추가가 아니라 existing behavior 정리가 목적이다.

## Inputs and Preconditions

- targeted test가 green이라는 기준선이 있어야 한다.
- 현재 behavior contract가 어떤 테스트로 잠겨 있는지 알고 있어야 한다.
- 현재 작업의 exec plan과 직전 green turn 결과를 이미 확인한 상태여야 한다.
- 테스트 파일을 건드릴 경우에도 의미 변경 없이 cleanup만 할 것이라는 기준을 먼저 지켜야 한다.
- assertion 의미를 바꿔야 할 것 같으면 refactor를 멈추고 사용자에게 질문한다.

## Output and Artifact Location

- 산출물은 pass를 유지한 구조 개선이다.
- production code는 수정할 수 있다.
- test file도 중복 제거, helper 추출, 이름 정리, setup 정돈처럼 비의미적 cleanup에 한해 수정할 수 있다.
- 작업 기록에는 어떤 코드 냄새를 줄였는지와 어떤 테스트로 green을 유지했는지 남긴다.

## Standard Commands

리팩터링 전후로 같은 기준의 테스트를 실행해 green 유지 여부를 확인한다.

예시:

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

필요하면 targeted test 외에 인접한 작은 suite를 추가로 확인한다. refactor 턴은 항상 green으로 끝나야 한다.

## Required Evidence

- refactor 후 green을 확인한 명령
- 변경한 file 목록
- test file을 수정했다면 "중복 제거", "helper 추출", "가독성 개선"처럼 비의미적 이유 요약
- behavior나 assertion 의미를 바꾸지 않았다는 확인

## Forbidden Shortcuts

- 새 behavior를 추가하지 않는다.
- failing test를 통과시키기 위해 기대 결과를 완화하지 않는다.
- assertion 의미, 시나리오 범위, contract 자체를 바꾸지 않는다.
- bug fix를 refactor로 위장하지 않는다.
- 테스트를 red 상태로 둔 채 끝내지 않는다.

## Parallel Ownership Rule

- refactor 대상 파일은 한 번에 한 agent만 소유한다.
- shared test file을 정리할 때는 그 파일을 건드리는 다른 agent 작업이 끝난 뒤 진행한다.
- implementation 변경과 test cleanup이 같이 들어가더라도 ownership 범위는 한 behavior slice 안으로 제한한다.

## Handoff

다음 작업으로 넘길 때는 아래를 정리한다.

- green을 유지한 검증 명령
- 제거한 중복 또는 개선한 구조 포인트
- 아직 남아 있지만 다음 slice로 넘긴 개선 항목
