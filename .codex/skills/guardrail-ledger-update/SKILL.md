---
name: guardrail-ledger-update
description: verification과 review 결과가 고정된 뒤 guardrail ledger entry를 작성한다. normalized root cause, evidence, promotion decision 입력을 한 entry로 정리하고 feedback close-out을 닫아야 할 때 이 skill을 사용한다.
---

# Guardrail Ledger Update

목표는 feedback section을 길게 쓰는 것이 아니라, root cause 하나당 하나의 canonical entry를 정확히 남기는 것이다.

## 언제 사용하나

- latest verification 결과가 `passed`이거나 `blocked` 이유가 고정됐다.
- latest review verdict가 고정됐거나 review 불가 사유가 정리됐다.
- spec close-out이나 follow-up artifact에 guardrail ledger entry를 남겨야 한다.

## 먼저 확인할 것

- approved spec 또는 close-out artifact 경로
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- latest verification evidence 또는 `Blocked` 이유
- latest review verdict 또는 review 불가 사유

## 작업 방식

1. trigger signal과 root cause를 구분한다.
2. root cause 하나당 entry 하나만 잡는다.
3. template field를 빠짐없이 채운다.
4. promotion decision이 비어 있으면 `failure-to-policy`로 먼저 넘긴다.

## 결과

- date
- task / spec
- stage
- failure class
- trigger signal
- root cause
- promotion decision
- owner / next action
