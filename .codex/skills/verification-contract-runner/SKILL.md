---
name: verification-contract-runner
description: Use this skill when implementation is ready for verification and you need to run the selected contract profile, write the latest verification report, and prepare reviewer handoff input.
---

# Verification Contract Runner

## Purpose

선택된 verification contract profile을 현재 issue에 적용해 required/conditional command를 실행하고, reviewer가 바로 읽을 수 있는 latest verification report를 남긴다. 목표는 검증 명령을 새로 발명하는 것이 아니라, source of truth에 이미 정의된 명령과 evidence shape를 같은 형식으로 재사용하는 것이다.

## Trigger

- 구현이나 문서 변경이 끝나서 review 전 검증이 필요하다.
- active exec plan에 verification contract profile이 이미 적혀 있다.
- repair 후 failed command를 다시 실행해 latest report를 갱신해야 한다.
- reviewer handoff 전에 command status와 evidence를 한 곳에 정리해야 한다.

## Inputs and Preconditions

- active exec plan이 있어야 한다.
- exec plan에 primary verification contract profile이 하나만 고정돼 있어야 한다.
- `docs/operations/verification-contract-registry.md`를 먼저 읽어 selected profile의 required command, conditional command, evidence minimum을 확인한다.
- backend/frontend 작업이면 해당 저장소의 entry doc과 manifest 또는 build entrypoint를 함께 확인한다.
- command 실행에 필요한 env, Docker, credential, worktree가 잠겨 있지 않으면 구현보다 먼저 blocker로 분류한다.
- review를 시작하기 전 단계여야 한다. reviewer handoff는 이 skill의 다음 단계다.

## Canonical Boundary

- contract selection, status vocabulary, report shape, retry budget, blocked semantics는 `docs/operations/verification-contract-registry.md`가 canonical source다.
- 이 skill은 해당 문서의 required/conditional command를 issue별로 실행하고 latest report를 정리하는 절차만 다룬다.
- profile을 합치거나 새 command를 정답처럼 추가하지 않는다. 필요한 override는 exec plan에 먼저 남긴다.

## Output and Artifact Location

- 산출물은 exec plan 또는 별도 verification artifact에 남기는 latest verification report다.
- report에는 최소한 아래를 남긴다.
  - `Contract profile`
  - `Overall status`
  - `Preconditions`
  - command별 `Status`
  - command별 `Evidence`
  - `Failure summary`
  - `Next action`
- reviewer handoff까지 이어질 예정이면 touched diff summary, source-of-truth update, remaining risk 초안도 함께 메모한다.
- representative timing breakdown이 있으면 command 실행 시간과 report 정리 시간을 구분해 간단히 남긴다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,320p' docs/operations/verification-contract-registry.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
git diff --check
./gradlew test
./gradlew build
npm run lint
npx tsc --noEmit
NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build
```

핵심은 profile 이름에 맞는 exact command set을 exec plan과 registry에서 꺼내 실행하는 것이다. command를 "문서 확인", "테스트 실행"처럼 추상화하지 않는다.

## Required Evidence

- 읽은 contract profile과 관련 entry doc
- required command 실행 결과
- conditional command 실행 여부와 trigger 또는 skip reason
- `Preconditions`에 필요한 env/runtime 전제
- latest verification report의 `Overall status`
- failure가 있으면 root cause 요약과 다음 action
- reviewer handoff로 이어질 경우 report가 latest revision 기준임을 보여주는 근거

## Forbidden Shortcuts

- selected profile의 required command를 일부만 실행하고 `passed`로 적지 않는다.
- conditional command를 생략하면서 이유를 비워 두지 않는다.
- baseline command가 실패했는데 아래 conditional command 성공을 최신 상태처럼 남기지 않는다.
- review 전에 verification report 없이 완료를 주장하지 않는다.
- 여러 profile이 필요하다는 이유로 issue 분해 대신 report를 임의로 합치지 않는다.

## Parallel Ownership Rule

- latest verification report의 최종 owner는 한 명이어야 한다.
- 다른 agent가 개별 command 결과를 수집할 수는 있지만, command status와 overall status 집계는 report owner가 잠근다.
- reviewer는 이 단계에서 command를 재분류하지 않고 latest report를 읽는 쪽에 머문다.

## Example Input

- Exec plan: `docs/exec-plans/active/<plan>.md`
- Contract profile: `workflow-docs`
- Changed files:
  - `.codex/skills/verification-contract-runner/SKILL.md`
  - `.codex/skills/reviewer-handoff/SKILL.md`
  - `.codex/skills/README.md`

## Example Output

```md
## Verification Report
- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - docs-only skill update
- Command: `find .codex/skills -maxdepth 2 -type f | sort`
  - Status: `passed`
  - Evidence: 새 skill 경로가 registry와 함께 확인됨
- Command: `sed -n '1,260p' .codex/skills/reviewer-handoff/SKILL.md`
  - Status: `passed`
  - Evidence: reviewer minimum context와 aggregation 규칙이 포함됨
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: whitespace 오류 없음
- Failure summary: 없음
- Next action: reviewer handoff
```

## Handoff

review로 넘길 때는 아래를 함께 전달한다.

- active exec plan 경로
- latest verification report
- touched diff summary
- source-of-truth update 목록 또는 불필요 사유
- remaining risk, skipped conditional command, timing note
