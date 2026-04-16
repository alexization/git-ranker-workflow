# Strengthen git-ranker core loop unit tests

- Task ID: `task-gitranker-core-loop-unit-tests`
- Primary Repo: `git-ranker`
- Status: `draft`

## Request

- `git-ranker`의 물리적 피드백 및 검증 루프에 대해 현재 구현된 로직을 기준으로 unit 테스트를 보강한다.
- 이미 존재하는 테스트 코드는 다시 검토해 개선하거나 추가해야 할 케이스를 반영한다.
- happy path만이 아니라 예외 케이스, 비즈니스 로직 검증, 경계값, fallback, side effect, non-interaction까지 놓치기 쉬운 부분을 세분화해 테스트로 고정한다.

## Problem

- 현재 `git-ranker`의 test baseline은 일부 service 중심으로만 구성되어 있어 핵심 피드백/검증 루프를 이루는 value object, batch, GitHub infra, orchestration 로직의 회귀 위험이 남아 있다.
- 기존 테스트도 happy path 위주인 곳이 있어 예외 번역, 경계값, null/empty fallback, metric 또는 repository side effect 누락 여부를 충분히 검증하지 못한다.
- 이 상태에서는 도메인 규칙이나 배치 루프를 수정할 때 의도하지 않은 동작 변화가 CI에서 충분히 드러나지 않을 수 있다.

## Goals

- 기존 unit 테스트를 재검토해 약한 assertion, 누락된 분기, 빠진 예외 케이스를 보강한다.
- 핵심 피드백/검증 루프에 해당하는 미테스트 로직에 대해 JUnit 5 + Mockito 중심의 좁은 unit 테스트를 추가한다.
- 각 대상 로직에 대해 정상 흐름, 경계값, null/empty/default, 예외 번역, side effect, non-interaction, time-dependent branch, mapping/invariant를 검증한다.
- 최종적으로 `git-ranker`에서 `./gradlew test`가 green 이어야 한다.

## Non-goals

- controller, security filter, `GlobalExceptionHandler`, config, repository integration, Micrometer wiring 테스트는 이번 작업에 포함하지 않는다.
- JaCoCo, coverage gate, CI workflow, Gradle dependency 변경은 이번 작업에 포함하지 않는다.
- production API, endpoint, batch schedule, 메시지 key, runtime contract 변경은 목표가 아니다.
- 테스트 고립이 막히는 경우를 제외하고 production code 리팩터링 자체를 이번 작업의 주목적으로 삼지 않는다.

## Constraints

- root `AGENTS.md` workflow 계약을 따른다. 승인된 spec 없이 phase 실행이나 구현을 시작하지 않는다.
- task state와 phase state는 `python3 scripts/workflow.py ...` 명령으로만 전이한다.
- 구현 변경에는 대응 테스트가 필요하며, 이번 작업은 `test_policy.mode=require_tests`를 따른다.
- canonical plan은 `workflows/tasks/task-gitranker-core-loop-unit-tests/phases.json` 하나다.
- 테스트 수준은 `JUnit 5 + Mockito` 중심의 좁은 unit로 고정하고 `@WebMvcTest`, `@SpringBootTest`는 쓰지 않는다.
- 수정은 active phase의 `allowed_write_paths` 안에서만 수행한다.

## Acceptance

- 기존 테스트 보강과 신규 핵심 루프 테스트가 `src/test/java` 아래에 추가되어 있다.
- 기존 테스트 보강 범위에는 최소한 `ActivityLogServiceTest`, `AuthServiceTest`, `UserPersistenceServiceTest`, `UserRegistrationServiceTest`, `UserRefreshServiceTest`, `UserQueryServiceTest`, `RankingServiceTest`, `RankingRecalculationServiceTest`, `BadgeServiceTest`, `BadgeFormatterTest`, `SvgBadgeRendererTest`, `TimeUtilsTest`, `UserDeletionServiceTest`가 포함된다.
- 신규 테스트 범위에는 최소한 `ActivityStatistics`, `Score`, `RankInfo`, `User`, `ActivityLog`, `ActivityLogOrchestrator`, batch strategy/processor/listener/tasklet/reader/writer/scheduler, GitHub service/mapper/error handler/client/token/query/dto 계열이 포함된다.
- 테스트는 happy path뿐 아니라 예외, 경계값, 비즈니스 규칙, fallback, side effect, non-interaction을 검증한다.
- `git-ranker`에서 `./gradlew test`가 통과한다.

## Socratic Clarification Log

- Q: 이번 task의 테스트 범위를 어디까지 잠글까요?
- A: 핵심 피드백/검증 루프를 우선 완결하고, trivial DTO/config/entity/interface 전수 테스트는 제외합니다.
- Decision: 핵심 피드백/검증 루프와 그 주변의 기존 unit test 보강만 이번 task 범위로 잠근다.

- Q: 테스트 수준은 어디까지 허용할까요?
- A: 좁은 unit 중심으로 가고 외부 I/O와 전체 Spring context 부팅은 피합니다.
- Decision: `JUnit 5 + Mockito` 중심의 좁은 unit test로 고정한다.

- Q: 기존 테스트 코드도 다시 검토하고 보강할까요?
- A: 네. 이미 있는 테스트도 다시 확인해 개선하거나 추가해야 할 케이스를 반영합니다.
- Decision: 신규 테스트 추가와 함께 기존 test file의 약한 assertion과 누락 분기를 보강한다.

- Q: happy path만 작성하면 되나요?
- A: 아니요. 예외 케이스, 필요한 비즈니스 로직 검증, 놓치기 쉬운 케이스까지 모두 고려해 세분화합니다.
- Decision: 각 대상 로직은 정상 흐름, 예외, 경계값, fallback, side effect, non-interaction, invariant를 포함해 테스트한다.

## Approval

- Actor: `user`
- Timestamp: `2026-04-16T05:47:28+00:00`
- Note: User approved the detailed unit-test implementation plan in chat.
