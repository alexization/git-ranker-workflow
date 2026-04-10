---
name: reviewer-handoff
description: review가 실제로 필요할 때 latest verification evidence를 바탕으로 reviewer minimum context를 묶고, open PR 기준 review evidence를 남긴다. implementer와 reviewer 세션 분리를 유지한 채 review를 시작해야 할 때 이 skill을 사용한다.
---

# Reviewer Handoff

reviewer가 더 많은 문서를 읽게 만드는 것이 목적이 아니다. review를 시작하기에 충분한 minimum context를 한 번만 만들고, 필요한 경우에만 reviewer를 붙인다.

## 언제 사용하나

- latest verification report 또는 verification summary의 overall status가 `passed`다.
- independent review를 시작해야 한다.
- open PR이 이미 생성됐다.
- review evidence를 exec plan이나 close-out artifact에 남겨야 한다.

## 먼저 확인할 것

- task brief 또는 active exec plan
- latest verification evidence
- touched diff summary와 touched file/doc 목록
- source-of-truth update 목록 또는 업데이트 불필요 사유
- remaining risk, skipped checks, follow-up 필요 사항
- `docs/operations/dual-agent-review-policy.md`

## 작업 방식

1. reviewer minimum context 다섯 가지를 한 번에 묶는다.
2. reviewer가 한 명이면 그대로 넘기고, high-risk surface일 때만 role과 role별 focus를 추가한다.
3. implementer와 reviewer 세션을 분리한 채 review를 시작한다.
4. finding과 verdict를 모은다.
5. reviewer pool을 썼다면 final verdict owner가 aggregated verdict를 잠그고 evidence block에 남긴다.

## 결과

산출물은 handoff summary와 `Independent Review` evidence block이다. evidence block에는 아래가 바로 보여야 한다.

- reviewer 역할
- reviewer 이름
- aggregated verdict if reviewer pool was used
- role별 finding 또는 no-blocking note
- final verdict owner if reviewer pool was used

review는 open PR 생성 이후에 수행한다. `approved` verdict는 publish timing을 뒤로 미루지 않는다.

## 빠른 점검 명령

```bash
sed -n '61,210p' docs/operations/dual-agent-review-policy.md
sed -n '257,296p' docs/operations/verification-contract-registry.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
git diff --stat
git diff --name-only
rg -n "## Verification Summary|## Verification Report|## Independent Review" docs/exec-plans/active/<plan>.md
```

## 피해야 할 것

- latest verification evidence가 `passed`가 아니면 review로 넘기지 않는다.
- implementer가 reviewer coordinator를 겸하지 않는다.
- reviewer role을 늘리면서 minimum context를 줄이지 않는다.
- skipped checks나 remaining risk를 숨긴 채 approval을 받으려 하지 않는다.
- verdict만 기록하고 reviewer input, role별 finding, aggregation 근거를 비워 두지 않는다.
- review가 필요 없는 작업에 형식적으로 reviewer pool을 붙이지 않는다.
