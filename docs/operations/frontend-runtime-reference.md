# Frontend Runtime Reference

이 문서는 `git-ranker-client`가 현재 어떤 env, 외부 서비스, 보안 헤더, 런타임 가정을 전제로 동작하는지 정리한다. route별 구조는 [../architecture/frontend-route-map.md](../architecture/frontend-route-map.md), 사용자 흐름은 [../domain/frontend-data-flows.md](../domain/frontend-data-flows.md)를 본다.

## Environment Variables

| 이름 | 필요도 | 사용 위치 | 기본값/대체값 | 비고 |
| --- | --- | --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | 필수 | [public-env.ts](../../git-ranker-client/src/shared/lib/public-env.ts), [api-client.ts](../../git-ranker-client/src/shared/lib/api-client.ts), [login/page.tsx](../../git-ranker-client/src/app/login/page.tsx), [user-profile-client.tsx](../../git-ranker-client/src/app/users/[username]/user-profile-client.tsx), [sitemap.ts](../../git-ranker-client/src/app/sitemap.ts), [opengraph-image.tsx](../../git-ranker-client/src/app/users/[username]/opengraph-image.tsx) | 없음 | backend API origin, OAuth 시작 URL, badge URL의 단일 기준이다. unset 또는 invalid absolute URL이면 fail-fast 한다. path component가 있어도 origin만 사용한다 |
| `NEXT_PUBLIC_BASE_URL` | 필수 | [public-env.ts](../../git-ranker-client/src/shared/lib/public-env.ts), [layout.tsx](../../git-ranker-client/src/app/layout.tsx), [page.tsx](../../git-ranker-client/src/app/page.tsx), [ranking/layout.tsx](../../git-ranker-client/src/app/ranking/layout.tsx), [users/[username]/page.tsx](../../git-ranker-client/src/app/users/[username]/page.tsx), [robots.ts](../../git-ranker-client/src/app/robots.ts), [sitemap.ts](../../git-ranker-client/src/app/sitemap.ts) | 없음 | canonical URL, OG URL, sitemap/robots 기준이다. unset 또는 invalid absolute URL이면 fail-fast 한다. path component가 있어도 origin만 사용한다 |
| `NEXT_PUBLIC_ANALYTICS_ENDPOINT` | 선택 | [web-vitals-reporter.tsx](../../git-ranker-client/src/shared/components/web-vitals-reporter.tsx) | 없음 | production에서만 `sendBeacon` 전송 |
| `NEXT_PUBLIC_SENTRY_DSN` | 선택 | [sentry.client.config.ts](../../git-ranker-client/sentry.client.config.ts), [sentry.server.config.ts](../../git-ranker-client/sentry.server.config.ts), [sentry.edge.config.ts](../../git-ranker-client/sentry.edge.config.ts) | 없음 | client/edge/server 공용 fallback |
| `SENTRY_DSN` | 선택 | [sentry.server.config.ts](../../git-ranker-client/sentry.server.config.ts), [sentry.edge.config.ts](../../git-ranker-client/sentry.edge.config.ts) | `NEXT_PUBLIC_SENTRY_DSN` fallback | server/edge 우선값 |
| `NODE_ENV` | 필수 런타임 전제 | [proxy.ts](../../git-ranker-client/src/proxy.ts), [auth/callback/page.tsx](../../git-ranker-client/src/app/auth/callback/page.tsx), [web-vitals-reporter.tsx](../../git-ranker-client/src/shared/components/web-vitals-reporter.tsx), Sentry 설정 파일 | framework 기본값 | proxy/CSP, 개발 로그, analytics/Sentry enablement를 가른다 |

## Build And Container Injection

- Docker build/runtime은 [Dockerfile](../../git-ranker-client/Dockerfile)과 [docker-compose.yml](../../git-ranker-client/docker-compose.yml)에서 `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_BASE_URL`를 주입한다.
- [public-env.ts](../../git-ranker-client/src/shared/lib/public-env.ts)가 두 env를 공용 helper에서 바로 검증하고 absolute URL의 `origin`만 사용하므로, unset 또는 invalid URL 상태에서는 build와 runtime이 fail-fast 한다.
- [README.md](../../git-ranker-client/README.md)와 [.env.example](../../git-ranker-client/.env.example)는 로컬 `http://localhost:3000` / `http://localhost:8080`, 프로덕션 `https://www.git-ranker.com` 기준 값을 함께 문서화한다.
- `NEXT_PUBLIC_*` 값은 build 시 inline 되므로, runtime에만 바꿔도 이미 번들된 값과 어긋날 수 있다.
- `NODE_ENV=production`은 container runtime에서 명시된다.

## External Dependencies

| 대상 | 사용 위치 | 목적 | 실패 영향 |
| --- | --- | --- | --- |
| Git Ranker backend (`NEXT_PUBLIC_API_URL`) | API client, OAuth 시작, sitemap, OG image, badge URL | ranking/user/auth/badge 데이터와 OAuth 진입점 | ranking/user/auth 흐름 전체 실패 |
| GitHub OAuth (`/oauth2/authorization/github`) | login page, user not found CTA | 로그인 시작 | 로그인 불가 |
| `avatars.githubusercontent.com` | avatar image, Next image remote pattern, layout preconnect | 사용자 프로필 이미지 렌더링 | avatar 깨짐 또는 느린 로드 |
| `github.com` | profile outbound link, Next image remote pattern | GitHub 프로필 이동 | 외부 링크만 영향 |
| `www.googletagmanager.com`, `www.google-analytics.com`, `region1.google-analytics.com` | [layout.tsx](../../git-ranker-client/src/app/layout.tsx), [proxy.ts](../../git-ranker-client/src/proxy.ts) | Google Analytics script/load/connect | 분석 데이터만 누락 |
| `NEXT_PUBLIC_ANALYTICS_ENDPOINT` | [web-vitals-reporter.tsx](../../git-ranker-client/src/shared/components/web-vitals-reporter.tsx) | optional web-vitals 전송 | 성능 분석만 누락 |
| Sentry ingest endpoint | Sentry 설정 파일 | 오류/리플레이 수집 | 에러 추적만 누락 |

## Security Headers And Network Policy

구현:

- [proxy.ts](../../git-ranker-client/src/proxy.ts)
- [next.config.ts](../../git-ranker-client/next.config.ts)

현재 proxy가 모든 응답에 아래 정책을 주입한다.

- `Content-Security-Policy`
  - `script-src`: self, inline, Google Tag Manager. `unsafe-eval`은 development에서만 허용한다
  - `style-src`: self, inline
  - `font-src`: self
  - `img-src`: self, data/blob, `NEXT_PUBLIC_API_URL`, GitHub avatar/GitHub, Google Analytics
  - `connect-src`: self, `NEXT_PUBLIC_API_URL`, analytics host 허용
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()`

`next.config.ts`는 remote image host를 `github.com`, `avatars.githubusercontent.com` 두 곳으로 제한한다. 폰트는 [layout.tsx](../../git-ranker-client/src/app/layout.tsx)의 `next/font/local`이 번들링한다.

## Observability Hooks

| 항목 | 구현 | 현재 상태 |
| --- | --- | --- |
| Google Analytics script | [layout.tsx](../../git-ranker-client/src/app/layout.tsx) | hard-coded measurement ID `G-QKZNEY525E` 사용 |
| Web Vitals reporter | [web-vitals-reporter.tsx](../../git-ranker-client/src/shared/components/web-vitals-reporter.tsx) | `web-vitals` 패키지가 설치돼 있지 않으면 no-op |
| Optional analytics endpoint | [web-vitals-reporter.tsx](../../git-ranker-client/src/shared/components/web-vitals-reporter.tsx) | `NEXT_PUBLIC_ANALYTICS_ENDPOINT`가 있을 때만 사용 |
| Sentry | [sentry.client.config.ts](../../git-ranker-client/sentry.client.config.ts), [sentry.server.config.ts](../../git-ranker-client/sentry.server.config.ts), [sentry.edge.config.ts](../../git-ranker-client/sentry.edge.config.ts) | production + DSN 존재 시에만 활성화 |

## Known Runtime Gaps

- [shared/lib/analytics.ts](../../git-ranker-client/src/shared/lib/analytics.ts)는 `/api/analytics/*`로 보내는 helper를 갖고 있지만 현재 import되지 않으며, client 저장소에는 해당 Next API route도 없다.
- OAuth callback은 backend 설정상 `/auth/callback`이 canonical이지만, client에는 동일 구현의 `/oauth2/redirect` route가 남아 있다.

## Harness Notes

- frontend build는 local font와 필수 `NEXT_PUBLIC_*` env를 전제로 반복 실행 가능해야 한다.
- ranking harness는 backend API, GitHub avatar CDN, proxy locale redirect를 함께 고려해야 한다.
