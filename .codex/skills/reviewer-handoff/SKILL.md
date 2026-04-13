---
name: reviewer-handoff
description: review가 실제로 필요할 때 latest verification evidence를 바탕으로 reviewer minimum context를 묶고, open PR 기준 review evidence를 남긴다.
---

# Reviewer Handoff

reviewer가 더 많은 문서를 읽게 만드는 것이 목적이 아니다.

## 언제 사용하나

- latest verification report 또는 summary의 overall status가 `passed`다.
- independent review를 시작해야 한다.
- open PR이 이미 생성됐다.

## 먼저 확인할 것

- approved spec
- latest verification evidence
- touched diff summary
- source-of-truth update 목록 또는 업데이트 불필요 사유
- remaining risk, skipped checks, follow-up 필요 사항
- `docs/operations/dual-agent-review-policy.md`

## 작업 방식

1. reviewer minimum context를 한 번에 묶는다.
2. reviewer가 한 명이면 그대로 넘기고, high-risk surface일 때만 role별 focus를 추가한다.
3. implementer와 reviewer 세션을 분리한 채 review를 시작한다.
4. finding과 verdict를 모은다.

## 결과

- reviewer 이름
- reviewer input
- review verdict
- finding 또는 no-blocking note
