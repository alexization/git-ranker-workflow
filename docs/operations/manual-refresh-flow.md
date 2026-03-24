# Manual Refresh Flow

수동 갱신은 로그인한 사용자가 자기 자신의 점수와 활동 로그를 즉시 다시 계산하는 full-scan 경로다. 배치와 달리 사용자 요청 하나에 대한 동기 응답을 돌려준다.

## 엔드포인트

- 경로: `/api/v1/users/{username}/refresh`
- 메서드: `POST`
- 인증: `Authorization: Bearer <JWT>` 또는 `accessToken` cookie
- controller: [UserController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserController.java)

## 선행조건

### 인증과 권한

- 인증 principal이 반드시 있어야 한다.
- principal의 `username`과 path `username`이 정확히 같아야 한다.
- 본인 외 계정 수동 갱신은 허용하지 않는다.

### 쿨다운

- 사용자별 full scan 쿨다운은 `5분`이다.
- 구현: [User.canTriggerFullScan()](../../git-ranker/src/main/java/com/gitranker/api/domain/user/User.java)
- 실패 시 `REFRESH_COOL_DOWN_EXCEEDED`가 반환된다.

## 처리 흐름

1. controller가 인증 여부와 본인 여부를 검사한다.
2. service가 `username`으로 사용자를 조회한다.
3. GitHub 가입일 이후 현재까지의 전체 활동을 GraphQL로 다시 수집한다.
4. 전체 응답을 현재 누적 통계로 변환한다.
5. 가입 연도가 올해보다 이전이면 전년도 말 기준 baseline 통계를 계산한다.
6. persistence service가 점수, 랭킹, 티어를 갱신하고 `lastFullScanAt`을 현재 시각으로 기록한다.
7. activity log orchestrator가 baseline log와 오늘 날짜 log를 갱신한다.
8. ranking 재산정을 시도하고, debounce에 걸리지 않으면 캐시를 함께 비운다.
9. `USER_REFRESH_REQUESTED` 로그와 `user_refreshes_total` 메트릭을 남긴다.
10. 최신 profile 응답을 `RegisterUserResponse`로 반환한다.

## Activity Log 규칙

- baseline log 날짜: 전년도 `12-31`
- 오늘 log가 이미 있으면 diff만 다시 계산해 update한다.
- 이전 날짜 log가 있으면 `today - previous` diff를 기록한다.
- 이전 log가 없으면 diff는 모두 `0`이다.

관련 구현:

- [ActivityLogOrchestrator.java](../../git-ranker/src/main/java/com/gitranker/api/domain/log/ActivityLogOrchestrator.java)
- [ActivityLogService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/log/ActivityLogService.java)

## 응답 표면

수동 갱신 응답은 profile read와 같은 [RegisterUserResponse](../../git-ranker/src/main/java/com/gitranker/api/domain/user/dto/RegisterUserResponse.java)를 사용한다.

주요 필드:

- `totalScore`
- `ranking`
- `tier`
- `percentile`
- 누적 활동 수치
- 전일 대비 diff 수치
- `lastFullScanAt`

## 실패 모드

| 상황 | 결과 |
| --- | --- |
| 인증 없음 | `401 UNAUTHORIZED` |
| path username과 principal 불일치 | `403 FORBIDDEN` |
| 사용자를 찾지 못함 | `404 USER_NOT_FOUND` |
| 5분 쿨다운 미경과 | `429 REFRESH_COOL_DOWN_EXCEEDED` |
| GitHub API 실패 | retryable/non-retryable 예외를 그대로 API 에러로 노출 |
| Rate limit | reset 시각 기반 retry-after 메시지를 반환 |

GitHub API 세부 정책은 [github-api-failure-policy.md](github-api-failure-policy.md)를 따른다.

## Harness 관점 수용 기준

- 인증된 본인만 수동 갱신할 수 있어야 한다.
- 성공 시 응답 body에 새 점수와 최신 diff가 반영돼야 한다.
- 쿨다운 중에는 재계산 대신 `429`가 반환돼야 한다.

## 참고 경로

- [UserController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserController.java)
- [UserRefreshService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRefreshService.java)
- [UserPersistenceService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserPersistenceService.java)
- [ActivityLogOrchestrator.java](../../git-ranker/src/main/java/com/gitranker/api/domain/log/ActivityLogOrchestrator.java)
- [SecurityConfig.java](../../git-ranker/src/main/java/com/gitranker/api/global/config/SecurityConfig.java)
