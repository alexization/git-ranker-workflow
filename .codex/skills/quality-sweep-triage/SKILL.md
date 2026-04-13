---
name: quality-sweep-triage
description: periodic 또는 targeted quality sweep에서 나온 signal을 `repair-now`, `cleanup-pr-candidate`, `guardrail-follow-up`, `no-action` 중 하나로 분류한다.
---

# Quality Sweep Triage

이 skill은 bounded quality drift를 evidence와 next action까지 붙은 후보로 바꾼다.

## 언제 사용하나

- `post-closeout` quality sweep을 해야 한다.
- `scheduled` sweep 결과가 들어왔다.
- reviewer note나 반복 finding 때문에 `targeted` sweep을 해야 한다.

## 먼저 확인할 것

- `docs/operations/continuous-quality-feedback-loop.md`
- `docs/operations/quality-sweep-report-template.md`
- source task, PR, baseline, reviewer note, detector output
- 대상 저장소와 bounded scan scope

## 결과

- trigger mode
- source repo와 source task/PR/baseline
- scan scope
- detection surface
- signal class
- selected disposition
- follow-up asset / issue / PR
- owner / next action
- 핵심 evidence
