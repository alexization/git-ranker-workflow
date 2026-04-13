# Verification Contract Registry

이 문서는 `Verifying`, `Repairing`, `Blocked` semantics를 실제 실행 규약으로 고정한다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md), spec 기준은 [sdd-spec-policy.md](sdd-spec-policy.md), review verdict 규칙은 [dual-agent-review-policy.md](dual-agent-review-policy.md)를 따른다.

## Registry Invariants

- 모든 실행 작업은 `Verifying`에 들어가기 전에 정확히 하나의 primary contract profile을 approved spec에 적어야 한다.
- contract profile은 repo-specific 세부 contract를 대체하지 않는다. 대신 각 저장소가 최소한 지켜야 할 기본 entrypoint, evidence, retry, `Blocked` semantics를 제공한다.
- `passed`는 모든 required command가 성공하고 required evidence가 남았을 때만 성립한다.
- required command가 실패하면 overall status는 `failed`다.
- required command를 실행할 수 없거나 canonical source, 환경 선행조건, access boundary가 비어 있으면 overall status는 `blocked`다.
- optional 또는 conditional command는 생략 가능하지만, trigger 부재 또는 제외 이유를 evidence에 남겨야 한다.

## Status Vocabulary

| Level | Status | Meaning | Next state |
| --- | --- | --- | --- |
| command | `passed` | 명령이 기대한 종료 상태와 evidence를 남겼다 | 계속 진행 |
| command | `failed` | 명령이 실행됐고 현재 write scope 안에서 수리 가능하다 | `Repairing` |
| command | `blocked` | 명령을 실행할 수 없거나 현재 subtask 안에서 수리할 수 없는 선행조건이 비어 있다 | `Blocked` |
| command | `skipped` | conditional command를 trigger 부재 또는 범위 제외 사유와 함께 생략했다 | 계속 진행 |
| overall | `passed` | 모든 required command가 `passed`이고 evidence 필드가 완전하다 | `Publishing` 또는 `User Validating` |
| overall | `failed` | required command 중 하나 이상이 `failed`다 | `Repairing` |
| overall | `blocked` | required command 중 하나 이상이 `blocked`이거나 retry budget을 초과했다 | `Blocked` |

## Contract Selection Rule

- `workflow 문서 수정`은 `workflow-docs`를 기본으로 쓴다.
- `cross-repo planning`은 `cross-repo-planning`을 기본으로 쓴다.
- `git-ranker` 코드/테스트/설정 변경은 `backend-change`를 쓴다.
- `git-ranker-client` route/UI/state/config 변경은 `frontend-change`를 쓴다.
- 하나의 subtask에서 둘 이상의 profile이 동시에 필요해지면 contract를 합치지 말고 subtask split 또는 spec 갱신으로 되돌린다.

## Contract Profiles

### `workflow-docs`

대상:

- `git-ranker-workflow`의 `docs/`, `.github/`, `.codex/skills/`, `docs/specs/` 변경

Required commands:

- `sed -n '1,<N>p' <touched-doc>`
- `rg -n "<핵심 용어 또는 hook>" <touched-docs-and-hooks>`
- `git diff --check`

Conditional commands:

- template 또는 GitHub 본문이 바뀌면 render 확인 명령을 추가한다.

Evidence minimum:

- 읽은 문서 경로
- 핵심 grep 또는 수동 검토 결과
- `git diff --check` 결과

### `cross-repo-planning`

Required commands:

- `sed -n '1,<N>p' <workflow-planning-doc>`
- impacted repo entry doc 또는 공식 remote source 확인
- `rg -n "<contract noun or repo name>" <planning-docs-and-hooks>`
- `git diff --check`

Evidence minimum:

- impacted repo별로 읽은 entry doc 또는 remote source
- planning hook 검토 결과
- `git diff --check` 결과

### `backend-change`

Required commands:

- `./gradlew test`
- `./gradlew build`

Conditional commands:

- DB, Testcontainers, runtime wiring, public API end-to-end 영향을 건드리면 `./gradlew integrationTest`
- public contract regeneration이 spec에 적혀 있으면 관련 command를 추가한다

Evidence minimum:

- baseline `test`, `build` 결과
- conditional command 실행 여부와 trigger 근거
- 실패 시 preflight 또는 환경 상태 요약

### `frontend-change`

Required commands:

- `npm run lint`
- `npx tsc --noEmit`
- `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`

Conditional commands:

- route runtime, locale redirect, browser-only behavior를 직접 바꾸면 local dev 또는 preview 확인 명령을 spec에 추가한다

Evidence minimum:

- `lint`, `tsc`, `build` 결과
- 사용한 `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL` 값
- conditional runtime 확인 여부와 사유

## Verification Evidence Shape

canonical verification evidence는 spec이나 별도 verification artifact 중 최소 한 곳에 남긴다.

### Compact Verification Summary

```md
## Verification Summary
- Contract profile: `workflow-docs`
- Overall status: `passed`
- Ran:
  - `sed -n '1,260p' docs/operations/workflow-governance.md`
  - `rg -n "spec|verification evidence" docs/operations docs/architecture .codex/skills`
  - `git diff --check`
- Evidence:
  - 관련 source of truth hook이 함께 정렬됐다.
- Failure or skipped summary: 없음
- Next action: user validation
```

### Detailed Verification Report

```md
## Verification Report
- Contract profile: `frontend-change`
- Overall status: `passed`
- Preconditions:
  - `NEXT_PUBLIC_BASE_URL=http://localhost:3000`
  - `NEXT_PUBLIC_API_URL=http://localhost:8080`
- Command: `npm run lint`
  - Status: `passed`
  - Evidence: 성공
- Command: `npx tsc --noEmit`
  - Status: `passed`
  - Evidence: 성공
- Command: `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`
  - Status: `passed`
  - Evidence: 성공
- Failure summary: 없음
- Next action: publish or user validation
```

## Repair Loop Policy

- required command가 `failed`면 `Repairing`으로 들어간다.
- required command가 `blocked`면 `Blocked`다.
- required evidence가 비어 있거나 stale이면 verification은 끝난 것으로 보지 않는다.
- 같은 root cause가 두 번의 repair 뒤에도 남으면 더 밀어붙이지 말고 `Blocked` 또는 subtask split으로 전환한다.
