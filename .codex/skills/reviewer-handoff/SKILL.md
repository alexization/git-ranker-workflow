---
name: reviewer-handoff
description: latest verification report가 `passed`일 때 reviewer minimum context를 한 번에 묶어 reviewer pool에 fan-out하고, role별 finding과 aggregated verdict evidence를 남긴다. implementer와 reviewer 세션 분리를 유지한 채 review를 시작해야 할 때 이 skill을 사용한다.
---

# Reviewer Handoff

reviewer가 더 많은 문서를 읽게 만드는 것이 목적이 아니다. review를 시작하기에 충분한 공통 minimum context를 한 번만 만들고, 그 위에 role별 focus만 얹는다.

## 언제 사용하나

- latest verification report의 overall status가 `passed`다.
- independent review를 시작해야 한다.
- review evidence를 exec plan이나 close-out artifact에 남겨야 한다.

## 먼저 확인할 것

- active exec plan
- latest verification report
- touched diff summary와 touched file/doc 목록
- source-of-truth update 목록 또는 업데이트 불필요 사유
- remaining risk, skipped checks, follow-up 필요 사항
- `docs/operations/dual-agent-review-policy.md`

## 작업 방식

1. reviewer minimum context 다섯 가지를 한 번에 묶는다.
2. reviewer role과 role별 focus를 정한다.
3. implementer와 reviewer 세션을 분리한 채 reviewer pool에 fan-out한다.
4. role별 finding을 모은다.
5. final verdict owner가 aggregated verdict를 잠그고 evidence block에 남긴다.

## 결과

산출물은 handoff summary와 `Independent Review` evidence block이다. evidence block에는 아래가 바로 보여야 한다.

- reviewer 역할
- reviewer 이름
- aggregated verdict
- role별 finding 또는 no-blocking note
- final verdict owner

`approved` verdict가 고정되면 그 다음 단계는 PR 생성이 아니라 feedback close-out 정리이며, publish는 `publish-after-review` 단계에서 따로 수행한다.

## 빠른 점검 명령

```bash
sed -n '61,210p' docs/operations/dual-agent-review-policy.md
sed -n '257,280p' docs/operations/verification-contract-registry.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
git diff --stat
git diff --name-only
rg -n "## Verification Report|## Independent Review" docs/exec-plans/active/<plan>.md
```

## 피해야 할 것

- latest verification report가 `passed`가 아니면 reviewer pool로 넘기지 않는다.
- implementer가 reviewer coordinator를 겸하지 않는다.
- reviewer role을 늘리면서 minimum context를 줄이지 않는다.
- skipped checks나 remaining risk를 숨긴 채 approval을 받으려 하지 않는다.
- verdict만 기록하고 reviewer input, role별 finding, aggregation 근거를 비워 두지 않는다.
- draft PR을 먼저 열어 두고 그 URL을 reviewer handoff의 기본 입력처럼 취급하지 않는다.
