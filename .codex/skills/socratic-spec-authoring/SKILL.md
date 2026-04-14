---
name: socratic-spec-authoring
description: 모든 즉시 실행 가능한 작업에서 소크라테스 질문으로 spec을 세부화하고, 더 이상 blocker 질문이 없을 때만 승인 요청을 거쳐 승인 상태까지 고정할 때 사용한다. 답보다 질문이 먼저여야 하고, spec 안에 하위 작업, write scope, verification, tracking 결정을 함께 넣어야 할 때 이 skill을 사용한다.
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
- `assets/spec-template.md`

## 작업 방식

1. 사실 확인과 question contract는 `docs/operations/sdd-spec-policy.md`를 그대로 따른다.
2. source of truth로 먼저 닫고도 남는 blocker만 질문한다.
3. 질문 루프와 답변 요약은 active spec의 clarification log에 직접 남긴다.
4. Harness가 approval gate를 채우기에 더 이상 blocker 질문이 없다고 판단하기 전에는 승인 요청으로 넘어가지 않는다.
5. approval gate, write scope, verification, tracking decision이 비어 있으면 spec을 `Approved`로 올리지 않는다.
6. 충분히 잠기면 spec 초안을 만들고, 그 초안에 대해 사용자에게 명시적 승인 요청을 한다.
7. 사용자가 현재 spec 초안에 명시적으로 동의했을 때만 `Approved`로 상태를 고정한다.
8. verification, review, user validation에서 spec defect가 드러나면 별도 planning 메모를 만들지 말고 spec을 다시 `Draft`로 내려 재질의응답을 연다.

## 결과

- `docs/specs/active/YYYY-MM-DD-<slug>.md` spec 문서
- clarification log와 approval gate가 채워진 canonical requirement artifact
- 다음 stage가 implementation이면 approved spec, 아니라면 reopened draft 또는 stop signal

## 피해야 할 것

- 질문 없이 바로 설계안이나 코드를 내놓지 않는다.
- 더 이상 blocker 질문이 남아 있는데 승인 요청부터 하지 않는다.
- 사용자의 작업 요청 자체를 spec approval로 간주하지 않는다.
- 승인 전 구현, issue 생성, PR 생성을 시작하지 않는다.
- 하위 작업이 필요한데 spec 밖 TODO로만 남기지 않는다.
- write scope와 verification을 비운 spec을 `Approved`로 올리지 않는다.
- late-discovered spec defect를 code repair만으로 흡수하지 않는다.
