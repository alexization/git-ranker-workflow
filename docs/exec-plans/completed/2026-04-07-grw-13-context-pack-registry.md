# 2026-04-07-grw-13-context-pack-registry

- Issue ID: `GRW-13`
- GitHub Issue: `#35`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-13-context-pack-registry`
- Task Slug: `2026-04-07-grw-13-context-pack-registry`

## Problem

`GRW-11`은 `Context Pack` 단계를 canonical state machine에 포함했고, `GRW-12`는 어떤 요청이 실행 가능한 작업인지까지 고정했다. 하지만 실제로 `Planned` 상태에서 `Context Ready`로 넘어갈 때 task type마다 어떤 문서를 필수로 읽고, 어떤 문서는 선택적으로만 열고, 어떤 컨텍스트는 금지해야 하는지는 아직 source of truth로 잠겨 있지 않다.

이 공백이 남아 있으면 같은 종류의 작업도 작업자마다 서로 다른 문서 세트를 읽게 되고, 한쪽은 과도한 컨텍스트를 한꺼번에 열어 scope drift가 생기고 다른 한쪽은 필요한 domain/runtime 문서를 놓쳐 잘못된 결정을 내릴 수 있다. 후속 tool boundary, pilot, skill pack도 같은 입력 기준을 공유할 수 없게 된다.

## Why Now

context pack registry는 하네스에서 `exec plan` 다음 단계의 실제 통제 지점이다. request routing만으로는 "작업을 시작해도 된다"까지만 고정되고, implementer가 무엇을 읽고 무엇을 읽지 말아야 하는지는 별도 규칙이 있어야 한다.

또한 `backend 수정`, `frontend 수정`, `workflow 문서 수정`, `cross-repo planning`은 서로 다른 문서 지형과 실패 모드를 가진다. `GRW-13`이 먼저 고정돼야 `GRW-14`, `GRW-18`, `GRW-S07`이 같은 context selection 기준 위에서 이어질 수 있다.

## Scope

- `docs/architecture/`에 context pack registry와 task-to-context mapping을 정의한다.
- 대표 task type별 required docs, optional docs, forbidden context, hot file 탐색 기준을 문서화한다.
- architecture 인덱스와 governance가 새 registry를 참조하도록 갱신한다.
- 대표 task 시뮬레이션 기준을 남기고 `GRW-13` close-out을 기록한다.

## Non-scope

- 자동 context loader 구현
- tool sandbox 또는 runtime 구현 변경
- backend/frontend 앱 코드 변경
- context-pack skill 작성

## Write Scope

- `docs/architecture/`
- `docs/operations/`
- `docs/exec-plans/`

## Outputs

- context pack registry source of truth
- task-to-context mapping 표
- context selection governance hook
- `GRW-13` 실행 기록

## Working Decisions

- context pack registry의 canonical source는 `docs/architecture/`에 둔다.
- task type 기본 분류는 `backend 수정`, `frontend 수정`, `workflow 문서 수정`, `cross-repo planning` 네 가지로 고정한다.
- required docs는 최소 공통 입력만 포함하고, domain/runtime 문서는 optional 또는 hot file 탐색 규칙으로 점진적으로 연다.
- cross-repo planning pack은 여러 저장소 문서를 읽을 수 있지만, 앱 코드 변경 권한을 바로 열지 않는다.

## Verification

- `sed -n '1,320p' docs/architecture/context-pack-registry.md`
  - 결과: registry 목적, common base context, surface cue selector, task-to-context mapping, pack definitions, representative simulation이 한 문서에 정리된 것을 확인했다.
- `rg -n "backend 수정|frontend 수정|workflow 문서 수정|cross-repo planning|required docs|optional docs|forbidden context|hot file" docs/architecture/context-pack-registry.md docs/operations/workflow-governance.md docs/architecture/README.md docs/architecture/harness-system-map.md`
  - 결과: 새 registry의 네 가지 task type, governance의 context pack 규칙, architecture 인덱스, system map 연결이 함께 grep되는 것을 확인했다.
- `sed -n '1,120p' docs/architecture/README.md`
  - 결과: architecture 인덱스가 `context-pack-registry.md`를 현재 기준 문서로 가리키는 것을 확인했다.
- `sed -n '18,40p' docs/architecture/control-plane-map.md`
  - 결과: 읽기 우선순위에 `docs/architecture/context-pack-registry.md`가 추가되어 architecture 기준 문서 목록에 포함된 것을 확인했다.
- `sed -n '26,48p' docs/operations/workflow-governance.md`
  - 결과: active exec plan 이후 primary context pack을 고르고 required/optional/forbidden 규칙을 따른다는 governance hook이 반영된 것을 확인했다.
- `gh issue view --repo alexization/git-ranker-workflow 35 --json body`
  - 결과: GitHub Issue `#35` 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- 대표 task 4종 수동 시뮬레이션
  - 결과: `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 각각에 대해 먼저 열 문서, 나중에 여는 문서, 열지 않는 문서를 한 표에서 구분할 수 있어 과도한 eager load 없이 context selection이 가능함을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- `docs/architecture/context-pack-registry.md`의 common base context, surface cue selector, task-to-context mapping, representative simulation
- `docs/operations/workflow-governance.md`의 context pack 규칙 section
- `docs/architecture/README.md`, `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`의 연결 결과
- GitHub Issue `#35` body 검증 결과
- verification 명령 결과 요약

## Risks or Blockers

- sibling app 저장소가 현재 workspace에 없을 수 있으므로, backend/frontend pack은 workflow 저장소가 소유하는 문서와 일반 탐색 규칙 중심으로 먼저 고정해야 한다.
- verification contract registry가 아직 없으므로, 이번 작업은 context selection까지만 다루고 검증 명령의 canonical source는 후속 작업으로 남긴다.
- target repo entry 문서 구성은 저장소별로 다를 수 있으므로, repo-specific hot file 예시는 후속 `context-pack-selection` skill이나 repo-level guide에서 더 구체화할 여지가 있다.

## Next Preconditions

- `GRW-14`: tool boundary matrix와 write scope 거버넌스 정의
- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증
- `GRW-S07`: context-pack/boundary skill pack

## Docs Updated

- `docs/architecture/context-pack-registry.md`
- `docs/architecture/README.md`
- `docs/architecture/control-plane-map.md`
- `docs/architecture/harness-system-map.md`
- `docs/operations/workflow-governance.md`
- `docs/exec-plans/completed/2026-04-07-grw-13-context-pack-registry.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 범위는 아니다. 대신 후속 `context-pack-selection`, `boundary-check` skill이 그대로 재사용할 수 있게 task type별 최소 컨텍스트와 금지 컨텍스트 규칙을 source of truth로 먼저 고정한다.
