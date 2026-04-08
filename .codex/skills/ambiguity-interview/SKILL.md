---
name: ambiguity-interview
description: "`request-intake` 결과가 `모호한 요청`일 때, 남아 있는 blocker를 줄여 하나의 executable issue, `Blocked`, 또는 `Rejected`로 수렴시킨다. source of truth를 읽고도 대상 저장소, 범위, verification을 바로 잠글 수 없을 때 이 skill을 사용한다."
---

# Ambiguity Interview

이 skill은 질문을 늘리는 용도가 아니라 질문을 줄이는 용도다. 남은 ambiguity signal을 하나씩 없애서, `issue-to-exec-plan`으로 넘길 수 있거나 더 이상 줄일 수 없다는 사실을 분명히 남긴다.

## 언제 사용하나

- `request-intake`가 `모호한 요청`으로 끝났다.
- source of truth를 읽고도 ambiguity signal이 남아 있다.
- 어떤 질문 하나가 scope를 실질적으로 줄일지 먼저 정해야 한다.

## 먼저 확인할 것

- 최신 사용자 요청 또는 issue draft
- `request-intake` summary
- `docs/operations/request-routing-policy.md`
- 관련 product 문서, 기존 exec plan, 저장소 entry 문서

interview 전에 문서로 해소 가능한 사실은 먼저 줄인다. 이미 있는 기본 결정을 다시 묻지 않는다.

## 작업 방식

1. 남아 있는 ambiguity signal을 짧게 적는다.
2. 그중 하나를 닫을 수 있는 질문 한 개를 고른다.
3. primary repo, 첫 issue, 완료 조건처럼 scope를 가장 많이 줄이는 질문부터 묻는다.
4. 답을 받은 뒤 `Planned`, `Blocked`, `Rejected` 중 하나로 정리한다.
5. 같은 signal이 두 라운드 뒤에도 그대로 남으면 더 밀어붙이지 않고 `Blocked` 또는 `Rejected`로 닫는다.

## 결과

산출물은 interview exit summary다.

- `Planned`
  - 문제 정의, why now, 범위, 비범위, write scope, verification을 적을 수 있는 입력을 남긴다.
  - 다음 단계는 `issue-to-exec-plan`이다.
- `Blocked`
  - 현재 issue 안에서 더 줄일 수 없는 blocker와 필요한 외부 입력을 남긴다.
- `Rejected`
  - canonical close-out reason을 남기고 실행을 종료한다.

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/request-routing-policy.md
rg -n "<repo|surface noun|issue-id>" docs/product docs/exec-plans docs .codex/skills
sed -n '1,220p' <candidate-source-of-truth>
```

## 피해야 할 것

- 한 번에 긴 설문을 던지지 않는다.
- 요구사항을 더 크게 만들거나 새 기능 아이디어를 제안하지 않는다.
- source of truth에 없는 제품/설계 선호를 대신 결정하지 않는다.
- `Planned`가 되기 전에는 issue 생성, exec plan 작성, 파일 편집을 시작하지 않는다.
- 같은 ambiguity signal이 두 번 남았는데도 더 많은 질문으로 밀어붙이지 않는다.
