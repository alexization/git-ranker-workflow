# 2026-03-25-grw-04-frontend-routes-data-flow-docs

- Issue ID: `GRW-04`
- GitHub Issue: `#16`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-04-frontend-routes-data-flow-docs`
- Task Slug: `2026-03-25-grw-04-frontend-routes-data-flow-docs`

## Problem

`git-ranker-client`의 라우트 구조, locale rewrite, 랭킹 조회 상태 흐름, 사용자 상세 모달, auth callback, 주요 env와 외부 의존성이 코드에 흩어져 있다. 이 상태에서는 후속 harness와 frontend 작업이 같은 기준 경로와 런타임 전제를 공유하기 어렵다.

## Why Now

`GRW-S02`, `GRC-03`, `GRC-04`는 모두 frontend의 현재 route entry, API 호출, auth callback 경로, env 의존성을 source of truth로 참조해야 한다. backend 도메인 문서는 이미 정리됐지만, client 쪽 구조와 데이터 흐름은 아직 workflow 문서에 고정되지 않았다.

## Scope

- `git-ranker-client`의 route map 정리
- ranking page의 상태와 API 흐름 정리
- user detail modal의 prefetch/query/open-close 흐름 정리
- auth callback과 locale routing 흐름 정리
- 주요 env와 외부 의존성 정리
- `GRW-04` 실행/완료 기록 남기기

## Non-scope

- `git-ranker-client` 코드 수정
- Playwright 테스트, build/runtime 변경, lint 정리
- backend API나 OAuth 설정 변경

## Write Scope

- `docs/architecture/`
- `docs/domain/`
- `docs/operations/`
- `docs/exec-plans/`

## Outputs

- `docs/architecture/frontend-route-map.md`
- `docs/domain/frontend-data-flows.md`
- `docs/operations/frontend-runtime-reference.md`
- `GRW-04` 실행/완료 기록

## Verification

- `find docs/architecture docs/domain docs/operations -maxdepth 1 -type f | sort`
- `rg -n "route|랭킹|사용자 상세|auth callback|NEXT_PUBLIC_API_URL|NEXT_PUBLIC_BASE_URL|middleware" docs/architecture docs/domain docs/operations`
- 문서에 연결한 `git-ranker-client` 코드 경로와 실제 구현 대조
- `perl -nle 'while(/\\]\\(([^)#]+)(?:#[^)]+)?\\)/g){print "$ARGV\\t$1"}' docs/architecture/*.md docs/domain/*.md docs/operations/*.md | while IFS=$'\\t' read -r src target; do dir=$(dirname "$src"); if ! test -e "$dir/$target"; then printf 'missing %s -> %s\n' "$src" "$target"; fi; done`

결과 요약:

- `find docs/architecture docs/domain docs/operations -maxdepth 1 -type f | sort`: architecture/domain/operations 각 디렉터리에 `frontend-route-map.md`, `frontend-data-flows.md`, `frontend-runtime-reference.md`가 기대 경로로 생성된 것을 확인했다.
- `rg -n "route|랭킹|사용자 상세|auth callback|NEXT_PUBLIC_API_URL|NEXT_PUBLIC_BASE_URL|middleware" docs/architecture docs/domain docs/operations`: route map, ranking/modal/callback 흐름, env/runtime 문서가 모두 grep 결과에 포함되는 것을 확인했다.
- relative link check: `docs/architecture/*.md`, `docs/domain/*.md`, `docs/operations/*.md` 안의 상대 링크에서 누락 경로가 없었다.
- 코드 교차 검토: backend의 `authorized-redirect-uri`가 `/auth/callback`을 가리키는 것, unused ranking prefetch 경로가 `ranking-section.tsx`에만 남아 있는 것, analytics helper가 `/api/analytics/*`를 참조하지만 실제 route는 없는 것을 확인했다.
- GitHub flow: `gh issue create --repo alexization/git-ranker-workflow ...`로 `GRW-04` 이슈 `#16`을 생성했다.

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 `git-ranker-client` 코드 경로, 검증 명령 결과, GitHub issue 생성 결과를 exec plan에 남긴다.

## Risks or Blockers

- `src/app/auth/callback/page.tsx`와 `src/app/oauth2/redirect/page.tsx`가 중복 구현이라 drift 위험이 있다.
- `src/app/ranking/page.tsx`는 fetch 실패를 `isError`로 분기하지 않아 empty state처럼 보일 수 있다.
- `src/features/ranking/components/ranking-section.tsx`는 현재 route에서 사용되지 않는 대체 구현이라, future refactor 시 source of truth와 구현이 다시 어긋날 수 있다.
- `src/app/users/[username]/opengraph-image.tsx`는 비-localized URL로 생성되고 middleware locale redirect에 의존한다.
- frontend 구조가 이후 빠르게 바뀌면 freshness가 떨어질 수 있다.

## Next Preconditions

- `GRW-S02`: 병렬 작업 분할과 contract sync skill이 route/data flow 문서를 입력으로 참조할 수 있어야 한다.
- `GRC-03`: build/runtime 하네스 친화화 시 env와 외부 네트워크 의존성 문서를 참조해야 한다.
- `GRC-04`: ranking harness 도입 시 ranking page, modal, callback 흐름을 그대로 테스트 시나리오에 연결해야 한다.

## Docs Updated

- `docs/architecture/README.md`
- `docs/architecture/frontend-route-map.md`
- `docs/domain/README.md`
- `docs/domain/frontend-data-flows.md`
- `docs/operations/README.md`
- `docs/operations/frontend-runtime-reference.md`
- `docs/exec-plans/completed/2026-03-25-grw-04-frontend-routes-data-flow-docs.md`

## Skill Consideration

이번 Issue는 frontend source of truth를 수집하는 단계다. 아직 skill을 만들 범위는 아니지만, `GRW-S02`와 `GRC-04`가 재사용할 route/data flow 기준 입력을 만든다.
