---
name: failure-to-policy
description: normalized root cause를 가장 작은 guardrail asset으로 연결한다. `docs-rule`, `skill`, `test`, `ci`, `template`, `no-new-guardrail` 중 무엇으로 승격할지와 그 이유를 결정해야 할 때 이 skill을 사용한다.
---

# Failure To Policy

이 skill은 같은 실패를 가장 이른 차단 지점에서 끊는 가장 작은 자산을 고르는 데 목적이 있다.

## 언제 사용하나

- guardrail ledger entry 초안은 있는데 `Promotion decision`과 `Guardrail status`가 비어 있다.
- 같은 root cause를 어떤 자산으로 승격할지 판단해야 한다.

## 먼저 확인할 것

- normalized root cause와 trigger signal
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- current issue disposition
- recurrence 근거
- existing guardrail 또는 `없음`

## 결과

- failure class
- existing guardrail
- recurrence
- selected promotion decision
- selected guardrail status
- decision rationale
- guardrail change or follow-up asset
- owner / next action
