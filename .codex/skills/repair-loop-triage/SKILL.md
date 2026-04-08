---
name: repair-loop-triage
description: verification 실패나 review `changes-requested` 이후, 현재 issue 안에서 수리할지 `Blocked`로 전환할지, follow-up으로 쪼갤지를 정한다. retry budget을 지키면서 rerun 대상 command를 좁혀야 할 때 이 skill을 사용한다.
---

# Repair Loop Triage

이 skill은 실패를 오래 끄는 대신, root cause 하나에 맞는 다음 행동만 좁히는 데 초점을 둔다.

## 언제 사용하나

- latest verification report에 `failed` command가 있다.
- required evidence가 빠졌거나 stale report가 지적됐다.
- reviewer가 `changes-requested`와 rerun을 요구했다.
- 같은 issue 안에서 repair를 이어갈지, `Blocked`로 멈출지, follow-up으로 쪼갤지 판단해야 한다.

## 먼저 확인할 것

- active exec plan
- latest verification report
- `docs/operations/verification-contract-registry.md`
- review finding이 있다면 `docs/operations/dual-agent-review-policy.md`
- retry budget 사용 이력

## 작업 방식

1. trigger가 된 command나 reviewer finding을 한 줄로 적는다.
2. root cause를 좁힌다.
3. budget 안에서 current issue 안 repair가 가능한지 판단한다.
4. 가능하면 rerun 대상 command를 구체적으로 정한다.
5. 불가능하면 `Blocked` 또는 follow-up split으로 넘긴다.

## 결과

산출물은 repair triage summary다. 아래가 최소로 보여야 한다.

- trigger
- 현재 결정: repair, `Blocked`, follow-up split
- root cause 요약
- budget remaining
- rerun 대상 command 또는 stop signal
- next owner

## 빠른 점검 명령

```bash
sed -n '178,280p' docs/operations/verification-contract-registry.md
sed -n '61,170p' docs/operations/dual-agent-review-policy.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
rg -n "Overall status|Command:|Failure summary|Next action" docs/exec-plans/active/<plan>.md
<rerun-failed-command>
```

## 피해야 할 것

- 같은 root cause를 세 번째 이상 계속 밀어붙이지 않는다.
- baseline command가 실패했는데 conditional command만 다시 실행하고 최신 상태라고 적지 않는다.
- `blocked` 사유를 단순 `failed`로 축소하지 않는다.
- reviewer finding을 해결하지 않은 채 stale verification report를 그대로 handoff하지 않는다.
- budget이 소진됐는데도 “한 번만 더” 식으로 암묵 재시도를 늘리지 않는다.
