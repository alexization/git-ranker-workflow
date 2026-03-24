# 2026-03-24 Readiness Evidence

- 확인일: `2026-03-24` (KST)
- 대상 저장소: `git-ranker-workflow`, `git-ranker`, `git-ranker-client`
- 목적: `GRW-02` readiness 기준선 문서의 판단 근거 보관

## git-ranker-workflow

### 문서 구조와 discoverability

- 명령: `find .github -maxdepth 3 -type f | sort`
  - 결과: `.github/ISSUE_TEMPLATE/config.yml`, `.github/ISSUE_TEMPLATE/engineering_task.yml`, `.github/PULL_REQUEST_TEMPLATE.md`
  - 메모: Issue/PR 템플릿은 있지만 workflow용 CI나 freshness check는 아직 없다.

- 명령: `rg --files docs`
  - 결과: `docs/architecture/control-plane-map.md`, `docs/operations/workflow-governance.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, `docs/exec-plans/*` 중심으로만 본문이 있다.
  - 메모: `docs/domain/`, `docs/reliability/`, `docs/security/`, `docs/generated/`는 아직 README 인덱스만 있다.

- 명령: `find . -maxdepth 2 \( -name 'Makefile' -o -name 'docker-compose.yml' -o -name 'compose.yml' -o -name 'package.json' -o -name 'build.gradle' -o -name 'scripts' -o -name 'skills' \) | sort`
  - 결과: workflow 루트에는 runtime/script/skill 자산이 없고, 하위 앱 저장소의 `docker-compose.yml`, `package.json`, `build.gradle`만 잡힌다.
  - 메모: control-plane 문서는 생겼지만 실행 런타임과 자동 검증은 아직 전이다.

## git-ranker

### 테스트와 정적 가드레일

- 명령: `./gradlew test jacocoTestReport`
  - 결과: `BUILD SUCCESSFUL`
  - 메모: 단위 테스트와 JaCoCo 리포트 생성은 현재 로컬에서 통과한다.

- 명령: `./gradlew integrationTest`
  - 결과: `ActivityLogRepositoryIT`, `UserRepositoryIT` 실패
  - 핵심 오류: `org.testcontainers.containers.ContainerFetchException`, `DockerClientProviderStrategy`
  - 메모: Testcontainers 기반 통합 테스트는 현재 환경에서 바로 실행되지 않는다. Docker preflight나 오류 안내 보강이 필요하다.

- 명령: `rg --files git-ranker/src/test`
  - 결과: controller/service/repository/logging/auth/badge/ranking 테스트와 `ArchitectureGuardrailTest` 포함
  - 메모: 테스트 자산은 존재하며 범위도 넓다.

- 명령: `rg -n "DockerClientProviderStrategy|testcontainers|integrationTest|api.version|jacocoTestCoverageVerification|minimum = 0.45" git-ranker/build.gradle git-ranker/src/test -g '!build'`
  - 결과: `integrationTest` task, `api.version=1.44`, Testcontainers 의존성, `jacocoTestCoverageVerification` 최소 `0.45` 확인
  - 메모: 정적/품질 가드레일은 정의돼 있으나 Docker 환경 가정이 강하다.

- 명령: `sed -n '1,220p' git-ranker/src/test/java/com/gitranker/api/architecture/ArchitectureGuardrailTest.java`
  - 결과: domain/infrastructure/global 패키지가 batch에 의존하지 않도록 ArchUnit rule 정의
  - 메모: 구조 경계에 대한 guardrail이 코드로 존재한다.

### API 계약

- 명령: `rg -n "springdoc|openapi|swagger|@OpenAPIDefinition|/v3/api-docs" git-ranker -g '!build'`
  - 결과: 매치 없음
  - 메모: OpenAPI나 생성 가능한 API 계약 자산은 아직 없다.

### 운영 재현성과 관측 가능성

- 명령: `docker compose -f docker-compose.yml config`
  - 결과: compose 해석은 성공했지만 `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `GITHUB_CLIENT_ID`, `JWT_SECRET`, `GF_SECURITY_ADMIN_USER` 등 다수 env가 빈 문자열로 대체된다는 경고 출력
  - 메모: compose 자산은 있으나 `.env.example`이나 README 기반 환경값 안내가 없다.

- 명령: `rg -n "management:|prometheus|exposure|actuator|metrics" git-ranker/src/main/resources/application*.yml`
  - 결과: `application.yml`, `application-prod.yml`에서 actuator, prometheus, metrics 노출 설정 확인
  - 메모: 관측 자산은 코드와 설정 레벨에서 준비돼 있다.

- 명령: `find git-ranker -maxdepth 2 -name '.env*' | sort`
  - 결과: 매치 없음
  - 메모: 환경 변수 샘플 파일이 없다.

- 명령: `find git-ranker -maxdepth 2 \( -name '.env*' -o -name 'docker-compose.yml' -o -name 'prometheus.yml' -o -name 'loki-config.yml' -o -name 'dashboard.yml' -o -name '*.md' \) | sort`
  - 결과: `README.md`, `docker-compose.yml`, `prometheus.yml`, `loki-config.yml`, `dashboard.yml` 확인
  - 메모: 런타임과 관측 설정 파일은 존재한다.

- 명령: `find git-ranker/.github -maxdepth 3 -type f | sort`
  - 결과: issue template, `ci.yml`, `deploy.yml`, `quality-gate.yml`
  - 메모: CI와 quality gate는 이미 저장소에 연결돼 있다.

## git-ranker-client

### 테스트와 정적 가드레일

- 명령: `npm run lint`
  - 결과: 종료 코드는 `0`, 총 `27 warnings`
  - 주요 경고: `react-hooks/set-state-in-effect`, `react-hooks/purity`, `react-hooks/use-memo`, `@typescript-eslint/no-unused-vars`, `jsx-a11y/alt-text`, `@next/next/no-html-link-for-pages`
  - 메모: lint 파이프라인은 있지만 핵심 규칙 다수가 warning으로 완화돼 있어 correctness 가드레일이 약하다.

- 명령: `npx tsc --noEmit`
  - 결과: 성공, 출력 없음
  - 메모: 현재 타입 검사는 통과한다.

- 명령: `npm run build`
  - 결과: 실패
  - 핵심 오류: `next/font: error: Failed to fetch 'JetBrains Mono' from Google Fonts`
  - 추가 경고: `"middleware" file convention is deprecated. Please use "proxy" instead.`
  - 메모: production build가 외부 네트워크 폰트 의존성과 deprecated convention에 영향을 받는다.

- 명령: `rg --files git-ranker-client | rg '(test|spec|playwright|vitest|jest|cypress)'`
  - 결과: 매치 없음
  - 메모: 자동화 테스트 자산이 없다.

- 명령: `sed -n '1,240p' git-ranker-client/eslint.config.mjs`
  - 결과: `react-hooks/*`, TypeScript, Next 관련 규칙 다수를 `warn`으로 완화
  - 메모: CI에서 `npm run lint`가 통과해도 품질 리스크가 남을 수 있다.

### API 계약

- 명령: `find git-ranker-client/src/shared/types git-ranker-client/src/shared/lib -maxdepth 2 -type f | sort`
  - 결과: `src/shared/types/api.ts`, `src/shared/lib/validations.ts` 동시 존재
  - 메모: 계약 정의가 둘로 나뉘어 있다.

- 명령: `rg -n "EMERALD|tierSchema|ApiResponseLegacy|resultType|result" git-ranker-client/src/shared/types/api.ts git-ranker-client/src/shared/lib/validations.ts`
  - 결과: `api.ts`의 `Tier`에는 `EMERALD`가 있으나 `validations.ts`의 `tierSchema`에는 `EMERALD`가 없다. `ApiResponse`와 `ApiResponseLegacy`도 동시 존재한다.
  - 메모: 계약 drift가 실제로 존재한다.

### 운영 재현성과 관측 가능성

- 명령: `docker compose -f docker-compose.yml config`
  - 결과: compose 해석은 성공했지만 `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_BASE_URL`가 빈 문자열로 대체된다는 경고 출력
  - 메모: runtime 자산은 있으나 env 샘플과 명시적 문서가 없다.

- 명령: `find git-ranker-client -maxdepth 2 -name '.env*' | sort`
  - 결과: 매치 없음
  - 메모: 환경 변수 샘플 파일이 없다.

- 명령: `find git-ranker-client -maxdepth 2 \( -name '.env*' -o -name 'docker-compose.yml' -o -name '*.md' -o -name 'middleware.ts' -o -name 'proxy.ts' \) | sort`
  - 결과: `README.md`, `docker-compose.yml`, `src/middleware.ts`
  - 메모: `proxy.ts`가 아니라 deprecated `middleware.ts`를 사용 중이다.

- 명령: `rg -n "playwright|vitest|jest|cypress|storybook|openapi|swagger|sentry|proxy\\.ts|middleware\\.ts|eslint|tsc --noEmit" git-ranker-client`
  - 결과: `sentry.*.config.ts`, `src/middleware.ts`, `eslint.config.mjs` 확인
  - 메모: Sentry 설정 파일은 있으나, 테스트/계약 산출물은 없다.

### 문서와 discoverability

- 명령: `sed -n '1,260p' git-ranker-client/README.md`
  - 결과: `create-next-app` 기본 README 본문
  - 메모: 실제 라우트, env, build 제약, 배포/운영 설명이 없다.

- 명령: `find git-ranker-client/.github -maxdepth 3 -type f | sort`
  - 결과: issue template, `ci.yml`, `deploy.yml`
  - 메모: GitHub workflow는 있으나 문서화 수준은 낮다.
