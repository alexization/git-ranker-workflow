# GitHub API Failure Policy

Git Ranker backend는 GitHub GraphQL 호출을 배치와 사용자 요청 양쪽에서 사용한다. 이 문서는 토큰 선택, rate-limit 보호선, 예외 분류, retry/skip 정책을 정리한다.

## 토큰 선택 규칙

토큰 풀 구현:

- [GitHubTokenPool.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/token/GitHubTokenPool.java)

선택 방식:

1. `github.api.tokens`를 comma-separated list로 읽는다.
2. 현재 인덱스부터 순회하면서 `remaining > threshold`인 토큰을 찾는다.
3. 사용 가능한 토큰이 없으면 가장 빠른 reset 시각을 계산해 `GitHubRateLimitExhaustedException`을 던진다.

환경별 threshold 기본값:

- `100`
- 설정: [application-local.yml](../../git-ranker/src/main/resources/application-local.yml), [application-prod.yml](../../git-ranker/src/main/resources/application-prod.yml)

## 호출 패턴

### 전체 조회

- merged PR search 1개
- 가입 연도부터 현재 연도까지 yearly contributions query
- query 병렬도: `5`

구현:

- [GitHubGraphQLClient.getAllActivities(...)](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubGraphQLClient.java)

### 연도별 조회

- 올해 contributions query 1개
- merged PR search 포함

구현:

- [GitHubGraphQLClient.getActivitiesForYear(...)](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubGraphQLClient.java)

## Rate-limit 보호선

### 토큰 풀 보호선

- 토큰 remaining이 `threshold` 이하이면 해당 토큰은 새 호출에 쓰지 않는다.
- 모든 토큰이 threshold 이하이면 `GitHubRateLimitExhaustedException`이 즉시 발생한다.

### 응답 후 보호선

- `getUserInfo(...)`, `getUserInfoByNodeId(...)`, `getActivitiesForYear(...)`는 GraphQL 응답의 `remaining < 50`이면 `RATE_LIMIT_WARNING` 로그를 남기고 `GitHubRateLimitException`을 던진다.
- 이 보호선은 토큰 풀 threshold와 별개로, 단일 응답이 안전 마진 아래로 떨어질 때 즉시 멈추기 위한 장치다.
- `getAllActivities(...)`는 병렬 yearly query를 합친 뒤 최종 rate-limit 정보만 기록하고, 같은 preemptive check를 직접 호출하지 않는다.

구현:

- [GitHubGraphQLClient.checkRateLimitSafety(...)](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubGraphQLClient.java)

## 예외 분류

| 상황 | 예외 분류 | 기본 처리 |
| --- | --- | --- |
| GraphQL errors에 `Could not resolve to a User` 포함 | non-retryable | 배치에서는 username drift 보정 시도 후 실패 시 skip |
| 기타 GraphQL partial error | retryable | 재시도 가능 |
| timeout / read timeout | retryable | 재시도 가능 |
| IO / 네트워크 오류 | retryable | 재시도 가능 |
| HTTP 4xx (`403`, `429` 제외) | retryable | 재시도 가능 |
| HTTP 5xx | retryable | 재시도 가능 |
| HTTP `403` 또는 `429` | retryable rate-limit 예외 | reset 시각 기반 대기 |
| 사용 가능한 토큰 없음 | retryable exhausted 예외 | 가장 빠른 reset 시각까지 대기 |

구현:

- [GitHubApiErrorHandler.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubApiErrorHandler.java)
- [GitHubRateLimitException.java](../../git-ranker/src/main/java/com/gitranker/api/global/error/exception/GitHubRateLimitException.java)
- [GitHubRateLimitExhaustedException.java](../../git-ranker/src/main/java/com/gitranker/api/global/error/exception/GitHubRateLimitExhaustedException.java)

## 배치 처리 정책

배치는 retryable / non-retryable 모두 사용자 단위 failure로 흡수할 수 있다.

- retryable: 최대 `3회` 재시도
- retry 실패 후: skip 대상으로 전환 가능
- non-retryable: 바로 skip 대상
- 총 skip 한도: `100`

skip 시 남기는 것:

- `BATCH_ITEM_FAILED` 로그
- `batch_failure_logs` 테이블 이력
- `retryable` 여부
- `READ`, `PROCESS`, `WRITE` phase

## 사용자 요청 처리 정책

수동 갱신이나 가입 흐름에서는 GitHub API 오류를 사용자 응답 에러로 그대로 노출한다.

- 일반 오류: `BusinessException` 또는 retryable GitHub 예외가 상위 핸들러로 전달
- rate limit: reset 시각을 포함한 안내 메시지 생성
- 에러 카운터: `errors_total{error_code=...}` 증가

관련 구현:

- [GlobalExceptionHandler.java](../../git-ranker/src/main/java/com/gitranker/api/global/error/GlobalExceptionHandler.java)
- [UserRegistrationService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRegistrationService.java)
- [UserRefreshService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRefreshService.java)

## 현재 구현 주의사항

- `GitHubRateLimitException`은 이름과 달리 내부 `ErrorType`으로 `GITHUB_API_TIMEOUT`을 사용한다.
- 로그와 GitHub API metrics는 rate-limit 전용 분류를 남기지만, `errors_total` 카운터는 현재 구현상 timeout 계열 코드로 집계될 수 있다.

이 차이는 관측성 분석 시 반드시 감안해야 한다.

## Harness 관점 수용 기준

- 토큰이 모두 소진되면 새로운 GitHub 호출을 시작하지 말아야 한다.
- rate-limit warning과 exhausted 예외는 reset 시각을 남겨야 한다.
- 배치는 retryable 오류를 최대 3회 재시도한 뒤 skip 처리할 수 있어야 한다.

## 참고 경로

- [GitHubTokenPool.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/token/GitHubTokenPool.java)
- [GitHubGraphQLClient.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubGraphQLClient.java)
- [GitHubApiErrorHandler.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubApiErrorHandler.java)
- [DailyScoreRecalculationJobConfig.java](../../git-ranker/src/main/java/com/gitranker/api/batch/job/DailyScoreRecalculationJobConfig.java)
