---
name: request-intake
description: 새 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 분류하고, 즉시 실행이면 `default`/`guarded` lane까지 고정한다. 요청이 설명형 대화인지 실제로 실행을 시작할 작업인지 먼저 가려야 할 때 이 skill을 사용한다.
---

# Request Intake

새 요청을 받으면 가장 먼저 route를 잠근다. 목표는 구현 아이디어를 늘리는 것이 아니라, 지금 이 턴이 답변으로 끝나는지, 인터뷰가 필요한지, 바로 실행 가능한지 빠르게 가르는 것이다.

## 언제 사용하나

- 새 사용자 요청이 들어왔다.
- 아직 issue, exec plan, 파일 편집을 시작하지 않았다.
- 요청이 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 어디에 속하는지 먼저 정해야 한다.

## 먼저 확인할 것

- 최신 사용자 요청 또는 issue draft
- `docs/operations/request-routing-policy.md`
- `docs/operations/workflow-governance.md`
- 관련 `docs/product/*.md` 또는 기존 exec plan

질문부터 던지지 말고 source of truth로 먼저 줄일 수 있는 ambiguity를 직접 줄인다. intake 단계에서는 아직 issue나 exec plan을 만들지 않는다.

## 작업 방식

1. 요청이 응답형 대화인지, 실제 실행 의도가 있는지 먼저 가른다.
2. 실행 의도가 있으면 ambiguity signal이 남아 있는지 본다.
3. source of truth만으로 대상 저장소, 산출물, write scope, verification을 잠글 수 있으면 `즉시 실행 가능한 작업`으로 둔다.
4. `즉시 실행 가능한 작업`이면 바로 `default lane`인지 `guarded lane`인지 고른다.
5. 하나라도 잠기지 않으면 `모호한 요청`으로 두고 남은 blocker만 정리한다.
6. 실행을 계속하지 않기로 하면 `Rejected` close-out reason을 남긴다.

## 결과

산출물은 짧은 route decision summary다.

- `대화`
  - 답변만 제공한다.
  - terminal close-out reason은 `conversation-only`다.
- `모호한 요청`
  - 남아 있는 ambiguity signal과 첫 blocker 질문을 남긴다.
  - 다음 단계는 `ambiguity-interview`다.
- `즉시 실행 가능한 작업`
  - 문제, 범위, write scope, verification 요약과 selected lane을 남긴다.
  - `guarded lane`이면 다음 단계는 `issue-to-exec-plan`이다.
  - `default lane`이면 task brief를 잠근 뒤 바로 구현으로 간다.
- `Rejected`
  - `cancelled`, `out-of-scope`, `missing-canonical-source` 같은 canonical reason을 남긴다.

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/request-routing-policy.md
sed -n '1,220p' docs/operations/workflow-governance.md
rg -n "<issue-id|task-name|surface noun>" docs/product docs/exec-plans .codex/skills
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
```

## 피해야 할 것

- source of truth를 읽기 전에 사용자에게 바로 여러 질문을 던지지 않는다.
- `즉시 실행 가능한 작업`으로 판정되기 전에는 issue, exec plan, 파일 편집을 시작하지 않는다.
- 여러 목표가 섞인 요청을 임의로 한 issue로 묶지 않는다.
- verification이나 write scope를 문서 근거 없이 상상해서 채우지 않는다.
- `대화` 요청을 구현 요청처럼 취급하지 않는다.
