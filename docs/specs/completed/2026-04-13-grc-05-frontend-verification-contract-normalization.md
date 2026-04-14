# 2026-04-13-grc-05-frontend-verification-contract-normalization

- Status: `Completed`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend repo의 verification surface를 repo-local canonical source 기준으로 정규화한다.

## Problem

workflow의 상위 verification semantics는 고정돼 있지만, frontend repo는 아직 자신의 build/lint/typecheck surface와 환경 전제를 repo-local verification contract로 충분히 잠그지 못했다. 이 상태에서는 workflow와 repo-local validation의 경계가 흐려진다.

## Goals

- frontend verification surface를 repo-local canonical source 기준으로 정리한다.
- build/lint/typecheck entrypoint와 환경 전제를 명시한다.
- 결과 해석 기준과 remaining risk를 기록한다.

## Non-goals

- 새 기능 구현
- frontend route or UI behavior 변경
- frontend CI 전면 재설계

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-05`를 spec-first workflow 안에 보존할 방법
- Why it mattered: frontend track의 prerequisite가 사라지면 후속 `GRC-07`, `GRC-06`의 출발점이 없어진다
- User answer / evidence:
  - current user request는 product의 task를 새로운 요구사항으로 전환하라고 명시한다
  - former catalog entry는 frontend 검증 문서, build/lint/typecheck entrypoint 정리를 핵심 작업으로 남겼다
- Closed gap: `GRC-05`는 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 exact frontend entrypoint와 environment precondition을 더 좁혀야 한다

### Round 2
- Prompted gap: exact frontend entrypoints, environment assumptions, tracking 여부
- Why it mattered: verification contract surface와 build precondition이 잠기지 않으면 후속 `GRC-07`, `GRC-06`이 다른 기준을 참조하게 된다
- User answer / evidence:
  - local `git-ranker-client/README.md`는 Node.js 20+, npm, `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL`, `.env.example`, Docker Compose usage를 current entry doc으로 이미 드러낸다
  - `git-ranker-client/package.json`은 `dev`, `build`, `start`, `lint`만 노출하고 있어 `typecheck` contract surface가 아직 script로 정규화되지 않았다
  - `git-ranker-client/tsconfig.json`은 `strict: true`, `noEmit: true`라서 repo-local typecheck baseline을 `tsc --noEmit`로 고정할 수 있다
  - `git-ranker-client/.github/workflows/ci.yml`, `Dockerfile`, `docker-compose.yml`, `src/shared/lib/public-env.ts`는 `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL`가 build/runtime 전제라는 점을 동일하게 가리킨다
- Closed gap: 이번 slice의 exact verification contract surface는 `package.json`, `README.md`, `docs/verification-contract.md`, `.env.example`로 잠그고, environment precondition은 Node.js 20+, npm, required public env 2개로 고정한다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: 없음
- workflow는 상위 verification semantics만 고정하고, repo-local command surface는 `git-ranker-client`가 소유한다.
- repo-local canonical source 확인 없이는 `Approved`로 올리지 않는다.
- `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL`가 비어 있거나 absolute URL이 아니면 build/runtime verification은 실패해야 한다.

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
  - `README.md`
  - `package.json`
  - `docs/verification-contract.md`
  - `.env.example`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grc-05-frontend-verification-contract-normalization.md`
- Explicitly forbidden:
  - backend repo changes
  - unrelated frontend feature work
  - `.github/workflows/` 변경
- Network / external systems:
  - package registry or declared verification endpoint only when future verification requires it
- Escalation triggers:
  - sandbox가 frontend verification command를 막을 때만

## Acceptance Criteria

- frontend verification contract가 repo-local canonical source에서 읽힌다.
- build/lint/typecheck command와 환경 전제가 문서화된다.
- verification 결과 해석 기준과 remaining risk가 기록된다.

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
- `frontend-verification-surface-inventory`
  - Target repo: `git-ranker-client`
  - Goal: current build/lint/typecheck surface와 환경 전제를 inventory한다.
  - In-scope: repo-local entry docs, scripts, config surface 확인
  - Done when: verification contract 초안에 필요한 command set이 잠긴다.
  - Verification hook: entry doc and script review
  - Tracking needed: `no`
- `repo-local-contract-normalization`
  - Target repo: `git-ranker-client`
  - Goal: workflow semantics와 충돌하지 않는 frontend verification contract를 repo-local 문서에 정리한다.
  - In-scope: verification doc wording, remaining risk 기록
  - Done when: 후속 frontend spec이 같은 contract를 재사용할 수 있다.
  - Verification hook: declared commands + doc review
  - Tracking needed: `conditional`

## Risks Or Open Questions

- 실제 frontend repo의 current script surface를 읽으면 command set이나 config path가 더 좁아질 수 있다.

## Approval
- Harness judgment: actual script surface, env precondition, write scope, tracking decision이 잠겨 repo-local verification contract slice로 바로 실행 가능하다.
- User approval: current user request가 sequenced frontend follow-up continuation까지 포함해 실행을 직접 요청했다.

## Verification Summary

- Contract profile: `frontend-change`
- Overall status: `passed`
- Ran:
  - `npm run lint`
  - `npm run typecheck`
  - `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`
  - `git diff --check`
- Evidence:
  - `package.json`에 `typecheck` script를 추가해 repo-local command surface를 `npm run` contract로 정규화했다.
  - `docs/verification-contract.md`를 새로 추가해 required env, command semantics, result interpretation, remaining risk를 repo-local canonical source로 분리했다.
  - `README.md`는 `npm run typecheck`를 entry command로 노출하고 새 verification contract 문서를 가리키도록 정리했다.
  - `npm run lint`와 `npm run typecheck`는 로컬 worktree에서 성공했다.
  - `npm run build`는 sandbox 안에서 Turbopack의 local port bind 제한으로 실패했지만, 같은 command를 sandbox 밖에서 재실행해 성공했다.
  - `git diff --check`가 통과했다.
- Failure or skipped summary:
  - sandbox 내부 `npm run build`는 Turbopack runtime 제약 때문에 verification evidence로 채택하지 않았다.
- Next action: completed

## Final Change Summary

- frontend repo verification contract를 `package.json` script surface와 `docs/verification-contract.md` 기준으로 정규화했다.
- required public env 2개와 local/CI build precondition을 repo-local 문서로 분리해 후속 `GRC-07`, `GRC-06`이 재사용할 수 있게 했다.
- root `README.md`는 concrete verification contract를 직접 들고 있지 않고 repo-local verification 문서를 가리키는 얇은 entry 역할로 줄였다.

## Final User Validation

- 사용자는 `이어서 작업을 진행햊수에ㅛ.`라고 요청해 backend follow-up 뒤 frontend prerequisite까지 이어서 실행하는 것을 직접 승인했다.
- 이번 slice는 frontend verification contract normalizing만 다루고, CI baseline 정렬과 `AGENTS.md` entrypoint는 각각 후속 `GRC-06`, `GRC-07`에 남긴다.

## Docs Updated

- `git-ranker-client/README.md`
- `git-ranker-client/docs/verification-contract.md`
- `docs/specs/completed/2026-04-13-grc-05-frontend-verification-contract-normalization.md`
