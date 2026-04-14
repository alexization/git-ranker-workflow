# 2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap

- Status: `Completed`
- Primary Repo: `git-ranker-client`
- Related Issue: `not created`
- Related PR: `not created`

## Request Summary

frontend repo가 `AGENTS.md` entrypoint와 frontend-only knowledge bootstrap surface를 repo-local canonical source로 노출하도록 정리한다.

## Problem

frontend repo가 자체 entrypoint와 bootstrap surface를 충분히 갖추지 못하면 workflow에서 내려보낸 handoff가 다시 workflow 문서 의존으로 되돌아간다. 이러면 federated ownership model이 frontend track에서 실제로 작동하지 않는다.

## Goals

- frontend repo의 `AGENTS.md` entrypoint requirement를 충족시킨다.
- frontend-only knowledge surface를 repo-local로 내린다.
- verification entry docs와 bootstrap linkage를 정리한다.

## Non-goals

- backend repo 수정
- frontend feature 구현
- workflow control-plane 정책 재설계

## Socratic Clarification Log

### Round 1
- Prompted gap: former product catalog의 `GRC-07`을 spec-first requirement로 보존할 방법
- Why it mattered: `GRC-05`와 `GRW-27` 뒤에 이어질 frontend bootstrap task가 product 제거와 함께 사라지면 안 된다
- User answer / evidence:
  - current user request는 product의 task를 새 요구사항으로 남기라고 요구한다
  - former catalog entry는 frontend entry docs, `.codex/skills/`, verification entry docs를 권장 write scope로 제시했다
- Closed gap: `GRC-07`은 frontend-change draft spec으로 승격한다
- Remaining blocker: approval 시점에 actual frontend entry docs와 bootstrap minimum을 더 좁혀야 한다

### Round 2
- Prompted gap: actual frontend entry docs, bootstrap minimum, tracking 여부
- Why it mattered: root `README.md`가 concrete entrypoint를 계속 들고 있거나 repo-local bootstrap minimum이 잠기지 않으면 workflow handoff 이후 first source가 다시 흔들린다
- User answer / evidence:
  - `GRW-27` completed contract는 target repo root `README.md`를 overview-only로 두고, concrete entrypoint responsibility를 `AGENTS.md`와 named entry docs에 둔다
  - `GRC-05` completed close-out으로 frontend verification entry surface는 `docs/verification-contract.md`, `package.json`, `.env.example`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml` 기준으로 정리됐다
  - current frontend repo에는 `.codex/skills/`가 없고, repo 구조는 `src/app`, `src/features`, `src/shared`, `src/fonts`, `docs`, `.github`가 실제 bootstrap surface다
- Closed gap: 이번 slice의 exact entry docs는 root `AGENTS.md`, overview-only `README.md`, `docs/verification-contract.md`, `package.json`, `.env.example`, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`로 잠그고, local skill surface는 optional/no로 둔다
- Remaining blocker: `none`

## Assumptions And Constraints

- Prerequisites before approval: `GRC-05`, `GRW-27`
- frontend-only knowledge surface는 `git-ranker-client`가 소유한다.
- repo-local bootstrap은 frontend verification contract와 일관돼야 한다.
- root `README.md`는 프로젝트 overview만 맡고, concrete bootstrap은 `AGENTS.md`와 named entry docs가 소유한다.

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
  - `AGENTS.md`
  - `README.md`
  - `docs/verification-contract.md`
  - `package.json`
  - `.env.example`
  - `.github/workflows/ci.yml`
  - `.github/workflows/deploy.yml`
- Control-plane artifacts:
  - `docs/specs/completed/2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap.md`
- Explicitly forbidden:
  - backend repo edits
  - unrelated frontend route or UI changes
- Network / external systems:
  - GitHub metadata only if future tracking requires it
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때만

## Acceptance Criteria

- frontend repo가 `AGENTS.md` entrypoint를 canonical source로 노출한다.
- frontend-only knowledge bootstrap surface가 workflow 밖으로 이동한다.
- verification entry docs와 bootstrap linkage가 문서화된다.

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
- `frontend-entrypoint-definition`
  - Target repo: `git-ranker-client`
  - Goal: frontend repo의 `AGENTS.md`와 entry docs requirement를 정의하고 적용한다.
  - In-scope: entrypoint wording, frontend-only source list
  - Done when: workflow handoff가 frontend repo entrypoint를 first source로 가리킨다.
  - Verification hook: entry doc review
  - Tracking needed: `conditional`
- `frontend-bootstrap-surface-alignment`
  - Target repo: `git-ranker-client`
  - Goal: frontend-only bootstrap surface를 repo-local ownership에 맞춰 정리한다.
  - In-scope: `.codex/skills/`, verification entry docs alignment
  - Done when: workflow repo가 frontend implementation knowledge를 다시 들고 있지 않다.
  - Verification hook: doc/skill review + declared verification commands
  - Tracking needed: `no`

## Risks Or Open Questions

- frontend repo entrypoint가 실제 codebase 구조와 맞지 않으면 approval 단계에서 subtask split이 더 필요할 수 있다.

## Approval
- Harness judgment: actual frontend entry docs, bootstrap minimum, no-skill fallback, tracking decision이 잠겨 repo-local docs slice로 바로 실행 가능하다.
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
  - frontend repo root에 `AGENTS.md`를 추가해 overview-only `README.md`와 분리된 concrete entrypoint를 repo-local로 노출했다.
  - 새 `AGENTS.md`는 `docs/verification-contract.md`, `package.json`, `.env.example`, workflow, config, `src/app`, `src/features`, `src/shared`, `src/proxy.ts`를 bootstrap discovery order로 고정했다.
  - local `.codex/skills/` 부재와 fallback first source를 `AGENTS.md` + nearest docs/config/code surface로 명시했다.
  - `README.md`는 프로젝트 overview만 남기고 concrete entrypoint responsibility를 `AGENTS.md`와 named entry docs로 넘겼다.
  - `npm run lint`, `npm run typecheck`, sandbox 밖 `npm run build`가 모두 성공했다.
  - `git diff --check`가 통과했다.
- Failure or skipped summary:
  - build는 Turbopack sandbox 제한 때문에 latest verification을 sandbox 밖에서 실행했다.
- Next action: completed

## Final Change Summary

- frontend repo root에 `AGENTS.md`를 추가해 workflow handoff 이후 first source를 repo-local canonical entrypoint로 고정했다.
- root `README.md`는 overview-only surface로 줄이고, verification/bootstrap 상세는 `AGENTS.md`와 named entry docs가 소유하도록 정리했다.
- local skill surface가 없는 현재 상태를 명시하고, 구현자가 workflow 문서로 역류하지 않도록 frontend repo 안에서 fallback discovery order를 닫았다.

## Final User Validation

- 사용자는 `이어서 작업을 진행햊수에ㅛ.`라고 요청해 frontend bootstrap continuation까지 직접 승인했다.
- 앞선 clarification에서 target repo root `README.md`는 프로젝트 설명만 둔다고 잠겨 있었고, 이번 close-out은 그 contract를 frontend repo에도 그대로 적용했다.

## Docs Updated

- `git-ranker-client/AGENTS.md`
- `git-ranker-client/README.md`
- `docs/specs/completed/2026-04-13-grc-07-frontend-agents-entrypoint-bootstrap.md`
