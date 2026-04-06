# 2026-04-07-grw-14-tool-boundary-matrix-write-scope-governance

- Issue ID: `GRW-14`
- GitHub Issue: `#37`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-14-tool-boundary-matrix-write-scope-governance`
- Task Slug: `2026-04-07-grw-14-tool-boundary-matrix-write-scope-governance`

## Problem

`GRW-11`은 `Context Ready`와 `Implementing` 사이에 도구 경계와 write scope 통제가 필요하다고 정의했고, `GRW-13`은 task type별 최소 컨텍스트를 고정했다. 하지만 실제 구현 단계에서 task type마다 어떤 읽기 범위와 쓰기 범위와 네트워크 접근과 권한 상승이 허용되는지는 아직 source of truth로 잠겨 있지 않다.

이 공백이 남아 있으면 같은 작업도 실행자마다 다른 도구를 사용하고, sibling 저장소를 불필요하게 읽거나, cross-repo 변경을 한 번에 시도하거나, 위험 명령과 권한 상승을 느슨하게 다루는 drift가 생길 수 있다. 후속 `GRW-15`, `GRW-16`, `GRW-17`, `GRW-18`, `GRW-S07`이 공유할 boundary 기준도 불안정해진다.

## Why Now

context pack registry는 "무엇을 읽을 수 있는가"를 잠갔지만, implementer 단계의 실제 통제력은 "무슨 도구를 어떤 범위로 쓸 수 있는가"가 정해져야 생긴다. `GRW-14`가 비어 있으면 같은 `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 작업도 read/write/network/escalation 판단이 매번 달라질 수 있다.

또한 cross-repo 작업을 workflow 문서 PR과 앱 코드 PR로 분리한다는 governance 규칙도, 각 task type의 write scope template와 금지 사례가 있어야 실제 작업 단위로 재현된다. pilot issue와 boundary skill pack에 앞서 도구 경계와 write scope 거버넌스를 먼저 고정해야 한다.

## Scope

- `docs/operations/`에 tool boundary matrix source of truth를 추가한다.
- task type별 read/write/network/escalation 허용 범위와 위험 명령 금지 규칙을 정의한다.
- write scope template와 representative allow/deny 사례를 문서화한다.
- 관련 architecture/operations 문서가 새 boundary policy를 참조하도록 갱신한다.
- `GRW-14` close-out을 기록한다.

## Non-scope

- 샌드박스 구현 자체 변경
- backend/frontend 앱 코드 변경
- verification contract registry 상세 설계
- boundary skill pack 작성

## Write Scope

- `docs/operations/`
- `docs/architecture/`
- `docs/exec-plans/`

## Outputs

- `docs/operations/tool-boundary-matrix.md`
- task type별 boundary rule과 write scope template
- operations/architecture의 boundary hook
- `GRW-14` 실행 기록

## Working Decisions

- boundary matrix의 canonical source는 `docs/operations/`에 둔다.
- task type 분류는 `GRW-13`의 `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 네 가지를 그대로 재사용한다.
- 프롬프트 제약보다 도구 경계를 우선하고, cross-repo 작업은 기본적으로 `workflow 문서 PR`과 `앱 코드 PR`로 분리한다.
- 위험 명령 금지와 escalation 기준은 "왜 필요한가", "허용 write scope 안인가", "더 좁은 대안이 없는가"를 함께 묻는 방식으로 정리한다.
- context pack selection만으로 tool/network/escalation 권한이 자동으로 열리지 않으며, 구현 전 boundary policy를 한 번 더 잠근다.

## Verification

- `sed -n '1,320p' docs/operations/tool-boundary-matrix.md`
  - 결과: boundary invariants, access class definitions, task matrix, dangerous command rules, escalation gate, write scope template, representative allow/deny 사례가 한 문서에 정리된 것을 확인했다.
- `rg -n "read boundary|write boundary|network|escalation|dangerous command|cross-repo|write scope template" docs/operations/tool-boundary-matrix.md docs/operations/workflow-governance.md docs/architecture/harness-system-map.md docs/architecture/context-pack-registry.md docs/operations/README.md`
  - 결과: 새 boundary policy의 핵심 용어와 governance/architecture hook이 함께 grep되는 것을 확인했다.
- 대표 task 4종에 대한 allow/deny 사례 수동 검토
  - 결과: `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 각각에 대해 허용/금지 사례를 표로 설명할 수 있음을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- `sed -n '1,80p' docs/operations/README.md` / `sed -n '34,60p' docs/operations/workflow-governance.md` / `sed -n '118,126p' docs/architecture/harness-system-map.md` / `sed -n '8,18p' docs/architecture/context-pack-registry.md`
  - 결과: operations index, governance hook, architecture-level boundary handoff, context-pack handoff 규칙이 새 문서를 올바르게 참조하는 것을 확인했다.
- GitHub Issue `#37` body render 확인
  - 결과: issue 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- task type별 read/write/network/escalation matrix
- 위험 명령 금지 규칙과 escalation 판단 기준
- write scope template와 representative allow/deny 사례
- architecture/governance 연결 결과
- GitHub Issue `#37` body 검증 결과

## Risks or Blockers

- sibling app 저장소의 실제 도구 제약은 repo-level guide에서 더 구체화될 수 있으므로, 이번 문서는 하네스 공통 기준을 먼저 고정하는 수준으로 유지해야 한다.
- verification contract registry가 아직 없으므로, network/escalation 규칙은 "검증 자체의 허용"보다 "해당 task type에서 필요한 access class" 중심으로 정리해야 한다.

## Next Preconditions

- `GRW-15`: verification contract registry와 repair loop 기준 정의
- `GRW-16`: dual-agent review policy 정의
- `GRW-17`: failure-to-guardrail feedback loop 정의
- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증
- `GRW-S07`: context-pack/boundary skill pack

## Docs Updated

- `docs/operations/tool-boundary-matrix.md`
- `docs/operations/README.md`
- `docs/operations/workflow-governance.md`
- `docs/architecture/harness-system-map.md`
- `docs/architecture/context-pack-registry.md`
- `docs/exec-plans/completed/2026-04-07-grw-14-tool-boundary-matrix-write-scope-governance.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 범위는 아니다. 대신 후속 `boundary-check` skill이 그대로 재사용할 수 있게 task type별 boundary rule, escalation 기준, write scope template를 source of truth로 먼저 고정한다.
