# Ranking Read Flow

랭킹 조회는 public read API다. 이 문서는 `/api/v1/ranking`의 요청 조건, 캐시, 저장소 조회 방식, 응답 형태를 정리한다.

## 엔드포인트

- 경로: `/api/v1/ranking`
- 메서드: `GET`
- 인증: 불필요
- 구현: [RankingController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingController.java)

## 입력 계약

| 파라미터 | 기본값 | 규칙 |
| --- | --- | --- |
| `page` | `0` | `0` 이상이어야 한다 |
| `tier` | 없음 | `Tier` enum 값 중 하나면 해당 티어만 조회한다 |

기본 페이지 크기:

- `20`
- 구현 위치: [RankingService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingService.java)

## 처리 흐름

1. controller가 `page`와 `tier`를 받는다.
2. service가 캐시 키 `page:<page>:tier:<tier>`로 조회를 시도한다.
3. `tier`가 없으면 `findAllByOrderByScoreValueDesc(...)`, 있으면 `findAllByRankInfoTierOrderByScoreValueDesc(...)`를 호출한다.
4. DB에서 받아온 `User` 엔티티를 `RankingList.UserInfo`로 매핑한다.
5. page metadata를 `RankingList.PageInfo`로 만든다.
6. `ApiResponse.success(...)`로 응답한다.

## 정렬과 페이징

- 정렬 기준은 `total_score DESC`다.
- 응답의 `ranking` 필드는 페이지 위치가 아니라 사용자의 저장된 `users.ranking` 값을 사용한다.
- tier 필터는 `users.tier`에 저장된 값으로 필터링한다.

## 캐시 규칙

- 캐시 이름: `rankings`
- 캐시 저장 키: `page:<page>:tier:<tier>`
- 만료: `5분`
- 최대 엔트리: `500`
- 구현: [CacheConfig.java](../../git-ranker/src/main/java/com/gitranker/api/global/config/CacheConfig.java)

캐시는 아래 이벤트에서 비워진다.

- [RankingRecalculationService.recalculateIfNeeded()](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingRecalculationService.java)

주의:

- 일일 batch의 [RankingRecalculationTasklet](../../git-ranker/src/main/java/com/gitranker/api/batch/tasklet/RankingRecalculationTasklet.java)은 DB 랭킹 필드만 갱신하고 ranking cache는 비우지 않는다.
- 따라서 batch 직전 캐시된 page는 최대 `5분` 동안 stale할 수 있다.

## 응답 형태

핵심 payload:

- `rankings[]`
  - `username`
  - `profileImage`
  - `ranking`
  - `totalScore`
  - `tier`
- `pageInfo`
  - `currentPage`
  - `pageSize`
  - `totalElements`
  - `totalPages`
  - `isFirst`
  - `isLast`

구현 DTO:

- [RankingList.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/dto/RankingList.java)

## 실패 모드

- `page < 0`이면 validation error로 `400`이 반환된다.
- 잘못된 `tier` enum 값은 Spring binding 단계에서 실패한다.
- 캐시 miss여도 fallback 조회가 가능해야 하며, 캐시 장애는 비즈니스 규칙으로 별도 처리하지 않는다.

## Harness 관점 수용 기준

- 첫 페이지 기본 응답은 `20`개 단위 page metadata를 포함해야 한다.
- `tier` 필터를 주면 응답 항목의 `tier`가 모두 요청 값과 일치해야 한다.
- service 경로의 랭킹 재산정은 캐시를 비워 stale page를 계속 반환하지 않아야 한다.
- batch 경로는 cache stale 가능성을 별도 운영 리스크로 기록해야 한다.

## 참고 경로

- [RankingController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingController.java)
- [RankingService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/RankingService.java)
- [RankingList.java](../../git-ranker/src/main/java/com/gitranker/api/domain/ranking/dto/RankingList.java)
- [UserRepository.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserRepository.java)
- [CacheConfig.java](../../git-ranker/src/main/java/com/gitranker/api/global/config/CacheConfig.java)
