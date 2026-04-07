---
name: request-intake
description: Use this skill when a new request arrives and you must classify it as `대화`, `모호한 요청`, or `즉시 실행 가능한 작업` before creating an issue, exec plan, or file edits.
---

# Request Intake

## Purpose

새 요청을 intake 단계에서 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 중 하나로 고정하고, route에 맞는 다음 행동만 남긴다. 실행을 계속하지 않는 경우에는 terminal close-out인 `Rejected` reason도 함께 남긴다. 목표는 구현 아이디어를 늘리는 것이 아니라 "지금 실행을 시작해도 되는가"를 같은 기준으로 판정하는 것이다.

## Trigger

- 새 사용자 요청이 들어왔다.
- 아직 GitHub issue, active exec plan, 파일 편집을 시작하지 않았다.
- 요청이 응답형 대화인지, interview가 필요한지, 바로 실행 가능한 작업인지 먼저 판정해야 한다.

## Inputs and Preconditions

- 최소한 아래 입력을 먼저 확인한다.
  - 최신 사용자 요청 또는 issue body
  - `docs/operations/request-routing-policy.md`
  - `docs/operations/workflow-governance.md`
  - 관련 `docs/product/*.md` 또는 기존 exec plan이 있으면 해당 문서
- source of truth로 줄일 수 있는 ambiguity는 먼저 직접 줄인다.
- 대상 저장소, 산출물, write scope, verification을 source of truth만으로 잠글 수 있는지 본다.
- intake 단계에서는 아직 issue를 만들거나 exec plan을 쓰지 않는다.

## Canonical Boundary

- route taxonomy, ambiguity signal, immediate execution criteria, `Rejected` semantics는 `docs/operations/request-routing-policy.md`가 canonical source다.
- 이 skill은 canonical route를 새로 정의하지 않고, 현재 요청이 어느 route에 해당하는지와 다음 handoff만 남긴다.
- policy와 skill 문구가 어긋나면 skill보다 policy를 먼저 수정하고 다시 맞춘다.

## Output and Artifact Location

- 산출물은 route decision summary다. 기본적으로 응답이나 작업 메모에 남긴다.
- route별 다음 행동은 canonical policy를 그대로 따르되, skill output에는 아래 handoff만 남긴다.
  - `대화`: 답변만 제공하고 terminal close-out reason `conversation-only`를 남긴다.
  - `모호한 요청`: 남아 있는 ambiguity signal과 첫 interview blocker를 정리해 `ambiguity-interview`로 넘김
  - `즉시 실행 가능한 작업`: 문제, 범위, write scope, verification 요약을 정리해 `issue-to-exec-plan`으로 넘김
- intake 단계에서 사용자가 취소했거나, 범위 밖 요청이거나, canonical source가 없어 실행을 계속하지 않기로 결정했다면 `Rejected` close-out reason을 함께 남긴다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,260p' docs/operations/request-routing-policy.md
sed -n '1,220p' docs/operations/workflow-governance.md
rg -n "<issue-id|task-name|surface noun>" docs/product docs/exec-plans .codex/skills
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
```

중요한 점은 명령을 많이 돌리는 것이 아니라, route 판정에 필요한 canonical source를 먼저 읽고 판단 근거를 남기는 것이다.

## Required Evidence

- 어떤 source of truth 문서를 읽었는지
- 최종 route: `대화`, `모호한 요청`, `즉시 실행 가능한 작업`
- intake 단계에서 실행을 종료했다면 terminal close-out reason: `conversation-only`, `cancelled`, `out-of-scope`, `missing-canonical-source`
- 남아 있는 ambiguity signal 또는 제거된 ambiguity 근거
- 다음 행동
  - `대화`: 답변만 제공하고 `conversation-only`로 종료
  - `모호한 요청`: `ambiguity-interview`
  - `즉시 실행 가능한 작업`: `issue-to-exec-plan`
  - intake에서 종료: `Rejected` close-out reason과 종료 근거
- `즉시 실행 가능한 작업`이 아니면 왜 issue/exec plan을 만들지 않았는지

## Forbidden Shortcuts

- source of truth를 읽기 전에 사용자에게 바로 여러 질문을 던지지 않는다.
- `즉시 실행 가능한 작업`으로 판정되기 전에는 issue, exec plan, 파일 편집을 시작하지 않는다.
- 여러 목표가 섞인 요청을 임의로 한 issue로 묶지 않는다.
- verification이나 write scope를 문서 근거 없이 상상해서 채우지 않는다.
- `대화` 요청을 구현 요청처럼 취급하지 않는다.

## Parallel Ownership Rule

- 최종 route decision summary는 한 agent만 소유한다.
- route가 잠기기 전에는 다른 agent가 issue 생성, exec plan 작성, 구현 착수를 병렬로 시작하지 않는다.
- `모호한 요청`으로 판정된 뒤에는 interview owner가 ambiguity를 줄이고, `즉시 실행 가능한 작업`으로 수렴한 뒤에만 planning owner에게 넘긴다.

## Example Input

- 요청: "랭킹 화면 좀 개선해줘"
- source 확인 결과:
  - 대상 저장소 불명확
  - 완료 조건 부재
  - write scope 부재

## Example Output

```md
Route: `모호한 요청`

남아 있는 ambiguity signal
- 대상 저장소가 고정되지 않음
- 완료 조건이 없음
- write scope를 잠글 수 없음

다음 행동
- `ambiguity-interview`로 전환
- 첫 질문은 "이번 턴의 primary repo와 첫 issue를 무엇으로 고정할지"만 묻는다.
```

## Handoff

route에 따라 아래처럼 넘긴다.

- `대화`
  - 답변만 제공
  - terminal close-out: `conversation-only`
- `모호한 요청`
  - 남아 있는 ambiguity signal 목록
  - source of truth로 이미 해소한 내용
  - 첫 interview blocker 한 개
- `즉시 실행 가능한 작업`
  - 대상 저장소
  - 고정된 문제/범위/비범위
  - write scope
  - verification 초안
  - 다음 단계: `issue-to-exec-plan`
- `Rejected` close-out
  - canonical close-out reason
  - intake 단계에서 실행을 종료하는 근거
  - issue, exec plan, 파일 편집을 시작하지 않았다는 점
