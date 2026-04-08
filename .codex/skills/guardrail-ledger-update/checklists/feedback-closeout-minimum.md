# Feedback Close-Out Minimum Checklist

feedback close-out 전에 아래를 확인한다. 이 checklist는 `docs/operations/failure-to-guardrail-feedback-loop.md`와 `docs/operations/guardrail-ledger-template.md`의 thin layer다.

## Input Ready

- [ ] exec plan 또는 close-out artifact 경로가 고정돼 있다.
- [ ] latest verification report 또는 `Blocked` 이유가 있다.
- [ ] latest review verdict 또는 review 불가 사유가 있다.
- [ ] remaining risk, skipped check, repair note 중 relevant input을 모았다.
- [ ] root cause를 한 문장으로 적을 수 있다.

## Entry Quality

- [ ] root cause 하나당 entry 하나만 쓴다.
- [ ] `Trigger signal`과 `Root cause`를 구분했다.
- [ ] `Failure class`를 canonical vocabulary에서 골랐다.
- [ ] `Recurrence`를 `first-seen | repeated | systemic` 중 하나로 골랐다.
- [ ] `Current issue disposition`을 현재 상태에 맞게 적었다.
- [ ] `Promotion decision`과 `Guardrail status`를 둘 다 채웠다.
- [ ] `Owner / next action`과 `Evidence`를 비우지 않았다.

## Decision Guard

- [ ] 같은 root cause가 반복됐다면 `no-new-guardrail` 예외 사유를 명시했다.
- [ ] rule 자체가 비어 있는 문제라면 `docs-rule`을 먼저 검토했다.
- [ ] structured input 누락이 아니라면 `template`만으로 닫지 않았다.
- [ ] behavior regression이면 `test` 또는 `ci` 가능성을 먼저 봤다.
- [ ] 현재 issue에서 이미 guardrail을 추가했다면 그 사실을 ledger entry에 남겼다.

## Close-Out Hook

- [ ] follow-up asset, issue, 또는 없음 사유를 적었다.
- [ ] exec plan close-out 또는 review artifact에 feedback 판단 요약을 남길 위치를 정했다.
- [ ] root cause가 둘 이상이면 entry를 분리했다.
