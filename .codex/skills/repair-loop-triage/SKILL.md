---
name: repair-loop-triage
description: verification 실패나 review `changes-requested` 이후, 현재 spec 안에서 수리할지 `Blocked`로 전환할지, follow-up으로 쪼갤지를 정한다.
---

# Repair Loop Triage

이 skill은 실패를 오래 끄는 대신, root cause 하나에 맞는 다음 행동만 좁히는 데 초점을 둔다.

## 언제 사용하나

- latest verification report에 `failed` command가 있다.
- required evidence가 빠졌거나 stale report가 지적됐다.
- reviewer가 `changes-requested`와 rerun을 요구했다.

## 먼저 확인할 것

- approved spec
- latest verification report
- `docs/operations/verification-contract-registry.md`
- review finding이 있다면 `docs/operations/dual-agent-review-policy.md`

## 결과

- trigger
- 현재 결정: repair, `Blocked`, follow-up split
- root cause 요약
- rerun 대상 command 또는 stop signal
- next owner
