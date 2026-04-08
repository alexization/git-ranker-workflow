---
name: parallel-work-split
description: 같은 issue에 둘 이상의 agent를 투입하기 전에 ownership, write set, merge 순서를 고정한다. shared file 충돌이나 cross-repo drift 위험이 있어 병렬 작업을 안전하게 나눠야 할 때 이 skill을 사용한다.
---

# Parallel Work Split

병렬화의 목적은 속도보다 충돌 제거다. critical path는 main rollout이 직접 잡고, 독립적인 side task만 분리한다.

## 언제 사용하나

- 한 issue에 둘 이상의 agent를 넣으려 한다.
- 작업이 여러 저장소, 여러 디렉터리, 여러 책임 영역으로 갈라진다.
- shared file 충돌이나 merge 순서 문제가 예상된다.

## 먼저 확인할 것

- active exec plan
- acceptance criteria, non-scope, write scope
- 대략적인 파일 집합

cross-repo 변경이면 `workflow 문서 PR`과 `앱 코드 PR`을 분리한다는 기본 원칙을 먼저 적용한다.

## 작업 방식

1. critical path와 side task를 먼저 나눈다.
2. agent별 disjoint write set을 만든다.
3. shared file이 꼭 필요하면 owner를 한 명만 둔다.
4. 저장소가 다르면 저장소별 branch/worktree를 분리한다.
5. ownership 표와 handoff 조건을 남긴 뒤에만 병렬 작업을 시작한다.

## 결과

산출물은 ownership 표 또는 동등한 분할 메모다. 최소 아래가 보이면 된다.

- owner
- 대상 저장소
- 목표
- write set
- read-only dependency
- handoff 조건
- merge 위험

## 빠른 점검 명령

```bash
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
rg --files skills docs git-ranker git-ranker-client
git -C git-ranker status --short
git -C git-ranker-client status --short
```

## 피해야 할 것

- `frontend`, `backend`, `docs`처럼 너무 넓은 이름만 적고 실제 write set을 비워두지 않는다.
- 같은 shared file을 두 agent에게 동시에 배정하지 않는다.
- 아직 결정되지 않은 요구사항을 agent별로 따로 해석하게 두지 않는다.
- cross-repo 변경을 한 PR이나 한 branch로 뭉개지 않는다.
- 바로 다음 행동이 막히는 critical path를 통째로 다른 agent에게 넘기고 기다리지 않는다.
