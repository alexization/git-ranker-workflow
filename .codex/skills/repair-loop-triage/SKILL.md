---
name: repair-loop-triage
description: Use this skill when verification fails or review requests changes and you need to classify the failure, preserve retry budget, and decide rerun versus blocked or follow-up split.
---

# Repair Loop Triage

## Purpose

verification failure나 review change request가 발생했을 때, 현재 이슈 안에서 수리할 수 있는지, 즉시 `Blocked`로 전환해야 하는지, 어떤 command를 다시 실행해야 하는지를 좁힌다. 목표는 오래 끄는 것이 아니라 retry budget 안에서 root cause를 하나씩 줄이는 것이다.

## Trigger

- latest verification report에 `failed` command가 있다.
- latest verification report에 required evidence 누락이 있다.
- reviewer가 diff와 verification report 불일치, required rerun, stale report를 지적했다.
- 같은 issue 안에서 repair attempt를 이어갈지 follow-up으로 넘길지 판단해야 한다.

## Inputs and Preconditions

- active exec plan과 latest verification report가 있어야 한다.
- `docs/operations/verification-contract-registry.md`의 repair loop policy를 먼저 확인한다.
- review finding으로 들어온 경우 `docs/operations/dual-agent-review-policy.md`의 repair loop와 verdict vocabulary를 함께 읽는다.
- 실패한 command 또는 blocking finding이 무엇인지 한 문장으로 적을 수 있어야 한다.
- retry budget 소모 이력을 확인해야 한다. 새 failure class가 드러나도 budget은 리셋되지 않는다.

## Canonical Boundary

- `failed`, `blocked`, `skipped`, retry budget, rerun rule, stop condition은 `docs/operations/verification-contract-registry.md`가 canonical source다.
- review 단계에서 들어온 `changes-requested`와 re-run expectation은 `docs/operations/dual-agent-review-policy.md`가 canonical source다.
- 이 skill은 두 문서의 규칙을 현재 failure에 적용해 next action만 좁힌다. 새 status vocabulary를 만들지 않는다.

## Output and Artifact Location

- 산출물은 exec plan, 작업 메모, 또는 verification artifact에 남기는 repair triage summary다.
- 최소 아래를 남긴다.
  - trigger가 된 command 또는 reviewer finding
  - 현재 결정: current issue 안에서 repair, `Blocked`, follow-up issue split 중 하나
  - root cause 요약
  - budget remaining
  - rerun 대상 command 또는 막힌 이유
  - next owner
- repair 후에는 updated verification report 경로를 다시 연결한다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '178,280p' docs/operations/verification-contract-registry.md
sed -n '61,170p' docs/operations/dual-agent-review-policy.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "Overall status|Command:|Failure summary|Next action" docs/exec-plans/active/<plan>.md
<rerun-failed-command>
```

핵심은 실패한 required command와 review finding을 latest revision 기준으로 다시 맞추는 것이다. repair할 command가 무엇인지 모른 채 넓게 재실행하지 않는다.

## Required Evidence

- trigger가 된 command 또는 review finding
- issue write scope 안에서 수리 가능한지 여부
- retry budget 사용 현황
- rerun 대상 command와 이유
- `blocked`면 missing canonical source, env, boundary conflict 같은 stop signal
- follow-up split이면 현재 issue에서 닫지 않는 이유와 다음 handoff

## Forbidden Shortcuts

- 같은 root cause를 세 번째 이상 계속 밀어붙이지 않는다.
- baseline command가 실패했는데 conditional command만 다시 실행하고 최신 상태라고 적지 않는다.
- `blocked` 사유를 단순 `failed`로 축소하지 않는다.
- reviewer finding을 해결하지 않은 채 stale verification report를 그대로 handoff하지 않는다.
- budget이 소진됐는데도 “한 번만 더” 식으로 암묵 재시도를 늘리지 않는다.

## Parallel Ownership Rule

- triage summary의 최종 owner는 한 명이어야 한다.
- implementer가 repair를 수행하고, reviewer는 updated report를 기준으로 다시 판단한다.
- 여러 agent가 실패 원인을 탐색하더라도 rerun 대상 command와 budget 집계는 triage owner가 잠근다.

## Example Input

- Trigger: `./gradlew build` failed
- Latest verification report: `failed`
- Repair attempts used: `1`
- Review finding: 없음

## Example Output

```md
Repair Triage
- Trigger: `./gradlew build`
- Decision: current issue 안에서 repair
- Root cause: generated spec path mismatch within current write scope
- Budget remaining: `1`
- Re-run target:
  - `./gradlew build`
  - `./gradlew generateOpenApiSpec`
- Next owner: implementer
```

## Handoff

repair가 가능하면 아래를 구현 owner에게 넘긴다.

- root cause 한 줄 요약
- 수정할 범위
- rerun 대상 command
- budget remaining

`blocked` 또는 split이면 아래를 남긴다.

- stop signal
- 현재 issue에서 더 진행하지 않는 이유
- follow-up issue 또는 planning 필요성
