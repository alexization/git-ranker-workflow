# 2026-03-25-grc-01-unify-api-contract-types

- Issue ID: `GRC-01`
- GitHub Issue: `alexization/git-ranker-client#2`
- Status: `Completed`
- Repository: `git-ranker-client`
- Branch Name: `feat/grc-01-unify-api-contract-types`
- Task Slug: `2026-03-25-grc-01-unify-api-contract-types`

## Problem

`git-ranker-client`는 같은 서버 응답 계약을 `src/shared/types/api.ts`, `src/shared/lib/validations.ts`, 일부 직접 fetch 소비자 파일에서 중복 선언하고 있다. 이 중복 때문에 `EMERALD` 누락처럼 backend OpenAPI 계약과 프런트 타입이 드리프트했다.

## Why Now

`GRC-01`은 `GRC-02`, `GRC-04`보다 먼저 계약 기준을 하나로 고정해야 한다. 타입 기준이 흔들리면 lint 정리나 Playwright 하네스가 잘못된 계약 위에 쌓인다.

## Scope

- `src/shared/types/api.ts`를 client 내부 단일 계약 기준으로 정리
- `src/shared/lib/validations.ts`에서 API 응답용 schema/type 중복 제거
- 직접 API 응답을 선언하는 소비자 파일을 단일 계약 경로로 정리
- backend `docs/openapi/openapi.json`과 수동 대조로 enum/type drift 제거

## Non-scope

- OpenAPI 기반 generated type 도입
- 전체 컴포넌트 리팩터링
- Playwright 도입

## Write Scope

- `git-ranker-client/src/shared/types/`
- `git-ranker-client/src/shared/lib/validations.ts`
- `git-ranker-client/src/shared/lib/api-client.ts`
- `git-ranker-client/src/app/sitemap.ts`
- `git-ranker-client/src/app/users/[username]/opengraph-image.tsx`
- `git-ranker-client/src/app/auth/callback/page.tsx`
- `git-ranker-client/src/app/oauth2/redirect/page.tsx`
- `git-ranker-client/src/shared/constants/tier-styles.ts`
- `git-ranker-client/src/app/ranking/page.tsx`
- `docs/exec-plans/`

## Outputs

- 단일 계약 타입 경로
- `tier` 값셋 단일화
- API 응답 중복 선언 제거
- `/ranking`, `/users/[username]`, `/auth/me` 직접 소비자 정합화
- `GRC-01` 실행 기록

## Verification

- `npx tsc --noEmit`
- backend `git-ranker/docs/openapi/openapi.json`과 수동 대조

결과 요약:

- `npx tsc --noEmit`: 성공
- `npm run lint`: 성공(0 error, 26 warning). warning은 기존 lint debt로 남았고 GRC-01 범위에서는 새 warning을 추가하지 않음
- backend OpenAPI 대조:
  - `tier` enum에 `EMERALD` 포함 확인
  - `role` enum이 `GUEST`, `USER`, `ADMIN`임을 확인
  - `/api/v1/ranking`, `/api/v1/users/{username}`, `/api/v1/auth/me` 응답 envelope 확인
- `git -C git-ranker-client diff --stat`: 9개 파일 수정, 중복 선언 제거 중심 변경

## Evidence

문서/타입 정리 작업이라 브라우저 artifact는 남기지 않았다. 대신 변경 파일과 타입 검증 결과, backend OpenAPI 대조 결과를 이 문서에 기록한다.

- GitHub Issue: `alexization/git-ranker-client#2`
- backend 기준 계약: `git-ranker/docs/openapi/openapi.json`
- 단일 계약 경로: `git-ranker-client/src/shared/types/api.ts`

## Risks or Blockers

- 이번 작업은 수동 단일화라 backend 계약 변경 시 후속 동기화 작업이 여전히 필요하다.
- `apiClient`가 legacy 응답 fallback을 일부 유지하고 있어, 완전한 legacy 제거는 후속 작업으로 남을 수 있다.

## Next Preconditions

- `GRC-02`: 단일 계약 기준 위에서 lint debt 정리
- `GRC-04`: ranking read Playwright 시나리오가 같은 타입 기준을 사용

## Docs Updated

- `docs/exec-plans/completed/2026-03-25-grc-01-unify-api-contract-types.md`
- 추가 source of truth 문서 업데이트는 하지 않았다. 기존 `docs/product/work-item-catalog.md`의 GRC-01 정의가 현재 작업 결과와 일치하고, 수동 기준 계약 위치는 `git-ranker-client/src/shared/types/api.ts` 상단 주석으로 명시했다.

## Skill Consideration

이번 작업은 client 계약 단일화 자체에 집중한다. backend OpenAPI와 client 타입을 대조하는 반복 루프는 이후 `api-contract-sync` skill 후보 입력으로 남긴다.
