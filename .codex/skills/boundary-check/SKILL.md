---
name: boundary-check
description: context pack selection 뒤에 task type별 read/write/network/escalation 경계와 approved spec의 write scope completeness를 다시 잠가야 할 때 사용한다.
---

# Boundary Check

이 skill의 목적은 더 넓은 접근을 정당화하는 것이 아니라, 현재 subtask가 이미 허용한 경계 안에서만 움직이도록 다시 확인하는 것이다.

## 언제 사용하나

- primary context pack이 정해졌고 구현 직전이다.
- approved spec에 write scope와 verification contract profile이 적혀 있다.

## 먼저 확인할 것

- approved spec
- `docs/operations/tool-boundary-matrix.md`
- `docs/operations/workflow-governance.md`
- 필요하면 `docs/operations/verification-contract-registry.md`

## 작업 방식

1. primary repo와 active subtask가 여전히 하나인지 확인한다.
2. 현재 읽으려는 문서와 파일이 selected context pack과 spec named input 안에 있는지 점검한다.
3. allowed write paths, control-plane artifacts, explicitly forbidden path가 spec에 모두 적혀 있는지 확인한다.
4. network와 escalation trigger를 최소 범위로 좁힌다.

## 결과

- task type
- read boundary
- write boundary
- control-plane artifact
- explicitly forbidden path
- network 필요 여부
- escalation trigger
