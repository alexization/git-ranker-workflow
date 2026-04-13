---
name: publish-after-review
description: legacy 이름이지만 current policy에서는 latest verification evidence 뒤 open PR을 publish하는 단계에 사용한다. review는 open PR 이후 필요할 때 수행한다.
---

# Publish After Review

이 skill의 목적은 latest verification evidence를 끝낸 결과를 open PR로 빠르게 공개하는 것이다.

## 언제 사용하나

- latest verification report 또는 summary가 최신이다.
- 이제 PR body를 만들고 publish해야 한다.

## 먼저 확인할 것

- approved spec
- latest verification evidence
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/operations/workflow-governance.md`

## 작업 방식

1. latest verification evidence가 current diff와 일치하는지 다시 확인한다.
2. PR body는 reader-first로 작성하고 detailed evidence는 spec이나 linked artifact에 둔다.
3. 사용자가 draft를 명시적으로 요청하지 않았다면 open PR을 생성한다.
4. 생성 직후 body render를 확인한다.

## 결과

- latest verification status
- open PR 또는 draft PR
- PR link
