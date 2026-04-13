---
name: context-pack-selection
description: approved spec 뒤에 task type별 primary context pack을 고르고, required docs와 optional trigger와 forbidden context를 잠가야 할 때 사용한다.
---

# Context Pack Selection

이 skill의 목적은 더 많은 문서를 읽는 것이 아니라, 지금 subtask에 필요한 최소 컨텍스트만 고정하는 것이다.

## 언제 사용하나

- approved spec이 준비됐고 구현 전에 primary context pack을 정해야 한다.
- task type은 이미 `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 중 하나로 좁혀졌다.

## 먼저 확인할 것

- approved spec
- `AGENTS.md`
- `docs/README.md`
- `SPECS.md`
- `docs/operations/workflow-governance.md`
- `docs/architecture/context-pack-registry.md`

## 작업 방식

1. spec에서 primary repo와 active subtask가 하나로 잠겼는지 확인한다.
2. registry의 mapping으로 primary context pack 하나를 고른다.
3. common base context와 선택한 pack의 required docs만 먼저 연다.
4. optional docs는 trigger와 함께 적고, forbidden context는 eager load 금지 surface로 분리한다.

## 결과

- primary repo
- active subtask
- primary context pack
- required docs
- optional docs trigger
- forbidden context
