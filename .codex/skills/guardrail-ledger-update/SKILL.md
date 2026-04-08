---
name: guardrail-ledger-update
description: Use this skill when verification and review outcomes are fixed and you need to write a guardrail ledger entry with normalized root cause, evidence, and close-out fields.
---

# Guardrail Ledger Update

## Purpose

feedback close-out에서 latest verification 결과, latest review verdict, 남은 리스크를 guardrail ledger entry 하나로 정리한다. 목표는 feedback section을 길게 쓰는 것이 아니라, root cause 하나당 하나의 canonical entry를 빠짐없이 남기는 것이다.

## Trigger

- latest verification report가 `passed`이거나 `blocked` 이유가 고정됐다.
- latest review verdict가 `approved`, `changes-requested`, `blocked` 중 하나로 고정됐거나 review 불가 사유가 정리됐다.
- exec plan close-out 또는 follow-up artifact에 guardrail ledger entry를 남겨야 한다.
- root cause normalization과 evidence minimum을 같은 형식으로 반복 적용해야 한다.

## Inputs and Preconditions

- active exec plan 또는 close-out artifact 경로가 있어야 한다.
- `docs/operations/failure-to-guardrail-feedback-loop.md`와 `docs/operations/guardrail-ledger-template.md`를 먼저 읽는다.
- latest verification report 또는 `Blocked` 이유가 있어야 한다.
- latest review verdict 또는 review를 시작하지 못한 이유가 있어야 한다.
- repair attempt 요약이 있으면 함께 모은다.
- remaining risk, skipped check, failure note를 한곳에 모아야 한다.

## Canonical Boundary

- feedback entry precondition, root cause normalization, failure class vocabulary, close-out minimum은 `docs/operations/failure-to-guardrail-feedback-loop.md`가 canonical source다.
- ledger field shape와 status vocabulary는 `docs/operations/guardrail-ledger-template.md`가 canonical source다.
- 이 skill은 entry를 작성하는 순서와 누락 방지 절차만 다룬다. 새 field나 새 vocabulary를 만들지 않는다.

## Output and Artifact Location

- 산출물은 exec plan close-out, review note, follow-up artifact 중 한 곳에 남기는 `Guardrail Ledger Entry` block이다.
- entry 하나에는 root cause 하나만 남긴다.
- 최소 아래를 채운다.
  - date
  - task / exec plan
  - stage
  - failure class
  - trigger signal
  - root cause
  - existing guardrail
  - recurrence
  - current issue disposition
  - promotion decision
  - guardrail status
  - decision rationale
  - guardrail change or follow-up asset
  - owner / next action
  - evidence
  - notes
- promotion decision이 아직 미정이면 `failure-to-policy`로 handoff한 뒤 돌아와 entry를 닫는다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,260p' docs/operations/failure-to-guardrail-feedback-loop.md
sed -n '1,220p' docs/operations/guardrail-ledger-template.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "## Verification Report|## Independent Review|Feedback|Guardrail" docs/exec-plans/active/<plan>.md
```

핵심은 verification, review, risk 입력을 먼저 고정한 뒤 entry를 쓰는 것이다. input이 비어 있는데 feedback close-out부터 쓰지 않는다.

## Required Evidence

- latest verification 상태 또는 `Blocked` 이유
- latest review verdict 또는 review 불가 사유
- trigger signal과 root cause의 구분
- `Date`, `Task / Exec Plan`, `Existing guardrail` 또는 `없음`
- root cause 하나당 entry 하나라는 근거
- remaining risk, skipped check, repair note 중 관련 입력
- follow-up asset 또는 없음 사유

## Forbidden Shortcuts

- verification 결과나 review verdict 없이 ledger entry를 먼저 닫지 않는다.
- 서로 다른 root cause를 한 entry에 섞지 않는다.
- symptom을 root cause 자리로 그대로 복사하지 않는다.
- promotion decision, guardrail status, owner / next action을 빈칸으로 두지 않는다.
- success path라는 이유로 `no-new-guardrail` 근거를 생략하지 않는다.

## Parallel Ownership Rule

- ledger entry의 최종 owner는 한 명이어야 한다.
- implementer가 close-out artifact를 기록할 수는 있지만 reviewer verdict를 새로 정하지 않는다.
- reviewer가 feedback note를 제안하더라도 final ledger entry는 current issue owner가 canonical artifact에 통합한다.

## Example Input

- Exec plan: `docs/exec-plans/active/<plan>.md`
- Latest verification report: `passed`
- Latest review verdict: `approved`
- Remaining risk: 없음
- Failure note: review input 누락이 과거 두 번 반복됨

## Example Output

```md
## Guardrail Ledger Entry
- Date: `2026-04-08`
- Task / Exec Plan: `docs/exec-plans/active/<plan>.md`
- Stage:
  - `Feedback Pending`
- Failure class:
  - `review-handoff`
- Trigger signal: reviewer input에 latest verification report 링크가 빠졌다.
- Root cause: review handoff minimum을 close-out 작성 단계에서 재확인하는 절차가 없었다.
- Existing guardrail: `docs/operations/dual-agent-review-policy.md`
- Recurrence:
  - `repeated`
- Current issue disposition:
  - `approved-with-note`
- Promotion decision:
  - `skill`
- Guardrail status:
  - `follow-up-created`
- Decision rationale: rule은 이미 있었고, 같은 입력 누락이 반복되어 thin-layer handoff 절차를 추가해야 한다.
- Guardrail change or follow-up asset: `.codex/skills/reviewer-handoff/SKILL.md`
- Owner / next action: feedback close-out skill pack에서 reviewer input checklist를 추가한다.
- Evidence: latest verification report, review note, prior close-out 사례
- Notes: root cause 하나만 기록했다.
```

## Handoff

promotion decision까지 확정됐다면 아래를 close-out owner에게 넘긴다.

- completed entry block
- entry가 들어갈 artifact 경로
- 남은 follow-up asset 또는 없음 사유

promotion decision이 비어 있으면 아래를 `failure-to-policy`에 넘긴다.

- normalized root cause
- failure class 후보
- recurrence 근거
- existing guardrail
- current issue disposition
