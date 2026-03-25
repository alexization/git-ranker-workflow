# Frontend Route Map

이 문서는 `git-ranker-client`의 현재 route entry와 locale rewrite 규칙을 workflow source of truth로 정리한다. 모든 사용자 페이지는 Next App Router 파일 시스템 route를 쓰지만, 실제 공개 URL은 [middleware.ts](../../git-ranker-client/src/middleware.ts)가 locale prefix를 붙여 관리한다.

## Route Resolution Rules

1. 지원 locale은 `en`, `ko` 두 개다.
2. locale prefix가 없는 일반 page 요청은 `/<locale>/...`로 `307` redirect 된다.
3. locale prefix가 있는 page 요청은 prefix를 제거한 내부 경로로 rewrite 되고, `x-locale` 헤더가 주입된다.
4. locale prefix가 붙은 backend 경로 `/api`, `/oauth2`, `/login/oauth2`는 rewrite가 아니라 prefix를 제거한 원본 경로로 다시 redirect 된다.
5. `/api/**`, `/oauth2/**`, `/login/oauth2/**`, `robots.txt`, `sitemap.xml`, `manifest.webmanifest`, 정적 자산은 locale routing을 우회한다.

구현 경로:

- [middleware.ts](../../git-ranker-client/src/middleware.ts)
- [config.ts](../../git-ranker-client/src/shared/i18n/config.ts)
- [server-locale.ts](../../git-ranker-client/src/shared/i18n/server-locale.ts)

## User-Facing Routes

모든 표의 route는 공개 URL 기준이다.

| route | entry file | 사용 API | 주요 상태 | env | 외부 의존성 |
| --- | --- | --- | --- | --- | --- |
| `/:locale` | [src/app/page.tsx](../../git-ranker-client/src/app/page.tsx), [hero-section.tsx](../../git-ranker-client/src/features/home/components/hero-section.tsx) | 직접 fetch 없음. 검색 후 `/:locale/users/[username]`로 이동 | `search-history` persisted store, `query`, `open`, `isFocused`, `selectedIndex` | `NEXT_PUBLIC_BASE_URL` | `framer-motion`, local storage, footer의 GitHub 링크 |
| `/:locale/login` | [src/app/login/page.tsx](../../git-ranker-client/src/app/login/page.tsx), [src/app/login/layout.tsx](../../git-ranker-client/src/app/login/layout.tsx) | 버튼 클릭 시 `${NEXT_PUBLIC_API_URL}/oauth2/authorization/github`로 이동 | `openModal` (`terms`/`privacy`) | `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_BASE_URL` | backend OAuth 시작 endpoint, `framer-motion` |
| `/:locale/ranking` | [src/app/ranking/page.tsx](../../git-ranker-client/src/app/ranking/page.tsx), [src/app/ranking/layout.tsx](../../git-ranker-client/src/app/ranking/layout.tsx) | `GET /api/v1/ranking?page=<n>&tier=<Tier>` | URL search param 기반 `page`, `selectedTier`; local `pageInput`, `selectedUsername`, `modalOpen` | `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL` | `@tanstack/react-query`, `framer-motion`, GitHub avatar image |
| `/:locale/users/[username]` | [src/app/users/[username]/page.tsx](../../git-ranker-client/src/app/users/[username]/page.tsx), [user-profile-client.tsx](../../git-ranker-client/src/app/users/[username]/user-profile-client.tsx) | `GET /api/v1/users/{username}`, `POST /api/v1/users/{username}/refresh`, badge URL `/api/v1/badges/{nodeId}` | React Query user cache, `displayPercentile`, `scoreInfoOpen`, refresh cooldown 계산 | `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_BASE_URL` | GitHub profile link, clipboard, `navigator.share`, remote avatar image |
| `/:locale/settings` | [src/app/settings/page.tsx](../../git-ranker-client/src/app/settings/page.tsx) | 직접 fetch 없음. modal을 통해 `DELETE /api/v1/users/me` 가능 | persisted auth store hydrate 상태, `deleteModalOpen` | 없음 | client-side redirect, persisted auth state |
| `/:locale/auth/callback` | [src/app/auth/callback/page.tsx](../../git-ranker-client/src/app/auth/callback/page.tsx) | `GET /api/v1/auth/me`, `GET /api/v1/users/{username}` | `currentStep`, `error`, `hasCalledRef` | `NODE_ENV`, `NEXT_PUBLIC_API_URL` 간접 사용 | backend가 심어준 auth cookie, `sonner` toast |
| `/oauth2/redirect` | [src/app/oauth2/redirect/page.tsx](../../git-ranker-client/src/app/oauth2/redirect/page.tsx) | `GET /api/v1/auth/me`, `GET /api/v1/users/{username}` | `/:locale/auth/callback`과 동일 | `NODE_ENV`, `NEXT_PUBLIC_API_URL` 간접 사용 | legacy/duplicate callback route. backend 설정의 canonical redirect target은 아님 |

## Metadata And Auxiliary Routes

| route | entry file | 사용 API | 주요 상태 | env | 외부 의존성 |
| --- | --- | --- | --- | --- | --- |
| `/robots.txt` | [src/app/robots.ts](../../git-ranker-client/src/app/robots.ts) | 없음 | 정적 생성 | `NEXT_PUBLIC_BASE_URL` | 없음 |
| `/sitemap.xml` | [src/app/sitemap.ts](../../git-ranker-client/src/app/sitemap.ts) | `GET /api/v1/ranking?page=<n>&size=20` 반복 호출 | 런타임 fetch 결과만 사용 | `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL` | backend ranking API |
| `/manifest.webmanifest` | [src/app/manifest.ts](../../git-ranker-client/src/app/manifest.ts) | 없음 | 정적 생성 | 없음 | 없음 |
| `/users/[username]/opengraph-image` | [opengraph-image.tsx](../../git-ranker-client/src/app/users/[username]/opengraph-image.tsx) | `GET /api/v1/users/{username}` | 런타임 fetch 결과만 사용 | `NEXT_PUBLIC_API_URL` | Edge runtime, backend user API. metadata는 이 비-localized URL을 생성하고 middleware가 locale을 보정한다 |

## Shared Layout Chain

모든 page route는 아래 공통 레이어를 지난다.

1. [middleware.ts](../../git-ranker-client/src/middleware.ts)가 locale을 결정하고 `x-locale` 헤더와 `git-ranker.locale` cookie를 정리한다.
2. [layout.tsx](../../git-ranker-client/src/app/layout.tsx)가 metadata, font, Google Analytics script, `Header`, `Toaster`, `WebVitalsReporter`를 주입한다.
3. provider 체인은 `ThemeProvider -> LocaleProvider -> QueryProvider -> AuthProvider` 순서다.

## Known Drift

- backend의 OAuth success redirect는 `/auth/callback`으로 설정돼 있지만, client에는 같은 구현의 [/oauth2/redirect](../../git-ranker-client/src/app/oauth2/redirect/page.tsx) route가 남아 있다.
- 랭킹 UI의 대체 구현인 [ranking-section.tsx](../../git-ranker-client/src/features/ranking/components/ranking-section.tsx)는 현재 route entry에서 사용되지 않는다. current source of truth는 [src/app/ranking/page.tsx](../../git-ranker-client/src/app/ranking/page.tsx)다.
- 일부 client-side redirect는 locale path를 직접 계산하지 않고 `/login`, `/users/...`, `/` 같은 bare path를 push한다. 현재는 middleware가 locale prefix를 복구한다.

## Related Docs

- [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md)
- [../operations/frontend-runtime-reference.md](../operations/frontend-runtime-reference.md)
