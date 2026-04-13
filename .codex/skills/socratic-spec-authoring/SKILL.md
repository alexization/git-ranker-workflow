---
name: socratic-spec-authoring
description: 모든 즉시 실행 가능한 작업에서 소크라테스 질문으로 spec을 작성하고 승인 상태까지 고정할 때 사용한다. 답보다 질문이 먼저여야 하고, spec 안에 하위 작업, write scope, verification, tracking 결정을 함께 넣어야 할 때 이 skill을 사용한다.
---

# Socratic Spec Authoring

이 skill의 목적은 spec을 예쁘게 쓰는 것이 아니라, 구현 전에 요구사항을 충분히 명확하게 고정하는 것이다.

## 언제 사용하나

- `request-intake`가 `즉시 실행 가능한 작업`으로 끝났다.
- `ambiguity-interview`가 single spec 후보를 만든 뒤다.
- 구현 전에 승인된 spec이 필요하다.

## 먼저 확인할 것

- 최신 사용자 요청
- relevant source of truth
- `SPECS.md`
- `docs/operations/sdd-spec-policy.md`
- `docs/operations/workflow-governance.md`

## 작업 방식

1. source of truth로 닫을 수 있는 사실을 먼저 닫는다.
2. 답을 내놓지 말고 질문부터 시작한다.
3. 질문은 기본적으로 한 번에 하나의 blocker를 겨냥하고, 왜 지금 필요한지 짧게 붙인다.
4. 각 라운드에서 숨은 전제, 용어 정의, 범위 framing, 예외/반례 중 최소 하나를 점검한다.
5. framing 자체가 흔들리면 바로 답안을 쓰지 말고 alternative framing 또는 spec split 가능성을 먼저 제기한다.
6. 각 라운드 뒤에 확정된 점, 뒤집힌 가정, 남은 공백, 논리 충돌 여부를 짧게 요약한다.
7. approval gate가 비어 있으면 질문 루프를 계속하고 `Approved`로 올리지 않는다.
8. 충분히 명확해지면 clarification log와 approval gate를 포함한 spec 초안을 만든다.
9. 하위 작업이 필요하면 spec 안에 분해한다.
10. tracking issue/PR이 필요한지 spec 안에서 결정한다.
11. Harness 판단과 사용자 승인이 끝나면 spec 상태를 `Approved`로 고정한다.
12. verification, review, user validation에서 spec defect가 드러나면 repair 메모로 덮지 말고 spec을 다시 `Draft`로 열어 clarification loop를 재개한다.

## 결과

산출물은 `docs/specs/active/YYYY-MM-DD-<slug>.md`의 spec 문서다. 최소 아래가 바로 보여야 한다.

- request summary
- problem
- goals / non-goals
- socratic clarification log
- approval gate
- assumptions and constraints
- write scope
- acceptance criteria
- verification
- delivery and tracking plan
- detailed subtasks 필요 시
- approval status

## 빠른 점검 명령

```bash
sed -n '1,220p' SPECS.md
sed -n '1,260p' docs/operations/sdd-spec-policy.md
sed -n '1,260p' docs/operations/workflow-governance.md
```

## 피해야 할 것

- 질문 없이 바로 설계안이나 코드를 내놓지 않는다.
- 승인 전 구현, issue 생성, PR 생성을 시작하지 않는다.
- 하위 작업이 필요한데 spec 밖 TODO로만 남기지 않는다.
- write scope와 verification을 비운 spec을 `Approved`로 올리지 않는다.
- late-discovered spec defect를 code repair만으로 흡수하지 않는다.
