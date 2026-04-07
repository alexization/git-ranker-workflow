---
name: reviewer-handoff
description: Use this skill when the latest verification report passed and you need to package reviewer minimum context once, fan it out to the reviewer pool, and record aggregated review evidence.
---

# Reviewer Handoff

## Purpose

latest verification report가 `passed`인 상태에서 reviewer minimum context를 한 번에 묶어 sub-agent reviewer pool에 fan-out하고, role별 finding과 aggregated verdict evidence를 같은 형식으로 남긴다. 목표는 reviewer가 더 많은 문서를 읽게 하는 것이 아니라, canonical handoff surface를 반복 가능한 입력으로 고정하는 것이다.

## Trigger

- latest verification report의 overall status가 `passed`다.
- independent review를 시작해야 한다.
- review evidence를 exec plan이나 close-out artifact에 정리해야 한다.
- implementer와 reviewer 세션 분리를 유지한 채 role-prompted reviewer pool을 운영해야 한다.

## Inputs and Preconditions

- active exec plan이 있어야 한다.
- latest verification report가 있어야 하고 latest revision 기준이어야 한다.
- touched diff summary와 touched file/doc 목록이 준비돼 있어야 한다.
- source-of-truth update 목록 또는 업데이트 불필요 사유가 있어야 한다.
- remaining risk, skipped conditional command, follow-up 필요 사항이 있어야 한다.
- `docs/operations/dual-agent-review-policy.md`와 `docs/operations/verification-contract-registry.md`의 handoff minimum을 먼저 읽는다.

## Canonical Boundary

- reviewer minimum context, read order, verdict vocabulary, aggregation 규칙, review evidence rule은 `docs/operations/dual-agent-review-policy.md`가 canonical source다.
- reviewer handoff minimum과 latest verification report requirement는 `docs/operations/verification-contract-registry.md`가 canonical source다.
- 이 skill은 두 문서가 요구하는 입력을 한 번에 fan-out하고, role prompt와 aggregation evidence를 얇게 추가하는 절차만 다룬다.

## Output and Artifact Location

- 산출물은 reviewer pool에 전달하는 handoff summary와 exec plan 또는 review artifact에 남기는 `Independent Review` evidence block이다.
- handoff summary에는 최소 다섯 가지 공통 입력을 모두 포함한다.
  - exec plan 경로
  - latest verification report
  - touched diff summary와 touched file/doc 목록
  - source-of-truth update 목록 또는 불필요 사유
  - remaining risk, skipped checks, follow-up 필요 사항
- evidence block에는 reviewer 역할, reviewer 이름, aggregated verdict, role별 finding 요약, final verdict owner를 남긴다.
- representative timing breakdown이 있으면 handoff 준비 시간, reviewer 대기 시간, aggregation 시간을 분리해 메모한다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '61,210p' docs/operations/dual-agent-review-policy.md
sed -n '257,280p' docs/operations/verification-contract-registry.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
git diff --stat
git diff --name-only
rg -n "## Verification Report|## Independent Review" docs/exec-plans/active/<plan>.md
```

핵심은 reviewer마다 다른 요약을 새로 만드는 것이 아니라, 공통 minimum context를 먼저 잠그고 role prompt는 그 위에 얹는 것이다.

## Required Evidence

- reviewer minimum context 다섯 가지 모두
- reviewer 역할과 역할별 focus
- final verdict owner
- role별 finding 또는 no-blocking note
- aggregated verdict 근거
- stale report가 아니라 latest revision 기준이라는 근거
- implementer/reviewer 세션 분리가 유지됐다는 기록

## Forbidden Shortcuts

- latest verification report가 `passed`가 아니면 reviewer pool로 넘기지 않는다.
- implementer가 reviewer coordinator를 겸하지 않는다.
- reviewer role을 늘리면서 minimum context를 줄이지 않는다.
- skipped checks나 remaining risk를 숨긴 채 approval을 받으려 하지 않는다.
- verdict만 기록하고 reviewer input, role별 finding, aggregation 근거를 비워 두지 않는다.

## Parallel Ownership Rule

- implementer는 handoff summary를 준비하지만 reviewer verdict를 소유하지 않는다.
- 각 reviewer는 read-only 분석과 finding만 남긴다.
- final verdict owner는 reviewer 역할 중 한 명이어야 하며 aggregated verdict를 잠근다.
- implementer는 결과를 close-out artifact에 반영할 수는 있어도 verdict를 완화하지 않는다.

## Example Input

- Exec plan: `docs/exec-plans/active/<plan>.md`
- Latest verification report: `passed`
- Diff summary: skill 3종 추가, registry 업데이트
- Source-of-truth update: `.codex/skills/README.md`
- Remaining risk: pilot 전 timing evidence는 first-pass 메모 수준

## Example Output

```md
## Independent Review
- Implementer: `Codex`
- Reviewer: `reviewer-coordinator`
- Additional Reviewers:
  - `scope-and-governance`: `agent-a`
  - `verification-and-regression`: `agent-b`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/active/<plan>.md`
  - Latest verification report: `passed`
  - Diff summary: verification skill 3종 추가
  - Source-of-truth update: `.codex/skills/README.md`
  - Remaining risks / skipped checks: pilot 전 timing baseline만 메모
- Review Verdict: `approved`
- Findings / Change Requests:
  - `scope-and-governance`: blocking finding 없음
  - `verification-and-regression`: blocking finding 없음
- Evidence:
  - reviewer minimum context와 current diff가 같은 revision으로 정렬됐고, 필수 reviewer 역할이 모두 verdict를 반환했다.
```

## Handoff

reviewer pool에 넘길 때는 아래를 같이 전달한다.

- 공통 minimum context 다섯 가지
- reviewer role별 focus
- role별 read subset이 있으면 그 범위
- aggregated verdict owner
- timing note와 follow-up 필요 사항
