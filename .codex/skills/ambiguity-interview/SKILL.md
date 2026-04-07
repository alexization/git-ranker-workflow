---
name: ambiguity-interview
description: Use this skill when request intake returns `모호한 요청` and you must reduce the remaining blockers into a single executable issue, `Blocked`, or `Rejected`.
---

# Ambiguity Interview

## Purpose

`모호한 요청`으로 분류된 작업에서 남은 ambiguity signal을 줄여 한 issue로 고정 가능한 입력을 만든다. 목표는 요구사항을 늘리는 것이 아니라 문제 정의, 범위, write scope, 산출물, verification을 잠그는 것이다.

## Trigger

- `request-intake` 결과가 `모호한 요청`이다.
- source of truth만으로는 하나 이상의 ambiguity signal이 남아 있다.
- 어떤 질문을 해야 issue/exec plan 가능한 상태로 수렴하는지 정리해야 한다.

## Inputs and Preconditions

- 최신 사용자 요청 또는 issue draft
- `request-intake` summary
- `docs/operations/request-routing-policy.md`
- 관련 product 문서, 기존 exec plan, 저장소 entry 문서
- 어떤 ambiguity signal이 남았는지 이미 적어 둘 수 있어야 한다.
- interview 전에 source of truth로 줄일 수 있는 사실은 먼저 줄인다.

## Canonical Boundary

- interview objective, question rule, exit condition, canonical close-out reason은 `docs/operations/request-routing-policy.md`가 관리한다.
- 이 skill은 남아 있는 ambiguity를 어떤 순서로 줄이고 어떤 exit summary를 남길지 operationalize한다.
- 새 종료 상태나 새 close-out reason이 필요해 보이면 skill에 추가하지 말고 policy를 먼저 갱신한다.

## Output and Artifact Location

- 산출물은 interview exit summary다. 기본적으로 응답이나 작업 메모에 남기고, 종료 상태에 따라 다음 단계가 갈린다.
- `Planned`
  - issue의 reader-facing summary와 exec plan의 `Problem`, `Why Now`, `Scope`, `Non-scope`, `Write Scope`, `Verification`을 채울 수 있는 요약을 남긴다.
  - 다음 단계는 `issue-to-exec-plan`이다.
- `Blocked`
  - 현재 issue 안에서 더 줄일 수 없는 blocker와 필요한 외부 입력을 남긴다.
- `Rejected`
  - canonical close-out reason을 남기고 실행을 종료한다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
sed -n '1,260p' docs/operations/request-routing-policy.md
rg -n "<repo|surface noun|issue-id>" docs/product docs/exec-plans docs .codex/skills
sed -n '1,220p' <candidate-source-of-truth>
```

핵심은 "질문 전에 source를 더 읽어 ambiguity를 줄일 수 있는가"를 먼저 확인하는 것이다.

## Required Evidence

- 남아 있는 ambiguity signal 목록
- 질문 전에 읽은 source of truth
- 실제로 사용자에게 던진 blocker 질문
- interview exit status: `Planned`, `Blocked`, `Rejected`
- 종료 근거
  - `Planned`: 고정된 문제/범위/write scope/verification
  - `Blocked`: 어떤 canonical source나 응답이 비어 있는지
  - `Rejected`: `docs/operations/request-routing-policy.md`의 canonical close-out reason 중 무엇을 적용했는지

## Forbidden Shortcuts

- 한 번에 긴 설문을 던지지 않는다.
- 요구사항을 더 크게 만들거나 새 기능 아이디어를 제안하지 않는다.
- source of truth에 없는 제품/설계 선호를 대신 결정하지 않는다.
- `Planned`가 되기 전에는 issue 생성, exec plan 작성, 파일 편집을 시작하지 않는다.
- 같은 ambiguity signal이 두 번 남았는데도 더 많은 질문으로 밀어붙이지 않는다.

## Parallel Ownership Rule

- 같은 interview thread는 한 agent만 소유한다.
- 다른 agent가 다른 가정으로 병렬 질문을 던지지 않는다.
- interview owner가 종료 상태를 고정하기 전에는 planning owner나 implementation owner가 범위를 확장하지 않는다.

## Interview Rules

- interview 규칙 자체는 `docs/operations/request-routing-policy.md`를 그대로 따른다.
- operational focus만 정리하면 아래와 같다.
  - 한 라운드에는 blocker 하나를 우선 줄인다.
  - 여러 저장소나 여러 목표가 섞였으면 primary repo나 첫 issue를 먼저 고정한다.
  - 기본 결정이 이미 source of truth에 있으면 그 결정을 재질문하지 않는다.
  - 같은 ambiguity signal이 두 라운드 뒤에도 남으면 더 묻지 말고 `Blocked` 또는 `Rejected`로 정리한다.

## Example Input

- 요청: "backend랑 client 인증 흐름 다 정리하고 필요한 것들 한 번에 고쳐줘"
- `request-intake` 결과:
  - route: `모호한 요청`
  - ambiguity:
    - 여러 저장소가 섞여 있음
    - 여러 목표가 한 issue로 묶여 있음

## Example Output

```md
Interview question
- "이번 턴의 primary repo를 먼저 `git-ranker`와 `git-ranker-client` 중 어디로 고정할까요?"

사용자 응답 이후 exit summary 예시
- Status: `Planned`
- Primary repo: `git-ranker`
- Problem: backend 인증 흐름 정리
- Non-scope: client UI 수정
- Next action: `issue-to-exec-plan`
```

## Handoff

interview 종료 후 아래를 넘긴다.

- `Planned`
  - 문제 정의
  - 왜 지금 필요한지
  - 범위와 비범위
  - 대상 저장소와 write scope
  - 기대 산출물
  - verification 방법
  - 다음 단계: `issue-to-exec-plan`
- `Blocked`
  - 남은 blocker
  - 필요한 외부 입력 또는 canonical source
- `Rejected`
  - canonical close-out reason
  - 실행을 계속하지 않는 이유
