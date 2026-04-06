# Observability Reference

이 문서는 후속 harness가 바로 참조할 수 있는 로그 이벤트, 공통 필드, 메트릭 이름, 관측 endpoint를 정리한다.

## 로그 공통 규칙

로그 컨텍스트 구현:

- [LogContext.java](../../git-ranker/src/main/java/com/gitranker/api/global/logging/LogContext.java)
- [LoggingFilter.java](../../git-ranker/src/main/java/com/gitranker/api/global/logging/LoggingFilter.java)
- [Event.java](../../git-ranker/src/main/java/com/gitranker/api/global/logging/Event.java)

### 요청 단위 공통 필드

모든 HTTP 요청 로그는 아래 request-scoped 필드를 공유할 수 있다.

- `trace_id`
- `client_ip`
- `user_agent`
- `request_method`
- `request_uri`
- `username` (인증 문맥이 있을 때, 마스킹된 값)

### 이벤트 공통 필드

각 `LogContext.event(...)` 호출은 최소 아래 필드를 채운다.

- `event`
- `log_category`
- `phase`
- `outcome`

## 주요 이벤트와 핵심 필드

| 이벤트 | 의미 | 핵심 필드 |
| --- | --- | --- |
| `HTTP_RESPONSE` | 모든 비정적 HTTP 응답 | `status`, `latency_ms`, `outcome` |
| `USER_REGISTERED` | 신규 사용자 등록 | `username`, `node_id`, `initial_score`, `initial_tier` |
| `USER_LOGIN` | OAuth 로그인 성공 | `username` |
| `USER_REFRESH_REQUESTED` | 수동 갱신 성공 | `username`, `old_score`, `new_score`, `score_diff` |
| `PROFILE_VIEWED` | 사용자 프로필 조회 | `target_username` |
| `BADGE_VIEWED` | 실제 badge 조회 | `target_username` |
| `TOKEN_REFRESHED` | 토큰 재발급 성공 | `username` |
| `LOGOUT` | 세션 로그아웃 | `username` |
| `AUTH_FAILED` | JWT 검증 실패 | `error_type`, `error_message` |
| `GITHUB_API_CALLED` | GitHub API 성공/실패 | `operation`, `target`, `latency_ms`, `outcome`, `cost`, `remaining`, `error_type` |
| `RATE_LIMIT_WARNING` | 잔여 호출 수 경고 | `remaining`, `threshold`, `reset_at` |
| `BATCH_STARTED` | 배치 시작 | `job_name`, `total_user_count` |
| `BATCH_COMPLETED` | 배치 완료 요약 | `job_name`, `status`, `total_count`, `success_count`, `fail_count`, `skip_count`, `duration_ms` |
| `BATCH_FAILED` | scheduler 수준 배치 실패 | `job_name`, `error_message` |
| `BATCH_ITEM_FAILED` | 사용자 단위 batch 실패 | `username`, `phase`, `error_type`, `error_message`, `retryable` |
| `ERROR_HANDLED` | API 에러 응답 변환 | `error_code`, `error_status`, `error_type`, `error_message` |

## 로그 출력 형식

- `prod`가 아니면 컬러 콘솔 텍스트 로그
- `prod`면 JSON 로그
- prod JSON은 MDC를 포함한다

구현:

- [logback-spring.xml](../../git-ranker/src/main/resources/logback-spring.xml)

## 메트릭 이름

### Business metrics

| 이름 | 의미 | 태그 |
| --- | --- | --- |
| `user_registrations_total` | 신규 등록 수 | 없음 |
| `user_logins_total` | 로그인 수 | 없음 |
| `profile_views_total` | 프로필 조회 수 | 없음 |
| `badge_views_total` | badge 조회 수 | 없음 |
| `user_refreshes_total` | 수동 갱신 수 | 없음 |
| `user_deletions_total` | 계정 삭제 수 | 없음 |
| `errors_total` | 에러 수 | `error_code` |

구현:

- [BusinessMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/global/metrics/BusinessMetrics.java)

### Batch metrics

| 이름 | 의미 | 태그 |
| --- | --- | --- |
| `batch_jobs_completed_total` | 성공한 batch job 수 | 없음 |
| `batch_jobs_failed_total` | 실패한 batch job 수 | 없음 |
| `batch_items_processed_total` | 성공 처리 item 수 | 없음 |
| `batch_items_skipped_total` | skip item 수 | 없음 |
| `batch_job_duration` | batch job duration | `status=success|failure` |

구현:

- [BatchMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/batch/metrics/BatchMetrics.java)

### GitHub API metrics

| 이름 | 의미 | 태그 |
| --- | --- | --- |
| `github_api_remaining` | 현재 토큰의 남은 호출 수 gauge | 없음 |
| `github_api_reset_at_epoch` | reset 시각 epoch gauge | 없음 |
| `github_api_cost_total` | 누적 GraphQL cost | 없음 |
| `github_api_calls_total` | GitHub 호출 수 | `result=success|failure|rate_limited` |
| `github_api_latency` | GitHub 호출 latency | 없음 |

구현:

- [GitHubApiMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubApiMetrics.java)

## Endpoint와 노출 규칙

관리 endpoint 설정:

- 포트: `9090`
- 기본 노출: `health`, `info`, `prometheus`, `metrics`, `loggers`, `env`, `threaddump`, `heapdump`
- prod 노출: `health`, `prometheus`

public로 허용된 endpoint:

- `/actuator/health`
- `/actuator/prometheus`

구현:

- [application.yml](../../git-ranker/src/main/resources/application.yml)
- [application-prod.yml](../../git-ranker/src/main/resources/application-prod.yml)
- [SecurityConfig.java](../../git-ranker/src/main/java/com/gitranker/api/global/config/SecurityConfig.java)

## Harness 관점 수용 기준

- 로그 evidence는 `trace_id`와 `event`를 기준으로 묶을 수 있어야 한다.
- 배치 evidence는 `BATCH_STARTED`, `BATCH_COMPLETED`, `BATCH_ITEM_FAILED` 중 최소 하나를 포함해야 한다.
- 메트릭 evidence는 business, batch, GitHub API 3축 중 이번 검증 대상과 맞는 지표를 선택해야 한다.

## 참고 경로

- [LogContext.java](../../git-ranker/src/main/java/com/gitranker/api/global/logging/LogContext.java)
- [Event.java](../../git-ranker/src/main/java/com/gitranker/api/global/logging/Event.java)
- [BusinessMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/global/metrics/BusinessMetrics.java)
- [BatchMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/batch/metrics/BatchMetrics.java)
- [GitHubApiMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubApiMetrics.java)
