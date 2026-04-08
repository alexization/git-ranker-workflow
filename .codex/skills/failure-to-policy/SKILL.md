---
name: failure-to-policy
description: Use this skill when a normalized failure must be mapped to the smallest guardrail asset that should be promoted next.
---

# Failure To Policy

## Purpose

normalized root cause를 `docs-rule`, `skill`, `test`, `ci`, `template`, `no-new-guardrail` 중 하나로 좁히고, 왜 그 자산이 가장 이른 차단 지점인지 결정한다. 목표는 follow-up을 많이 만드는 것이 아니라, 반복될 실패를 가장 작은 guardrail로 끊는 것이다.

## Trigger

- guardrail ledger entry 초안은 있는데 `Promotion decision`과 `Guardrail status`를 아직 고정하지 못했다.
- 같은 root cause가 반복돼 어떤 자산으로 승격할지 판단해야 한다.
- success path, repair path, blocked path 중 무엇이든 feedback close-out에서 `no-new-guardrail` 예외를 검토해야 한다.
- follow-up asset이나 현재 issue 내 적용 대상을 정해야 한다.

## Inputs and Preconditions

- normalized root cause와 trigger signal이 있어야 한다.
- `docs/operations/failure-to-guardrail-feedback-loop.md`를 먼저 읽는다.
- current issue disposition과 recurrence 근거가 있어야 한다.
- existing guardrail이 있으면 적고, 없으면 `없음`이라고 적는다.
- 관련 과거 사례가 있으면 completed exec plan이나 review artifact에서 recurrence 증거를 찾는다.

## Canonical Boundary

- failure taxonomy, promotion target vocabulary, selection rule, recurrence rule, `no-new-guardrail` 기준은 `docs/operations/failure-to-guardrail-feedback-loop.md`가 canonical source다.
- 이 skill은 현재 failure를 그 policy에 대입해 next asset만 좁힌다. 새 decision target이나 예외 규칙을 만들지 않는다.

## Output and Artifact Location

- 산출물은 ledger entry에 복사 가능한 policy decision summary다.
- 최소 아래를 남긴다.
  - failure class
  - existing guardrail
  - recurrence
  - selected promotion decision
  - selected guardrail status
  - decision rationale
  - guardrail change or follow-up asset
  - owner / next action
- selected guardrail status는 canonical ledger template의 vocabulary를 그대로 따른다.
  - current issue 안에서 바로 적용되면 `applied-now`
  - 후속 이슈나 자산이 필요하면 `follow-up-created` 또는 `deferred`
  - 새 guardrail이 필요 없다는 결론이면 `no-new-guardrail`

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,260p' docs/operations/failure-to-guardrail-feedback-loop.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "Guardrail Ledger Entry|Failure class|Promotion decision|Root cause" docs/exec-plans docs/operations
```

핵심은 recurrence와 existing guardrail을 근거로 가장 이른 차단 지점을 고르는 것이다. 근거 없이 `skill`이나 `no-new-guardrail`로 기울지 않는다.

## Required Evidence

- selected failure class와 그 이유
- existing guardrail 유무
- recurrence가 `first-seen`, `repeated`, `systemic` 중 무엇인지와 근거
- selected promotion decision과 selection rule 근거
- `no-new-guardrail`이면 예외 사유
- selected guardrail status와 canonical template vocabulary의 일치 여부
- follow-up asset 또는 현재 issue 내 적용 자산

## Forbidden Shortcuts

- 같은 root cause가 반복됐는데 예외 근거 없이 `no-new-guardrail`로 닫지 않는다.
- canonical rule이 비어 있는데 `skill`이나 `template`만으로 덮지 않는다.
- behavior regression을 문서 메모만으로 닫지 않는다.
- structured input 누락이 아닌 문제를 `template`으로 오분류하지 않는다.
- 새 decision vocabulary나 새 recurrence level을 만들지 않는다.

## Parallel Ownership Rule

- promotion decision summary의 final owner는 한 명이어야 한다.
- 여러 reviewer가 의견을 줄 수는 있지만 decision vocabulary와 rationale 통합은 current issue owner가 맡는다.
- follow-up asset이 필요한 경우 asset 이름과 next owner를 하나로 잠근다.

## Example Input

- Root cause: feedback close-out에서 repeated failure를 어떤 자산으로 승격할지 매번 수동으로 판단한다.
- Existing guardrail: `docs/operations/failure-to-guardrail-feedback-loop.md`
- Recurrence: `repeated`
- Current issue disposition: `approved-with-note`

## Example Output

```md
Policy Decision
- Failure class: `evidence-closeout`
- Existing guardrail: `docs/operations/failure-to-guardrail-feedback-loop.md`
- Recurrence: `repeated`
- Promotion decision: `skill`
- Guardrail status: `applied-now`
- Decision rationale: canonical rule은 이미 있지만, 같은 feedback close-out 누락이 반복돼 thin-layer execution recipe가 필요하다.
- Guardrail change or follow-up asset: `.codex/skills/guardrail-ledger-update/SKILL.md`
- Owner / next action: current issue에서 skill 추가 후 ledger entry에 반영
```

## Handoff

결정이 끝나면 아래를 `guardrail-ledger-update` 또는 close-out owner에게 넘긴다.

- selected failure class
- selected promotion decision
- selected guardrail status
- decision rationale
- guardrail change or follow-up asset
- owner / next action
