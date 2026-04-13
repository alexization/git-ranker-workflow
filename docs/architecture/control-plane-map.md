# Workflow Control Plane Map

`git-ranker-workflow`는 앱 저장소의 시스템 오브 레코드를 대체하지 않는다. 대신 cross-repo 작업을 시작하고 검증하고 증거를 정리하는 컨트롤 플레인 역할을 맡는다.

## 문서 배치 원칙

| 항목 | 공식 위치 | 설명 |
| --- | --- | --- |
| 컨트롤 플레인 구조 | `docs/architecture/` | 하네스 구성요소, 상태 전이, context pack 정의 |
| 작업 운영 규칙 | `docs/operations/` | Issue/PR 규칙, evidence, close-out 규칙 |
| 실행 순서와 backlog | `docs/product/` | 단계별 우선순위와 작업 카탈로그 |
| 작업 spec 문서 | `docs/specs/` | 현재 작업의 승인된 요구사항, 하위 작업, 완료 기록 |
| 앱별 canonical source | 각 앱 저장소 | `AGENTS.md`, `README.md`, 코드, 테스트, 저장소별 계약 문서 |

## 읽기 우선순위

1. 루트 인덱스: `AGENTS.md`, `SPECS.md`
2. 아키텍처 기준: `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`, `docs/architecture/context-pack-registry.md`
3. 공통 운영 규칙: `docs/operations/sdd-spec-policy.md`, `docs/operations/workflow-governance.md`
4. 실행 순서와 작업 카탈로그: `docs/product/*.md`
5. 해당 작업의 spec: `docs/specs/active/*.md` 또는 `docs/specs/completed/*.md`
6. 앱 저장소 엔트리 문서와 해당 코드/테스트

## 이관 원칙

- 현재 control plane source of truth는 `docs/architecture/`, `docs/operations/`, `docs/product/`, `docs/specs/`로 한정한다.
- readiness/history/generated/runtime 전용 자산은 현재 Harness 범위에 포함하지 않는다.
- 앱 동작 설명이 필요하면 workflow 복제 문서 대신 대상 저장소의 문서와 코드를 직접 읽는다.
- 새 문서가 생기면 이 구조를 깨지 않도록 가장 가까운 목적 디렉터리에 추가한다.
