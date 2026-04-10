---
name: publish-after-review
description: legacy 이름이지만 current policy에서는 latest verification 뒤 open PR을 publish하는 단계에 사용한다. review는 open PR 이후 필요할 때 수행한다.
---

# Publish After Review

이 skill의 목적은 latest verification을 끝낸 결과를 open PR로 빠르게 공개하는 것이다. 이름은 남아 있지만 canonical timing은 `verification -> open PR publish -> optional review`다.

## 언제 사용하나

- latest verification report가 최신이다.
- 이제 PR body를 만들고 publish해야 한다.
- draft PR은 사용자가 명시적으로 요청한 경우에만 쓴다.

## 먼저 확인할 것

- task brief 또는 active exec plan
- latest verification report
- review가 이미 있었다면 latest `Independent Review` evidence
- feedback close-out이 이미 있었다면 그 note
- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `.github/PULL_REQUEST_TEMPLATE.md`

## 작업 방식

1. latest verification report가 현재 diff와 일치하는지 다시 확인한다.
2. PR body file에 reader-first summary만 채우고, detailed evidence는 exec plan이나 linked artifact에 둔다.
3. 사용자가 draft를 명시적으로 요청하지 않았다면 open PR을 생성한다.
4. 사용자가 draft를 명시적으로 요청했다면 `gh pr create --draft --base develop --body-file <body-file>`로 draft PR을 생성한다.
5. 생성 직후 body render를 확인하고 PR link를 close-out artifact에 기록한다.

## 결과

산출물은 publish summary와 PR link다. 최소 아래가 보여야 한다.

- latest verification status
- latest review verdict if it already exists
- feedback summary if it already exists
- open PR 또는 draft PR
- PR link

## 빠른 점검 명령

```bash
sed -n '116,190p' docs/operations/workflow-governance.md
sed -n '1,220p' docs/operations/dual-agent-review-policy.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "## Verification Report|## Independent Review|Feedback|Guardrail" docs/exec-plans/active/<plan>.md
sed -n '1,260p' .github/PULL_REQUEST_TEMPLATE.md
gh pr create --base develop --body-file <body-file>
gh pr create --draft --base develop --body-file <body-file>
gh pr view --json body,title,number
```

## 피해야 할 것

- latest verification 없이 PR publish를 시작하지 않는다.
- detailed verification/review/feedback evidence를 PR 본문에 그대로 dump하지 않는다.
- user request가 없는데 draft PR을 기본값처럼 쓰지 않는다.
- stale verification report나 stale review verdict로 publish하지 않는다.
