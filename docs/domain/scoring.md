# Scoring Rules

Git Ranker의 점수는 `ActivityStatistics`에 모인 활동 집계를 `Score.calculate(...)`에 넣어 계산한다. 이 문서는 점수 계산식 자체와, 각 흐름이 어떤 방식으로 입력값을 만드는지를 정리한다.

## 핵심 규칙

| 활동 | 입력 필드 | 가중치 | 계산 위치 |
| --- | --- | --- | --- |
| Commit | `commitCount` | `1` | [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java) |
| Issue | `issueCount` | `2` | [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java) |
| Review | `reviewCount` | `5` | [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java) |
| PR Open | `prOpenedCount` | `5` | [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java) |
| PR Merged | `prMergedCount` | `8` | [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java) |

공식 계산식:

```text
totalScore
= (commitCount × 1)
+ (issueCount × 2)
+ (reviewCount × 5)
+ (prOpenedCount × 5)
+ (prMergedCount × 8)
```

## 점수 입력이 만들어지는 경로

### 1. 신규 등록

1. OAuth 로그인 성공 후 [UserRegistrationService](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRegistrationService.java)가 GitHub 가입일 이후 전체 활동을 가져온다.
2. [GitHubDataMapper](../../git-ranker/src/main/java/com/gitranker/api/infrastructure/github/GitHubDataMapper.java)가 전체 응답을 `ActivityStatistics`로 바꾼다.
3. `baselineStats`가 있으면 전년도 말 기준 activity log를 따로 남기고, 오늘 날짜 log에는 전체 누적값을 기록한다.
4. [User.updateActivityStatistics](../../git-ranker/src/main/java/com/gitranker/api/domain/user/User.java)가 계산된 점수를 사용자 엔티티에 반영한다.

### 2. 수동 갱신

1. [UserRefreshService](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRefreshService.java)가 GitHub 가입일부터 현재까지 전체 활동을 다시 수집한다.
2. 현재 응답에서 전체 집계를 계산하고, 필요하면 전년도 말 baseline 통계를 다시 계산한다.
3. [UserPersistenceService](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserPersistenceService.java)가 점수, 티어, 랭킹, 오늘 날짜 activity log를 갱신한다.
4. 이전 점수와 새 점수 차이를 `USER_REFRESH_REQUESTED` 로그에 남긴다.

### 3. 일일 배치

1. [ScoreRecalculationProcessor](../../git-ranker/src/main/java/com/gitranker/api/batch/processor/ScoreRecalculationProcessor.java)가 사용자별로 전체 또는 증분 집계를 다시 만든다.
2. baseline log가 있으면 증분 전략을 쓰고, 없으면 전체 조회를 쓴다.
3. 새 집계로 점수를 계산한 뒤 오늘 날짜 activity log를 남긴다.
4. chunk 저장과 최종 랭킹 재산정을 거쳐 랭킹 조회 표면에 반영된다.

## 집계 시 주의할 구현 규칙

- `ActivityStatistics.calculateScore()`가 최종 점수 계산의 단일 진입점이다. 랭킹, 프로필, 배지 모두 이 값을 소비한다.
- `merged PR` 수는 GitHub contributions collection이 아니라 별도 search 쿼리에서 가져온다. 따라서 `PR Open`과 집계 경로가 다르다.
- 전년도 이전 누적치는 baseline log로 보존되고, 증분 배치에서는 baseline에 올해 활동만 더해 전체 점수를 다시 만든다.
- 점수는 음수가 될 수 없다. `Score.of(...)`와 `Score.calculate(...)`는 음수를 거부한다.

## 출력 표면

점수는 아래 응답과 저장 필드에 반영된다.

- `users.total_score`
- [RegisterUserResponse](../../git-ranker/src/main/java/com/gitranker/api/domain/user/dto/RegisterUserResponse.java)의 `totalScore`
- [RankingList.UserInfo](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/dto/RankingList.java)의 `totalScore`
- [SvgBadgeRenderer](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/SvgBadgeRenderer.java)가 렌더링하는 badge 본문

## 실패 모드

- GitHub 활동 수집이 실패하면 점수 재계산도 중단된다.
- 배치에서는 retry/skip 정책에 따라 사용자 단위 실패로 처리할 수 있다. 상세 규칙은 [github-api-failure-policy.md](../operations/github-api-failure-policy.md)를 따른다.
- 수동 갱신은 GitHub API 오류를 API 응답 에러로 바로 노출한다.

## Harness 관점 수용 기준

- 동일한 활동 집계를 다시 넣었을 때 점수는 항상 같아야 한다.
- `merged PR`와 `PR Open`은 별도 필드로 유지돼야 한다.
- 모든 활동 수가 `0`이면 점수는 `0`이어야 한다.

## 참고 경로

- [ActivityStatistics.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/ActivityStatistics.java)
- [Score.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/Score.java)
- [UserRegistrationService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRegistrationService.java)
- [UserRefreshService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/service/UserRefreshService.java)
- [ScoreRecalculationProcessor.java](../../git-ranker/src/main/java/com/gitranker/api/batch/processor/ScoreRecalculationProcessor.java)
