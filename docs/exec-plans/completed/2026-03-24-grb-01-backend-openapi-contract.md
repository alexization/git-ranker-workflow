# 2026-03-24-grb-01-backend-openapi-contract

- Issue ID: `GRB-01`
- GitHub Issue: `alexization/git-ranker#72`
- GitHub PR: `alexization/git-ranker#73`
- Status: `Completed`
- Repository: `git-ranker`
- Branch Name: `feat/grb-01-openapi-contract`
- Merged Commit: `8b434a6`
- Task Slug: `2026-03-24-grb-01-backend-openapi-contract`

## Problem

`git-ranker`에는 frontend/workflow가 기준 계약으로 소비할 수 있는 OpenAPI 산출물이 없다. 공개 API 계약을 코드 탐색에만 의존하면 타입 드리프트와 문서/계약 불일치가 계속 발생한다.

## Why Now

`GRB-01`은 `GRC-01`과 `GRW-03`의 선행 작업이다. backend에서 먼저 기계가 읽을 수 있는 계약과 재생성 루프를 고정해야 후속 저장소가 같은 source of truth를 참조할 수 있다.

## Scope

- `./git-ranker`에 OpenAPI/Swagger 생성 기반 추가
- `/api/v1/**` 전체 엔드포인트 계약 생성
- 저장소에 추적되는 `openapi.json` 기준 파일 추가
- `/v3/api-docs`와 Swagger UI 노출
- 생성 절차와 검증 절차 문서화

## Non-scope

- 프런트엔드 generated client 생성
- API 비즈니스 로직 변경
- workflow에서 계약 소비 자동화 구현

## Write Scope

- `git-ranker` build/config/test/doc 관련 파일
- `docs/exec-plans/`

## Outputs

- backend OpenAPI/Swagger 설정
- backend `openapi.json` 기준 파일
- backend 생성/검증 절차 문서
- `GRB-01` 실행 기록

## Verification

- OpenAPI 생성 명령 실행
- 생성 JSON에 `/api/v1/**` 주요 경로 포함 여부 확인
- `/v3/api-docs`와 Swagger UI 노출 확인
- 관련 테스트 실행

결과 요약:

- `./gradlew test --tests "com.gitranker.api.docs.OpenApiDocsTest"`: 성공
- `./gradlew generateOpenApiSpec`: 성공
- `./gradlew test`: 성공
- `rg -n '"/api/v1/(...)' docs/openapi/openapi.json`: 주요 `/api/v1/**` 경로 확인
- `git-ranker` `develop` 기준 최종 반영 SHA: `8b434a6`

## Evidence

문서/설정 중심 작업이므로 명령 결과 요약과 생성 파일 경로를 남긴다. 브라우저 artifact는 남기지 않았고, 대신 테스트와 생성 산출물로 확인했다.

- 생성 파일: `git-ranker/docs/openapi/openapi.json`
- 런타임 경로: `git-ranker` 기준 `/v3/api-docs`, `/swagger-ui/index.html`
- 생성 명령: `git-ranker` 기준 `./gradlew generateOpenApiSpec`
- merge 기준 PR/commit: `alexization/git-ranker#73`, `8b434a6`

## Risks or Blockers

- springdoc 도입 시 보안 허용 경로와 충돌할 수 있다.
- 계약 생성 루프가 실제 운영 시크릿 없이 재현 가능해야 한다.
- 인증/응답 래퍼가 기대보다 덜 풍부하게 표현되면 추가 문서 보강이 필요할 수 있다.

## Next Preconditions

- `GRC-01`: backend `openapi.json`을 기준으로 계약 타입 단일화
- `GRW-03`: workflow 계약 문서 수집 시 backend 기준 계약 참조

## Docs Updated

- `docs/exec-plans/completed/2026-03-24-grb-01-backend-openapi-contract.md`
- `git-ranker/docs/openapi/README.md`
- `git-ranker/README.md`

## Skill Consideration

이번 작업은 반복 실행 가능한 계약 생성/검증 절차를 만든다. 생성 명령과 확인 루프는 이후 freshness/check skill 후보 입력으로 재사용 가능하다.
