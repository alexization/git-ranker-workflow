# Context Pack Registry

이 문서는 [harness-system-map.md](harness-system-map.md)의 `Context Pack` 단계를 실제 registry 형태로 고정한다. 목적은 `Planned` 상태의 작업이 `Context Ready`로 넘어가기 전에 "무엇을 읽고 무엇을 읽지 말아야 하는가"를 task type별로 잠그는 것이다.

관련 intake 기준은 [../operations/request-routing-policy.md](../operations/request-routing-policy.md), 공통 운영 규칙은 [../operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.

## Registry Invariants

- 실행 가능한 작업은 항상 하나의 primary context pack만 가진다.
- 모든 pack은 공통 base context를 먼저 읽고, 그 다음 pack별 required docs를 연다.
- optional docs는 issue, exec plan, hot file 탐색이 명시한 trigger가 있을 때만 연다.
- 다른 pack의 required docs까지 필요해지면 임의로 pack을 합치지 않고 issue를 쪼개거나 exec plan을 갱신한다.
- workflow 저장소는 현재 Harness control plane 문서만 유지한다. 앱 동작과 계약의 canonical source는 각 앱 저장소의 엔트리 문서와 코드/테스트다.
- target repo의 entrypoint 문서나 worktree가 없으면 `Context Ready`를 선언하지 않는다. 이 경우 worktree 준비 또는 `Blocked` 판단이 먼저다.
- primary repo, task type, write scope가 하나로 잠기지 않으면 `request-routing` 또는 planning으로 되돌린다.

## Common Base Context

모든 pack은 아래 입력을 기본으로 공유한다.

| 입력 | 목적 |
| --- | --- |
| `AGENTS.md` | 시작 순서, source of truth 우선순위, 저장소 운영 규칙 확인 |
| `docs/README.md` | 현재 문서 구조와 목적 디렉터리 확인 |
| `PLANS.md` | exec plan 상태와 파일명 규칙 확인 |
| [../operations/workflow-governance.md](../operations/workflow-governance.md) | issue/PR, evidence, write scope, close-out 규칙 확인 |
| request record 또는 GitHub issue | 이번 작업의 문제 정의, 범위, 완료 조건 확인 |
| active exec plan | 이번 작업의 scope, non-scope, write scope, verification contract 확인 |

추가 규칙:

- primary repo가 `git-ranker-workflow`가 아니면 target repo의 root entry 문서를 먼저 연다. 기본값은 `AGENTS.md`가 있으면 그것을, 없으면 `README.md`를 entrypoint로 사용한다.
- 현재 issue나 exec plan이 이미 특정 source of truth를 named input으로 적었다면, 해당 문서는 base context 다음 순서로 연다.

## Task-To-Context Mapping

| Task type | Primary repo | Primary pack | 기본 목표 | 기본 금지 |
| --- | --- | --- | --- | --- |
| `workflow 문서 수정` | `git-ranker-workflow` | `workflow-docs` | harness 문서, template, skill, exec plan을 같은 용어와 규칙으로 수정 | sibling app repo code tree, retired 문서군 eager load |
| `backend 수정` | `git-ranker` | `backend-change` | backend 코드, 테스트, 스크립트, 설정을 한 저장소 범위 안에서 수정 | frontend 전체 pack, unrelated workflow docs eager load |
| `frontend 수정` | `git-ranker-client` | `frontend-change` | client route, UI, state, config를 한 저장소 범위 안에서 수정 | backend 내부 구현 탐색, unrelated workflow docs eager load |
| `cross-repo planning` | `git-ranker-workflow` | `cross-repo-planning` | 여러 저장소 작업을 issue/PR 단위로 분해하고 contract만 정렬 | app code 구현 착수, multi-repo code diff 동시 작성 |

위 분류가 하나로 고정되지 않으면 request routing 단계로 되돌아가 issue를 더 좁혀야 한다.

## Pack Definitions

### `workflow-docs`

대상:

- `docs/`, `.github/`, `.codex/skills/`, `docs/exec-plans/` 수정
- 하네스 정책, template, planning, index 정렬

Required docs:

- touched directory의 `README.md` 또는 가장 가까운 index 문서
- issue 또는 exec plan이 직접 named input으로 적은 현재 source of truth 문서
- 같은 주제의 최근 completed exec plan이 있으면 그 close-out

Optional docs:

- primary 문서에서 직접 링크한 adjacent source of truth
- stage semantics를 바꾸는 경우 [harness-system-map.md](harness-system-map.md)

Forbidden context:

- sibling `git-ranker`, `git-ranker-client` 코드 트리를 "혹시 필요할까" 수준으로 먼저 여는 것
- 현재 issue와 무관한 앱 동작 설명이나 운영 세부사항을 workflow에 새로 복제하는 것
- 현재 control plane 범위 밖으로 정리된 retired 디렉터리를 근거로 삼는 것

Hot file exploration:

1. issue noun과 write scope를 기준으로 `docs/`, `.github/`, `.codex/skills/` 안에서 `rg -n`으로 시작한다.
2. target 문서 하나와 직접 링크된 이웃 문서만 먼저 연다.
3. app code를 읽어야만 정책을 결정할 수 있다면 `workflow-docs` pack이 아니라 `cross-repo-planning` 또는 repo-specific pack으로 되돌아간다.

### `backend-change`

대상:

- `git-ranker`의 코드, 테스트, 설정, verification entrypoint 수정

Required docs:

- target repo entrypoint 문서: `AGENTS.md`가 있으면 우선, 없으면 `README.md`
- active exec plan과 issue에 적힌 backend write scope
- target repo의 build/test/contract entrypoint 중 현재 issue가 직접 건드리는 문서나 파일

Optional docs:

- verification, write scope, repair semantics를 다시 확인해야 하면 [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md) 또는 [../operations/tool-boundary-matrix.md](../operations/tool-boundary-matrix.md)
- 직접 영향 받는 public contract 설명이 target repo에 따로 있으면 해당 문서 1개
- 같은 surface를 다룬 최근 completed exec plan

Forbidden context:

- frontend route/component/state 전체 pack
- backend와 무관한 workflow policy 문서 전체 eager load
- workflow 저장소 안에 앱 동작 복제 문서를 새 canonical source처럼 취급하는 것

Hot file exploration:

1. issue에 적힌 endpoint, class, package, env var, test 이름으로 target repo를 `rg -n` 한다.
2. entry handler, service, nearest test를 first ring으로 연다.
3. 필요한 경우 repository, DTO, config처럼 인접한 한 단계만 확장한다.
4. consumer 영향이 보이면 workflow 복제 문서를 만들기보다 target repo contract와 exec plan evidence를 먼저 갱신한다.

### `frontend-change`

대상:

- `git-ranker-client`의 route, UI, state, config, build/runtime 설정 수정

Required docs:

- target repo entrypoint 문서: `AGENTS.md`가 있으면 우선, 없으면 `README.md`
- active exec plan과 issue에 적힌 frontend write scope
- target repo의 `package.json`, `README.md`, `.env.example`처럼 현재 issue가 직접 의존하는 entrypoint 문서나 파일

Optional docs:

- verification, write scope, repair semantics를 다시 확인해야 하면 [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md) 또는 [../operations/tool-boundary-matrix.md](../operations/tool-boundary-matrix.md)
- 직접 영향 받는 backend contract를 target repo가 소비하는 위치
- 같은 surface를 다룬 최근 completed exec plan

Forbidden context:

- backend 내부 service/repository 구현까지 한꺼번에 읽는 것
- workflow 문서 트리를 근거 없이 전부 여는 것
- workflow 저장소 안에 frontend 동작 복제 문서를 새 canonical source처럼 만드는 것

Hot file exploration:

1. issue의 route segment, component 이름, hook 이름, env var로 target repo를 `rg -n` 한다.
2. page/layout 또는 entry component, data hook/service, nearest test를 first ring으로 연다.
3. import chain은 한 hop씩만 확장한다.
4. backend 동작을 알아야 하면 backend 내부 구현보다 backend repo의 공식 contract surface를 먼저 추가한다.

### `cross-repo-planning`

대상:

- 여러 저장소의 contract, template, workflow, 분해 계획을 정렬하는 planning 작업
- 아직 어느 저장소가 first implementation repo인지 고정되지 않은 작업

Required docs:

- [control-plane-map.md](control-plane-map.md)
- [harness-system-map.md](harness-system-map.md)
- 관련 product 문서와 active exec plan
- 영향받는 각 저장소의 root entry 문서

Optional docs:

- repo별 write scope를 좁히기 위한 manifest, verification entrypoint, 공식 contract 문서
- verification/reporting semantics를 다시 확인해야 하면 [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md)

Forbidden context:

- 여러 저장소 code tree를 동시에 깊게 여는 것
- issue를 나누기 전에 app code 구현을 시작하는 것
- workflow 문서 PR과 앱 코드 PR을 하나의 scope로 묶는 것

Hot file exploration:

1. 먼저 impacted repo 목록, canonical source, split 기준을 문서로 고정한다.
2. 그 다음 repo별 첫 issue에 필요한 문서만 한 저장소씩 연다.
3. code-level 조사보다 `문제 정의`, `scope`, `write scope`, `verification`을 먼저 잠근다.

## Representative Selection Simulation

| 대표 요청 | 선택 pack | 먼저 열 문서 | 나중에 여는 문서 | 열지 않는 문서 |
| --- | --- | --- | --- | --- |
| "하네스 정책 문서를 정리한다" | `workflow-docs` | `AGENTS.md`, `docs/README.md`, `PLANS.md`, [../operations/workflow-governance.md](../operations/workflow-governance.md), active exec plan, 관련 product/precedent docs | [harness-system-map.md](harness-system-map.md), 직접 링크된 adjacent docs | sibling app code tree |
| "backend verification command를 정리한다" | `backend-change` | target repo entry docs, active exec plan, backend build/test entrypoint | [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md), target repo contract 문서 | frontend route/component tree |
| "frontend build contract를 정리한다" | `frontend-change` | target repo entry docs, active exec plan, `package.json` 또는 `.env.example` | [../operations/verification-contract-registry.md](../operations/verification-contract-registry.md), nearest test or config | backend service/repository internals |
| "backend와 client 사이 작업을 먼저 분해한다" | `cross-repo-planning` | [control-plane-map.md](control-plane-map.md), [harness-system-map.md](harness-system-map.md), active exec plan, 두 저장소 entry docs | verification entrypoint 문서, repo manifest | 두 저장소 code tree의 광범위한 동시 탐색 |

이 시뮬레이션에서 핵심은 "필수 문서 전체를 한 번에 최대화하지 않는다"는 점이다. 필요한 판단이 남아 있으면 hot file rule을 따라 한 단계씩만 확장한다.
