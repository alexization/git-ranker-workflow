# Tiering Rules

Git Ranker는 점수와 상대 위치를 함께 써서 티어를 만든다. 이 문서는 per-user 계산과 전체 재산정에서 랭킹, 백분위, 티어가 어떻게 결정되는지 설명한다.

## 티어 기준

| 티어 | 조건 |
| --- | --- |
| `CHALLENGER` | `totalScore >= 2000` 이고 상위 `1%` 이내 |
| `MASTER` | `totalScore >= 2000` 이고 상위 `5%` 이내 |
| `DIAMOND` | `totalScore >= 2000` 이고 상위 `12%` 이내 |
| `EMERALD` | `totalScore >= 2000` 이고 상위 `25%` 이내 |
| `PLATINUM` | `totalScore >= 2000` 이고 상위 `45%` 이내 |
| `GOLD` | `1500`점 이상 |
| `SILVER` | `1000`점 이상 |
| `BRONZE` | `500`점 이상 |
| `IRON` | `500`점 미만 |

기준 구현:

- [RankInfo.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/RankInfo.java)
- [UserRepository.bulkUpdateRanking()](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserRepository.java)

## 랭킹과 백분위 계산

### per-user 즉시 계산

신규 등록과 수동 갱신은 저장 직전에 아래 식으로 랭킹과 백분위를 먼저 계산한다.

```text
ranking = higherScoreCount + 1
percentile = ranking / totalUserCount * 100
```

이 계산은 [RankInfo.calculate(...)](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/RankInfo.java)에서 수행한다.

### 전체 재산정

배치 또는 랭킹 재산정 서비스는 DB 전체를 다시 계산한다.

- `ranking`: SQL `RANK() OVER (ORDER BY total_score DESC)`
- `percentile`: SQL `CUME_DIST() OVER (ORDER BY total_score DESC) * 100`
- `tier`: 같은 SQL 문 안에서 threshold 규칙으로 계산

이 bulk 재산정은 [UserRepository.bulkUpdateRanking()](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserRepository.java)에 정의돼 있다.

## 언제 재산정되는가

### 신규 등록 / 수동 갱신

- 사용자 단위 점수, 랭킹, 티어는 즉시 계산된다.
- 이후 [RankingRecalculationService](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingRecalculationService.java)가 전체 랭킹 재산정을 시도한다.
- 전체 재산정은 `5분` debounce가 있다. 최근 `5분` 안에 이미 실행됐다면 skip한다.

### 일일 배치

- 모든 사용자의 점수를 갱신한 다음 `rankingRecalculationStep`에서 bulk 재산정을 수행한다.
- 배치 경로에서는 마지막 단계가 끝나야 전체 랭킹 표면이 새 순위를 일관되게 본다.

## 동률 처리

- 즉시 계산 경로는 `higherScoreCount`만 세므로 같은 점수는 같은 `ranking` 값을 공유한다.
- 최종 bulk 재산정은 SQL `RANK()`를 쓰므로 같은 점수는 같은 순위를 공유하고, 다음 순위는 건너뛸 수 있다.
- 랭킹 조회 API는 정렬을 `score DESC`로만 수행하므로 동률 내부 정렬 순서는 별도 보장하지 않는다.

## 랭킹 조회와의 관계

- 랭킹 페이지가 보여주는 `ranking`, `tier`, `percentile`은 `users` 테이블에 저장된 값이다.
- 랭킹 API는 조회 시 새 순위를 계산하지 않는다.
- 따라서 신규 등록이나 수동 갱신 직후 debounce 때문에 bulk 재산정이 생략되면, 그 시점의 값은 per-user 계산 결과를 그대로 사용할 수 있다.

## 실패 모드와 주의사항

- 총 사용자 수가 `0`이면 `RankInfo.initial()`을 사용해 `IRON`, `100%`, `0위`로 초기화한다.
- tier 승급 판단은 `ordinal` 비교를 사용한다. enum 순서가 계약이므로 enum 순서를 바꾸면 안 된다.
- 배치가 중간에 실패하면 일부 사용자의 점수는 갱신됐더라도 전체 랭킹 재산정이 끝나지 않을 수 있다.

## Harness 관점 수용 기준

- `totalScore >= 2000`이 아니면 상위 백분위여도 `PLATINUM` 이상 티어를 부여하지 않는다.
- 동점자는 같은 rank를 공유해야 한다.
- 랭킹 재산정 후에는 랭킹 캐시가 비워져야 한다.

## 참고 경로

- [Tier.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/Tier.java)
- [RankInfo.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/vo/RankInfo.java)
- [User.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/User.java)
- [UserRepository.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserRepository.java)
- [RankingRecalculationService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingRecalculationService.java)
