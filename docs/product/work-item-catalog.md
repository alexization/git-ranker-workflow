# Work Item Catalog

이 문서는 현재 하네스 시스템의 active/pending 작업 카탈로그다.

## 사용 순서

1. [docs/operations/sdd-spec-policy.md](../operations/sdd-spec-policy.md)를 읽는다.
2. [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 읽는다.
3. 아래에서 해당 work item의 선행조건, write scope, 기본 결정을 확인한다.
4. `docs/specs/active/YYYY-MM-DD-<slug>.md`를 만든다.
5. 작업 후에는 문서를 `docs/specs/completed/`로 이동한다.

## Workflow Track

### GRW-26. federated ownership model alignment

- 저장소: `git-ranker-workflow`
- 상태: `pending`
- 선행조건: `GRB-04`, `GRC-05`
- 권장 write scope: `docs/product`, `docs/architecture`, `docs/operations`, `.codex/skills/`
- 기본 결정: workflow는 orchestration만 소유하고, repo-specific implementation knowledge는 target repo로 내린다.
- 핵심 작업: ownership matrix, workflow-vs-repo 책임 경계, workflow-local skill의 thin-layer 기준, migration exit criteria를 stable source of truth에 반영한다.
- 비범위: backend/frontend repo 실제 파일 생성, repo-local CI 구현
- 검증: architecture/product/operations 문서 용어 정렬, workflow-local knowledge duplication no-go 확인

### GRW-27. federated repo handoff contract

- 저장소: `git-ranker-workflow`
- 상태: `pending`
- 선행조건: `GRW-26`
- 권장 write scope: `docs/architecture`, `docs/operations`, `docs/product`, 필요 시 `.codex/skills/`
- 기본 결정: workflow는 target repo에 필요한 최소 handoff만 남기고, 각 repo는 `AGENTS.md`를 canonical entrypoint로 노출해야 한다.
- 핵심 작업: `AGENTS.md` requirement, handoff summary shape, local skill discovery order, repo bootstrap checklist를 정의한다.
- 비범위: backend/frontend repo 실제 bootstrap 수행
- 검증: representative handoff simulation, required `AGENTS.md` checklist review

## Backend Track

### GRB-04. backend verification contract reset

- 저장소: `git-ranker`
- 상태: `active`
- 선행조건: 없음
- 권장 write scope: backend 검증 문서, build/test entrypoint, 필요 최소한의 preflight
- 기본 결정: workflow의 상위 verification semantics는 fixed로 보고, backend repo는 자신의 verification surface를 repo-local canonical source로 정렬한다.
- 핵심 작업: 현재 backend 검증 명령, fail-fast 조건, 환경 전제, 결과 해석 기준을 backend repo 기준으로 정리한다.
- 비범위: 새 기능 구현
- 검증: contract에 적힌 명령과 실제 실행 결과 대조

### GRB-06. backend test/CI removal

- 저장소: `git-ranker`
- 상태: `active`
- 선행조건: 없음
- 권장 write scope: `src/test/`, `build.gradle`, `.github/workflows/`
- 기본 결정: legacy test/CI surface는 repo-local verification/TDD 재구성 전까지 baseline reset 대상으로 본다.
- 핵심 작업: 기존 backend test source/resource tree와 obsolete test/integration task surface를 제거하고, rebuild preconditions를 정리한다.
- 비범위: 새 테스트 코드 작성, 새 CI 검증 로직 도입, `src/main/` production 동작 변경
- 검증: `./gradlew test`, `./gradlew build`, `git diff --check`

### GRB-07. backend `AGENTS.md` entrypoint and knowledge bootstrap

- 저장소: `git-ranker`
- 상태: `pending`
- 선행조건: `GRB-04`, `GRW-27`
- 권장 write scope: backend entry docs, `.codex/skills/`, verification entry docs
- 기본 결정: Spring Boot 구현 규칙과 backend-only skill은 workflow가 아니라 backend repo가 소유한다.

### GRB-05. backend GC baseline 정렬

- 저장소: `git-ranker`
- 상태: `pending`
- 선행조건: `GRB-04`, `GRB-07`
- 권장 write scope: `build.gradle`, backend static analysis config, `.github/workflows/`, backend README 또는 verification entry docs
- 기본 결정: backend GC는 workflow repo가 아니라 backend repo의 Gradle task와 GitHub Actions가 소유한다.

## Client Track

### GRC-05. frontend verification contract 정규화

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: 없음
- 권장 write scope: frontend 검증 문서, build/lint/typecheck entrypoint
- 기본 결정: workflow의 상위 verification semantics는 fixed로 보고, frontend repo는 자신의 verification surface를 repo-local canonical source로 정리한다.

### GRC-07. frontend `AGENTS.md` entrypoint and knowledge bootstrap

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: `GRC-05`, `GRW-27`
- 권장 write scope: frontend entry docs, `.codex/skills/`, verification entry docs
- 기본 결정: React/Next 구현 규칙과 frontend-only knowledge surface는 workflow가 아니라 frontend repo가 소유한다.

### GRC-06. frontend GC baseline 정렬

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: `GRC-05`, `GRC-07`
- 권장 write scope: `package.json`, frontend static analysis config, `.github/workflows/`, frontend README 또는 repo entry docs
- 기본 결정: frontend GC는 repo-local npm scripts와 GitHub Actions가 소유한다.
