# 2026-03-25-grw-03-backend-domain-operations-docs

- Issue ID: `GRW-03`
- GitHub Issue: `#12`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-03-backend-domain-operations-docs`
- Task Slug: `2026-03-25-grw-03-backend-domain-operations-docs`

## Problem

`git-ranker` backend에는 점수 계산, 티어 판정, 랭킹 조회, 배지 서빙, 수동 갱신, 배치, GitHub API 장애 대응 규칙이 코드와 산출물에 흩어져 있다. 이 상태에서는 후속 harness 문서와 검증 루프가 같은 규칙을 참조하기 어렵고, Agent가 코드 탐색 없이 안전하게 행동하기도 어렵다.

## Why Now

`GRW-05`, `GRW-06`, `GRW-08`, `GRW-09`는 모두 backend의 현재 도메인/운영 규칙을 workflow source of truth로 참조해야 한다. `GRB-01`에서 OpenAPI 계약은 고정했지만, 배치/관측성/랭킹 규칙은 아직 workflow 문서에 정리되지 않았다.

## Scope

- backend 점수 계산 규칙 문서화
- 티어 판정과 랭킹 재산정 규칙 문서화
- 랭킹 조회와 배지 서빙 흐름 문서화
- 수동 갱신과 일일 배치 운영 흐름 문서화
- GitHub API 실패, retry, skip, rate-limit 정책 정리
- 주요 로그 이벤트, 필드, 메트릭 이름 정리
- `GRW-03` 실행/완료 기록 남기기

## Non-scope

- `git-ranker` backend 코드 수정
- 새 OpenAPI 생성, seed 데이터, Playwright 테스트 추가
- runtime, PromQL, LogQL 자동화 구현

## Write Scope

- `docs/domain/`
- `docs/operations/`
- `docs/exec-plans/`

## Outputs

- `docs/domain/scoring.md`
- `docs/domain/tiering.md`
- `docs/domain/ranking-read-flow.md`
- `docs/domain/badge-serving-flow.md`
- `docs/operations/manual-refresh-flow.md`
- `docs/operations/daily-batch-flow.md`
- `docs/operations/github-api-failure-policy.md`
- `docs/operations/observability-reference.md`
- `GRW-03` 실행/완료 기록

## Verification

- `find docs/domain docs/operations -maxdepth 1 -type f | sort`
- `rg -n "점수 계산|티어 판정|랭킹 조회|배지 서빙|수동 갱신|일일 배치|GitHub API Failure Policy|GitHub API 실패 정책|관측성" docs/domain docs/operations`
- 문서에 연결한 backend 코드 경로와 실제 구현 대조
- `perl -nle 'while(/\\]\\(([^)#]+)(?:#[^)]+)?\\)/g){print "$ARGV\\t$1"}' docs/domain/*.md docs/operations/*.md | while IFS=$'\t' read -r src target; do dir=$(dirname "$src"); if ! test -e "$dir/$target"; then printf 'missing %s -> %s\n' "$src" "$target"; fi; done`
- `gh issue create --title "[Task] GRW-03 백엔드 도메인/운영 문서를 workflow에 수집" ...`

결과 요약:

- `find docs/domain docs/operations -maxdepth 1 -type f | sort`: domain 5개, operations 6개 문서가 기대 경로에 생성된 것을 확인했다.
- `rg -n ... docs/domain docs/operations`: 점수, 티어, 랭킹, badge, 수동 갱신, batch, GitHub API 실패 정책, 관측성 문서가 모두 존재함을 확인했다.
- relative link check: `docs/domain/*.md`, `docs/operations/*.md` 안의 상대 링크에서 누락 경로가 없었다.
- 코드 대조: `git-ranker`의 controller/service/batch/logging/metrics/config 경로와 문서 규칙이 모순되지 않는지 교차 검토했다.
- GitHub flow: `gh issue create`로 `GRW-03` 이슈 `#12`를 생성했다.

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 backend 코드 경로, OpenAPI/README, 검증 명령 결과를 exec plan에 남긴다.

## Risks or Blockers

- backend 구현이 이후 빠르게 바뀌면 freshness가 떨어질 수 있다.
- 일일 batch의 `rankingRecalculationStep`은 DB 랭킹은 갱신하지만 ranking cache를 비우지 않는다. 따라서 랭킹 API는 최대 5분 stale window를 가질 수 있다.
- `GitHubRateLimitException`은 현재 `GITHUB_API_TIMEOUT` 에러 코드로 집계돼, 로그와 `errors_total` 해석이 어긋날 수 있다.
- 일부 운영 규칙은 OpenAPI가 아니라 코드와 설정에만 있으므로 문서가 drift 감지 장치 역할도 함께 해야 한다.

## Next Preconditions

- `GRW-05`: 표준 검증 런타임 설계 시 batch, cache, management port 규칙 참조
- `GRW-06`: 로그/메트릭 evidence query 설계 시 event/metric 이름 참조
- `GRW-08`: badge harness 계획 수립 시 badge 응답/캐시 규칙 참조
- `GRW-09`: batch harness 계획 수립 시 retry/skip/failure 정책 참조

## Docs Updated

- `docs/domain/README.md`
- `docs/domain/scoring.md`
- `docs/domain/tiering.md`
- `docs/domain/ranking-read-flow.md`
- `docs/domain/badge-serving-flow.md`
- `docs/operations/README.md`
- `docs/operations/manual-refresh-flow.md`
- `docs/operations/daily-batch-flow.md`
- `docs/operations/github-api-failure-policy.md`
- `docs/operations/observability-reference.md`
- `docs/exec-plans/completed/2026-03-25-grw-03-backend-domain-operations-docs.md`

## Skill Consideration

이번 Issue는 source of truth 본문을 수집하는 단계다. 아직 skill을 만들 범위는 아니지만, `GRW-S02`, `GRW-S03`, `GRW-S04`에서 재사용할 domain/ops 규칙의 기준 입력을 만든다.
