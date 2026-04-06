# 2026-04-06-grw-12-request-routing-ambiguity-policy

- Issue ID: `GRW-12`
- GitHub Issue: `#33`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-12-request-routing-ambiguity-policy`
- Task Slug: `2026-04-06-grw-12-request-routing-ambiguity-policy`

## Problem

`GRW-11`은 `Router`, `Interviewing`, `Rejected` 상태의 상위 semantics를 정의했지만, 실제 intake 단계에서 어떤 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류할지와 인터뷰를 언제 시작하고 끝낼지는 아직 문서화되지 않았다.

이 상태로 후속 context pack, tool boundary, verification, review, intake skill 작업을 진행하면 같은 요청이 작업자별로 다른 route를 타고, exec plan 생성 여부와 질문 개수도 일관되지 않게 된다.

## Why Now

요청 라우팅 정책은 context pack, tool boundary, verification, review policy가 공유해야 하는 intake 기준이다. `GRW-12`가 먼저 고정돼야 다음 단계가 "무엇을 실행 가능한 작업으로 볼 것인가"를 같은 기준으로 다룰 수 있다.

또한 pilot과 intake skill이 재현 가능한 intake 절차를 사용하려면, 인터뷰가 요구사항을 늘리는 절차가 아니라 범위를 줄여 exec plan 가능한 작업으로 만드는 절차라는 점을 먼저 source of truth에 고정해야 한다.

## Scope

- `docs/operations/` 아래에 request routing과 ambiguity interview 정책 문서를 작성한다.
- 요청 분류 기준, ambiguity signal, 인터뷰 질문 규칙, 종료 조건, 일반 대화 fallback, `Rejected` semantics를 정의한다.
- operations 인덱스와 governance 문서가 새 정책을 참조하도록 갱신한다.
- stable source of truth 문서에 남아 있는 직접적인 work item ID 참조를 일반 서술로 정리한다.
- 이후 close-out에서 같은 문제가 반복되지 않도록 governance와 exec plan 작성 절차에 task ID 정리 규칙을 추가한다.
- `GRW-12` exec plan을 작성하고 완료 시점에 close-out을 남긴다.

## Non-scope

- 신규 에이전트 런타임 구현
- backend/frontend 앱 코드 변경
- intake/ambiguity skill 작성
- context pack registry, tool boundary, verification contract, review policy의 상세 정의

## Write Scope

- `.codex/skills/issue-to-exec-plan/`
- `docs/architecture/`
- `docs/operations/`
- `docs/quality-score/`
- `docs/exec-plans/`

## Outputs

- request routing과 ambiguity interview를 함께 다루는 운영 정책 문서
- 갱신된 `docs/operations/README.md`
- 갱신된 `docs/operations/workflow-governance.md`
- stable source of truth용 task ID cleanup 규칙
- evergreen harness 문서의 task ID 일반화
- `GRW-12` 실행 기록

## Working Decisions

- route category는 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 세 가지로 유지한다.
- ambiguity interview는 새 기능 아이디어를 늘리는 절차가 아니라 범위, 저장소, write scope, 완료 조건을 줄여 고정하는 절차로 정의한다.
- 일반 대화는 exec plan을 만들지 않고 응답으로 종료한다.
- `Rejected`는 대화성 요청, 사용자 취소, 범위 밖 요청, canonical source 부재처럼 실행을 계속하지 않기로 결정한 경우에만 사용한다.

## Verification

- `sed -n '1,320p' docs/operations/request-routing-policy.md`
  - 결과: route category 3종, ambiguity signal, immediate execution criteria, interview rules, exit condition, `Rejected` reason, example classification 5건이 한 문서에 정리된 것을 확인했다.
- `rg -n "대화|모호한 요청|즉시 실행 가능한 작업|ambiguity|interview|Rejected|fallback" docs/operations/request-routing-policy.md docs/operations/workflow-governance.md docs/operations/README.md`
  - 결과: 새 정책 문서, governance, operations 인덱스에서 intake 핵심 용어와 `Rejected` semantics가 함께 grep되는 것을 확인했다.
- `sed -n '1,180p' docs/operations/workflow-governance.md`
  - 결과: 요청 intake 규칙 section과 stable source of truth의 task ID cleanup 규칙이 추가됐고, `즉시 실행 가능한 작업`만 issue와 exec plan으로 보낸다는 규칙이 GitHub Issue/PR 운영 규칙과 실행 순서에 반영된 것을 확인했다.
- `sed -n '1,80p' docs/operations/README.md`
  - 결과: operations 인덱스가 `request-routing-policy.md`를 현재 기준 문서로 가리키는 것을 확인했다.
- `rg -n "GRW-[0-9]+|GRW-S[0-9]+|GRB-[0-9]+|GRC-[0-9]+" docs/architecture docs/operations docs/domain docs/reliability docs/security docs/quality-score`
  - 결과: stable source of truth 쪽에서는 식별자 형식 설명과 historical baseline 문맥만 남고, evergreen harness 설명 문장에서는 직접적인 work item ID가 제거된 것을 확인했다.
- `sed -n '96,132p' docs/architecture/harness-system-map.md`
  - 결과: 후속 정책 surface와 retry/guardrail 설명이 work item ID 대신 자산 이름 기준으로 일반화된 것을 확인했다.
- `sed -n '1,120p' .codex/skills/issue-to-exec-plan/SKILL.md`
  - 결과: exec plan 작성 skill에 stable source of truth 문서의 task ID cleanup 계획과 금지 규칙이 반영된 것을 확인했다.
- GitHub Issue `#33` body 확인
  - 결과: issue 본문이 template 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- 예시 요청 5건 수동 검토
  - 결과: `대화`, `모호한 요청`, `즉시 실행 가능한 작업`, `Rejected` close-out이 서로 다른 다음 행동을 갖도록 일관되게 정리된 것을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 만들지 않는다. 대신 아래를 근거로 남긴다.

- `docs/operations/request-routing-policy.md`의 route taxonomy와 ambiguity interview 규칙
- `docs/operations/workflow-governance.md`의 intake gate와 갱신된 실행 순서
- `docs/operations/README.md`의 source of truth 인덱스 반영
- `docs/architecture/harness-system-map.md`, `docs/operations/workflow-verification-runtime.md`, `docs/operations/observability-reference.md`, `docs/operations/frontend-runtime-reference.md`, `docs/quality-score/agent-readiness-scorecard.md`의 task ID 일반화 결과
- `.codex/skills/issue-to-exec-plan/SKILL.md`의 stable 문서 cleanup 가드레일
- GitHub Issue `#33` 본문 확인 결과

## Risks or Blockers

- 이후 skill이나 후속 정책 문서를 작성할 때 stable source of truth 대신 planning 문서의 task ID를 다시 본문으로 끌어오면 같은 drift가 반복될 수 있다.
- `missing-canonical-source`와 `non-executable-after-interview`는 둘 다 non-execution close-out이지만, 이후 planning workflow에서 후속 issue 생성 규칙을 더 세밀하게 다룰 여지가 있다.

## Next Preconditions

- `GRW-13`: context pack registry와 task-to-context 매핑 정의
- `GRW-14`: tool boundary matrix와 write scope 거버넌스 정의
- `GRW-S06`: intake/ambiguity skill pack

## Docs Updated

- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `docs/architecture/harness-system-map.md`
- `docs/operations/request-routing-policy.md`
- `docs/operations/workflow-governance.md`
- `docs/operations/README.md`
- `docs/operations/workflow-verification-runtime.md`
- `docs/operations/observability-reference.md`
- `docs/operations/frontend-runtime-reference.md`
- `docs/quality-score/agent-readiness-scorecard.md`
- `docs/exec-plans/completed/2026-04-06-grw-12-request-routing-ambiguity-policy.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 범위는 아니다. 대신 후속 intake/ambiguity skill이 그대로 재사용할 수 있게 route 결정 입력, ambiguity signal, interview 종료 조건, `Rejected` close-out reason을 문서형 source of truth로 먼저 고정했다.
