---
name: request-intake
description: 새 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류한다. 실행 의도가 보이면 구현 전에 spec authoring으로 갈 수 있는지 먼저 가려야 할 때 사용한다.
---

# Request Intake

새 요청을 받으면 가장 먼저 route를 잠근다.

## 언제 사용하나

- 새 사용자 요청이 들어왔다.
- 아직 spec, issue, PR, 파일 편집을 시작하지 않았다.

## 먼저 확인할 것

- 최신 사용자 요청
- `docs/operations/request-routing-policy.md`
- `docs/operations/sdd-spec-policy.md`
- `docs/operations/workflow-governance.md`

## 작업 방식

1. 요청이 응답형 대화인지, 실제 실행 의도가 있는지 먼저 가른다.
2. 실행 의도가 있으면 single executable requirement로 줄일 수 있는지 본다.
3. 줄일 수 있으면 `즉시 실행 가능한 작업`으로 두고 다음 단계로 `socratic-spec-authoring`을 지정한다.
4. 줄일 수 없으면 `모호한 요청`으로 두고 남은 blocker를 정리한다.
5. 실행을 계속하지 않기로 하면 `Rejected` close-out reason을 남긴다.

## 결과

- `대화`
  - 답변만 제공한다.
- `모호한 요청`
  - 남아 있는 ambiguity signal과 첫 blocker 질문을 남긴다.
  - 다음 단계는 `ambiguity-interview`다.
- `즉시 실행 가능한 작업`
  - problem, primary repo candidate, expected outcome, next step이 보이는 route summary를 남긴다.
  - 다음 단계는 `socratic-spec-authoring`이다.
- `Rejected`
  - `cancelled`, `out-of-scope`, `missing-canonical-source` 같은 canonical reason을 남긴다.
