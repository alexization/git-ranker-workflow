# Exec Plans

이 디렉터리는 Issue 단위 실행 문서를 관리한다.

## 목적

- 현재 작업의 범위와 비범위를 고정한다
- 검증 근거와 결과를 남긴다
- 후속 작업의 전제조건을 기록한다
- completed plan은 historical close-out record로 남기되 full transcript처럼 불리지 않게 유지한다

## 디렉터리 규칙

- [active](active/README.md): 아직 끝나지 않은 작업 문서
- [completed](completed/README.md): 완료된 작업 문서

## Active Plan 권장 섹션

- Task metadata
- Problem
- Why now
- Scope
- Non-scope
- Write scope
- Outputs
- Verification
- Risks or blockers
- Next preconditions

## Completed Plan 기본 섹션

- Task metadata
- Problem 또는 effective change summary
- Why now 필요 시
- Scope 또는 final change summary
- Write scope
- Outputs
- Verification Summary 또는 Verification Report
- Risks or blockers
- Docs updated

## Optional Close-out 섹션

- Evidence
- Context Selection Summary
- Boundary Check Summary
- Independent Review
- Feedback / Guardrail
- Close-out reconciliation
- Skill consideration
- Next preconditions

## 피해야 할 것

- 같은 사실을 여러 섹션에 반복하는 것
- raw log, full command inventory, render check chronology를 불필요하게 inline dump하는 것
- 실제로 수행하지 않은 절차를 형식적으로 섹션만 남기는 것

## 파일명

- `YYYY-MM-DD-<issue-id-lower>-<slug>.md`
- 예시: `2026-03-24-grw-01-workflow-skeleton.md`
