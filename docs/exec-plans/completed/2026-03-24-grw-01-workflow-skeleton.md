# 2026-03-24-grw-01-workflow-skeleton

- Issue ID: `GRW-01`
- GitHub Issue: `#2`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-01-workflow-skeleton`
- Task Slug: `2026-03-24-grw-01-workflow-skeleton`

## Problem

workflow 저장소에는 계획, source of truth, evidence 위치를 설명하는 공식 구조가 없었다. 이 상태에서는 이후 작업이 로드맵 한 파일에 과도하게 의존하고, 새 Agent가 어디를 읽어야 하는지 빠르게 판단하기 어렵다.

## Why Now

`GRW-02`, `GRW-03`, `GRW-04`, `GRW-S01` 이후 작업은 모두 문서 구조와 exec plan 위치가 먼저 정해져 있어야 안정적으로 이어진다.

## Scope

- 루트 인덱스 문서 `AGENTS.md`, `PLANS.md` 추가
- `docs/` 하위 표준 디렉터리와 각 디렉터리 인덱스 문서 추가
- 공통 운영 규칙, 실행 순서, 작업 카탈로그를 새 구조로 1차 이관
- `.artifacts/` 보관 규칙 문서화와 `.gitignore` 반영
- `GRW-01` 완료 기록용 exec plan 작성

## Non-scope

- 실제 하네스 스크립트 작성
- backend 또는 client 저장소 코드 수정
- PromQL, LogQL, Playwright 세부 구현

## Write Scope

- 저장소 루트
- `docs/`
- `.gitignore`
- `.artifacts/.gitkeep`

## Outputs

- `AGENTS.md`
- `PLANS.md`
- `docs/README.md`
- `docs/architecture/control-plane-map.md`
- `docs/operations/workflow-governance.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/*`

## Verification

- `find docs -maxdepth 3 -type d | sort`
- `cat AGENTS.md`
- `cat PLANS.md`
- 원본 roadmap에서 새 문서 경로로 진입 가능하도록 링크 확인

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 남기지 않았다. 대신 검증 명령 결과와 변경된 source of truth 문서 경로를 남긴다.

## Risks

- 작업 카탈로그는 1차 정규화 버전이라 이후 각 영역 문서가 늘어나면 세부 링크를 더 쪼개야 한다.
- 일부 후속 Issue는 작업 착수 전에 도메인 문서를 더 상세화해야 한다.

## Next Preconditions

- `GRW-02`: `docs/quality-score/` 아래 readiness score 문서 추가
- `GRW-S01`: `skills/` 구조와 template 정의
- `GRW-03`, `GRW-04`: 도메인 및 화면 흐름 문서를 각 목적 디렉터리에 추가

## Docs Updated

- 루트 인덱스와 계획 규칙
- 컨트롤 플레인 구조 문서
- 공통 운영 규칙과 Definition of Done
- 실행 순서와 작업 카탈로그
- exec plan 구조와 완료 기록

## Skill Consideration

이번 Issue에서는 새 skill을 추가하지 않았다. 다만 issue를 exec plan으로 옮기는 반복 흐름은 `GRW-S01`, `GRW-S02`에서 skill 후보로 이어간다.
