---
name: failure-to-policy
description: normalized root cause를 가장 작은 guardrail asset으로 연결한다. `docs-rule`, `skill`, `test`, `ci`, `template`, `no-new-guardrail` 중 무엇으로 승격할지와 그 이유를 결정해야 할 때 이 skill을 사용한다.
---

# Failure To Policy

이 skill은 follow-up을 많이 만드는 데 목적이 있지 않다. 같은 실패를 가장 이른 차단 지점에서 끊는 가장 작은 자산을 고르는 데 목적이 있다.

## 언제 사용하나

- guardrail ledger entry 초안은 있는데 `Promotion decision`과 `Guardrail status`가 비어 있다.
- 같은 root cause를 어떤 자산으로 승격할지 판단해야 한다.
- `no-new-guardrail` 예외를 써도 되는지 검토해야 한다.

## 먼저 확인할 것

- normalized root cause와 trigger signal
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- current issue disposition
- recurrence 근거
- existing guardrail 또는 `없음`

## 작업 방식

1. failure class를 고른다.
2. existing guardrail과 recurrence를 함께 본다.
3. 가장 이른 차단 지점을 기준으로 promotion decision을 고른다.
4. canonical vocabulary에 맞춰 guardrail status를 적는다.
5. rationale, follow-up asset, next owner를 남긴다.

## 결과

산출물은 ledger entry에 바로 복사할 수 있는 policy decision summary다. 최소 아래가 필요하다.

- failure class
- existing guardrail
- recurrence
- selected promotion decision
- selected guardrail status
- decision rationale
- guardrail change or follow-up asset
- owner / next action

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/failure-to-guardrail-feedback-loop.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "Guardrail Ledger Entry|Failure class|Promotion decision|Root cause" docs/exec-plans docs/operations
```

## 피해야 할 것

- 같은 root cause가 반복됐는데 예외 근거 없이 `no-new-guardrail`로 닫지 않는다.
- canonical rule이 비어 있는데 `skill`이나 `template`만으로 덮지 않는다.
- behavior regression을 문서 메모만으로 닫지 않는다.
- structured input 누락이 아닌 문제를 `template`으로 오분류하지 않는다.
- 새 decision vocabulary나 새 recurrence level을 만들지 않는다.
