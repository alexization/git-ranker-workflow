# Workflow Control Plane Map

`git-ranker-workflow`는 앱 저장소의 시스템 오브 레코드를 대체하지 않는다. 대신 cross-repo 작업을 시작하고 검증하고 증거를 정리하는 컨트롤 플레인 역할을 맡는다.

## 문서 배치 원칙

| 항목 | 공식 위치 | 설명 |
| --- | --- | --- |
| 작업 운영 규칙 | `docs/operations/` | Issue/PR 규칙, evidence, 아티팩트 보관 규칙 |
| 실행 순서와 backlog | `docs/product/` | 단계별 우선순위와 작업 카탈로그 |
| 실행 문서 | `docs/exec-plans/` | 현재 작업 계획과 완료 기록 |
| 도메인 규칙 | `docs/domain/` | 점수, 티어, API 계약, 흐름 설명 |
| 품질 기준선 | `docs/quality-score/` | readiness 점수와 상태표 |
| 생성 산출물 | `docs/generated/` | OpenAPI, export snapshot 같은 기계 생성 결과 |
| 참고 자료 | `docs/references/` | 외부 자료, 이관 전 역사 문서, 임시 참고 링크 |
| 작업 증거 | `.artifacts/<task-slug>/` | 브라우저, 로그, 메트릭, 요약 결과 |

## 읽기 우선순위

1. 루트 인덱스: `AGENTS.md`, `PLANS.md`
2. 아키텍처 기준: `docs/architecture/control-plane-map.md`, `docs/architecture/harness-system-map.md`
3. 공통 운영 규칙: `docs/operations/workflow-governance.md`
4. 실행 순서와 작업 카탈로그: `docs/product/*.md`
5. 해당 작업의 exec plan: `docs/exec-plans/active/*.md` 또는 `docs/exec-plans/completed/*.md`
6. 도메인/운영 상세 문서

## 이관 원칙

- `docs/references/git-ranker-harness-issue-pr-roadmap.md`는 초기 분해를 보관하는 역사 문서다.
- 현재 계획 source of truth는 `docs/product/`와 `docs/exec-plans/`에 둔다.
- 이후 작업 지시는 원칙적으로 `docs/product/`, `docs/operations/`, `docs/exec-plans/`에서 읽는다.
- 새 문서가 생기면 이 구조를 깨지 않도록 가장 가까운 목적 디렉터리에 추가한다.
