# 2026-04-09-grb-04-backend-verification-contract-reset

- Issue ID: `GRB-04`
- GitHub Issue: `alexization/git-ranker#77`
- GitHub PR: `alexization/git-ranker#78`
- Status: `In Progress`
- Repository: `git-ranker`
- Branch Name: `feat/grb-04-backend-verification-contract-reset`
- Task Slug: `2026-04-09-grb-04-backend-verification-contract-reset`
- Primary Context Pack: `backend-change`
- Verification Contract Profile: `backend-change`

## Problem

`git-ranker`에는 현재 harness 기준으로 재사용하기 어려운 legacy verification surface가 남아 있다. `build.gradle`의 custom verification task(`integrationTest`, coverage gate, OpenAPI spec generation), `.github/workflows/ci.yml`/`quality-gate.yml`, `docs/openapi/README.md`, verification 성격의 테스트가 서로 다른 failure semantics를 가진 채 병존하고 있었다.

cleanup 이후 review에서 두 가지 회귀가 드러났다. `test`가 `*IT`를 계속 제외하는데 `integrationTest` task가 사라져 repository integration test가 orphan 상태가 되었고, `deploy.yml`만 남아 `main` push 시 검증 없이 배포가 가능해졌다.

## Why Now

`GRW-15`가 verification contract registry를 고정했고, `GRB-04`는 backend repo가 그 상위 semantics에 맞게 다시 정렬되는 첫 작업이다. legacy surface 제거는 이미 끝냈지만, review에서 드러난 orphan integration lane과 pre-deploy verification gap은 같은 issue 안에서 바로 수리 가능하다. 이 둘을 남겨두면 clean baseline이 아니라 regressions를 포함한 intermediate state가 된다.

## Scope

- `git-ranker/build.gradle`에서 legacy verification task/plugin/dependency를 제거하거나 neutralize한다.
- backend verification CI workflow를 harness-compatible minimum으로 재구성한다.
- backend deploy workflow 앞단에 최소 verification gate를 복구한다.
- verification-specific 문서와 테스트 자산을 제거한다.
- control-plane exec plan에 cleanup 범위와 후속 재구성 전제조건을 기록한다.

## Non-scope

- 새 harness-aligned verification contract 구현
- backend 기능/API/배치 동작 변경
- frontend repo 또는 workflow stable policy 본문 재설계
- coverage/OpenAPI/Docker preflight legacy surface 복구

## Write Scope

- Primary repo: `git-ranker`
- Allowed write paths:
  - `README.md`
  - `build.gradle`
  - `.github/workflows/`
  - `docs/openapi/`
  - `src/test/java/com/gitranker/api/architecture/`
  - `src/test/java/com/gitranker/api/docs/`
  - `src/test/java/com/gitranker/api/testsupport/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - `/tmp/grb-04-issue-body.md`
- Explicitly forbidden:
  - `git-ranker-client` code tree
  - `git-ranker` production source(`src/main/`)의 기능 변경
  - workflow stable source of truth mass update
- Network / external systems:
  - GitHub issue creation/check for `alexization/git-ranker`
- Escalation triggers:
  - sandbox가 `gh issue create` 또는 backend verification command 실행을 막을 때만

## Outputs

- `git-ranker/build.gradle`에서 legacy verification surface 제거를 유지하면서 minimal `integrationTest` lane 복구
- `git-ranker/.github/workflows/ci.yml`을 minimal verification workflow로 복구
- `git-ranker/.github/workflows/quality-gate.yml` 제거 유지
- `git-ranker/.github/workflows/deploy.yml`에 pre-deploy verification gate 추가
- `git-ranker/docs/openapi/README.md`, `git-ranker/docs/openapi/openapi.json` 제거
- `git-ranker/README.md`의 legacy verification section 제거
- verification-specific test asset 제거
- `GRB-04` active exec plan with review-driven repair evidence

## Working Decisions

- 이번 작업의 primary repo와 task type은 `git-ranker` / `backend 수정`으로 고정한다.
- public feature behavior는 바꾸지 않고 verification ownership surface만 비운다.
- legacy verification surface 제거 후에도 repo가 기본 빌드 가능한 상태를 유지하도록 한다.
- review가 지적한 orphan integration lane과 deploy gate gap만 최소 단위로 복구한다.
- coverage/OpenAPI/Docker preflight surface는 이번 repair에서 되살리지 않는다.
- 새 verification contract 도입은 follow-up implementation으로 남기고, 이번 턴은 clean baseline 준비에 집중한다.

## Context Selection Summary

- Task type: `backend 수정`
- Primary context pack: `backend-change`
- Required docs:
  - `AGENTS.md`
  - `docs/README.md`
  - `PLANS.md`
  - `docs/operations/workflow-governance.md`
  - `docs/architecture/context-pack-registry.md`
  - `docs/operations/tool-boundary-matrix.md`
  - `docs/operations/verification-contract-registry.md`
  - `docs/product/work-item-catalog.md`
  - `../git-ranker/README.md`
  - `../git-ranker/build.gradle`
  - `../git-ranker/.github/workflows/ci.yml`
  - `../git-ranker/.github/workflows/quality-gate.yml`
  - `../git-ranker/.github/workflows/deploy.yml`
  - `../git-ranker/docs/openapi/README.md`
- Optional docs trigger:
  - verification-specific test 삭제 범위를 잠글 때 `OpenApiDocsTest`, `ArchitectureGuardrailTest`를 연다.
  - 기존 hardening 맥락이 필요할 때 completed exec plan `2026-03-26-grb-02-backend-verification-hardening.md`를 참고한다.
- Forbidden context:
  - frontend repo code/tree
  - unrelated workflow policy 문서 eager load
  - `src/main/` production feature 탐색 확장
- First-ring hot file cue:
  - `integrationTest`
  - `jacoco`
  - `generateOpenApiSpec`
  - `quality-gate`
  - `deploy.yml`
  - `OpenApiDocsTest`
  - `ArchitectureGuardrailTest`

## Boundary Check Summary

- Read boundary:
  - `backend-change` pack required docs와 legacy verification asset 인접 파일까지만 읽는다.
- Write boundary:
  - `git-ranker/build.gradle`
  - `git-ranker/.github/workflows/`
  - `git-ranker/docs/openapi/`
  - `git-ranker/src/test/java/com/gitranker/api/architecture/`
  - `git-ranker/src/test/java/com/gitranker/api/docs/`
  - current workflow exec plan
- Control-plane artifact:
  - current active exec plan and GitHub issue body
- Explicitly forbidden path:
  - `git-ranker/src/main/`
  - sibling frontend repo
  - workflow stable docs outside control-plane artifact
- Network:
  - GitHub issue creation/check only
- Escalation:
  - sandbox가 `gh issue create` 또는 declared verification command를 막을 때만

## Verification

- `./gradlew test`
- `./gradlew integrationTest`
- `./gradlew build`
- `git diff --check`

## Evidence

- removed legacy verification inventory:
  - Gradle: `jacoco`, `verifyDockerAvailable`, legacy `integrationTest` semantics, `generateOpenApiSpec`
  - CI: `.github/workflows/ci.yml`, `.github/workflows/quality-gate.yml`
  - Docs: `README.md` verification section, `docs/openapi/README.md`, `docs/openapi/openapi.json`
  - Tests: `ArchitectureGuardrailTest`, `OpenApiDocsTest`, `DockerPreflight*`
- review-repair inventory:
  - Gradle: dedicated `integrationTest` lane만 minimal하게 복구하고 Docker preflight/coverage/OpenAPI task는 복구하지 않는다.
  - CI: `.github/workflows/ci.yml`을 unit + integration verification lane으로 복구한다.
  - Deploy: `.github/workflows/deploy.yml`에 pre-deploy verification job을 추가한다.
- latest `test`, `build`, `git diff --check` result
- follow-up rebuild preconditions for harness-aligned backend contract

## Repair Triage Summary

- Trigger: PR `alexization/git-ranker#78` review에서 unresolved P1 두 건이 보고됐다. `integrationTest` 제거로 `*IT` 테스트가 어디에서도 실행되지 않고, `deploy.yml`이 `main` push 시 검증 없이 배포를 시작한다.
- Decision: current issue 안에서 `repair`
- Root cause: legacy verification surface cleanup가 "모든 repo-local verification lane 제거"로 과도하게 수렴하면서, harness-compatible minimum lane까지 함께 지워졌다.
- Budget remaining: same-issue repair 1회 가능
- Rerun targets:
  - `./gradlew test`
  - `./gradlew integrationTest`
  - `./gradlew build`
  - `git -C .worktrees/grb-04 diff --check`
  - `git diff --check`
- Next owner: `Codex`

## Verification Report

- Contract profile: `backend-change`
- Overall status: `passed`
- Preconditions:
  - backend worktree: `feat/grb-04-backend-verification-contract-reset` from `origin/develop@64c0541`
  - scope is limited to legacy verification cleanup 뒤 review가 지적한 minimum integration lane / pre-deploy gate repair와 control-plane exec plan update
  - local Docker daemon is currently unavailable at `unix:///Users/hyoseok/.orbstack/run/docker.sock`, so restored integration lane는 GitHub Actions `Unit and Integration Verification` check(run `24178313661`)로 최종 확인했다.
- Command: `./gradlew test`
  - Status: `passed`
  - Evidence: `test` baseline는 여전히 성공하고 `*IT` 제외 unit lane이 깨지지 않았다.
- Command: `./gradlew integrationTest`
  - Status: `passed`
  - Evidence: local rerun은 Docker daemon 부재로 `ContainerFetchException`에서 멈췄지만, PR `#78`의 GitHub Actions `Unit and Integration Verification` check가 `./gradlew integrationTest`를 포함한 lane를 `1m47s`에 성공시켜 restored lane가 executable임을 확인했다.
- Command: `./gradlew build`
  - Status: `passed`
  - Evidence: `build`는 계속 성공하고, restored `integrationTest` lane을 `check`에 묶지 않은 상태도 의도대로 유지됐다.
- Command: `git -C .worktrees/grb-04 diff --check`
  - Status: `passed`
  - Evidence: backend repo patch formatting 오류가 없다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: workflow exec plan patch formatting 오류가 없다.
- Failure summary: 없음
- Next action:
  - latest verification report는 passed로 갱신됐다.
  - 필요 시 refreshed reviewer evidence를 추가하고 current issue close-out 또는 follow-up planning으로 넘긴다.

## Reviewer Handoff Preparation

- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - Latest verification report: `passed`
  - Diff summary: backend repo에 minimal `integrationTest` lane, `ci.yml` verification workflow, `deploy.yml` pre-deploy verification gate를 복구했다. legacy coverage/OpenAPI/Docker preflight surface는 복구하지 않았다.
  - Touched files:
    - `.github/workflows/ci.yml`
    - `.github/workflows/deploy.yml`
    - `build.gradle`
  - Source-of-truth update:
    - workflow exec plan에 review-driven repair 범위와 latest verification evidence를 기록했다.
  - Remaining risks / skipped checks:
    - local Docker daemon은 여전히 없지만 remote GitHub Actions run으로 restored lane integrity를 확인했다.
    - coverage/OpenAPI/Docker preflight surface는 의도적으로 복구하지 않았다.

## Risks or Blockers

- local Docker daemon이 내려가 있어 Testcontainers 기반 `integrationTest`를 이 세션의 local runtime만으로 재현할 수 없다.
- restored `integrationTest` lane은 GitHub Actions에서 통과했지만, local Docker 환경 복구 전까지 동일 evidence를 workstation에서 재현할 수는 없다.
- tracked OpenAPI snapshot을 이번 cleanup에서 제거하면 후속 contract source를 다시 잠가야 한다.
- legacy surface 일부가 production behavior와 강하게 결합돼 있으면 범위를 줄이거나 follow-up으로 분리해야 한다.

## Repair Note

- `2026-04-09`: first reviewer pool pass에서 `README.md`와 `src/test/java/com/gitranker/api/testsupport/`가 write scope에 누락된 것이 blocking finding으로 보고됐다.
- 같은 날 exec plan write scope를 실제 diff와 일치하도록 보정했고, formatting check를 다시 실행한 뒤 reviewer pool에 refreshed verdict를 요청한다.
- `2026-04-09`: PR `#78`의 thread-aware review에서 `.github/workflows/ci.yml` 삭제와 `integrationTest` 제거가 각각 P1 finding으로 보고됐다.
- 같은 날 minimal `integrationTest` lane, `ci.yml`, `deploy.yml` verification gate를 복구했고, local Docker daemon 부재는 남아 있지만 GitHub Actions verification pass로 latest report를 `passed`로 갱신했다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `pending refresh`
- Additional Reviewers:
  - previous cleanup-only review: `Ohm`, `Godel`, `Nietzsche`
- Reviewer Roles / Prompt Focus:
  - `scope-and-governance`
  - `verification-and-regression`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/active/2026-04-09-grb-04-backend-verification-contract-reset.md`
  - Latest verification report: `passed`
  - Diff summary: minimal integration lane와 pre-deploy verification gate를 복구하는 repair diff가 cleanup-only diff 위에 추가됐다.
  - Source-of-truth update: workflow exec plan에 review-driven repair와 Docker blocker 이력을 반영했다.
  - Remaining risks / skipped checks: local Docker daemon unavailable, refreshed internal reviewer pass not yet run
- Review Verdict: `blocked`
- Findings / Change Requests:
  - current repair diff는 latest verification report를 확보했지만, refreshed internal reviewer pass는 아직 실행하지 않았다.
  - previous cleanup-only approval은 new repair diff 이후 stale 상태다.
- Evidence:
  - thread-aware GitHub review는 unresolved P1 두 건이 `.github/workflows/ci.yml`과 `build.gradle`에 남아 있음을 확인했다.
  - latest verification report는 local Docker blocker 이력을 남기면서도 GitHub Actions `Unit and Integration Verification` pass로 current repair diff를 `passed`로 기록한다.
  - `git diff --check`와 `git -C .worktrees/grb-04 diff --check`는 모두 통과한다.

## Feedback / Guardrail Follow-up

- Stage: `Repairing`
- Failure class: `review-regression`
- Promotion decision: `pending`
- Rationale:
  - external review가 orphan integration lane과 pre-deploy verification gap을 현재 issue 안에서 바로 수리 가능한 regression으로 좁혀 줬다.
  - refreshed internal reviewer verdict가 아직 없어 promotion decision을 닫지 않는다.
- Core evidence:
  - thread-aware GitHub review에서 unresolved P1 두 건이 확인됐다.
  - minimal repair diff 후 `./gradlew test`, `./gradlew build`, diff checks는 통과했고, restored `integrationTest` lane는 GitHub Actions `Unit and Integration Verification` check에서 통과했다.
- Follow-up asset:
  - remote CI green 이후 current issue close-out 또는 별도 backend verification rebuild follow-up 판단

## Publish Result

- GitHub PR `alexization/git-ranker#78`은 open 상태다.
- repair commit `b973b36` (`ci: 백엔드 최소 검증 게이트 복구`)를 PR branch에 push했다.
- `Unit and Integration Verification` GitHub Actions check가 새 commit 기준으로 `pass`됐다.

## Next Preconditions

- clean baseline 위에서 `backend-change` contract에 맞는 repo-local verification command/doc/CI를 다시 설계한다.
- OpenAPI snapshot을 유지할지, 새 contract에서 다른 canonical source로 대체할지 결정해야 한다.

## Docs Updated

- `docs/exec-plans/active/2026-04-09-grb-04-backend-verification-contract-reset.md`

## Skill Consideration

이번 작업은 기존 `request-intake`, `issue-to-exec-plan`, `context-pack-selection`, `boundary-check` 흐름으로 닫을 수 있다. repo-specific verification rebuild 절차가 반복되면 후속 `GRB-04` close-out에서 별도 backend verification skill 또는 template 후보로 승격 여부를 검토한다.
