# 2026-03-24-grw-02-readiness-baseline

- Issue ID: `GRW-02`
- GitHub Issue: `#4`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-02-readiness-baseline`
- Task Slug: `2026-03-24-grw-02-readiness-baseline`

## Problem

workflow 문서 구조는 만들어졌지만, `git-ranker-workflow`, `git-ranker`, `git-ranker-client`의 현재 readiness 수준을 같은 축으로 비교한 기준선 문서가 없다. 이 상태에서는 다음 하네스 작업의 우선순위와 선행조건을 근거 있게 정하기 어렵다.

## Why Now

`GRW-03`, `GRW-04`, `GRW-05`, `GRB-01`, `GRC-01`은 모두 현재 문서화 수준, 검증 루프, 계약 상태를 기준으로 작업 범위를 정해야 한다. 지금 기준선을 남겨야 후속 작업이 같은 판단 근거를 공유할 수 있다.

## Scope

- 세 저장소의 readiness 상태를 공통 기준으로 점검
- 문서화, 테스트, 정적 가드레일, API 계약, 운영 재현성, 관측 가능성, Agent 탐색 가능성 평가
- 실제 확인 명령과 확인 날짜를 포함한 quality score 기준선 문서 작성
- `GRW-02` exec plan에 점검 결과와 후속 전제조건 기록

## Non-scope

- backend 또는 client 코드 수정
- 새 하네스 스크립트, OpenAPI 산출물, Playwright 테스트 추가
- 점수 개선 작업 자체 수행

## Write Scope

- `docs/quality-score/`
- `docs/references/`
- `docs/exec-plans/`

## Outputs

- `docs/quality-score/agent-readiness-scorecard.md`
- `docs/quality-score/baseline-2026-03-24.md`
- `docs/references/2026-03-24-readiness-evidence.md`
- `GRW-02` 실행/완료 기록

## Verification

- `rg --files docs/quality-score docs/references docs/exec-plans`
- `./gradlew test jacocoTestReport`
- `./gradlew integrationTest`
- `npm run lint`
- `npx tsc --noEmit`
- `npm run build`
- `docker compose -f docker-compose.yml config`
- readiness 판단에 사용한 실제 명령 결과와 문서 대조
- 문서 링크와 상대경로 확인
- 결과 요약: backend unit test/JaCoCo 성공, backend integration test는 Testcontainers/Docker provider 단계에서 실패, client lint/typecheck는 통과, client build는 Google Fonts fetch와 deprecated middleware 경고로 실패

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 각 저장소에서 실제로 확인한 명령과 날짜, 핵심 결과를 [readiness evidence](../../references/2026-03-24-readiness-evidence.md)에 남겼다.

## Risks or Blockers

- `git-ranker`: integration test가 Docker/Testcontainers provider 단계에서 실패해 환경 문제와 코드 문제를 바로 분리하기 어렵다.
- `git-ranker-client`: build가 Google Fonts fetch에 의존해 네트워크 제약 환경에서 재현성이 낮다.
- `git-ranker-workflow`: control-plane 문서 skeleton은 생겼지만 runtime/query/freshness 자동화가 아직 없다.

## Next Preconditions

- `GRB-01`: backend OpenAPI 계약 생성 기반
- `GRB-02`: integration test preflight와 오류 메시지 개선
- `GRC-01`: client 계약 타입 단일화
- `GRC-03`: client build/runtime 재현성 개선
- `GRW-03`, `GRW-04`: workflow에 backend/frontend source of truth 본문 수집

## Docs Updated

- `docs/product/work-item-catalog.md`
- `docs/quality-score/README.md`
- `docs/quality-score/agent-readiness-scorecard.md`
- `docs/quality-score/baseline-2026-03-24.md`
- `docs/references/README.md`
- `docs/references/2026-03-24-readiness-evidence.md`
- `docs/exec-plans/completed/2026-03-24-grw-02-readiness-baseline.md`

## Skill Consideration

이번 Issue는 readiness 기준선 자체를 문서화하는 단계다. 점검 절차와 evidence 정리 패턴은 반복 가능성이 높으므로 이후 `GRW-S02` 또는 `GRW-07`에서 governance/check skill 후보로 검토한다.
