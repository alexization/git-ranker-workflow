# 2026-03-26-grb-02-backend-verification-hardening

- Issue ID: `GRB-02`
- GitHub Issue: `alexization/git-ranker#74`
- GitHub PR: `alexization/git-ranker#75`
- Status: `Completed`
- Repository: `git-ranker`
- Branch Name: `feat/grb-02-backend-verification-hardening`
- Commit: `67234f6`
- Task Slug: `2026-03-26-grb-02-backend-verification-hardening`

## Problem

`git-ranker`의 `./gradlew integrationTest`는 Docker daemon이 내려가 있으면 Testcontainers 초기화 단계에서 바로 `ContainerFetchException`과 `DockerClientProviderStrategy` 예외를 내고 실패한다. 현재 출력만으로는 환경 문제인지 코드 회귀인지 빠르게 구분하기 어렵다.

## Why Now

`GRB-02`는 backend 검증 루프를 하네스 친화적으로 만드는 작업이다. 이후 `GRW-05` 표준 검증 런타임과 ranking harness 검증이 안정적으로 동작하려면 Docker 의존 통합 테스트가 fail-fast 하면서도 원인을 명확히 드러내야 한다.

## Scope

- Docker preflight를 `integrationTest` 실행 전에 추가
- Docker 미가동/미설치 상황에서 명확한 실패 메시지 제공
- unit, coverage, integration 검증 절차를 backend 문서에 정리
- 실제 로컬 환경에서 unit/coverage와 integration 경로를 재검증

## Non-scope

- 비즈니스 기능 변경
- Testcontainers 기반 통합 테스트 구조 전면 리팩터링
- workflow 런타임 또는 CI 파이프라인 변경

## Write Scope

- `git-ranker` Gradle/test/doc 관련 파일
- `docs/exec-plans/`

## Outputs

- Docker preflight Gradle task 또는 동등한 fail-fast 실행 경로
- preflight 메시지를 뒷받침하는 테스트 자산
- backend 검증 절차 문서
- `GRB-02` 실행 기록

현재 산출물:

- `git-ranker/build.gradle`의 `verifyDockerAvailable`, `integrationTest` 연결
- `git-ranker/src/test/java/com/gitranker/api/testsupport/DockerPreflightCheck.java`
- `git-ranker/src/test/java/com/gitranker/api/testsupport/DockerPreflightMain.java`
- `git-ranker/src/test/java/com/gitranker/api/testsupport/DockerPreflightCheckTest.java`
- `git-ranker/README.md`의 verification 절차 섹션

## Verification

- `docker version`으로 현재 Docker daemon 상태 확인
- `./gradlew test jacocoTestCoverageVerification`
- `./gradlew integrationTest`
- Docker 미가동 환경에서 preflight 실패 메시지 확인

결과 요약:

- `docker version`: OrbStack context `orbstack`, server API `1.51` 확인
- `./gradlew test --tests "com.gitranker.api.testsupport.DockerPreflightCheckTest"`: 성공
- `./gradlew test jacocoTestCoverageVerification`: 성공
- `./gradlew verifyDockerAvailable`:
  - Docker 미기동 상태: 명확한 fail-fast 메시지 확인
  - Docker 기동 상태: `Docker preflight passed. context=orbstack serverApiVersion=1.51`
- `./gradlew integrationTest`:
  - Docker 미기동 상태: Testcontainers 진입 전 preflight 단계에서 실패
  - Docker 기동 상태: 성공

## Evidence

작업 중 수집한 명령 결과 요약과 문서 갱신 경로를 남긴다. 브라우저, 로그, 메트릭 artifact는 이번 Issue 범위가 아니다.

- baseline 확인:
  - `docker version` -> daemon 연결 실패
  - `./gradlew integrationTest` -> `ContainerFetchException`, `DockerClientProviderStrategy`
- 변경 후 확인:
  - `./gradlew verifyDockerAvailable` -> Docker 미기동 시 원인/다음 단계가 포함된 fail-fast 메시지 출력
  - `./gradlew integrationTest` -> Docker 미기동 시 `verifyDockerAvailable` 단계에서 즉시 실패
  - `docker version` -> OrbStack 실행 후 server 연결 성공
  - `./gradlew verifyDockerAvailable` -> 성공
  - `./gradlew integrationTest` -> 성공

## Risks or Blockers

- 로컬 Docker context 종류에 따라 실패 문구 일부가 다를 수 있다.
- `docker version --format "{{.Server.APIVersion}}"`를 지원하지 않는 매우 오래된 Docker CLI는 별도 보정이 필요할 수 있다.

## Next Preconditions

- `GRW-05`: backend integration preflight를 표준 runtime 검증 순서에 연결
- `GRB-03`: 결정적 seed 검증 시 통합 테스트 환경 전제조건으로 재사용

## Docs Updated

- `docs/exec-plans/completed/2026-03-26-grb-02-backend-verification-hardening.md`
- `git-ranker/README.md`

## Skill Consideration

Docker preflight와 unit/coverage/integration 분리 절차는 Spring Boot 검증 루프에서 반복될 가능성이 높다. 이번 작업 결과는 이후 project-specific verification skill이나 runtime runbook 입력으로 재사용할 수 있다.
