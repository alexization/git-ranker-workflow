---
name: quality-sweep-triage
description: Use this skill when a periodic or targeted quality sweep must classify coding-rule drift, duplication, or unused code into cleanup candidates, guardrail follow-up, or repair-now.
---

# Quality Sweep Triage

## Purpose

quality sweep signal을 `repair-now`, `cleanup-pr-candidate`, `guardrail-follow-up`, `no-action` 중 하나로 좁히고, 다음 work item이 바로 시작될 수 있게 report와 handoff를 고정한다. 목표는 "정리할 것 같음" 수준의 메모를 남기는 것이 아니라, bounded quality drift를 evidence와 next action까지 포함한 candidate로 바꾸는 것이다.

## Trigger

- completed issue/PR 뒤에 `post-closeout` quality sweep을 해야 한다.
- repo maintainer나 runtime이 `scheduled` sweep 결과를 넘겼다.
- reviewer note나 반복 finding 때문에 `targeted` sweep을 해야 한다.
- lint drift, duplication, unused code signal을 cleanup candidate로 분리할지 판단해야 한다.

## Inputs and Preconditions

- `docs/operations/continuous-quality-feedback-loop.md`를 먼저 읽는다.
- `docs/operations/quality-sweep-report-template.md`를 먼저 읽는다.
- signal이 나온 source task, PR, baseline, reviewer note, 또는 repo-specific detector output이 있어야 한다.
- 대상 저장소와 scan scope를 한 문장으로 적을 수 있어야 한다.
- blocking regression 가능성이 보이면 `docs/operations/failure-to-guardrail-feedback-loop.md`와 repair/bug follow-up 가능성을 함께 본다.

## Canonical Boundary

- trigger mode, signal class, disposition vocabulary, cleanup handoff minimum은 `docs/operations/continuous-quality-feedback-loop.md`가 canonical source다.
- report field shape는 `docs/operations/quality-sweep-report-template.md`가 canonical source다.
- repeated detector gap을 guardrail 자산으로 승격하는 규칙은 `docs/operations/failure-to-guardrail-feedback-loop.md`를 따른다.
- 이 skill은 현재 signal을 policy에 대입해 next action만 좁힌다. 새 signal class나 disposition을 만들지 않는다.

## Output and Artifact Location

- 산출물은 quality sweep report에 복사 가능한 triage summary다.
- 최소 아래를 남긴다.
  - trigger mode
  - source repo와 source task/PR/baseline
  - scan scope
  - detection surface
  - signal class
  - trigger signal
  - severity
  - selected disposition
  - follow-up asset / issue / PR
  - owner / next action
  - 핵심 evidence

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,260p' docs/operations/continuous-quality-feedback-loop.md
sed -n '1,220p' docs/operations/quality-sweep-report-template.md
sed -n '1,260p' docs/exec-plans/completed/<plan>.md
rg -n "lint|duplicate|unused|quality sweep|cleanup" docs/exec-plans docs/operations
```

핵심은 detector output이나 review note를 "새 cleanup work item으로 바로 넘길 수 있는가" 기준으로 좁히는 것이다. evidence 없이 후보를 늘리지 않는다.

## Required Evidence

- trigger mode와 source artifact
- bounded scan scope
- signal class와 그 이유
- trigger signal
- detection surface
- severity 판단 근거
- selected disposition과 selection rule 근거
- cleanup candidate 또는 guardrail follow-up의 next owner
- `no-action`이면 explicit rationale

## Forbidden Shortcuts

- blocking regression을 `cleanup-pr-candidate`로 축소하지 않는다.
- original issue completion verdict를 quality sweep note 하나로 뒤집지 않는다.
- 여러 signal class를 한 report에 섞지 않는다.
- evidence 없이 "중복", "unused" 같은 추정만 남기지 않는다.
- cleanup candidate를 current issue diff에 슬쩍 섞어 넣지 않는다.
- repo-specific detector가 없는데 workflow 문서가 임의의 도구를 canonical로 발명하지 않는다.

## Parallel Ownership Rule

- quality sweep report의 final owner는 한 명이어야 한다.
- 여러 reviewer나 maintainer가 signal을 제보할 수는 있지만, disposition과 next action 통합은 current sweep owner가 맡는다.
- cleanup candidate가 여러 개면 report와 follow-up owner를 candidate별로 분리한다.

## Example Input

- Trigger mode: `post-closeout`
- Source repo: `git-ranker-client`
- Scan scope: `src/features/ranking`
- Signal: ranking helper 2개가 route refactor 이후 호출되지 않는다.
- Evidence: lint warning과 reviewer note

## Example Output

```md
Sweep Decision
- Trigger mode: `post-closeout`
- Source repo: `git-ranker-client`
- Scan scope: `src/features/ranking`
- Detection surface: lint warning summary, reviewer note
- Signal class: `unused-code-drift`
- Trigger signal: ranking helper 2개가 route refactor 이후 호출되지 않는다.
- Severity: `non-blocking`
- Disposition: `cleanup-pr-candidate`
- Follow-up asset / issue / PR: cleanup issue 초안
- Owner / next action: `request-intake`로 새 cleanup issue를 시작한다.
- Evidence: unused helper 이름, grep path inventory, reviewer note
```

## Handoff

결정이 끝나면 아래처럼 넘긴다.

- `cleanup-pr-candidate`
  - 대상 저장소
  - bounded scan scope
  - 핵심 evidence
  - non-scope
  - next step: `request-intake` -> `issue-to-exec-plan`
- `guardrail-follow-up`
  - repeated detector gap 또는 missing gate 근거
  - next step: `failure-to-policy`
- `repair-now`
  - blocking signal
  - next step: 새 bug/repair issue 또는 repair owner handoff
- `no-action`
  - explicit rationale
  - duplicate or false-positive note
