# PLANS.md

이 문서는 exec plan의 파일명 규칙과 상태 전이 규칙만 다룬다.

## 파일 위치

- 진행 중이거나 아직 끝나지 않은 작업 문서: [docs/exec-plans/active](docs/exec-plans/active/README.md)
- 완료된 작업 문서: [docs/exec-plans/completed](docs/exec-plans/completed/README.md)

## 파일명 규칙

- 기본 형식: `YYYY-MM-DD-<issue-id-lower>-<slug>.md`
- 예시: `2026-03-24-grw-01-workflow-skeleton.md`
- task slug 기본 형식: `YYYY-MM-DD-<issue-id-lower>-<slug>`
- 권장 브랜치명 형식: `feat/<issue-id-lower>-<slug>`

## 상태 규칙

plan 문서 본문 상단에는 최소한 아래 상태 중 하나를 명시한다.

- `Draft`: 문제 정의와 범위만 정리된 상태
- `Ready`: 선행조건과 write scope가 정리되어 바로 작업 가능한 상태
- `In Progress`: 작업이 진행 중인 상태
- `Blocked`: 선행조건 미충족이나 외부 이슈로 진행이 막힌 상태
- `Completed`: 검증과 문서 반영까지 끝난 상태

## 전이 규칙

- `Draft`, `Ready`, `In Progress`, `Blocked` 상태 문서는 `docs/exec-plans/active/`에 둔다.
- 작업이 끝나고 검증 결과까지 남기면 `Completed`로 갱신하고 `docs/exec-plans/completed/`로 옮긴다.
- 완료 문서는 삭제하지 않고 후속 작업의 전제조건과 판단 근거로 유지한다.
