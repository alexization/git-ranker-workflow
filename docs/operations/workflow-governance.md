# Workflow Governance

이 문서는 workflow 저장소를 기준으로 모든 작업이 공유해야 하는 운영 규칙을 정의한다.

## Reader-First Body 규칙

- Issue와 PR 본문은 사람이 빠르게 맥락과 판단 포인트를 이해하기 위한 reader-first 문서로 쓴다.
- 본문에는 문제, 배경, 접근, 영향, 검토 포인트, 남은 리스크처럼 사람이 바로 판단할 정보를 우선 적는다.
- 한 섹션은 가능하면 짧은 문단 하나 또는 1~3개 bullet로 끝낸다.
- raw verification command, spec 경로, 브랜치 이름, reviewer runtime dump, ledger detail은 본문 기본값으로 넣지 않는다.
- 이런 운영 상세는 spec, verification artifact, review note, feedback artifact에 남긴다.

## 문서 링크 규칙

- 저장소 문서 본문에는 저장소 기준 상대경로를 사용한다.
- 로컬 도구 응답에서만 절대경로를 사용한다.

## Stable Source Of Truth의 Task ID 규칙

- `docs/specs/`, GitHub Issue/PR 본문처럼 tracking이 본질인 문서는 work item ID를 직접 써도 된다.
- `docs/architecture/`, `docs/operations/` 같은 stable source of truth 문서에는 future work 설명을 위해 직접적인 work item ID를 남기지 않는다.
- stable 문서에서 후속 확장을 가리킬 때는 task ID 대신 정책, registry, skill, guardrail 같은 자산 이름을 쓴다.

## Policy / Skill Boundary

- `request-routing-policy.md`는 route 결정과 ambiguity exit condition만 다룬다.
- `sdd-spec-policy.md`는 Socratic question contract, clarification loop, approval gate를 다룬다.
- 이 문서는 runtime 순서, artifact/lane 운영, evidence minimum을 다룬다.
- project-local skill은 위 policy를 대체하지 않고 한 stage의 반복 workflow와 handoff만 다룬다.

## Runtime Principles

- 모든 즉시 실행 가능한 작업은 `request -> Socratic spec loop -> Harness no-more-questions judgment -> user approval request -> approved spec -> implementation` 순서를 따른다.
- 추가 planning 문서를 따로 만들지 않는다. 작업을 더 자세히 정의해야 하면 spec을 갱신한다.
- spec은 요구사항, 하위 작업, write scope, verification, tracking 결정을 함께 소유한다.
- verification, review, user validation에서 spec defect가 드러나면 patch로 밀어붙이지 말고 spec을 다시 `Draft`로 내려 clarification과 재승인을 반복한다.
- issue는 추적이 필요할 때만 만든다.
- PR은 publish가 필요한 결과를 latest verification 뒤 공개하는 기본 surface다.
- independent review와 feedback close-out은 중요한 통제지만 기본 happy path의 공통 선행조건은 아니다.
- 마지막 완료 판정은 사용자 최종 검증까지 포함한다.

## Request And Spec 규칙

- 작업 시작 전 [request-routing-policy.md](request-routing-policy.md)로 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다.
- `모호한 요청`은 먼저 single executable requirement로 줄인다.
- `즉시 실행 가능한 작업`은 곧바로 구현하지 않고 [sdd-spec-policy.md](sdd-spec-policy.md)에 따라 spec을 먼저 만든다.
- 작업 요청 자체를 spec 승인으로 취급하지 않는다.
- Harness가 더 이상 blocker 질문이 없다고 판단한 뒤에만 사용자에게 현재 spec 초안의 승인 요청을 할 수 있다.
- remaining planned work도 별도 roadmap/catalog이 아니라 `docs/specs/active/`의 `Draft` spec으로 유지한다.
- 승인되지 않은 spec은 canonical source가 아니다.
- 구현 중 범위가 바뀌면 별도 planning 문서를 만들지 말고 spec을 다시 승인받는다.
- review나 user validation에서 current spec이 요구사항을 잘못 잠근 것으로 드러나면 구현 수리보다 먼저 spec을 재초안하고 다시 승인받는다.

## Lane 규칙

lane은 approved spec이 만들어진 뒤에 고른다.

| Lane | 언제 쓰나 | 기본 산출물 | 생략 가능한 것 |
| --- | --- | --- | --- |
| `default lane` | 단일 저장소, bounded scope, rollback cost 낮음, tracking 필요 없음 | approved spec, verification evidence, 필요 시 open PR | parent issue, subtask issue, independent review |
| `guarded lane` | tracked backlog, cross-repo planning, public contract/auth/schema/CI/migration/destructive change, 또는 formal tracking이 필요한 작업 | approved spec, tracking issue 필요 시, verification evidence, 필요 시 review/feedback, 필요 시 open PR | 불필요한 multi-reviewer pool |

`guarded lane`이라도 spec이 canonical source다. issue는 spec을 대체하지 않는다.

## Subtask 규칙

- 한 spec 안에서 여러 하위 작업이 필요하면 spec 안에 먼저 분해한다.
- 하위 작업 하나는 하나의 목표를 가진다.
- 저장소가 둘 이상이면 하위 작업도 저장소별로 나눈다.
- 하위 작업별 issue/PR은 tracking 필요가 있을 때만 만든다.
- current 구현 루프는 항상 하나의 active subtask만 가진다.

## Context / Boundary 규칙

- 구현 전 [../architecture/context-pack-registry.md](../architecture/context-pack-registry.md)에서 primary context pack 하나를 고른다.
- [tool-boundary-matrix.md](tool-boundary-matrix.md)로 read boundary, write boundary, network, escalation을 spec 기준으로 잠근다.
- approved spec에 없는 저장소 쓰기나 broad network access가 필요해지면 spec을 먼저 갱신하고 다시 승인받는다.
- cross-repo planning은 여러 저장소를 읽을 수 있어도 app 구현은 시작하지 않는다.

## Verification / Review / Feedback 규칙

- verification contract profile은 spec에 적는다.
- latest verification evidence는 spec이나 별도 verification artifact에 남긴다.
- independent review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때 수행한다.
- feedback close-out은 blocker, 반복 실패, guardrail promotion 필요성이 있을 때만 남긴다.
- quality sweep signal은 original task completion과 분리해 follow-up으로 보낸다.

## Issue / PR 단위 규칙

- tracked backlog 또는 guarded lane에서는 `Issue 1개 = 목표 1개`, `PR 1개 = 목표 1개`를 유지한다.
- default lane의 작은 직접 요청은 issue 없이 진행할 수 있다.
- 하나의 PR은 하나의 목표만 해결한다.
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다.
- cross-repo 작업은 workflow 문서 PR과 앱 코드 PR로 나눈다.

## 각 Spec에 반드시 들어가야 할 내용

- 대상 저장소
- 문제 또는 배경
- 목표와 비목표
- 소크라테스 질문으로 확정한 핵심 결정
- approval gate 또는 그에 준하는 readiness 판단
- write scope
- 수용 기준
- verification 방법
- 하위 작업 필요 시 그 분해
- issue/PR tracking 필요 여부
- 남아 있는 리스크나 open question

## 각 Issue에 반드시 들어가야 할 내용

- target repo
- problem / background
- why now
- expected outcome
- scope / non-scope
- approach note
- impact or dependency
- risk or open question

## 각 PR에 반드시 들어가야 할 내용

- linked issue 또는 no-issue reason
- 무엇이 바뀌었는지와 왜 필요한지
- 어떤 spec 또는 subtask를 구현한 것인지
- verification 결과 요약과 남은 공백
- reviewer focus 필요 시
- impact / risks

## 증거 규칙

- human-facing Issue/PR 본문과 운영용 close-out artifact를 분리한다.
- verification evidence 최소 필드:
  - contract profile
  - overall status
  - 무엇을 실행했는지
  - 핵심 evidence
  - failure or skipped summary
  - next action
- review evidence 최소 필드:
  - implementer
  - reviewer
  - reviewer input
  - verdict
  - finding 또는 no-blocking note
- feedback evidence 최소 필드:
  - stage
  - failure class
  - promotion decision
  - follow-up asset 또는 `no-new-guardrail` 이유
- quality sweep evidence 최소 필드:
  - trigger mode
  - scan scope
  - signal class
  - disposition
  - evidence

## GitHub Issue / PR 운영 규칙

- issue는 approved spec이 추적 surface를 요구할 때만 만든다.
- GitHub 본문은 먼저 파일로 작성한 뒤 `gh issue create --body-file ...` 또는 `gh pr create --body-file ...`로 보낸다.
- issue와 PR 본문은 대상 저장소의 template 형식을 따른다.
- PR은 latest verification이 끝난 뒤 open 상태로 생성한다.
- draft PR은 사용자가 명시적으로 요청했을 때만 사용한다.
- Issue/PR 본문에는 사람이 확인할 요약만 적고, raw command literal이나 detailed artifact dump는 넣지 않는다.

## 현재 기준 실행 순서

1. `request-routing-policy.md`로 요청을 분류한다.
2. 즉시 실행 가능한 작업이면 소크라테스 질문으로 spec 초안을 세부화한다.
3. Harness가 approval gate를 채우기에 더 이상 blocker 질문이 없다고 판단하면 현재 spec 초안에 대한 승인 요청을 사용자에게 한다.
4. 사용자가 그 spec 초안에 명시적으로 동의하면 spec을 `Approved`로 고정한다.
5. spec이 요구하면 parent issue와 subtask issue를 만든다.
6. 현재 active subtask를 구현한다.
7. verification evidence를 남긴다.
8. publish가 필요한 결과면 open PR을 만든다.
9. review, feedback, user validation 중 spec defect가 드러나면 spec을 `Draft`로 내려 clarification loop와 재승인을 다시 연다.
10. review 또는 feedback이 trigger되면 그 evidence를 남긴다.
11. 사용자 최종 검증으로 완료를 닫는다.

## 공통 실행 지시

- 이 spec 또는 active subtask의 목표만 수행한다. 범위를 넓히지 않는다.
- spec이 승인되기 전에는 구현에 들어가지 않는다.
- draft spec이 있더라도 사용자 명시적 approval이 없으면 `Approved`로 취급하지 않는다.
- 허용된 write scope 밖의 파일은 수정하지 않는다.
- 늦게 드러난 spec defect를 code repair나 reviewer note로만 덮지 않는다.
- network나 escalation이 필요하면 spec 또는 close-out artifact에 남긴다.
- verification failure가 나면 retry budget 안에서만 repair loop를 돌린다.
- source of truth 문서를 함께 업데이트하거나, 업데이트가 불필요한 이유를 남긴다.
- 동일 작업이 반복될 가능성이 높다면 skill화 여부를 검토한다.

## 공통 Definition Of Done

- 왜 이 작업이 필요한지 approved spec에 남아 있다.
- 변경 범위가 한 가지 목표 또는 active subtask에 집중되어 있다.
- verification 결과가 spec, verification artifact, PR 중 적절한 위치에 남아 있다.
- publish가 필요했다면 latest verification을 반영한 open PR이 생성됐거나, publish하지 않은 이유가 명시되어 있다.
- review나 feedback이 실제로 필요했다면 그 evidence가 남아 있다.
- 사용자 최종 검증이 완료되었거나 follow-up 필요성이 명시되어 있다.
- source of truth 문서가 함께 업데이트되었거나 불필요 사유가 명시되어 있다.
