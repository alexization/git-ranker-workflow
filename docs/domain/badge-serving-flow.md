# Badge Serving Flow

배지 API는 public SVG read surface다. 실제 사용자 badge와 티어 미리보기 badge는 같은 renderer를 쓰지만, 입력과 캐시 규칙은 다르다.

## 엔드포인트

| 경로 | 목적 | 인증 |
| --- | --- | --- |
| `/api/v1/badges/{nodeId}` | 실제 사용자 badge 렌더링 | 불필요 |
| `/api/v1/badges/{tier}/badge` | 티어 preview badge 렌더링 | 불필요 |

구현:

- [BadgeController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/BadgeController.java)
- [BadgeService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/BadgeService.java)

## 실제 사용자 badge 흐름

1. `nodeId`로 사용자를 조회한다.
2. 가장 최근 activity log를 읽고, 없으면 오늘 날짜의 빈 log를 합성한다.
3. `BADGE_VIEWED` 이벤트에 `target_username`을 남긴다.
4. `badge_views_total` 메트릭을 1 증가시킨다.
5. `SvgBadgeRenderer`가 tier gradient, score, rank, 활동 통계, diff를 포함한 SVG를 만든다.
6. controller가 `image/svg+xml` 응답과 cache header를 내려준다.

## 응답 헤더 규칙

실제 사용자 badge 응답은 아래 헤더를 설정한다.

- `Content-Type: image/svg+xml`
- `Cache-Control: max-age=3600, must-revalidate`
- `Pragma: no-cache`
- `Expires: 0`

현재 구현은 `1시간` 캐시와 `must-revalidate`를 주면서도 `Pragma`/`Expires`를 함께 내려준다. 하네스는 우선 `Cache-Control`의 `1시간` 정책을 기준으로 보고, CDN 또는 브라우저 동작 차이는 별도 증거로 남긴다.

## badge 본문에 들어가는 정보

`SvgBadgeRenderer`는 아래 값을 렌더링한다.

- username
- tier 표시명
- total score
- top percentile
- ranking
- commit / issue / PR open / PR merged / review 누적값
- 각 활동의 일일 diff

티어 색상은 [TierGradientProvider.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/TierGradientProvider.java)에서 관리한다.

## 폰트와 외부 의존성

SVG 본문에는 Google Fonts `@import`가 들어간다.

- 구현: [SvgBadgeRenderer.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/SvgBadgeRenderer.java)
- 영향: 폰트를 가져오지 못하는 환경에서는 동일한 레이아웃이 보장되지 않을 수 있다.

이 이슈에서는 동작 문서화만 다루고, 외부 폰트 제거는 후속 runtime/build 친화화 이슈에서 다룬다.

## 티어 preview badge 흐름

`/{tier}/badge`는 DB를 조회하지 않는다.

1. 요청 티어로 synthetic user와 synthetic activity log를 만든다.
2. 고정 score/rank/activity 예시값을 넣는다.
3. 같은 renderer로 SVG를 생성한다.
4. 별도 metrics/logging 증가는 하지 않는다.

## 실패 모드

- `nodeId`가 없으면 `USER_NOT_FOUND`로 실패한다.
- 최신 activity log가 없어도 badge는 실패하지 않고 빈 통계 badge를 반환한다.
- 잘못된 `tier` enum 값은 request binding 단계에서 실패한다.

## Harness 관점 수용 기준

- 실제 사용자 badge는 `image/svg+xml`과 `Cache-Control`을 내려줘야 한다.
- activity log가 없는 신규 사용자도 badge 렌더링이 가능해야 한다.
- 티어 preview badge는 DB 상태와 무관하게 항상 같은 구조의 SVG를 반환해야 한다.

## 참고 경로

- [BadgeController.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/BadgeController.java)
- [BadgeService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/BadgeService.java)
- [SvgBadgeRenderer.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/SvgBadgeRenderer.java)
- [BadgeFormatter.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/BadgeFormatter.java)
- [TierGradientProvider.java](../../git-ranker/src/main/java/com/gitranker/api/domain/badge/TierGradientProvider.java)
