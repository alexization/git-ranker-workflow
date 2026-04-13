---
name: parallel-work-split
description: 같은 spec에 둘 이상의 agent를 투입하기 전에 ownership, write set, merge 순서를 고정한다. shared file 충돌이나 cross-repo drift 위험이 있어 병렬 작업을 안전하게 나눠야 할 때 이 skill을 사용한다.
---

# Parallel Work Split

병렬화의 목적은 속도보다 충돌 제거다.

## 언제 사용하나

- 한 spec에 둘 이상의 agent를 넣으려 한다.
- 작업이 여러 저장소, 여러 디렉터리, 여러 책임 영역으로 갈라진다.

## 먼저 확인할 것

- approved spec
- active subtask와 acceptance criteria
- 대략적인 파일 집합

## 작업 방식

1. critical path와 side task를 먼저 나눈다.
2. agent별 disjoint write set을 만든다.
3. shared file이 꼭 필요하면 owner를 한 명만 둔다.
4. 저장소가 다르면 저장소별 branch/worktree를 분리한다.

## 결과

- owner
- 대상 저장소
- 목표
- write set
- read-only dependency
- handoff 조건
