# Dual-Agent Review Policy

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Reviewing`, `Repairing`, `Feedback Pending` semantics를 실제 운영 규칙으로 고정한다. [verification-contract-registry.md](verification-contract-registry.md)가 reviewer handoff 전의 verification 완료 조건을 잠근다면, 이 문서는 reviewer가 어떤 입력을 읽고 어떤 verdict를 남기며 어떤 경우에 repair 또는 `Blocked`로 되돌리는지를 잠근다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md), verification handoff minimum은 [verification-contract-registry.md](verification-contract-registry.md)를 따른다.

## Policy Invariants

- implementer와 reviewer는 반드시 서로 다른 agent 또는 사람이어야 한다.
- independent review의 canonical runtime은 현재 Codex 세션에서 분리 생성한 session-isolated sub-agent reviewer pool이다.
- review의 독립성은 "다른 모델인가"보다 "다른 세션, 다른 컨텍스트, 다른 역할 프롬프트를 가졌는가"로 판단한다.
- reviewer separation의 근거에는 output ownership 분리도 포함된다. reviewer verdict를 누가 최종 owner로 남기는지 evidence에서 추적 가능해야 한다.
- review는 latest verification report의 overall status가 `passed`이고 reviewer handoff minimum이 채워진 뒤에만 시작할 수 있다.
- PR 존재 여부는 review의 선행조건이 아니다. 기본 publish 흐름은 local diff와 verification 결과를 먼저 review하고, 그 verdict를 PR에 싣는 순서다.
- draft PR 또는 open PR 생성 자체는 canonical review start signal이 아니다. review/repair loop는 local diff와 latest artifact에서 먼저 닫고, PR은 승인된 결과를 publish하는 reader-facing container로 쓴다.
- reviewer는 diff만 보지 않고 exec plan, latest verification report, 남은 리스크를 함께 읽어야 한다.
- reviewer는 현재 issue의 scope, write scope, verification contract, source of truth를 기준으로 판단한다. 새 목표 추가나 범위 확장은 review 단계에서 승인하지 않는다.
- review evidence는 필수 산출물이다. verdict만 있고 reviewer input이나 finding 근거가 없으면 `Completed` 판정으로 보지 않는다.
- MCP 기반 외부 reviewer runtime, 외부 모델 호출, implementer 세션 안의 self-review는 canonical review 경로가 아니며 사용하지 않는다.
- reviewer pool은 최소 두 개의 sub-agent reviewer로 구성한다. 각 reviewer는 implementer와 분리된 세션에서 시작하고 reviewer minimum context와 역할 프롬프트만 받아야 한다.
- reviewer가 여러 명이면 최종 verdict는 pool aggregation 규칙으로 잠그고, implementer는 그 verdict를 임의로 완화할 수 없다.
- future skill, template, checklist는 이 문서를 압축해서 재사용할 수 있지만, 이 문서를 대체하거나 override할 수는 없다.

## Role Split

| Role | Must Do | Must Not Do | Required Output |
| --- | --- | --- | --- |
| Implementer | exec plan 범위 안에서 변경을 만들고 latest verification report를 준비한다. reviewer에게 diff summary, touched doc, 남은 리스크, conditional command 생략 사유를 넘긴다. review finding이 blocking이면 수정 후 관련 명령을 다시 실행한다. publish path에 필요한 evidence가 고정되면 그 최신 결과를 PR body에는 요약으로, canonical evidence에는 상세로 반영해 publish한다. open path는 `approved` verdict와 feedback outcome을, blocker-sharing draft path는 declared blocker와 blocker disclosure를 함께 반영한다. | 자기 결과를 최종 승인하지 않는다. review 전에 verification report 없이 완료를 주장하지 않는다. blocking finding을 non-blocking note로 축소하지 않는다. approved 전 draft PR을 review workspace처럼 기본값으로 쓰지 않는다. | diff, latest verification report, reviewer handoff input, publish-ready PR body |
| Reviewer | implementer와 분리된 관점으로 scope, verification, diff, source-of-truth update, residual risk를 검토한다. role이 나뉜 sub-agent reviewer들이 finding을 남기고, reviewer coordinator sub-agent가 이를 집계해 final verdict를 남긴다. | implementer 역할까지 겸해 자기 손으로 수정하며 review를 종료하지 않는다. verification이 비어 있는데 승인하지 않는다. 범위 밖 작업을 구두로 끼워 넣지 않는다. PR이 아직 없다는 이유로 review를 미루지 않는다. implementer가 reviewer coordinator를 겸해 self-approval를 우회하지 않는다. draft PR 생성 자체를 review 개시 조건으로 요구하지 않는다. | review verdict, findings, review evidence |

## Sub-Agent Isolation Model

- independent review는 현재 작업 세션과 분리된 sub-agent reviewer들을 spawn해 수행한다.
- 같은 base model을 써도 reviewer가 implementer의 live session, draft reasoning, write ownership, output ownership을 공유하지 않으면 독립 reviewer로 인정할 수 있다.
- MCP나 외부 모델 runtime을 reviewer로 호출해 independent review를 대체하지 않는다.
- reviewer input은 `Reviewer Minimum Context`와 role-specific prompt focus로 제한한다. implementer가 봤던 전체 탐색 문서 묶음, 미정 설계 메모, repair 중간 상태를 그대로 reviewer에게 넘기는 것은 기본값이 아니다.
- reviewer는 read-only 분석과 verdict 산출을 맡는다. 파일 수정이나 repair 적용은 implementer가 다시 맡는다.

## Reviewer Pool Mode

- review는 항상 role-prompted sub-agent reviewer pool로 수행한다.
- 최소 reviewer 구성은 아래 두 역할이다.
  - `scope-and-governance`
  - `verification-and-regression`
- security, reliability, 운영 영향이 크면 `security-and-reliability` reviewer를 추가한다.
- reviewer pool을 쓸 때도 공통 handoff surface는 `Reviewer Minimum Context`로 유지한다. 다만 각 reviewer는 자기 역할에 필요한 subset과 역할별 focus를 받을 수 있고, final verdict owner는 최소 컨텍스트 다섯 가지를 모두 추적 가능해야 한다.

권장 role prompt 예시:

| Reviewer Role | Primary Focus |
| --- | --- |
| `scope-and-governance` | exec plan scope, write scope, source-of-truth update, policy contradiction |
| `verification-and-regression` | latest verification report, diff/report consistency, correctness, regression risk |
| `security-and-reliability` | security, reliability, operational risk, follow-up 필요성 |

추가 규칙:

- role prompt는 집중 검토 영역을 좁히기 위한 것이지, reviewer minimum context를 생략하기 위한 핑계가 아니다.
- reviewer coordinator는 별도 reviewer이거나 reviewer 중 한 명일 수 있다. implementer는 결과를 기록할 수는 있어도 verdict를 새로 정하지 않는다.
- reviewer pool coordinator는 reviewer 역할에 속한 owner여야 한다. implementer는 findings를 전달할 수는 있어도 aggregation owner가 되지 않는다.

## Reviewer Minimum Context

reviewer는 최소한 아래 입력을 받아야 한다.

- exec plan 경로와 linked issue. PR이 이미 있다면 링크를 추가하고, 아직 없으면 생략 가능하다.
- latest verification report
- touched diff summary와 touched file 또는 doc 목록
- source-of-truth update 목록 또는 "업데이트 불필요" 사유
- 남은 리스크, skipped conditional command, follow-up 필요 사항

sub-agent reviewer pool을 쓰더라도 위 다섯 가지가 공통 handoff surface라는 사실은 변하지 않는다. role prompt는 이 minimum 위에 덧붙는 추가 focus일 뿐이며, 역할별 reviewer는 필요한 subset만 읽을 수 있다.

선택 입력:

- screenshot, trace, video, log 요약, metric evidence
- 이전 repair attempt 요약
- 관련 review comment thread 링크

reviewer는 아래 중 하나라도 있으면 verdict를 `blocked`로 둔다.

- latest verification report가 없거나 latest가 아니다
- latest verification report의 overall status가 `passed`가 아니다
- exec plan이나 write scope를 확인할 수 없다
- diff summary와 실제 변경 범위가 맞지 않아 검토 기준을 고정할 수 없다
- canonical source가 없어 reviewer가 새 정책을 발명해야만 verdict를 낼 수 있다

## Review Read Order

1. exec plan에서 문제 정의, scope, non-scope, write scope, verification contract를 확인한다.
2. latest verification report에서 required command 결과와 skipped 이유를 확인한다.
3. diff와 touched source-of-truth를 읽고 실제 변경이 issue 목표와 일치하는지 본다.
4. 남은 리스크와 follow-up을 읽고 이번 issue 안에서 닫히는지, 다음 issue로 넘겨야 하는지를 판단한다.

이 순서를 건너뛰어도 되는 경우는 없다. reviewer는 최소 컨텍스트를 읽기 전에 verdict를 먼저 선언하지 않는다.

sub-agent reviewer pool에서는 각 reviewer가 자기 focus에 맞는 읽기 순서를 강조할 수 있지만, final verdict owner는 위 순서를 건너뛰지 않는다.

## Verdict Vocabulary

| Verdict | Meaning | Required Consequence |
| --- | --- | --- |
| `approved` | implementer/reviewer 분리가 지켜졌고 latest verification report, diff, source-of-truth update, 남은 리스크를 검토한 결과 blocking finding이 없다 | `Feedback Pending`으로 진행한다 |
| `changes-requested` | 현재 issue 범위 안에서 수리 가능한 blocking finding이 하나 이상 있다 | `Repairing`으로 되돌린다 |
| `blocked` | 별도 reviewer 부재, missing canonical source, missing review input, boundary conflict처럼 현재 issue 안에서 review를 닫을 수 없다 | `Blocked` 또는 follow-up planning으로 전환한다 |

추가 규칙:

- non-blocking note는 `approved`와 함께 남길 수 있다.
- implementer와 reviewer가 동일하면 기본 verdict는 `changes-requested`다. 별도 reviewer를 배정할 수 없는 상황까지 확인되면 `blocked`로 올린다.
- reviewer는 `approved`를 주면서 blocking finding을 함께 남기지 않는다.

## Verdict Aggregation

sub-agent reviewer pool의 overall verdict는 아래 규칙으로 잠근다.

- 필수 reviewer 역할 중 하나라도 빠지면 overall verdict는 `blocked`다.
- 한 reviewer라도 `blocked`를 반환하면 overall verdict는 기본적으로 `blocked`다.
- `blocked`가 없고 한 reviewer라도 blocking finding과 함께 `changes-requested`를 반환하면 overall verdict는 `changes-requested`다.
- 모든 reviewer가 `approved`이거나 non-blocking note만 남기면 overall verdict는 `approved`다.
- reviewer 간 해석이 충돌하면 더 엄격한 verdict를 우선하고, implementer가 그 차이를 임의 설명으로 상쇄하지 않는다.
- final evidence에는 role별 finding 요약과 aggregated verdict 근거가 함께 남아야 한다.
- finding aggregation이 불가능하거나 latest verification report와 reviewer finding의 revision이 맞지 않으면 overall verdict는 `blocked`다.

## Finding Classification

### Blocking Finding

아래 중 하나라도 해당하면 `changes-requested` 또는 `blocked` 사유가 된다.

- issue scope 또는 write scope를 벗어난 변경
- verification report 누락, stale report, diff와 report 불일치
- required command 재실행이 필요한데 latest report가 갱신되지 않음
- source-of-truth update가 필요하지만 빠져 있음
- correctness, regression, contract, security, reliability에 직접 영향을 주는 문제
- reviewer separation invariant 위반

### Non-Blocking Note

아래는 기본적으로 approval을 막지 않는다.

- naming, wording, comment 정리
- 후속 issue로 넘겨도 되는 guardrail 후보
- 현재 목표와 무관한 선택적 refactor 제안

non-blocking note도 기록은 남겨야 하지만, implementer가 같은 턴에서 반드시 해결해야 하는 의무로 바꾸지 않는다.

## Review Repair Loop

- `changes-requested` verdict에는 최소한 blocking finding, 기대 next action, 다시 확인할 command 또는 문서가 들어가야 한다.
- implementer는 blocking finding을 줄이는 실제 수정 하나 이상을 남기고, 영향을 받은 required command를 다시 실행한 뒤 latest verification report를 갱신한다.
- baseline command가 영향을 받았으면 conditional command 성공을 유지로 간주하지 않는다. latest report에 다시 적어야 한다.
- reviewer는 stale finding 대신 latest report와 현재 diff를 기준으로 다시 판단한다.
- draft PR review thread는 canonical repair loop가 아니다. 기본 repair loop는 local diff, latest verification report, reviewer evidence를 기준으로 닫는다. open path는 `approved`와 feedback outcome이 고정된 뒤 publish하고, blocker-sharing exception이 선언되면 blocker disclosure를 고정한 뒤 draft path로 publish한다.
- 같은 root cause가 두 번의 repair 뒤에도 남아 있으면 더 길게 밀어붙이지 말고 `blocked` 또는 follow-up issue split으로 전환한다.
- review 단계에서 새 범위가 드러나면 기존 issue에 끼워 넣지 않고 exec plan 갱신 또는 새 issue 분해로 되돌린다.

## Review Evidence Rule

canonical review evidence는 review comment나 exec plan close-out 중 최소 한 곳에 아래 필드를 남긴다. PR 본문에는 필요하면 verdict와 핵심 finding 요약만 싣는다.

```md
## Independent Review
- Implementer: `agent-or-name`
- Reviewer: `agent-or-name | reviewer-coordinator`
- Additional Reviewers:
  - `<role>: agent-or-name`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
  - `<security-and-reliability when needed>`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/...`
  - Latest verification report: `passed`
  - Diff summary: `<summary>`
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
- sub-agent reviewer pool의 필수 역할과 reviewer 이름을 남기고, role별 finding 요약 또는 `no-blocking note`를 남긴다.
- `Reviewer Input`에는 최소 컨텍스트 다섯 가지가 요약돼야 한다.
- `approved`면 blocking finding이 없다는 점이 드러나야 한다.
- `changes-requested`면 어떤 수정이 필요한지와 re-run 대상이 드러나야 한다.
- 문서 전용 issue라도 review evidence를 생략하지 않는다. artifact가 없을 뿐, verdict 근거는 남겨야 한다.
- PR을 나중에 publish하면 latest review verdict 요약을 reader-facing body에 반영할 수 있다. PR 생성이 verdict 시점을 뒤로 미루는 근거가 되지 않는다.

## Draft Checklist

- implementer와 reviewer가 분리돼 있는가
- 최소 두 개의 session-isolated sub-agent reviewer가 배정됐는가
- reviewer와 implementer 사이의 세션, 컨텍스트, 역할 프롬프트, output ownership 분리가 evidence에 드러나는가
- exec plan의 scope, non-scope, write scope가 현재 diff와 일치하는가
- latest verification report가 존재하고 overall status가 `passed`인가
- skipped conditional command와 remaining risk가 reviewer input에 기록돼 있는가
- diff와 verification report, source-of-truth update가 서로 모순되지 않는가
- blocking finding과 non-blocking note가 명확히 구분돼 있는가
- verdict와 next action이 state machine의 `Feedback Pending`, `Repairing`, `Blocked` 중 하나로 자연스럽게 이어지는가

## Relationship To Skills

- future `reviewer-handoff` skill은 이 문서의 `Reviewer Minimum Context`, `Review Read Order`, `Review Evidence Rule`을 얇게 재사용한다.
- future `reviewer-handoff` skill은 session-isolated sub-agent reviewer pool에 동일한 minimum context를 fan-out하고, role prompt와 aggregation만 thin layer로 추가한다.
- future `publish-after-review` skill은 `approved` verdict와 fixed feedback outcome 뒤에 open PR을 publish하거나, blocker-sharing exception이 선언되면 draft PR을 publish하는 thin-layer handoff만 담당하고, review ordering이나 draft 예외 규칙은 계속 이 문서와 workflow governance가 canonical source다.
- template와 checklist는 future skill 폴더 안에 둘 수 있지만, verdict vocabulary와 blocking 기준은 계속 이 문서가 canonical source다.
