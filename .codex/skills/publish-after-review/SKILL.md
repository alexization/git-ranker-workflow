---
name: publish-after-review
description: latest review verdict가 `approved`이거나 blocker-sharing draft exception이 선언된 상태에서, feedback close-out outcome 또는 blocker disclosure가 고정된 뒤 open PR 또는 draft PR을 publish한다. reviewer-handoff 이후 PR 생성 순서를 고정하고 draft-first drift를 막는 publish 단계에 적용한다.
---

# Publish After Review

이 skill의 목적은 PR을 더 빨리 여는 것이 아니라, 이미 검증된 결과를 publish-ready container로 보내는 것이다.

## 언제 사용하나

- latest verification report가 최신이다.
- publish path가 아래 중 하나로 고정됐다.
  - latest review verdict가 `approved`이고 feedback close-out outcome이 고정됐다.
  - blocker-sharing draft exception이 선언됐고, blocker reason과 draft disclosure가 exec plan 또는 PR body에 고정됐다.
- 이제 PR body를 만들고 publish해야 한다.

draft PR이 필요한 경우는 user request 또는 blocker-sharing exception뿐이다.

## 먼저 확인할 것

- active exec plan 또는 completed 직전 exec plan
- latest verification report
- latest `Independent Review` evidence
- feedback close-out block, blocker disclosure note, 또는 follow-up note
- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `.github/PULL_REQUEST_TEMPLATE.md`

## 작업 방식

1. `approved` verdict 또는 declared blocker state가 latest verification report와 현재 diff에 일치하는지 다시 확인한다.
2. open path면 feedback close-out outcome이 고정됐는지 확인하고, draft exception path면 blocker reason과 draft disclosure가 body/exec plan에 고정됐는지 확인한다.
3. PR body file에 reader-first summary만 채우고, detailed evidence는 exec plan이나 linked artifact에 둔다.
4. blocker-sharing exception이 없으면 open PR을 생성한다.
5. blocker-sharing exception이면 `gh pr create --draft --base develop --body-file <body-file>`로 draft PR을 생성하고, 그 이유를 body와 exec plan에 남긴다.
6. 생성 직후 body render를 확인하고 PR link를 close-out artifact에 기록한다.

## 결과

산출물은 publish summary와 PR link다. 최소 아래가 보여야 한다.

- latest verification status
- latest review verdict 또는 declared blocker status
- feedback outcome summary 또는 blocker summary
- open PR 또는 draft PR
- PR link

## 빠른 점검 명령

```bash
sed -n '116,180p' docs/operations/workflow-governance.md
sed -n '1,220p' docs/operations/dual-agent-review-policy.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "## Verification Report|## Independent Review|Feedback|Guardrail" docs/exec-plans/active/<plan>.md
sed -n '1,260p' .github/PULL_REQUEST_TEMPLATE.md
gh pr create --base develop --body-file <body-file>
gh pr create --draft --base develop --body-file <body-file>
gh pr view --json body,title,number
```

## 피해야 할 것

- declared blocker나 explicit draft exception이 없는데 `approved` 전 PR을 review workspace처럼 먼저 만들지 않는다.
- feedback close-out 또는 blocker disclosure가 비었는데 PR publish로 덮지 않는다.
- detailed verification/review/feedback evidence를 PR 본문에 그대로 dump하지 않는다.
- user request나 blocker가 없는데 draft PR을 기본값처럼 쓰지 않는다.
- stale verification report나 stale review verdict, stale blocker note로 publish하지 않는다.
