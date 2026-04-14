# 2026-04-13-grb-07-backend-agents-entrypoint-bootstrap

- Status: `Completed`
- Primary Repo: `git-ranker`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

backend repo가 `AGENTS.md` entrypoint와 backend-only knowledge bootstrap surface를 repo-local canonical source로 노출하도록 정리한다.

## Problem

workflow가 federated handoff를 하더라도 backend repo 자체의 entrypoint와 backend-only skill/bootstrap surface가 부족하면 구현 단계의 first source가 여전히 workflow로 역류할 수 있다.

## Goals

- backend repo의 `AGENTS.md` entrypoint requirement를 충족시킨다.
- backend-only knowledge bootstrap surface를 repo-local로 내린다.
- verification entry docs와의 연결을 정리한다.

## Non-goals

- workflow repo의 control-plane 정책 재설계
- backend production feature 변경
- frontend repo 수정

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRB-07`을 spec-first requirement로 남길 방법
- Why it mattered: backend repo-local ownership bootstrap이 사라지면 `GRW-27` 이후 실제 handoff destination이 비게 된다
- User answer / evidence:
  - current user request는 product의 task를 새 요구사항으로 남기라고 한다
  - former catalog entry는 backend entry docs, `.codex/skills/`, verification entry docs를 권장 write scope로 제시했다
- Closed gap: `GRB-07`은 backend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 actual backend entry docs 범위와 bootstrap minimum을 더 좁혀야 한다

### Round 2
- Prompted gap: actual backend entry docs, bootstrap minimum, tracking 여부
- Why it mattered: entry docs 범위와 bootstrap minimum이 잠기지 않으면 `AGENTS.md`가 다시 workflow 문서를 복제하거나, 반대로 handoff destination이 비어 있게 된다
- User answer / evidence:
  - `GRW-27` completed contract는 root `README.md`를 overview-only로 두고, concrete entrypoint responsibility를 `AGENTS.md`와 named entry docs에 둔다
  - `GRB-04` completed close-out으로 backend verification entry surface는 `build.gradle`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `src/test/java/**/*IT.java` 기준으로 다시 설명 가능해졌다
  - current backend repo root에는 `README.md`, `build.gradle`, `settings.gradle`만 있고 `.codex/skills/`와 `AGENTS.md`는 아직 없다
- Closed gap: 이번 slice의 exact entry docs는 root `AGENTS.md`, overview-only `README.md`, `build.gradle`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`로 잠그고, local skill surface는 optional/no로 둔다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: `GRB-04`, `GRW-27`
- backend-only implementation knowledge는 workflow가 아니라 `git-ranker`가 소유한다.
- repo-local bootstrap은 verification contract와 충돌하지 않아야 한다.
- root `README.md`는 프로젝트 설명만 유지할 수 있고, concrete bootstrap은 `AGENTS.md`가 맡는다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `yes`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker`
- Allowed write paths:
  - `AGENTS.md`
  - `README.md`
  - `build.gradle`
  - `.github/workflows/ci.yml`
  - `.github/workflows/deploy.yml`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grb-07-backend-agents-entrypoint-bootstrap.md`
- Explicitly forbidden:
  - frontend repo edits
  - unrelated backend production code changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- backend repo가 `AGENTS.md` entrypoint를 canonical source로 노출한다.
- backend-only knowledge bootstrap surface가 workflow 밖으로 이동한다.
- verification entry docs와 bootstrap linkage가 문서화된다.

## Verification
- Contract profile: `backend-change`
- Commands:
  - `./gradlew test`
  - `./gradlew build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `backend-entrypoint-definition`
  - Target repo: `git-ranker`
  - Goal: backend repo의 `AGENTS.md`와 entry docs requirement를 정의하고 적용한다.
  - In-scope: entrypoint wording, backend-only source list, verification/deploy entry doc linkage
  - Done when: workflow handoff가 backend repo entrypoint를 first source로 가리킨다.
  - Verification hook: entry doc review
  - Tracking needed: `no`
- `backend-bootstrap-surface-alignment`
  - Target repo: `git-ranker`
  - Goal: backend-only skill/bootstrap surface를 repo-local ownership에 맞춰 정리한다.
  - In-scope: no-skill fallback 결정, verification entry docs alignment
  - Done when: workflow repo가 backend implementation knowledge를 다시 들고 있지 않다.
  - Verification hook: doc/skill review + declared verification commands
  - Tracking needed: `no`

## Risks Or Open Questions

- repo-local bootstrap을 너무 넓게 잡으면 thin-layer handoff contract와 경계가 다시 흐려질 수 있다.

## Approval
- Harness judgment: exact backend entry docs, bootstrap minimum, tracking decision이 잠겨 repo-local docs slice로 바로 실행 가능하다.
- User approval: current user request가 sequenced backend follow-up continuation을 직접 요청했다.

## Verification Summary

- Contract profile: `backend-change`
- Overall status: `passed`
- Ran:
  - `./gradlew test`
  - `./gradlew build`
  - `git diff --check`
- Evidence:
  - backend writable worktree에 root `AGENTS.md`를 추가해 overview-only `README.md`와 분리된 concrete entrypoint를 repo-local로 노출했다.
  - 새 `AGENTS.md`는 `build.gradle`, `settings.gradle`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `src/test/java/**/*IT.java`, `src/main/java`, `src/main/resources`를 backend bootstrap surface로 고정했다.
  - local `.codex/skills/` 부재를 명시하고, fallback first source를 `AGENTS.md`와 nearest code/test surface로 정리했다.
  - backend worktree에서 `./gradlew test`와 `./gradlew build`가 모두 성공했다.
  - `git diff --check`가 통과했고, backend worktree 기준 변경 파일은 새 `AGENTS.md`만 남았다.
- Failure or skipped summary:
  - 없음
- Next action: completed

## Final Change Summary

- backend repo root에 `AGENTS.md`를 추가해 workflow handoff 이후의 concrete entrypoint를 repo-local canonical source로 고정했다.
- root `README.md`는 overview-only로 유지하고, verification/bootstrap 상세는 `AGENTS.md`, Gradle build surface, CI/deploy workflow, test tree가 소유하도록 정리했다.
- repo-local skill surface가 없는 현재 상태를 명시하고, 구현자가 workflow 문서로 역류하지 않도록 fallback discovery order를 backend repo 안에서 닫았다.

## Final User Validation

- 사용자는 `이어서 작업을 진행햊수에ㅛ.`라고 요청해 `GRW-27` 후속인 backend bootstrap continuation을 직접 승인했다.
- 앞선 clarification에서 target repo root `README.md`는 프로젝트 설명만 둔다고 잠겨 있었고, 이번 close-out은 그 contract를 backend repo에 그대로 적용했다.

## Docs Updated

- `git-ranker/AGENTS.md`
- `docs/specs/completed/2026-04-13-grb-07-backend-agents-entrypoint-bootstrap.md`
