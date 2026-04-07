---
name: parallel-work-split
description: Use this skill when more than one agent will work on the same issue and ownership, write sets, and merge risk must be fixed first.
---

# Parallel Work Split

## Purpose

여러 agent가 같은 목표를 동시에 다룰 때 write set, ownership, merge 위험, handoff 순서를 먼저 고정한다. 목적은 “많이 나누는 것”이 아니라 “겹치지 않게 나누는 것”이다.

## Trigger

- 한 Issue에 둘 이상의 agent를 투입하려고 한다.
- 작업이 여러 저장소, 여러 디렉터리, 여러 책임 영역으로 갈라진다.
- shared file 충돌이나 cross-repo drift 위험이 높다.
- critical path와 side task를 먼저 구분해야 한다.

## Inputs and Preconditions

- active exec plan이 이미 있어야 한다.
- acceptance criteria, non-scope, write scope가 고정돼 있어야 한다.
- 어떤 저장소와 파일 집합이 바뀔지 대략 알고 있어야 한다.
- cross-repo 변경이면 `workflow 문서 PR`과 `앱 코드 PR`을 분리한다는 governance 규칙을 먼저 따른다.
- 가장 긴급한 blocking task는 main rollout이 직접 잡고, 독립 side task만 병렬로 나눈다.
- ownership이 애매하면 agent를 나누기 전에 사용자에게 질문한다.

## Output and Artifact Location

- 산출물은 exec plan, 작업 메모, 또는 PR 설명에 남기는 ownership 표다.
- 표에는 최소한 아래가 들어간다.
  - agent 또는 담당자 이름
  - 대상 저장소
  - 목표
  - write set
  - read-only dependency
  - handoff 조건
  - merge 위험
- 저장소가 다르면 저장소별 branch/worktree를 분리한다.

## Standard Commands

겹치는 파일과 범위를 확인하는 기본 명령 예시:

```bash
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
rg --files skills docs git-ranker git-ranker-client
git -C git-ranker status --short
git -C git-ranker-client status --short
```

핵심은 명령 자체보다, 같은 파일을 둘 이상 건드리지 않게 ownership 표를 만드는 것이다.

## Required Evidence

- ownership 표 또는 동등한 분할 기록
- 겹치지 않는 write set 목록
- shared file 또는 순차 작업이 필요한 파일 목록
- critical path와 side task 구분
- cross-repo라면 저장소별 PR 분리 원칙 반영 여부

## Forbidden Shortcuts

- `frontend`, `backend`, `docs`처럼 너무 넓은 이름만 적고 실제 write set을 비워두지 않는다.
- 같은 shared file을 두 agent에게 동시에 배정하지 않는다.
- 아직 결정되지 않은 요구사항을 agent별로 따로 해석하게 두지 않는다.
- cross-repo 변경을 한 PR이나 한 branch로 뭉개지 않는다.
- 바로 다음 행동이 막히는 critical path를 통째로 다른 agent에게 넘기고 기다리지 않는다.

## Parallel Ownership Rule

- agent마다 disjoint write set을 가져야 한다.
- shared file이 꼭 필요하면 한 agent만 owner가 되고, 나머지는 read-only로 둔다.
- 저장소가 다르면 저장소별 branch/worktree를 분리한다.
- 문서 owner, 구현 owner, 검증 owner를 나눌 수는 있지만 최종 통합 책임자는 한 명이어야 한다.

## Parallel Execution Don'ts

- 같은 파일을 “조금씩” 나눠서 동시에 수정하지 않는다.
- backend contract가 아직 정해지지 않았는데 client/doc 작업을 병렬 시작하지 않는다.
- plan owner 없이 각 agent가 scope를 재정의하게 두지 않는다.
- merge 순서가 필요한 작업을 독립 작업처럼 포장하지 않는다.

## Example Input

- Issue: `<issue-id>`
- Goal: route-level E2E harness
- Known write scope:
  - `<target-repo>/<config-file>`
  - `<target-repo>/<test-dir>/**`
  - 최소 test hook 후보 파일
  - workflow 문서의 artifact 규칙

## Example Output

```md
| owner | repo | goal | write set | handoff |
| --- | --- | --- | --- | --- |
| main | `<target-repo>` | base config | `<config-file>`, package script | config green 후 spec owner로 전달 |
| agent-a | `<target-repo>` | route spec | `<test-spec-file>` | config merge 기준에 맞춰 spec 작성 |
| agent-b | `git-ranker-workflow` | artifact/doc 연결 | `docs/exec-plans/...`, workflow artifact note | spec path와 artifact path 확인 후 문서 반영 |
```

이 예시에서 `<config-file>`은 main owner만 수정한다. config가 고정되기 전에는 spec과 workflow artifact 문서를 병렬로 밀어붙이지 않는다.

## Handoff

병렬 작업을 시작할 때는 아래를 함께 전달한다.

- ownership 표
- 금지된 shared file 목록
- merge 순서
- 각 owner가 남겨야 할 evidence
