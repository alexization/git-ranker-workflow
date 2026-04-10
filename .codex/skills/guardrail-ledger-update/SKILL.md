---
name: guardrail-ledger-update
description: verification과 review 결과가 고정된 뒤 guardrail ledger entry를 작성한다. normalized root cause, evidence, promotion decision 입력을 한 entry로 정리하고 feedback close-out을 닫아야 할 때 이 skill을 사용한다.
---

# Guardrail Ledger Update

목표는 feedback section을 길게 쓰는 것이 아니라, root cause 하나당 하나의 canonical entry를 정확히 남기는 것이다.

## 언제 사용하나

- latest verification 결과가 `passed`이거나 `blocked` 이유가 고정됐다.
- latest review verdict가 `approved`, `blocked`으로 고정됐거나 review 불가 사유가 정리됐다.
- exec plan close-out이나 follow-up artifact에 guardrail ledger entry를 남겨야 한다.

## 먼저 확인할 것

- active exec plan 또는 close-out artifact 경로
- `docs/operations/failure-to-guardrail-feedback-loop.md`
- `docs/operations/guardrail-ledger-template.md`
- latest verification evidence 또는 `Blocked` 이유
- latest review verdict 또는 review 불가 사유
- 관련 repair attempt, remaining risk, skipped check

빠뜨리기 쉬운 항목은 [references/feedback-closeout-minimum.md](references/feedback-closeout-minimum.md)로 다시 점검한다.

## 작업 방식

1. trigger signal과 root cause를 구분한다.
2. root cause 하나당 entry 하나만 잡는다.
3. template field를 빠짐없이 채운다.
4. promotion decision이 비어 있으면 `failure-to-policy`로 먼저 넘긴다.
5. decision이 돌아오면 ledger entry를 닫고 close-out artifact에 넣는다.

## 결과

산출물은 `Guardrail Ledger Entry` block이다. 최소 아래가 보이면 된다.

- date
- task / exec plan
- stage
- failure class
- trigger signal
- root cause
- existing guardrail
- recurrence
- current issue disposition
- promotion decision
- guardrail status
- decision rationale
- guardrail change or follow-up asset
- owner / next action
- evidence

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/failure-to-guardrail-feedback-loop.md
sed -n '1,220p' docs/operations/guardrail-ledger-template.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "## Verification Summary|## Verification Report|## Independent Review|Feedback|Guardrail" docs/exec-plans/active/<plan>.md
```

## 피해야 할 것

- verification 결과나 review verdict 없이 ledger entry를 먼저 닫지 않는다.
- latest review verdict가 `changes-requested`인데 feedback close-out trigger로 취급하지 않는다.
- 서로 다른 root cause를 한 entry에 섞지 않는다.
- symptom을 root cause 자리로 그대로 복사하지 않는다.
- promotion decision, guardrail status, owner / next action을 빈칸으로 두지 않는다.
- success path라는 이유로 `no-new-guardrail` 근거를 생략하지 않는다.
