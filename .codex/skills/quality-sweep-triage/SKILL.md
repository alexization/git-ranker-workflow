---
name: quality-sweep-triage
description: periodic 또는 targeted quality sweep에서 나온 signal을 `repair-now`, `cleanup-pr-candidate`, `guardrail-follow-up`, `no-action` 중 하나로 분류한다. lint drift, duplication, unused code를 새 work item이나 guardrail follow-up으로 좁혀야 할 때 이 skill을 사용한다.
---

# Quality Sweep Triage

이 skill은 "나중에 정리하면 좋겠다" 수준의 메모를 남기는 대신, bounded quality drift를 evidence와 next action까지 붙은 후보로 바꾼다.

## 언제 사용하나

- completed issue 뒤에 `post-closeout` quality sweep을 해야 한다.
- `scheduled` sweep 결과가 들어왔다.
- reviewer note나 반복 finding 때문에 `targeted` sweep을 해야 한다.

## 먼저 확인할 것

- `docs/operations/continuous-quality-feedback-loop.md`
- `docs/operations/quality-sweep-report-template.md`
- source task, PR, baseline, reviewer note, detector output
- 대상 저장소와 bounded scan scope

blocking regression 가능성이 보이면 repair나 bug follow-up 가능성도 같이 본다.

## 작업 방식

1. signal source와 scan scope를 고정한다.
2. signal class와 severity를 정한다.
3. `repair-now`, `cleanup-pr-candidate`, `guardrail-follow-up`, `no-action` 중 하나를 고른다.
4. follow-up asset과 next owner를 적는다.
5. quality sweep report에 바로 붙일 수 있는 summary로 남긴다.

## 결과

산출물은 quality sweep report용 triage summary다. 최소 아래를 포함한다.

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

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/operations/continuous-quality-feedback-loop.md
sed -n '1,220p' docs/operations/quality-sweep-report-template.md
sed -n '1,260p' docs/exec-plans/completed/<plan>.md
rg -n "lint|duplicate|unused|quality sweep|cleanup" docs/exec-plans docs/operations
```

## 피해야 할 것

- blocking regression을 `cleanup-pr-candidate`로 축소하지 않는다.
- original issue completion verdict를 quality sweep note 하나로 뒤집지 않는다.
- 여러 signal class를 한 report에 섞지 않는다.
- evidence 없이 "중복", "unused" 같은 추정만 남기지 않는다.
- cleanup candidate를 current issue diff에 슬쩍 섞어 넣지 않는다.
- repo-specific detector가 없는데 workflow 문서가 임의의 도구를 canonical로 발명하지 않는다.
