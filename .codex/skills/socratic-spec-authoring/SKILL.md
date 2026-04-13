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
3. 질문은 기본적으로 한 번에 하나의 blocker를 겨냥한다.
4. 각 라운드 뒤에 확정된 점, 가정, 남은 공백을 짧게 요약한다.
5. 충분히 명확해지면 spec 초안을 만든다.
6. 하위 작업이 필요하면 spec 안에 분해한다.
7. tracking issue/PR이 필요한지 spec 안에서 결정한다.
8. Harness 판단과 사용자 승인이 끝나면 spec 상태를 `Approved`로 고정한다.

## 결과

산출물은 `docs/specs/active/YYYY-MM-DD-<slug>.md`의 spec 문서다. 최소 아래가 바로 보여야 한다.

- request summary
- problem
- goals / non-goals
- socratic clarification summary
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
