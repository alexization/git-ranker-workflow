# 2026-03-26-grc-03-frontend-build-runtime-harness

- Issue ID: `GRC-03`
- GitHub Issue: `alexization/git-ranker-client#6`
- GitHub PR: `alexization/git-ranker-client#7`
- Status: `Completed`
- Repository: `git-ranker-client`
- Branch Name: `feat/grc-03-frontend-build-runtime-harness`
- Task Slug: `2026-03-26-grc-03-frontend-build-runtime-harness`

## Problem

`git-ranker-client`의 `npm run build`는 `next/font/google`의 `JetBrains Mono` fetch에 의존해 외부 네트워크가 없으면 실패한다. 동시에 Next.js 16 기준 `middleware.ts` file convention은 deprecated 되었고, `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL` 정책도 파일마다 달라 build/runtime 전제조건이 흔들린다.

## Why Now

`GRC-03`는 `GRC-04` Playwright harness와 `GRW-05` 표준 검증 런타임보다 먼저 frontend build/runtime을 반복 실행 가능한 상태로 만드는 작업이다. build가 외부 폰트 네트워크나 암묵적 env fallback에 의존하면 하네스 기준선 자체가 불안정하다.

## Scope

- 같은 `JetBrains Mono`를 로컬 font asset으로 전환해 build 외부 네트워크 의존성을 제거한다.
- `middleware.ts`를 `proxy.ts`로 전환하고 Google Fonts 관련 CSP/preconnect를 정리한다.
- `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL`를 공용 helper 기준 필수 env로 통일한다.
- `README.md`, `.env.example`와 관련 source of truth 문서에 로컬/프로덕션 실행 전제조건을 문서화한다.

## Non-scope

- UI 디자인 개편
- Playwright 또는 단위 테스트 도입
- backend API 동작 변경
- analytics/Sentry 기능 추가

## Write Scope

- `git-ranker-client/src/app/`
- `git-ranker-client/src/shared/`
- `git-ranker-client/src/features/user/`
- `git-ranker-client/src/fonts/`
- `git-ranker-client/README.md`
- `git-ranker-client/.env.example`
- `git-ranker-client/Dockerfile`
- `git-ranker-client/docker-compose.yml`
- `docs/architecture/frontend-route-map.md`
- `docs/domain/frontend-data-flows.md`
- `docs/exec-plans/`
- `docs/operations/frontend-runtime-reference.md`

## Outputs

- local font 기반 build 설정
- 공식 JetBrains Mono 로컬 자산과 OFL 라이선스 파일
- `proxy.ts` 기반 runtime security/locale routing
- 공용 public env helper와 일관된 URL 참조
- 갱신된 frontend 실행 문서와 `GRC-03` 실행 기록

## Verification

- `npm run lint`
- `npx tsc --noEmit`
- `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`
- `git diff --stat`

## Evidence

- 시작 기준: `npm run build`가 Google Fonts fetch 실패 및 `middleware.ts` deprecated 경고를 보임
- 종료 기준: build가 로컬 폰트와 필수 env 설정으로 재현 가능하게 통과
- 폰트 증거: `src/fonts/JetBrainsMonoVariable.ttf`, `src/fonts/JetBrainsMono-OFL.txt`
- 문서 증거: `README.md`, `.env.example`, `frontend-route-map.md`, `frontend-data-flows.md`, `frontend-runtime-reference.md`
- workflow sync PR: `alexization/git-ranker-workflow#25`
- 후속 수정: `public-env.ts`의 동적 `process.env[name]` 접근을 direct `process.env.NEXT_PUBLIC_*` 참조로 바꿔 dev client runtime에서도 env가 주입되도록 수정

결과 요약:

- `npm run lint`: 성공
- `npx tsc --noEmit`: 성공
- `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`: 성공
- `npm run dev` (권한 확장): 성공. `http://localhost:3001/ko`에 `200 OK` 응답과 local font preload 확인
- 첫 번째 build 시도는 sandbox 제한 때문에 Turbopack subprocess가 포트를 바인딩하지 못해 실패했으며, 권한 확장 후 재실행에서는 코드 오류 없이 통과했다.
- build 출력에는 `Using edge runtime on a page currently disables static generation for that page` 경고가 남지만, 이는 `opengraph-image.tsx`의 Edge runtime에 따른 Next.js 기본 경고다.

## Risks or Blockers

- 로컬 폰트 자산 추가 후 렌더링 메트릭이나 타이포그래피가 미세하게 달라질 수 있다.
- env fail-fast 도입으로 기존 fallback에 기대던 실행 방식은 명시적 설정 없이는 바로 실패한다.
- workflow 문서 변경과 client 코드 변경은 governance 규칙에 따라 `alexization/git-ranker-client#7`, `alexization/git-ranker-workflow#25`로 분리했다.

## Next Preconditions

- `GRC-04`: build/runtime 기준선 위에서 Playwright harness를 도입한다.
- `GRW-05`: client runtime/env 문서를 workflow 표준 런타임에 반영한다.

## Docs Updated

- `docs/architecture/frontend-route-map.md`
- `docs/domain/frontend-data-flows.md`
- `docs/operations/frontend-runtime-reference.md`
- `docs/exec-plans/completed/2026-03-26-grc-03-frontend-build-runtime-harness.md`

## Skill Consideration

이번 작업은 roadmap item을 active exec plan으로 고정하는 `issue-to-exec-plan` skill을 적용했다. 폰트 로컬화와 public env fail-fast 정리는 현재 저장소 구조에 맞춘 일회성 구현이므로 별도 skill 후보로 분리하지 않는다.
