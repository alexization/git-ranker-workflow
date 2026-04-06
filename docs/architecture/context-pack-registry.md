# Context Pack Registry

이 문서는 [harness-system-map.md](harness-system-map.md)의 `Context Pack` 단계를 실제 registry 형태로 고정한다. 목적은 `Planned` 상태의 작업이 `Context Ready`로 넘어가기 전에 "무엇을 읽고 무엇을 읽지 말아야 하는가"를 task type별로 잠그는 것이다.

관련 intake 기준은 [../operations/request-routing-policy.md](../operations/request-routing-policy.md), 공통 운영 규칙은 [../operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.

## Registry Invariants

- 실행 가능한 작업은 항상 하나의 primary context pack만 가진다.
- 모든 pack은 공통 base context를 먼저 읽고, 그 다음 pack별 required docs를 연다.
- optional docs는 issue, exec plan, hot file 탐색이 명시한 trigger가 있을 때만 연다.
- 다른 pack의 required docs까지 필요해지면 임의로 pack을 합치지 않고 issue를 쪼개거나 exec plan을 갱신한다.
- `docs/references/`와 generated snapshot은 default context가 아니다. 현재 source of truth가 부족하거나 생성 계약을 확인할 때만 연다.
- target repo의 entrypoint 문서나 worktree가 없으면 `Context Ready`를 선언하지 않는다. 이 경우 worktree 준비 또는 `Blocked` 판단이 먼저다.

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

## Surface Cue Selector

backend/frontend pack은 issue에 적힌 surface cue에 따라 workflow 저장소의 domain/operations 문서를 추가한다. 아래 표는 eager load가 아니라 "어떤 cue가 보일 때 어떤 문서를 연다"는 selector다.

| Surface cue | 우선 열 문서 | 보조 문서 |
| --- | --- | --- |
| ranking API, pagination, tier filter, ranking page | [../domain/ranking-read-flow.md](../domain/ranking-read-flow.md) | [frontend-route-map.md](frontend-route-map.md), [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md) |
| user profile, user detail modal, auth callback, locale route | [frontend-route-map.md](frontend-route-map.md) | [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md), [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md) |
| score, refresh, batch score rebuild, activity stats | [../domain/scoring.md](../domain/scoring.md) | [../domain/tiering.md](../domain/tiering.md), [../operations/observability-reference.md](../operations/observability-reference.md) |
| tier, percentile, rank recomputation, ranking recalculation | [../domain/tiering.md](../domain/tiering.md) | [../domain/ranking-read-flow.md](../domain/ranking-read-flow.md), [../operations/observability-reference.md](../operations/observability-reference.md) |
| badge, SVG, cache header, preview badge | [../domain/badge-serving-flow.md](../domain/badge-serving-flow.md) | [../operations/observability-reference.md](../operations/observability-reference.md) |
| env, CSP, analytics, image host, frontend build/runtime | [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md) | [frontend-route-map.md](frontend-route-map.md) |
| logs, metrics, actuator, Prometheus, Loki, evidence query | [../operations/observability-reference.md](../operations/observability-reference.md) | [../operations/workflow-verification-runtime.md](../operations/workflow-verification-runtime.md) |
| OpenAPI, generated schema, export snapshot | [../generated/README.md](../generated/README.md) | 생성 명령을 설명하는 source 문서와 active exec plan |

하나의 cue에 해당하는 문서를 모두 여는 것이 기본은 아니다. primary pack이 요구하는 최소 문서 한두 개를 먼저 열고, 남는 ambiguity가 있을 때만 보조 문서를 추가한다.

## Task-To-Context Mapping

| Task type | Primary repo | Primary pack | 기본 목표 | 기본 금지 |
| --- | --- | --- | --- | --- |
| `workflow 문서 수정` | `git-ranker-workflow` | `workflow-docs` | harness 문서, template, skill, exec plan을 같은 용어와 규칙으로 수정 | sibling app repo code tree, 역사 문서 eager load |
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
- 배경 비교가 꼭 필요할 때만 `docs/references/*`

Forbidden context:

- sibling `git-ranker`, `git-ranker-client` 코드 트리를 "혹시 필요할까" 수준으로 먼저 여는 것
- 현재 issue와 무관한 domain/runtime 문서를 전부 읽는 것
- generated 산출물을 canonical policy처럼 취급하는 것

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
- `Surface Cue Selector`에서 현재 issue와 가장 직접적으로 맞는 workflow 문서 최소 1개

Optional docs:

- public contract를 바꾸는 경우 consumer-facing workflow 문서 1개
- observability/runtime evidence가 필요한 경우 [../operations/observability-reference.md](../operations/observability-reference.md) 또는 [../operations/workflow-verification-runtime.md](../operations/workflow-verification-runtime.md)
- 같은 surface를 다룬 최근 completed exec plan

Forbidden context:

- frontend route/component/state 전체 pack
- backend와 무관한 workflow policy 문서 전체 eager load
- `docs/references/*`를 현재 동작 spec처럼 사용하는 것

Hot file exploration:

1. issue에 적힌 endpoint, class, package, batch step, env var로 target repo를 `rg -n` 한다.
2. entry handler, service, nearest test를 first ring으로 연다.
3. 필요한 경우 repository, DTO, config처럼 인접한 한 단계만 확장한다.
4. consumer 영향이 보이면 frontend pack 전체를 열지 말고 contract surface 문서만 추가한다.

### `frontend-change`

대상:

- `git-ranker-client`의 route, UI, state, config, build/runtime 설정 수정

Required docs:

- target repo entrypoint 문서: `AGENTS.md`가 있으면 우선, 없으면 `README.md`
- active exec plan과 issue에 적힌 frontend write scope
- `Surface Cue Selector`에서 현재 issue와 가장 직접적으로 맞는 workflow 문서 최소 1개

Optional docs:

- route-level 행동을 다루면 [frontend-route-map.md](frontend-route-map.md)와 [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md) 중 필요한 문서만 추가
- backend contract를 소비하는 UI면 [../domain/ranking-read-flow.md](../domain/ranking-read-flow.md) 또는 generated contract 문서
- runtime/env 이슈면 [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md)

Forbidden context:

- backend 내부 service/repository 구현까지 한꺼번에 읽는 것
- workflow 문서 트리를 근거 없이 전부 여는 것
- duplicate/legacy route를 canonical route보다 먼저 근거로 삼는 것

Hot file exploration:

1. issue의 route segment, component 이름, hook 이름, env var로 target repo를 `rg -n` 한다.
2. page/layout 또는 entry component, data hook/service, nearest test를 first ring으로 연다.
3. import chain은 한 hop씩만 확장한다.
4. backend 동작을 알아야 하면 backend 내부 구현 대신 workflow의 contract/domain 문서를 먼저 추가한다.

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

- repo별 write scope를 좁히기 위한 domain/runtime 문서
- background 비교가 필요할 때만 `docs/references/*`
- machine-generated contract가 canonical input일 때만 [../generated/README.md](../generated/README.md)와 해당 산출물

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
| "`GRW-13`처럼 하네스 정책 문서를 작성한다" | `workflow-docs` | `AGENTS.md`, `docs/README.md`, `PLANS.md`, [../operations/workflow-governance.md](../operations/workflow-governance.md), active exec plan, 관련 product/precedent docs | [harness-system-map.md](harness-system-map.md), 직접 링크된 adjacent docs | sibling app code tree |
| "ranking API tier filter 버그를 backend에서 수정한다" | `backend-change` | target repo entry docs, active exec plan, [../domain/ranking-read-flow.md](../domain/ranking-read-flow.md) | [../domain/tiering.md](../domain/tiering.md), [../operations/observability-reference.md](../operations/observability-reference.md) | frontend route/component tree |
| "ranking page pagination 동작을 frontend에서 수정한다" | `frontend-change` | target repo entry docs, active exec plan, [frontend-route-map.md](frontend-route-map.md) 또는 [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md) 중 직접적인 문서 1개 | [../domain/ranking-read-flow.md](../domain/ranking-read-flow.md), [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md) | backend service/repository internals |
| "backend와 client 사이 API contract rename 작업을 먼저 분해한다" | `cross-repo-planning` | [control-plane-map.md](control-plane-map.md), [harness-system-map.md](harness-system-map.md), active exec plan, 두 저장소 entry docs | [../generated/README.md](../generated/README.md), 관련 domain 문서 | 두 저장소 code tree의 광범위한 동시 탐색 |

이 시뮬레이션에서 핵심은 "필수 문서 전체를 한 번에 최대화하지 않는다"는 점이다. 필요한 판단이 남아 있으면 selector와 hot file rule을 따라 한 단계씩만 확장한다.
