# 2026-04-13-grc-06-frontend-gc-baseline-alignment

- Status: `Completed`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend GC baseline을 repo-local npm script와 GitHub Actions ownership으로 정렬한다.

## Problem

frontend quality baseline이 workflow repo가 아니라 frontend repo의 script/CI surface로 고정되지 않으면 federated ownership model 아래에서 guardrail 위치가 계속 흔들린다.

## Goals

- frontend GC baseline ownership을 repo-local npm script와 GitHub Actions로 고정한다.
- static analysis config와 verification entry docs의 연결을 정리한다.
- workflow repo는 상위 semantics만 남긴다.

## Non-goals

- frontend feature 구현
- backend repo 수정
- workflow repo에 frontend GC implementation guide를 추가하는 것

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-06`을 product 제거 후에도 남길 canonical surface
- Why it mattered: frontend track의 repo-local guardrail baseline alignment가 future work로 계속 남아 있어야 한다
- User answer / evidence:
  - current user request는 product task를 새로운 요구사항으로 전환하라고 한다
  - former catalog entry는 `package.json`, frontend static analysis config, `.github/workflows/`, frontend README 또는 repo entry docs`를 권장 write scope로 제시했다
- Closed gap: `GRC-06`은 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact frontend GC surface와 retained CI scope를 더 좁혀야 한다

### Round 2
- Prompted gap: exact frontend GC surface, retained CI scope, tracking 여부
- Why it mattered: script와 CI baseline이 다른 command set을 가리키면 repo-local ownership이 다시 흔들리고 verification evidence 해석도 갈라진다
- User answer / evidence:
  - `GRC-05` completed close-out으로 `package.json`은 `lint`, `typecheck`, `build` script surface를 노출하고 `docs/verification-contract.md`가 result interpretation을 canonical source로 가진다
  - `GRC-07` completed close-out으로 `AGENTS.md`가 repo entrypoint가 됐고 root `README.md`는 overview-only로 줄었다
  - current `eslint.config.mjs`와 `tsconfig.json`은 각각 lint/typecheck baseline config surface고, `.github/workflows/ci.yml`는 아직 `lint`와 `build`만 실행해 explicit `typecheck` lane이 빠져 있다
- Closed gap: 이번 slice의 exact GC surface는 `package.json`, `docs/verification-contract.md`, `AGENTS.md`, `eslint.config.mjs`, `tsconfig.json`, `.github/workflows/ci.yml`로 잠그고, retained CI scope는 `lint -> typecheck -> build`로 고정한다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: `GRC-05`, `GRC-07`
- frontend GC baseline ownership은 repo-local이다.
- workflow repo는 상위 semantics와 evidence rule만 유지한다.
- root `README.md`는 overview-only surface로 유지하고 GC baseline detail은 entry docs와 workflow가 소유한다.

## Approval Gate
- Problem and goal locked: `yes`
- Non-goals explicit: `yes`
- Primary repo and write scope locked: `yes`
- Verification method locked: `yes`
- Subtask split decided: `yes`
- Tracking decision locked: `yes`
- Remaining blockers: `none`

## Write Scope
- Primary repo: `git-ranker-client`
- Allowed write paths:
  - `package.json`
  - `eslint.config.mjs`
  - `tsconfig.json`
  - `.github/workflows/ci.yml`
  - `docs/verification-contract.md`
  - `AGENTS.md`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grc-06-frontend-gc-baseline-alignment.md`
- Explicitly forbidden:
  - backend repo edits
  - unrelated frontend route or UI changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- frontend GC baseline ownership이 repo-local npm script/CI surface로 설명된다.
- static analysis config, workflow, verification docs가 같은 baseline semantics를 따른다.
- workflow repo가 frontend GC implementation detail을 소유하지 않는다.

## Verification
- Contract profile: `frontend-change`
- Commands:
  - `npm run lint`
  - `npm run typecheck`
  - `npm run build`
  - `git diff --check`

## Delivery And Tracking Plan
- Lane: `guarded lane`
- Parent issue needed: `no`
- PR needed: `conditional`

## Detailed Subtasks
- `frontend-gc-surface-inventory`
  - Target repo: `git-ranker-client`
  - Goal: current GC/static analysis/CI surface를 inventory하고 repo-local ownership 범위를 잠근다.
  - In-scope: script, config, workflow references
  - Done when: retained baseline surface가 설명 가능하다.
  - Verification hook: config and workflow review
  - Tracking needed: `no`
- `repo-local-baseline-alignment`
  - Target repo: `git-ranker-client`
  - Goal: frontend GC baseline을 repo-local entry docs와 함께 정렬한다.
  - In-scope: verification docs, CI wording, retained scripts
  - Done when: workflow repo 없이도 frontend GC baseline을 해석할 수 있다.
  - Verification hook: declared commands + doc review
  - Tracking needed: `conditional`

## Risks Or Open Questions

- current frontend repo의 GC surface가 실제 script/config 상태와 다르면 approval 단계에서 더 좁은 split이 필요할 수 있다.

## Approval
- Harness judgment: actual script/config/workflow surface, retained CI scope, tracking decision이 잠겨 repo-local baseline alignment slice로 바로 실행 가능하다.
- User approval: current user request가 sequenced frontend follow-up continuation을 직접 요청했다.

## Verification Summary

- Contract profile: `frontend-change`
- Overall status: `passed`
- Ran:
  - `npm run lint`
  - `npm run typecheck`
  - `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`
  - `git diff --check`
- Evidence:
  - `.github/workflows/ci.yml`가 `lint -> typecheck -> build` baseline order를 explicit job chain으로 실행하도록 정렬됐다.
  - `docs/verification-contract.md`는 CI가 same command trio를 실행한다고 반영했고, follow-up remaining risk를 제거했다.
  - `AGENTS.md`는 repo entrypoint에서 same baseline order를 직접 가리키도록 갱신됐다.
  - `npm run lint`, `npm run typecheck`, sandbox 밖 `npm run build`가 모두 성공했다.
  - `git diff --check`가 통과했다.
- Failure or skipped summary:
  - build는 Turbopack sandbox 제한 때문에 latest verification을 sandbox 밖에서 실행했다.
- Next action: completed

## Final Change Summary

- frontend GC baseline ownership을 `package.json` script surface와 `.github/workflows/ci.yml` job chain으로 고정했다.
- verification contract 문서와 `AGENTS.md`가 CI의 same baseline order를 가리키도록 맞춰 repo-local 해석 기준을 하나로 합쳤다.
- workflow repo가 frontend GC implementation detail을 들고 있지 않아도 repo-local script, config, workflow만으로 baseline을 설명할 수 있게 정리했다.

## Final User Validation

- 사용자는 `이어서 작업을 진행햊수에ㅛ.`라고 요청해 frontend baseline alignment까지 포함한 sequenced continuation을 직접 승인했다.
- 이번 slice로 `GRC-05`, `GRC-07`, `GRC-06`이 연속해서 닫혀 frontend repo-local verification/bootstrap baseline이 현재 contract 기준으로 정렬됐다.

## Docs Updated

- `git-ranker-client/AGENTS.md`
- `git-ranker-client/docs/verification-contract.md`
- `docs/specs/completed/2026-04-13-grc-06-frontend-gc-baseline-alignment.md`
