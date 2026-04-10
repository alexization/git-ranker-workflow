# Work Item Catalog

이 문서는 현재 하네스 시스템의 active/pending 작업 카탈로그다. 완료된 작업은 여기서 제거하고 `docs/exec-plans/completed/` historical record에서 읽는다.

현재 카탈로그는 workflow가 orchestration을 맡고, 각 app repo가 implementation knowledge를 소유하는 federation 구조로 전환하는 남은 작업만 다룬다.

## 사용 순서

1. [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 읽는다.
2. 아래에서 해당 Issue 항목의 선행조건, write scope, 기본 결정을 확인한다.
3. `docs/exec-plans/active/YYYY-MM-DD-<issue-id-lower>-<slug>.md`를 만든다.
4. 작업 후에는 문서를 `docs/exec-plans/completed/`로 이동한다.

## Workflow Track

### GRW-24. product federation roadmap cleanup

- 저장소: `git-ranker-workflow`
- 상태: `active`
- 선행조건: 없음
- 권장 write scope: `docs/product/`, `docs/exec-plans/active/`
- 기본 결정: product 문서는 completed backlog를 계속 들고 있지 않고, current transition work와 federation ownership 기준만 보여 준다.
- 핵심 작업: completed task를 product 문서에서 제거하고, workflow orchestration / app-repo implementation ownership 구조, `AGENTS.md` entrypoint, `GRW-18` active queue reconciliation 범위를 roadmap과 catalog에 반영한다.
- 비범위: backend/frontend 앱 코드 변경, target repo `AGENTS.md` 실제 생성
- 산출물: updated product docs, `GRW-24` active exec plan, publish-ready diff
- 검증: completed task reference 제거, federation wording/`AGENTS.md` hook 확인, `git diff --check`

### GRW-18. workflow pilot and active queue close-out reconciliation

- 저장소: `git-ranker-workflow`
- 상태: `active`
- 선행조건: 없음
- 권장 write scope: pilot 대상 문서, `docs/exec-plans`
- 기본 결정: foundation policy는 이미 fixed 상태로 보고, workflow repo는 current active exec plan queue를 주기적으로 점검해 completed로 가야 할 문서를 historical record로 옮긴다. 다만 app repo의 미완료 구현을 `GRW-18` issue에 흡수하지는 않는다.
- 핵심 작업: current active exec plan queue를 검토해 completed 조건을 이미 만족한 문서를 `completed/`로 이동하고, 아직 미완료인 작업은 workflow-only close-out 잔여인지 owner issue의 구현 잔여인지 구분한다. workflow artifact/state sync만 남은 항목은 `GRW-18` 과정에서 close-out까지 마무리한다.
- 비범위: backend/frontend 기능 개발, app repo의 미완료 구현을 `GRW-18` issue로 흡수하는 것
- 산출물: reconciled pilot exec plan, active queue review 결과, moved completed exec plans, verification/review/feedback close-out 근거
- 검증: active/completed exec plan 상태, linked GitHub issue/PR 상태, latest verification/review evidence 정합성 확인, current active queue triage 결과

### GRW-26. federated ownership model alignment

- 저장소: `git-ranker-workflow`
- 상태: `pending`
- 선행조건: `GRW-18`, `GRB-04`, `GRC-05`
- 권장 write scope: `docs/product`, `docs/architecture`, `docs/operations`, `.codex/skills/`
- 기본 결정: workflow는 orchestration만 소유하고, repo-specific implementation knowledge는 target repo로 내린다.
- 핵심 작업: ownership matrix, workflow-vs-repo 책임 경계, workflow-local skill의 thin-layer 기준, migration exit criteria를 stable source of truth에 반영한다.
- 비범위: backend/frontend repo 실제 파일 생성, repo-local CI 구현
- 산출물: federation ownership source of truth, migration checklist, updated workflow skill ownership rules
- 검증: architecture/product/operations 문서 용어 정렬, workflow-local knowledge duplication no-go 확인

### GRW-27. federated repo handoff contract

- 저장소: `git-ranker-workflow`
- 상태: `pending`
- 선행조건: `GRW-26`
- 권장 write scope: `docs/architecture`, `docs/operations`, `docs/product`, 필요 시 `.codex/skills/`
- 기본 결정: workflow는 target repo에 필요한 최소 handoff만 남기고, 각 repo는 `AGENTS.md`를 canonical entrypoint로 노출해야 한다.
- 핵심 작업: `AGENTS.md` requirement, handoff summary shape, local skill discovery order, repo bootstrap checklist를 정의한다.
- 비범위: backend/frontend repo 실제 bootstrap 수행
- 산출물: federated `AGENTS.md` handoff contract, repo bootstrap checklist, related workflow hook update
- 검증: backend/frontend representative handoff simulation, required `AGENTS.md` checklist review

## Backend Track

### GRB-04. backend verification contract reset

- 저장소: `git-ranker`
- 상태: `active`
- 선행조건: 없음
- 권장 write scope: backend 검증 문서, build/test entrypoint, 필요 최소한의 preflight
- 기본 결정: workflow의 상위 verification semantics는 이미 fixed로 보고, backend repo는 자신의 verification surface를 repo-local canonical source로 다시 정렬한다.
- 핵심 작업: 현재 backend 검증 명령, fail-fast 조건, 환경 전제, 결과 해석 기준을 backend repo 기준으로 정리하고 orphan lane을 제거한다.
- 비범위: 새 기능 구현
- 산출물: backend verification contract, 필요한 문서/스크립트 정리, workflow handoff에 쓸 repo-local entry surface
- 검증: contract에 적힌 명령과 실제 실행 결과 대조

### GRB-07. backend `AGENTS.md` entrypoint and knowledge bootstrap

- 저장소: `git-ranker`
- 상태: `pending`
- 선행조건: `GRB-04`, `GRW-27`
- 권장 write scope: backend entry docs, `.codex/skills/`, verification entry docs, 필요 시 supporting README
- 기본 결정: Spring Boot 구현 규칙과 backend-only skill은 workflow가 아니라 backend repo가 소유한다.
- 핵심 작업: repo root `AGENTS.md`를 추가하고, local skill registry, backend-only implementation knowledge surface를 만들고 workflow handoff contract와 연결한다.
- 비범위: frontend repo 변경, workflow policy 재설계, broad CI rollout
- 산출물: backend `AGENTS.md`, backend local skill surface, workflow handoff와 연결된 repo-local reference
- 검증: `AGENTS.md` entrypoint 문서 review, local skill discovery path 확인, representative backend task handoff simulation

### GRB-05. backend GC baseline 정렬

- 저장소: `git-ranker`
- 상태: `pending`
- 선행조건: `GRB-04`, `GRB-07`
- 권장 write scope: `build.gradle`, backend static analysis config, `.github/workflows/`, backend README 또는 verification entry docs
- 기본 결정: backend GC는 workflow repo가 아니라 backend repo의 Gradle task와 GitHub Actions가 소유한다. PR gate에는 low-noise static analysis만 넣고, duplication/wide dead code scan은 scheduled quality sweep으로 분리한다.
- 핵심 작업: repo-local GC command surface를 추가하고 blocking lane / sweep lane을 분리하며, cleanup candidate와 guardrail follow-up evidence를 repo-local surface에 반영한다.
- 비범위: workflow repo policy 재설계, broad auto-delete, frontend repo 변경
- 산출물: backend GC command, CI/scheduled workflow, repo-local docs update
- 검증: PR gate command 통과, scheduled sweep artifact shape 확인, representative duplication/unused signal triage

## Client Track

### GRC-05. frontend verification contract 정규화

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: 없음
- 권장 write scope: frontend 검증 문서, build/lint/typecheck entrypoint
- 기본 결정: workflow의 상위 verification semantics는 이미 fixed로 보고, frontend repo는 자신의 verification surface를 repo-local canonical source로 정리한다.
- 핵심 작업: 현재 frontend 검증 명령, 필수 env, 실패 의미, 수동 확인이 필요한 공백을 frontend repo 기준으로 정리한다.
- 비범위: UI 개편
- 산출물: frontend verification contract, 필요한 문서/스크립트 정리, workflow handoff에 쓸 repo-local entry surface
- 검증: contract에 적힌 명령과 실제 실행 결과 대조

### GRC-07. frontend `AGENTS.md` entrypoint and knowledge bootstrap

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: `GRC-05`, `GRW-27`
- 권장 write scope: frontend entry docs, `.codex/skills/`, verification entry docs, 필요 시 supporting README
- 기본 결정: React/Next 구현 규칙과 frontend-only knowledge surface는 workflow가 아니라 frontend repo가 소유한다.
- 핵심 작업: repo root `AGENTS.md`를 추가하고, local skill registry, frontend-only implementation knowledge surface를 만들고 workflow handoff contract와 연결한다.
- 비범위: backend repo 변경, workflow policy 재설계, broad UI rewrite
- 산출물: frontend `AGENTS.md`, frontend local skill surface, workflow handoff와 연결된 repo-local reference
- 검증: `AGENTS.md` entrypoint 문서 review, local skill discovery path 확인, representative frontend task handoff simulation

### GRC-06. frontend GC baseline 정렬

- 저장소: `git-ranker-client`
- 상태: `pending`
- 선행조건: `GRC-05`, `GRC-07`
- 권장 write scope: `package.json`, frontend static analysis config, `.github/workflows/`, frontend README 또는 repo entry docs
- 기본 결정: frontend GC는 repo-local npm scripts와 GitHub Actions가 소유한다. 기존 `lint/build` PR gate 위에 unused export/file/dependency detector를 추가하되, duplication scan과 wide cleanup은 scheduled sweep lane으로 분리한다.
- 핵심 작업: repo-local GC scripts, PR blocking lane, scheduled sweep lane, cleanup candidate handoff, autofix boundary를 current frontend structure에 맞게 추가한다.
- 비범위: backend repo 변경, workflow repo policy 재설계, high-risk refactor auto-merge
- 산출물: frontend GC scripts/workflows/docs, repo-local quality handoff surface
- 검증: PR gate command 통과, scheduled sweep report shape 확인, representative unused/duplication signal triage

## 참고

- 공통 운영 규칙과 Definition of Done은 [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.
- 새 작업의 기본 지시는 이 카탈로그와 active exec plan에서 읽는다.
- workflow는 orchestration layer의 backlog만 유지하고, repo-local implementation knowledge backlog는 각 app repo에서 이어간다.
