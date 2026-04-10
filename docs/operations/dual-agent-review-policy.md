# Dual-Agent Review Policy

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Reviewing`과 review-driven `Repairing` semantics를 실제 운영 규칙으로 고정한다. [verification-contract-registry.md](verification-contract-registry.md)가 publish 전 검증 완료 조건을 잠근다면, 이 문서는 open PR 이후 independent review를 언제 수행하고, 어떤 입력으로 verdict를 남기며, 어떤 경우에 repair 또는 `Blocked`로 되돌리는지를 잠근다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md), verification handoff minimum은 [verification-contract-registry.md](verification-contract-registry.md)를 따른다.

## Policy Invariants

- independent review는 중요한 통제지만, 모든 작업의 publish 선행조건은 아니다.
- canonical 기본 흐름은 `implement -> verify -> open PR publish`다. review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때 open PR 위에서 수행한다.
- independent review를 수행할 때만 implementer와 reviewer는 반드시 서로 다른 agent 또는 사람이어야 한다.
- review의 독립성은 "다른 모델인가"보다 "다른 세션, 다른 컨텍스트, 다른 역할 프롬프트를 가졌는가"로 판단한다.
- review는 latest verification report 또는 verification summary가 최신이고, review minimum context가 채워진 뒤에만 시작할 수 있다.
- reviewer는 diff만 보지 않고 task brief 또는 exec plan, verification 결과, 남은 리스크를 함께 읽어야 한다.
- review evidence는 independent review를 실제로 수행한 경우에만 필수 산출물이다.
- reviewer pool은 기본값이 아니다. 추가 reviewer는 security, reliability, public contract, migration처럼 실제로 다른 초점이 필요한 경우에만 붙인다.
- MCP 기반 외부 reviewer runtime이나 외부 모델 호출은 필수 canonical 경로가 아니다. current Codex 세션의 session-isolated reviewer나 사람 reviewer로 충분하면 그것을 우선한다.

## Review Trigger Rules

아래 중 하나라도 해당하면 independent review를 수행한다.

- 작업이 `guarded lane`이다.
- public API/schema, auth/permission, security, CI, migration, destructive change를 포함한다.
- 사용자가 reviewer 또는 sub-agent 검토를 명시적으로 요청했다.
- verification은 통과했지만 implementer가 residual risk가 높다고 판단했다.

아래는 기본적으로 independent review를 생략할 수 있다.

- bounded docs-only 또는 editorial change
- single-file low-risk refactor
- task brief만으로 scope와 verification이 충분히 닫히고 rollback cost가 낮은 direct request

review를 생략한 경우에도 verification evidence는 남겨야 한다.

## Role Split

| Role | Must Do | Must Not Do | Required Output |
| --- | --- | --- | --- |
| Implementer | scope 안에서 변경을 만들고 latest verification evidence를 준비한 뒤 open PR을 publish한다. review가 시작되면 reviewer에게 diff summary, verification 결과, source-of-truth update, 남은 리스크를 넘긴다. | verification 없이 PR을 publish-ready라고 주장하지 않는다. reviewer가 남긴 blocking finding을 non-blocking note로 축소하지 않는다. | diff, verification evidence, open PR, review handoff input |
| Reviewer | implementer와 분리된 관점으로 open PR 또는 latest diff를 검토하고 verdict를 남긴다. | implementer 역할까지 겸해 자기 손으로 수정하며 review를 종료하지 않는다. verification이 비어 있는데 승인하지 않는다. 범위 밖 작업을 구두로 끼워 넣지 않는다. | review verdict, findings, review evidence |

## Reviewer Runtime

- review를 Codex 안에서 수행할 때 기본값은 session-isolated reviewer 한 명이다.
- 사람이 직접 review하는 경우에도 이 문서의 minimum context와 verdict vocabulary를 그대로 따른다.
- 같은 base model을 써도 reviewer가 implementer의 live session, draft reasoning, write ownership, output ownership을 공유하지 않으면 독립 reviewer로 인정할 수 있다.
- reviewer는 read-only 분석과 verdict 산출을 맡는다. repair 적용은 implementer가 다시 맡는다.

## Single Reviewer Mode

- default review shape는 reviewer 한 명이다.
- reviewer는 open PR, latest verification, task brief 또는 exec plan을 읽고 verdict를 남긴다.
- reviewer 한 명으로도 scope, verification, source-of-truth update, residual risk를 평가할 수 있으면 추가 reviewer를 붙이지 않는다.

## Reviewer Pool Mode

- reviewer pool은 아래 경우에만 올린다.
  - security, reliability, operational blast radius가 큰 작업
  - public contract와 verification semantics를 동시에 강하게 봐야 하는 작업
  - 사용자가 다중 reviewer를 명시적으로 요청한 경우
- pool을 쓸 때 권장 role은 아래와 같다.

| Reviewer Role | Primary Focus |
| --- | --- |
| `scope-and-governance` | scope, write scope, source-of-truth update, policy contradiction |
| `verification-and-regression` | latest verification, diff/report consistency, correctness, regression risk |
| `security-and-reliability` | security, reliability, migration, operational risk |

- reviewer pool을 사용했을 때만 final verdict owner와 aggregation 근거를 남긴다.

## Reviewer Minimum Context

reviewer는 최소한 아래 입력을 받아야 한다.

- open PR link 또는 latest diff reference
- latest verification report 또는 verification summary
- task brief 또는 exec plan 경로
- touched diff summary와 touched file/doc 목록
- source-of-truth update 목록 또는 업데이트 불필요 사유
- 남은 리스크, skipped conditional command, follow-up 필요 사항

reviewer는 아래 중 하나라도 있으면 verdict를 `blocked`로 둔다.

- latest verification evidence가 없거나 latest가 아니다
- task brief 또는 exec plan이 없어 scope를 고정할 수 없다
- diff summary와 실제 변경 범위가 맞지 않는다
- canonical source가 없어 reviewer가 새 정책을 발명해야만 verdict를 낼 수 있다

## Review Read Order

1. task brief 또는 exec plan에서 문제 정의, scope, non-scope, write scope, verification 방법을 확인한다.
2. latest verification evidence에서 required command 결과와 skipped 이유를 확인한다.
3. open PR 또는 latest diff와 touched source-of-truth를 읽고 실제 변경이 목표와 일치하는지 본다.
4. 남은 리스크와 follow-up을 읽고 이번 PR에서 닫히는지, 후속 issue로 넘겨야 하는지를 판단한다.

이 순서를 건너뛰어도 되는 경우는 없다.

## Verdict Vocabulary

| Verdict | Meaning | Required Consequence |
| --- | --- | --- |
| `approved` | latest verification과 current diff를 기준으로 blocking finding이 없다 | PR은 current state로 유지되고 merge 또는 후속 handoff로 진행할 수 있다 |
| `changes-requested` | 현재 PR 범위 안에서 수리 가능한 blocking finding이 하나 이상 있다 | implementer가 open PR에서 repair 후 affected verification을 다시 실행한다 |
| `blocked` | missing reviewer input, missing canonical source, boundary conflict처럼 현재 PR 안에서 review를 닫을 수 없다 | `Blocked` 또는 follow-up planning으로 전환한다 |

추가 규칙:

- non-blocking note는 `approved`와 함께 남길 수 있다.
- reviewer는 `approved`를 주면서 blocking finding을 함께 남기지 않는다.
- implementer와 reviewer가 동일하면 independent review verdict로 간주하지 않는다.

## Verdict Aggregation

reviewer pool의 overall verdict는 아래 규칙으로 잠근다.

- 필수 reviewer 역할 중 하나라도 빠지면 overall verdict는 `blocked`다.
- 한 reviewer라도 `blocked`를 반환하면 overall verdict는 기본적으로 `blocked`다.
- `blocked`가 없고 한 reviewer라도 blocking finding과 함께 `changes-requested`를 반환하면 overall verdict는 `changes-requested`다.
- 모든 reviewer가 `approved`이거나 non-blocking note만 남기면 overall verdict는 `approved`다.
- reviewer 간 해석이 충돌하면 더 엄격한 verdict를 우선한다.

single reviewer mode에서는 aggregation을 따로 쓰지 않는다.

## Finding Classification

### Blocking Finding

아래 중 하나라도 해당하면 `changes-requested` 또는 `blocked` 사유가 된다.

- task brief 또는 exec plan scope를 벗어난 변경
- verification evidence 누락, stale evidence, diff와 evidence 불일치
- required command 재실행이 필요한데 latest evidence가 갱신되지 않음
- source-of-truth update가 필요하지만 빠져 있음
- correctness, regression, contract, security, reliability에 직접 영향을 주는 문제
- reviewer separation invariant 위반

### Non-Blocking Note

아래는 기본적으로 approval을 막지 않는다.

- naming, wording, comment 정리
- 후속 issue로 넘겨도 되는 quality/guardrail 후보
- 현재 목표와 무관한 선택적 refactor 제안

## Review Repair Loop

- `changes-requested` verdict에는 최소한 blocking finding, 기대 next action, 다시 확인할 command 또는 문서가 들어가야 한다.
- implementer는 open PR의 current diff에서 blocking finding을 줄이는 실제 수정을 남기고, 영향을 받은 required command를 다시 실행한 뒤 verification evidence를 갱신한다.
- baseline command가 영향을 받았으면 conditional command 성공을 유지로 간주하지 않는다.
- reviewer는 stale finding 대신 latest verification evidence와 현재 PR diff를 기준으로 다시 판단한다.
- 추가 reviewer를 다시 붙이는 것은 high-risk surface가 바뀌었거나 reviewer가 명시적으로 요구한 경우에만 한다.
- 같은 root cause가 두 번의 repair 뒤에도 남아 있으면 더 길게 밀어붙이지 말고 `blocked` 또는 follow-up issue split으로 전환한다.

## Review Evidence Rule

canonical review evidence는 review comment, PR comment, exec plan close-out 중 최소 한 곳에 아래 필드를 남긴다.

```md
## Independent Review
- Implementer: `agent-or-name`
- Reviewer: `agent-or-name`
- Additional Reviewers:
  - `<role>: agent-or-name`
- Reviewer Input:
  - PR or diff: `<url-or-summary>`
  - Latest verification report: `passed`
  - Task brief / exec plan: `<summary-or-path>`
  - Source-of-truth update: `<updated docs or why not needed>`
  - Remaining risks / skipped checks: `<summary>`
- Review Verdict: `approved | changes-requested | blocked`
- Findings / Change Requests:
  - `<blocking finding or no-blocking-notes>`
- Evidence:
  - `<why this verdict is justified>`
```

필수 규칙:

- `Implementer`, `Reviewer`, `Review Verdict`는 항상 적는다.
- reviewer pool을 사용했을 때만 `Additional Reviewers`와 aggregation 근거를 남긴다.
- `Reviewer Input`에는 minimum context가 요약돼야 한다.
- `changes-requested`면 어떤 수정이 필요한지와 re-run 대상이 드러나야 한다.
- independent review를 수행하지 않았다면 빈 evidence block을 만들지 않는다.

## Review Start Checklist

- latest verification evidence가 current diff와 같은 revision을 가리키는가
- open PR 또는 diff reference가 준비됐는가
- task brief 또는 exec plan이 current scope를 설명하는가
- skipped conditional command와 remaining risk가 reviewer input에 기록됐는가
- reviewer와 implementer의 세션 또는 ownership이 분리돼 있는가

## Relationship To Skills

- `reviewer-handoff` skill은 이 문서의 `Reviewer Minimum Context`, `Review Read Order`, `Review Evidence Rule`을 얇게 재사용한다.
- `reviewer-handoff`는 review가 실제로 필요한 경우에만 호출한다.
- `publish-after-review` skill 이름은 legacy지만, current canonical timing은 `verification -> open PR publish -> optional review`다. skill은 PR publish step을 얇게 돕는 용도로만 쓴다.
