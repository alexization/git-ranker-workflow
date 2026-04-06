# 2026-04-06-grw-10-harness-foundation-alignment

- Issue ID: `GRW-10`
- GitHub Issue: `#30`
- Status: `Ready`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-10-harness-foundation-alignment`
- Task Slug: `2026-04-06-grw-10-harness-foundation-alignment`

## Problem

현재 workflow source of truth는 앞으로 적용할 하네스 시스템의 canonical flow, 역할 분리, 완료 판정을 한 문장으로 묶어 보여주지 못하고 있다. 바로 다음 턴부터 issue/PR 단위 작업을 시작할 계획이라면, 모든 후속 작업이 같은 기준을 읽을 수 있도록 foundation 문서를 먼저 정렬해야 한다.

이번 기준에서 하네스의 핵심은 `라우팅`, `컨텍스트 제한`, `도구 경계`, `결정론적 검증`, `구현/리뷰 Agent 분리`, `실패의 가드레일화`다. 따라서 첫 작업은 이 여섯 축을 current source of truth에 명시하는 것이다.

## Why Now

사용자가 바로 다음 턴부터 issue/PR 단위로 새 Harness workflow를 적용할 계획이다. 따라서 시작점인 `roadmap`, `catalog`, `governance`, `index`가 먼저 현재 기준으로 정렬되어 있어야 이후 exec plan과 PR 운영 규칙이 흔들리지 않는다.

이 작업은 실제 구현 작업에 들어가기 전, 앞으로의 공식 계획과 운영 용어를 잠그는 foundation 단계다.

## Scope

- roadmap, catalog, index, 운영 문서를 현재 하네스 기준으로 정렬한다.
- canonical flow와 역할 분리 기준을 source of truth에 반영한다.
- 구현 Agent와 review Agent를 분리하는 정책을 후속 Issue가 바로 이어받을 수 있도록 기준점을 만든다.
- 새 하네스 기준의 후속 Issue 순서를 고정한다.

## Non-scope

- backend/frontend 앱 코드 변경
- CI 파이프라인 구현
- skill 본문 신규 작성

## Write Scope

- `docs/product/`
- `docs/architecture/`
- `docs/operations/`
- `.codex/skills/README.md`
- `docs/exec-plans/`

## Outputs

- 새 하네스 기준으로 갱신된 roadmap와 work item catalog
- 관련 index/governance 문서의 방향성 정렬
- 후속 Issue 진입 기준

## Working Decisions

- `docs/domain/*`와 실제 앱 동작을 설명하는 운영 문서는 컨텍스트 자산으로 유지한다.
- 완료된 exec plan은 historical evidence로 유지한다.
- 이후 하네스의 canonical flow는 `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback`이다.
- 완료 판정은 `결정론적 검증 통과`와 `별도 review Agent 승인`을 함께 요구한다.

## Verification

- `cat docs/product/harness-roadmap.md`
  - 결과 기대: 새 canonical flow와 phase별 Issue 순서가 명시되어 있어야 한다.
- `cat docs/product/work-item-catalog.md`
  - 결과 기대: 즉시 issue/PR로 전환 가능한 새 작업 카탈로그가 있어야 한다.
- `rg -n "Implementer|Reviewer|dual-agent|verification contract|ambiguity interview" docs/product docs/architecture docs/operations .codex/skills/README.md`
  - 결과 기대: 역할 분리와 검증 중심 흐름이 source of truth에 반영되어 있어야 한다.
- 문서 링크 검토
  - 결과 기대: 루트 인덱스와 product 인덱스가 여전히 올바른 경로를 가리켜야 한다.

## Evidence

문서 정렬 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- 새 canonical flow가 어디에 적혔는지
- 구현 Agent와 review Agent 분리 기준이 어디에 적혔는지
- 바로 다음 Issue가 무엇인지

## Risks or Blockers

- `workflow-governance.md`와 `control-plane-map.md`는 후속 Issue에서 더 정밀한 용어 정리가 필요할 수 있다.
- 구현/리뷰 Agent 분리를 문서에 적는 것과 실제 작업 절차에 녹이는 것은 다르므로, `GRW-16`에서 운영 규칙까지 닫아야 한다.

## Next Preconditions

- `GRW-11`: 하네스 시스템 맵과 상태 머신 정의
- `GRW-12`: 요청 라우팅과 ambiguity interview 정책 정의
- `GRW-15`: verification contract registry 정의
- `GRW-16`: dual-agent review policy 정의

## Docs Updated

- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/active/2026-04-06-grw-10-harness-foundation-alignment.md`

## Skill Consideration

이번 작업은 새 skill을 만드는 단계가 아니다. 다만 이후 `GRW-S08`에는 verification 이후 review handoff와 repair loop를 함께 다루는 skill이 포함되어야 한다.
