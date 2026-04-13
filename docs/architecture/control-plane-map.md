# Workflow Control Plane Map

`git-ranker-workflow`는 앱 저장소의 시스템 오브 레코드를 대체하지 않는다. 대신 cross-repo 작업을 시작하고 검증하고 증거를 정리하는 컨트롤 플레인 역할을 맡는다.

## 문서 배치 원칙

| 항목 | 공식 위치 | 설명 |
| --- | --- | --- |
| 컨트롤 플레인 구조 | `docs/architecture/` | 하네스 구성요소, 상태 전이, context pack 정의 |
| 작업 운영 규칙 | `docs/operations/` | Issue/PR 규칙, evidence, close-out 규칙 |
| 작업 spec 문서와 requirement queue | `docs/specs/` | 현재 작업의 draft/approved requirement, 하위 작업, 완료 기록 |
| 앱별 canonical source | 각 앱 저장소 | `AGENTS.md`, `README.md`, 코드, 테스트, 저장소별 계약 문서 |

## Federated Ownership Matrix

| Surface | Workflow control plane owns | Repo-local app owns | Workflow must not own |
| --- | --- | --- | --- |
| planning and sequencing | cross-repo request routing, spec, context pack, verification semantics, evidence, publish choreography | repo 안에서의 concrete implementation sequencing | repo-local implementation playbook를 stable workflow policy로 다시 쓰는 것 |
| runtime entrypoint and knowledge | target repo discovery order, handoff minimum, 다음 source를 고르는 기준 | target repo `AGENTS.md`, `README.md`, 코드, 테스트, repo-local contract docs | app 동작 설명, troubleshooting, config 해석을 workflow 문서로 복제하는 것 |
| verification and guardrail baseline | contract profile vocabulary, evidence minimum, publish/review stage rule | concrete command surface, CI wiring, bootstrap, env preconditions, static analysis config | app verification command/config를 workflow-owned canonical text로 유지하는 것 |
| skill layer | workflow stage procedure, orchestration handoff wording | repo-local bootstrap and implementation skill | backend/frontend implementation knowledge를 workflow-local skill에 축적하는 것 |

## 읽기 우선순위

1. 루트 인덱스: `AGENTS.md`, `SPECS.md`
2. 아키텍처 기준: `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`, `docs/architecture/context-pack-registry.md`
3. 공통 운영 규칙: `docs/operations/sdd-spec-policy.md`, `docs/operations/workflow-governance.md`
4. 해당 작업의 draft/approved spec: `docs/specs/active/*.md`
5. 완료 기록이 필요할 때의 historical spec: `docs/specs/completed/*.md`
6. 앱 저장소 엔트리 문서와 해당 코드/테스트

## 이관 원칙

- 현재 control plane source of truth는 `docs/architecture/`, `docs/operations/`, `docs/specs/`로 한정한다.
- readiness/history/generated/runtime 전용 자산은 현재 Harness 범위에 포함하지 않는다.
- 별도 roadmap/catalog 문서는 유지하지 않고, remaining work는 active draft spec과 그 prerequisite로 표현한다.
- 앱 동작 설명이 필요하면 workflow 복제 문서 대신 대상 저장소의 문서와 코드를 직접 읽는다.
- 새 문서가 생기면 이 구조를 깨지 않도록 가장 가까운 목적 디렉터리에 추가한다.

## No-Duplication Rule

- sibling app repo에 이미 canonical source가 있으면 workflow는 link, handoff boundary, remaining-work spec만 남긴다.
- workflow stable docs는 "언제 어디로 넘기는지"까지만 설명하고, command, config path, feature behavior 같은 repo-local detail을 canonical text로 다시 적지 않는다.

## Migration Exit Criteria

- workflow stable docs가 app knowledge를 복제하지 않고 repo-local canonical source를 가리킨다.
- workflow-local skill이 thin-layer로 남아 stage procedure와 handoff만 다룬다.
- repo-specific verification, bootstrap, implementation detail은 sibling repo 또는 follow-up spec이 소유한다.
