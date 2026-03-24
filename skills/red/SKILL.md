---
name: red
description: Use this skill for the red phase of TDD when the current turn must end with exactly one failing test file and zero production code changes.
---

# Red Test Turn

## Purpose

한 개의 작은 행동 조각을 실행 가능한 failing test로 고정한다. 이 턴의 목적은 구현이 아니라 기대 동작을 먼저 잠그는 것이다.

## Trigger

- 사용자가 TDD로 시작하자고 요청했다.
- 현재 slice를 설명하는 failing test가 아직 없다.
- 다음 단계에서 구현보다 명세 고정이 먼저 필요하다.

## Inputs and Preconditions

- 구현할 동작 slice가 하나로 좁혀져 있어야 한다.
- 대상 저장소와 현재 테스트 프레임워크를 알고 있어야 한다.
- 현재 작업의 exec plan과 관련 source of truth 문서를 이미 확인한 상태여야 한다.
- 기대 동작이나 실패 방식이 애매하면 테스트를 쓰기 전에 사용자에게 질문한다.
- 이 턴에 섞일 다른 production 변경은 분리되어 있어야 한다.

## Output and Artifact Location

- 산출물은 변경된 test file 하나뿐이다.
- 새 파일을 만들거나 기존 test file 하나를 수정할 수는 있지만, test file은 하나만 건드린다.
- production code, config, docs, fixture helper 파일은 바꾸지 않는다.
- exec plan 또는 작업 기록에는 failing command와 실패 이유 요약을 남긴다.

## Standard Commands

가장 좁은 범위의 기존 테스트 명령을 선택해 red를 확인한다.

예시:

```bash
./gradlew test --tests com.gitranker.ranking.RankingServiceTest
npm test -- ranking-page.test.ts
npx vitest run src/features/ranking/ranking-page.test.ts
```

실패 원인은 구현 공백이어야 한다. syntax error, import 오류, 환경 미설정 같은 잡음으로 실패하면 red로 간주하지 않는다.

## Required Evidence

- 변경한 test file 경로
- red를 확인한 명령
- 기대한 이유로 실패했다는 요약
- production file이 변경되지 않았다는 확인

## Forbidden Shortcuts

- production code를 수정하지 않는다.
- test file을 둘 이상 수정하지 않는다.
- helper, fixture, mock, config 파일을 추가하지 않는다.
- green을 쉽게 만들기 위해 assertion을 약하게 쓰지 않는다.
- 여러 행동 조각을 한 red turn에 묶지 않는다.

## Parallel Ownership Rule

- 한 agent는 한 behavior slice와 한 test file만 소유한다.
- 같은 slice의 green/refactor를 다른 agent가 하고 있다면 동시에 같은 파일을 건드리지 않는다.
- 공용 test file을 수정해야 하면 먼저 ownership을 명확히 나눈다.

## Handoff

green 턴으로 넘길 때는 아래 세 가지를 함께 전달한다.

- failing test file 경로
- red를 재현하는 명령
- 이 테스트가 잠그는 행동 설명 한 줄
