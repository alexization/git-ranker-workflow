# 2026-03-26-grc-02-frontend-lint-debt

- Issue ID: `GRC-02`
- GitHub Issue: `alexization/git-ranker-client#4`
- GitHub PR: `alexization/git-ranker-client#5`
- Status: `Completed`
- Repository: `git-ranker-client`
- Branch Name: `feat/grc-02-frontend-lint-debt`
- Merged Commit: `5f6a6dd`
- Task Slug: `2026-03-26-grc-02-frontend-lint-debt`

## Problem

`git-ranker-client`의 `npm run lint`는 error 없이 통과하지만 warning이 26개 누적돼 있다. 이 중 `react-hooks/set-state-in-effect`, `react-hooks/static-components`, `react-hooks/purity`, `react-hooks/use-memo`는 hydration, 렌더링 안정성, hook purity에 직접 영향을 줄 수 있어 신호 품질이 낮다.

## Why Now

`GRC-02`는 `GRC-03` build/runtime harness 친화화와 `GRC-04` Playwright harness 도입 전에 프런트 코드의 정적 경고 신호를 먼저 정리하는 작업이다. warning이 그대로 남아 있으면 후속 작업에서 새 회귀와 기존 debt를 구분하기 어렵다.

## Scope

- 현재 `npm run lint`가 보고하는 warning 전체를 정리한다.
- `react-hooks/set-state-in-effect`, `react-hooks/static-components`, `react-hooks/purity`, `react-hooks/use-memo` 경고를 우선 제거한다.
- 함께 드러난 `no-unused-vars`, `no-explicit-any`, `no-empty-object-type`, `no-require-imports`, `@next/next/no-html-link-for-pages` warning도 같은 PR에서 정리한다.
- ranking, user, badge, auth, home, shared component/hook/provider 경로의 동작을 유지하면서 lint 신호만 개선한다.

## Non-scope

- UI 디자인 개편
- Playwright 또는 단위 테스트 도입
- backend API 계약 변경
- build/runtime 정책 변경 자체

## Write Scope

- `git-ranker-client/src/app/`
- `git-ranker-client/src/features/`
- `git-ranker-client/src/shared/`
- `git-ranker-client/tailwind.config.ts`
- `docs/exec-plans/`

## Outputs

- warning 26개를 제거한 frontend 코드
- mounted/hydration/media-query 패턴 정리를 위한 shared hook/hook refactor
- static component, tooltip, link, config warning을 정리한 ranking/user/shared 코드
- `GRC-02` 실행 기록

현재 산출물:

- `git-ranker-client/src/shared/hooks/use-has-mounted.ts`
- `git-ranker-client/src/features/auth/store/auth-store.ts`
- `git-ranker-client/src/features/home/components/hero-section.tsx`
- `git-ranker-client/src/shared/hooks/use-media-query.ts`
- `git-ranker-client/src/shared/hooks/use-reduced-motion.ts`
- `git-ranker-client/src/shared/hooks/use-throttle.ts`
- `git-ranker-client/src/shared/providers/locale-provider.tsx`
- `git-ranker-client/src/shared/components/ui/heatmap-background.tsx`
- `git-ranker-client/src/app/users/[username]/user-profile-client.tsx`
- `git-ranker-client/src/features/user/components/badge-generator.tsx`
- `git-ranker-client/src/features/user/components/stats-chart-impl.tsx`
- `git-ranker-client/src/app/global-error.tsx`
- `git-ranker-client/src/features/ranking/api/ranking-service.ts`
- `git-ranker-client/src/shared/components/theme-toggle.tsx`
- `git-ranker-client/src/shared/components/command.tsx`
- `git-ranker-client/src/shared/components/input.tsx`
- `git-ranker-client/src/features/user/components/score-info-modal.tsx`
- `git-ranker-client/tailwind.config.ts`

## Verification

- `npm run lint`
- `npx tsc --noEmit`
- `npm run build`
- `git diff --stat`
- 변경 화면 수동 확인이 가능한 파일 단위 점검

결과 요약:

- `npm run lint`: 성공. warning 0개
- `npx tsc --noEmit`: 성공
- `npm run build`: 실패. `next/font/google`의 `JetBrains Mono` fetch와 `middleware.ts` deprecated convention 경고로 중단
- `git -C git-ranker-client show --stat --oneline 5f6a6dd -n 1`: merged `develop` 기준 최종 반영 확인. 18개 파일 수정, review feedback 포함
- 수동 화면 확인: 이번 턴에서는 브라우저 실행을 하지 않아 미실시

## Evidence

브라우저 artifact는 필수 범위가 아니므로, 이번 작업은 lint/typecheck/build 결과와 변경 파일 요약을 증거로 남긴다.

- 시작 기준: `npm run lint` warning 26개
- 종료 기준: `npm run lint` warning 0개
- 주요 정리 규칙:
  - `react-hooks/set-state-in-effect`
  - `react-hooks/static-components`
  - `react-hooks/purity`
  - `react-hooks/use-memo`
  - `@typescript-eslint/no-unused-vars`
  - `@typescript-eslint/no-explicit-any`
  - `@typescript-eslint/no-empty-object-type`
  - `@typescript-eslint/no-require-imports`
  - `@next/next/no-html-link-for-pages`
- 추가 확인:
  - `npm run build` 실패 원인은 기존 readiness baseline과 일치하는 Google Fonts 외부 fetch 및 `middleware.ts` deprecated convention이다.
  - merged client `develop` SHA: `5f6a6dd`

## Risks or Blockers

- `npm run build`는 여전히 Google Fonts 외부 fetch와 `middleware.ts` deprecated convention 때문에 실패한다. 이는 `GRC-03` 범위에서 해결할 항목이다.
- hydration/mounted 패턴을 여러 shared hook으로 이동했으므로 실제 브라우저에서 home/user/header 상호작용을 한 번 더 확인하는 것이 좋다.

## Next Preconditions

- `GRC-03`: warning debt가 정리된 상태에서 build/runtime 재현성 작업 진행
- `GRC-04`: cleaner lint baseline 위에서 Playwright harness 도입

## Docs Updated

- `docs/exec-plans/completed/2026-03-26-grc-02-frontend-lint-debt.md`
- 추가 source of truth 문서 업데이트는 하지 않았다. 기존 `docs/product/work-item-catalog.md`의 GRC-02 정의와 현재 결과가 일치하고, 남은 build/runtime 이슈는 후속 `GRC-03` 범위로 유지한다.

## Skill Consideration

이번 작업은 특정 lint 규칙을 이 저장소 패턴에 맞게 정리하는 일회성 코드 수정에 가깝다. 현재로서는 별도 skill로 분리하지 않고, 반복성이 확인되면 이후 frontend lint cleanup checklist 후보로만 남긴다.
