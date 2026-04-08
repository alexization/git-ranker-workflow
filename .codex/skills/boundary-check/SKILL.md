---
name: boundary-check
description: context pack selection 뒤에 task type별 read/write/network/escalation 경계와 exec plan의 write scope completeness를 다시 잠가야 할 때 사용한다. 구현 전에 scope drift, sibling repo write, broad escalation을 막는 점검 절차에 적용한다.
---

# Boundary Check

이 skill의 목적은 더 넓은 접근을 정당화하는 것이 아니라, 지금 task가 이미 허용한 경계 안에서만 움직이도록 다시 확인하는 것이다.

## 언제 사용하나

- primary context pack이 정해졌고 구현 직전이다.
- active exec plan에 write scope와 verification contract profile이 적혀 있다.
- read/write/network/escalation 경계가 현재 task와 맞는지 다시 잠가야 한다.

write scope가 비어 있거나 primary repo가 흔들리면 구현으로 가지 말고 exec plan 또는 planning으로 되돌린다.

## 먼저 확인할 것

- active exec plan
- `docs/operations/tool-boundary-matrix.md`
- `docs/operations/workflow-governance.md`
- 필요하면 `docs/operations/verification-contract-registry.md`
- selected primary context pack summary

## 작업 방식

1. primary repo와 task type이 여전히 하나인지 확인한다.
2. 현재 읽으려는 문서와 파일이 selected context pack, issue, exec plan named input 안에 있는지 점검한다.
3. allowed write paths, control-plane artifacts, explicitly forbidden path가 exec plan에 모두 적혀 있는지 확인한다.
4. network 필요 여부를 `없음` 또는 목적 있는 외부 시스템으로 좁힌다.
5. escalation trigger는 sandbox에서 막힌 필수 명령만 남기고 convenience escalation은 지운다.
6. boundary conflict가 있으면 구현을 진행하지 말고 planning 갱신, scope 축소, `Blocked` 중 하나로 되돌린다.

## 결과

산출물은 boundary check summary다. 아래가 최소로 보여야 한다.

- task type
- read boundary
- write boundary
- control-plane artifact
- explicitly forbidden path
- network 필요 여부
- escalation trigger
- dangerous command no-go 또는 return signal

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/tool-boundary-matrix.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "Write Scope|Allowed write paths|Control-plane artifacts|Explicitly forbidden|Network / external systems|Escalation triggers" docs/exec-plans/active/<plan>.md
sed -n '1,220p' docs/operations/workflow-governance.md
```

## 피해야 할 것

- TODO, follow-up 메모, 사용자 한 줄 요청으로 write scope를 넓히지 않는다.
- network를 default allow처럼 취급하지 않는다.
- 더 좁은 대안이 있는데도 broad escalation을 요청하지 않는다.
- 여러 저장소 구현을 현재 issue 하나에 묶지 않는다.
- dangerous command를 필요성, 대상 경로, 대안 검토 없이 실행하지 않는다.
