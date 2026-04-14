# Context Pack Registry

이 문서는 승인된 spec에서 구현 컨텍스트로 넘어갈 때 무엇을 읽고 무엇을 읽지 말아야 하는지 task type별로 고정한다.

관련 intake 기준은 [../operations/request-routing-policy.md](../operations/request-routing-policy.md), spec 기준은 [../operations/sdd-spec-policy.md](../operations/sdd-spec-policy.md), 공통 운영 규칙은 [../operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.

## Registry Invariants

- 실행 가능한 작업은 항상 하나의 primary context pack만 가진다.
- 모든 pack은 공통 base context를 먼저 읽고, 그 다음 pack별 required docs를 연다.
- optional docs는 approved spec이나 hot file 탐색이 명시한 trigger가 있을 때만 연다.
- 다른 pack의 required docs까지 필요해지면 임의로 pack을 합치지 않고 spec의 subtask split 또는 tracking split로 되돌린다.
- repo entrypoint와 local skill discovery는 [repo-handoff-contract.md](repo-handoff-contract.md)의 순서를 따른다.
- target repo entrypoint 문서나 worktree가 없으면 `Context Ready`를 선언하지 않는다.

## Common Base Context

모든 pack은 아래 입력을 기본으로 공유한다.

| 입력 | 목적 |
| --- | --- |
| `AGENTS.md` | 시작 순서와 source of truth 확인 |
| `docs/README.md` | 현재 문서 구조 확인 |
| `SPECS.md` | spec 상태와 파일명 규칙 확인 |
| [../operations/sdd-spec-policy.md](../operations/sdd-spec-policy.md) | spec 작성과 승인 규칙 확인 |
| [../operations/workflow-governance.md](../operations/workflow-governance.md) | 운영 규칙 확인 |
| request record 또는 GitHub issue | 요청 배경 확인 |
| approved spec | 문제, 하위 작업, write scope, verification, tracking 결정 확인 |

## Task-To-Context Mapping

| Task type | Primary repo | Primary pack | 기본 목표 | 기본 금지 |
| --- | --- | --- | --- | --- |
| `workflow 문서 수정` | `git-ranker-workflow` | `workflow-docs` | harness 문서, template, skill, spec을 같은 용어로 수정 | sibling app repo code tree eager load |
| `backend 수정` | `git-ranker` | `backend-change` | backend 코드, 테스트, 설정을 한 저장소 범위에서 수정 | frontend 전체 pack eager load |
| `frontend 수정` | `git-ranker-client` | `frontend-change` | client route, UI, state, config를 한 저장소 범위에서 수정 | backend 내부 구현 eager load |
| `cross-repo planning` | `git-ranker-workflow` | `cross-repo-planning` | 여러 저장소 작업을 spec과 tracking 단위로 분해 | multi-repo code diff 동시 작성 |

## Pack Definitions

### `workflow-docs`

대상:

- `docs/`, `.github/`, `.codex/skills/`, `docs/specs/` 수정

Required docs:

- touched directory의 `README.md`
- approved spec에서 named input으로 적은 현재 source of truth
- stage semantics를 바꾸는 경우 [harness-system-map.md](harness-system-map.md)

Optional docs:

- directly linked adjacent docs
- 같은 surface를 다루는 현재 active spec 또는 가까운 completed spec

Forbidden context:

- sibling app repo code tree
- workflow에 앱 canonical source를 새로 복제하는 것

### `backend-change`

Required docs:

- target repo entrypoint 문서
- approved spec에 적힌 backend write scope
- current subtask가 직접 건드리는 build/test/contract entrypoint

Optional docs:

- verification contract나 tool boundary 확인이 필요할 때 관련 operations 문서
- directly impacted public contract doc

Forbidden context:

- frontend route/component/state 전체 pack
- workflow stable docs eager load

### `frontend-change`

Required docs:

- target repo entrypoint 문서
- approved spec에 적힌 frontend write scope
- current subtask가 직접 건드리는 `package.json`, `.env.example`, route entrypoint

Optional docs:

- verification contract나 tool boundary 확인이 필요할 때 관련 operations 문서
- directly impacted backend contract surface

Forbidden context:

- backend 내부 service/repository 구현 eager load
- workflow stable docs eager load

### `cross-repo-planning`

Required docs:

- [control-plane-map.md](control-plane-map.md)
- [harness-system-map.md](harness-system-map.md)
- approved spec
- 영향받는 각 저장소의 root entry 문서

Optional docs:

- repo별 verification entrypoint
- repo manifest 또는 contract surface

Forbidden context:

- 여러 저장소 code tree를 동시에 깊게 읽는 것
- app 구현 착수

## Hot File Exploration Rules

1. 먼저 approved spec의 active subtask와 write scope를 기준으로 `rg -n` 한다.
2. first ring은 entry handler, nearest config, nearest test만 연다.
3. import chain은 한 hop씩만 확장한다.
4. 다른 pack이 필요해지면 spec split 또는 task split로 되돌린다.
