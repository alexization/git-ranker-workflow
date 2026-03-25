# Frontend Data Flows

이 문서는 `git-ranker-client`에서 후속 harness가 직접 검증해야 하는 세 가지 흐름을 정리한다.

- 랭킹 조회
- 사용자 상세 모달
- auth callback

공통 route 구조는 [../architecture/frontend-route-map.md](../architecture/frontend-route-map.md), env와 외부 의존성은 [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md)를 본다.

## Shared Client State Layers

| 계층 | 구현 | 역할 |
| --- | --- | --- |
| locale | [middleware.ts](../../git-ranker-client/src/middleware.ts), [server-locale.ts](../../git-ranker-client/src/shared/i18n/server-locale.ts), [locale-provider.tsx](../../git-ranker-client/src/shared/providers/locale-provider.tsx) | URL prefix, cookie, `x-locale` 헤더를 기준으로 locale 결정 |
| query cache | [query-provider.tsx](../../git-ranker-client/src/shared/providers/query-provider.tsx) | 모든 React Query cache의 기본 `staleTime=1m`, `retry=1`, `refetchOnWindowFocus=false` 제공 |
| auth store | [auth-store.ts](../../git-ranker-client/src/features/auth/store/auth-store.ts) | `auth-storage`에 `user`, `isAuthenticated` persisted |
| recent search store | [search-store.ts](../../git-ranker-client/src/features/home/store/search-store.ts) | 홈 검색 히스토리 최대 5개 보관 |
| API transport | [api-client.ts](../../git-ranker-client/src/shared/lib/api-client.ts) | `withCredentials` 요청, `ApiResponse` unwrap, `401 -> /auth/refresh -> retry` 처리 |

## Ranking Read Flow

진입점:

- [src/app/ranking/page.tsx](../../git-ranker-client/src/app/ranking/page.tsx)
- [ranking-service.ts](../../git-ranker-client/src/features/ranking/api/ranking-service.ts)

### 상태 소유권

| 상태 | 저장 위치 | 설명 |
| --- | --- | --- |
| `page` | URL search param `page` | 사용자에게는 `1`부터 보이지만 내부 query는 `0` 기반 |
| `selectedTier` | URL search param `tier` | `ALL`은 query string에서 제거된다 |
| `pageInput` | local state | pagination input용 임시 값 |
| `selectedUsername`, `modalOpen` | local state | 상세 모달 open/close 제어 |
| ranking list | React Query `['ranking', page, tier]` | 이전 응답을 `placeholderData`로 유지한다 |

### 처리 순서

1. 사용자가 `/:locale/ranking`에 들어오면 [ranking/layout.tsx](../../git-ranker-client/src/app/ranking/layout.tsx)가 locale별 metadata를 만든다.
2. [ranking/page.tsx](../../git-ranker-client/src/app/ranking/page.tsx)가 `useSearchParams()`에서 `page`, `tier`를 읽어 local UI state를 파생한다.
3. [useRankingList()](../../git-ranker-client/src/features/ranking/api/ranking-service.ts)가 query key `['ranking', page, tier]`로 [getRankingList()](../../git-ranker-client/src/features/ranking/api/ranking-service.ts)를 호출한다.
4. [getRankingList()](../../git-ranker-client/src/features/ranking/api/ranking-service.ts)는 `page`, `tier`를 `URLSearchParams`로 만들어 `/ranking?...` 요청을 보낸다.
5. [apiClient](../../git-ranker-client/src/shared/lib/api-client.ts)가 `${NEXT_PUBLIC_API_URL}/api/v1` base URL을 사용하고, 성공 시 `response.data.data`만 반환한다.
6. 사용자는 tier 버튼이나 pagination 버튼을 누를 때마다 `router.push()`로 URL을 갱신하고, 리스트 상단으로 scroll 한다.
7. 항목 클릭 시 `selectedUsername`과 `modalOpen`이 바뀌며 상세 모달 흐름으로 넘어간다.

### 화면 상태

| 조건 | UI |
| --- | --- |
| `isLoading` | skeleton list |
| `!isLoading && rankings.length === 0` | empty state |
| `!isLoading && rankings.length > 0` | list + pagination |

주의:

- 현재 routed ranking page는 `isError`를 별도로 소비하지 않는다. 요청 실패도 결과적으로 empty state로 보일 수 있다.
- route에서 [usePrefetchUser()](../../git-ranker-client/src/features/user/api/user-service.ts)를 사용하지 않으므로, 상세 모달은 click 이후에야 user query를 시작한다.

## User Detail Modal Flow

진입점:

- [UserDetailModal](../../git-ranker-client/src/features/user/components/user-detail-modal.tsx)
- [useUser()](../../git-ranker-client/src/features/user/api/user-service.ts)

### 처리 순서

1. 랭킹 리스트에서 사용자를 클릭하면 `selectedUsername`이 채워지고 `modalOpen=true`가 된다.
2. modal component가 mount되면 `useUser(username, { enabled: !!username && open })`가 활성화된다.
3. query key는 `['user', username]`이며 `retry=1`, `staleTime=5m`을 사용한다.
4. 요청 성공 시 tier, ranking, percentile, score, [ActivityGrid](../../git-ranker-client/src/features/user/components/activity-grid.tsx), profile/GitHub 링크를 렌더링한다.
5. modal footer의 `View Report`는 `/:locale/users/[username]` 전체 페이지로 이동하고, `Visit GitHub`는 외부 GitHub profile로 이동한다.
6. modal을 닫으면 부모 route가 `selectedUsername`을 `null`로 되돌린다.

### 상태와 분기

| 상태 | 트리거 | 결과 |
| --- | --- | --- |
| loading | modal open 직후, cache miss | avatar/stats skeleton |
| success | `/api/v1/users/{username}` 성공 | 상세 카드, activity grid, CTA |
| error | query failure 또는 `user` 없음 | 간단한 실패 메시지 |

구현상 특성:

- modal의 swipe-to-close는 모바일에서만 켜진다.
- same username을 다시 열면 React Query cache 재사용이 가능하다.
- 현재 routed ranking page에는 hover/focus prefetch가 없다. 다만 [usePrefetchUser()](../../git-ranker-client/src/features/user/api/user-service.ts)는 존재하고, 미사용 route 구현 [ranking-section.tsx](../../git-ranker-client/src/features/ranking/components/ranking-section.tsx)에서만 사용된다.

## Auth Callback Flow

진입점:

- canonical page: [src/app/auth/callback/page.tsx](../../git-ranker-client/src/app/auth/callback/page.tsx)
- duplicate legacy page: [src/app/oauth2/redirect/page.tsx](../../git-ranker-client/src/app/oauth2/redirect/page.tsx)

backend 관련 경로:

- OAuth 시작: `${NEXT_PUBLIC_API_URL}/oauth2/authorization/github`
- backend redirect target: [application-local.yml](../../git-ranker/src/main/resources/application-local.yml), [application-prod.yml](../../git-ranker/src/main/resources/application-prod.yml)의 `/auth/callback`

### 처리 순서

1. 사용자가 login 화면이나 user-not-found 화면에서 GitHub 로그인 버튼을 누르면 backend OAuth 시작 endpoint로 이동한다.
2. backend가 인증 성공 후 `/auth/callback`으로 redirect 한다.
3. [middleware.ts](../../git-ranker-client/src/middleware.ts)가 bare path `/auth/callback`을 locale path로 redirect 한 뒤 내부적으로 `/auth/callback` page route로 rewrite 한다.
4. callback page는 fake progress interval을 돌리면서, 1회만 `apiClient.get('/auth/me')`를 호출한다.
5. `AuthMeResponse.username`을 받으면 [getUser()](../../git-ranker-client/src/features/user/api/user-service.ts)로 전체 user profile을 다시 읽는다.
6. 성공 시 persisted auth store의 `login(user)`를 호출하고 toast를 띄운 뒤 `/users/${user.username}`로 replace 한다.
7. 실패 시 `getErrorMessage()`로 에러 문구를 만들고 error state UI로 전환한다. 여기서 retry 또는 login page 이동을 선택할 수 있다.

### 상태와 분기

| 상태 | 로컬 상태 | 의미 |
| --- | --- | --- |
| initial/loading | `currentStep`, `error=null`, `hasCalledRef=false` | progress UI와 API 호출 시작 전/중 |
| success | store login 후 route replace | 정상 로그인 완료 |
| failure | `error` 설정 | retry 또는 login 이동 |

주의:

- callback success/failure 후 이동 경로는 locale path를 직접 계산하지 않고 bare path를 쓴다. 현재는 middleware가 locale prefix를 복구한다.
- `/auth/callback`과 `/oauth2/redirect` 구현이 동일해 drift 위험이 있다. source of truth와 backend 설정 기준 canonical 경로는 `/auth/callback`이다.

## Harness Notes

- ranking harness는 ranking API 성공과 list 렌더링만이 아니라, 실패 시 empty state로 오인되는 현재 동작도 고려해야 한다.
- modal 검증은 click 후 query 시작, loading skeleton, success/error 분기를 모두 봐야 한다.
- auth callback 검증은 backend cookie 기반 `/auth/me` 호출과 후속 `/users/{username}` fetch를 한 세트로 봐야 한다.
