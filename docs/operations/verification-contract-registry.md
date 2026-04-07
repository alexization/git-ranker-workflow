# Verification Contract Registry

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Verifying`, `Repairing`, `Blocked` semantics를 실제 실행 규약으로 고정한다. [tool-boundary-matrix.md](tool-boundary-matrix.md)가 "어떤 도구를 어디까지 쓸 수 있는가"를 잠근다면, 이 문서는 "무슨 명령을 어떤 증거와 함께 통과해야 다음 상태로 갈 수 있는가"를 잠근다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md), review verdict 규칙은 [dual-agent-review-policy.md](dual-agent-review-policy.md)를 따른다.

## Registry Invariants

- 모든 실행 작업은 `Verifying`에 들어가기 전에 정확히 하나의 primary contract profile을 exec plan에 적어야 한다.
- contract profile은 repo-specific 세부 contract를 대체하지 않는다. 대신 각 저장소가 최소한 지켜야 할 기본 entrypoint, evidence, retry, `Blocked` semantics를 제공한다.
- `passed`는 모든 required command가 성공하고 required evidence가 남았을 때만 성립한다.
- required command가 실행은 되었지만 실패하면 overall status는 `failed`다. 이 경우 repair loop budget 안에서만 `Repairing`으로 되돌린다.
- required command를 실행할 수 없거나 canonical source, 환경 선행조건, access boundary가 비어 있으면 overall status는 `blocked`다. 이 경우 추가 구현보다 blocker 정리가 먼저다.
- optional 또는 conditional command는 생략 가능하지만, 생략 시에도 trigger 부재 또는 제외 이유를 verification report에 남겨야 한다.
- reviewer에게 넘기는 verification report는 필수 산출물이다. report가 없거나 필드가 비어 있으면 verification은 끝난 것으로 보지 않는다.

## Status Vocabulary

| Level | Status | Meaning | Next state |
| --- | --- | --- | --- |
| command | `passed` | 명령이 기대한 종료 상태와 evidence를 남겼다 | 계속 진행 |
| command | `failed` | 명령이 실행됐고 실패 원인이 현재 write scope 안에서 수리 가능하다 | `Repairing` |
| command | `blocked` | 명령을 실행할 수 없거나 현재 issue 안에서 수리할 수 없는 선행조건이 비어 있다 | `Blocked` |
| command | `skipped` | conditional command를 trigger 부재 또는 범위 제외 사유와 함께 생략했다 | 계속 진행 |
| overall | `passed` | 모든 required command가 `passed`이고 report 필드가 완전하다 | `Reviewing` |
| overall | `failed` | required command 중 하나 이상이 `failed`이고 repair budget이 남아 있다 | `Repairing` |
| overall | `blocked` | required command 중 하나 이상이 `blocked`이거나 retry budget을 초과했다 | `Blocked` |

## Contract Selection Rule

- `workflow 문서 수정`은 `workflow-docs`를 기본으로 쓴다.
- `cross-repo planning`은 `cross-repo-planning`을 기본으로 쓴다.
- `git-ranker` 코드/테스트/설정 변경은 `backend-change`를 쓴다.
- `git-ranker-client` route/UI/state/config 변경은 `frontend-change`를 쓴다.
- 하나의 issue에서 둘 이상의 profile이 동시에 필요해지면 contract를 합치지 말고 issue 분해 또는 exec plan 갱신으로 되돌린다.

현재 control plane은 workflow 소유 runtime/orchestration 프로필을 유지하지 않는다. 이런 작업이 다시 범위에 들어오면 그때 별도 contract profile을 추가한다.

## Contract Profiles

### `workflow-docs`

대상:

- `git-ranker-workflow`의 `docs/`, `.github/`, `.codex/skills/`, `docs/exec-plans/` 변경

Required commands:

- `sed -n '1,<N>p' <touched-doc>`
- `rg -n "<핵심 용어 또는 hook>" <touched-docs-and-hooks>`
- `git diff --check`

Conditional commands:

- 직접 링크된 이웃 문서가 바뀌는 경우 관련 `sed -n` 또는 `rg -n` 검토를 추가한다.
- template 또는 GitHub 본문이 바뀌면 `gh issue view --json body` 또는 `gh pr view --json body`로 render를 확인한다.

Pass signal:

- 문서 본문에 scope, rule, hook, evidence semantics가 일관되게 반영되고 grep 결과로 인접 hook이 확인된다.

Blocked triggers:

- named source of truth가 없거나 서로 충돌해 새 정책 발명이 필요한 경우
- touched doc의 인접 hook을 설명할 수 없을 정도로 context가 비어 있는 경우

Evidence minimum:

- 읽은 문서 경로
- 핵심 grep 또는 수동 검토 결과
- `git diff --check` 결과

### `cross-repo-planning`

대상:

- workflow 저장소에만 쓰지만 sibling repo의 entrypoint, contract, verification surface를 읽어야 하는 planning 작업

Required commands:

- `sed -n '1,<N>p' <workflow-planning-doc>`
- impacted repo entry doc 또는 공식 remote source 확인
- `rg -n "<contract noun or repo name>" <planning-docs-and-hooks>`
- `git diff --check`

Conditional commands:

- 로컬 worktree가 없으면 GitHub의 공식 file fetch 또는 issue metadata 확인으로 대체하되, 어떤 remote source를 썼는지 report에 적는다.

Pass signal:

- 각 impacted repo의 기본 entrypoint와 verification surface가 plan/source of truth에 명시되고, workflow 문서가 이를 정확히 인용한다.

Blocked triggers:

- impacted repo entry doc, worktree, 공식 remote source 중 어떤 것도 확보되지 않는 경우
- 여러 저장소 구현을 한 issue에 묶어야만 verification을 설명할 수 있는 경우

Evidence minimum:

- impacted repo별로 읽은 entry doc 또는 remote source
- workflow planning hook 검토 결과
- `git diff --check` 결과

### `backend-change`

대상:

- `git-ranker`의 backend 코드, 테스트, 설정, OpenAPI snapshot entrypoint 변경

Required commands:

- `./gradlew test`
- `./gradlew build`

Conditional commands:

- DB, Testcontainers, 배치, runtime wiring, public API end-to-end 영향을 건드리면 `./gradlew integrationTest`
- line coverage gate를 직접 다루면 `./gradlew jacocoTestCoverageVerification`
- public `/api/v1/**` contract를 바꾸면 `./gradlew generateOpenApiSpec`

Pass signal:

- unit/build baseline이 통과하고, trigger된 integration/coverage/OpenAPI 명령도 모두 성공한다.

Blocked triggers:

- required integration test에 필요한 Docker 또는 runtime 선행조건이 없고 현재 issue 안에서 복구할 수 없는 경우
- OpenAPI snapshot을 갱신해야 하지만 source contract 또는 출력 경로가 잠겨 있지 않은 경우

Evidence minimum:

- baseline `test`, `build` 결과
- conditional command 실행 여부와 trigger 근거
- 실패 시 preflight 또는 환경 상태 요약

Source notes:

- baseline Gradle entrypoint는 `git-ranker/build.gradle`을 기준으로 한다.
- OpenAPI regeneration entrypoint는 `git-ranker/docs/openapi/README.md`를 기준으로 한다.

### `frontend-change`

대상:

- `git-ranker-client`의 route, UI, state, config, build/runtime env 변경

Required commands:

- `npm run lint`
- `npx tsc --noEmit`
- `NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build`

Conditional commands:

- route runtime, locale redirect, CSP, browser-only behavior를 직접 바꾸면 local dev 또는 preview 확인 명령을 exec plan에 추가한다.
- remote source inspection만 가능한 경우 현재 repo README와 package manifest를 함께 근거로 남긴다.

Pass signal:

- lint, typecheck, build가 모두 성공하고 required `NEXT_PUBLIC_*` env 전제가 report에 남는다.

Blocked triggers:

- required public env 값이나 runtime origin 정책이 잠겨 있지 않은 경우
- local worktree와 공식 remote source 모두 없어 current entrypoint를 확인할 수 없는 경우

Evidence minimum:

- `lint`, `tsc`, `build` 결과
- 사용한 `NEXT_PUBLIC_BASE_URL`, `NEXT_PUBLIC_API_URL` 값
- conditional runtime 확인 여부와 사유

Source notes:

- 기본 명령과 env 전제는 `git-ranker-client/README.md`, `git-ranker-client/package.json`, `git-ranker-client/.env.example`를 기준으로 한다.

## Verification Report Shape

verification report는 exec plan이나 PR 본문 중 최소 한 곳에 아래 필드를 남긴다.

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
- Next action: reviewer handoff
```

필수 필드:

- `Contract profile`
- `Overall status`
- `Preconditions` 또는 relevant env/runtime 전제
- command별 `Status`
- command별 `Evidence`
- `Failure summary`
- `Next action`

추가 규칙:

- conditional command를 생략하면 `Status: skipped`와 생략 이유를 같이 적는다.
- reviewer는 최신 report 하나만 읽어도 전체 required command 상태를 판단할 수 있어야 한다.
- 이전 repair attempt의 실패 로그는 남길 수 있지만, 최종 report에는 "현재 최신 기준에서 어떤 명령이 통과했는가"가 다시 요약돼야 한다.

## Repair Loop Policy

### Entry Criteria

아래 중 하나가 생기면 `Repairing`으로 들어간다.

- required command가 `failed`다.
- required evidence가 비어 있다.
- reviewer가 "diff와 verification report가 불일치한다"고 판단했다.

아래 중 하나면 곧바로 `Blocked`다.

- required command가 `blocked`다.
- canonical source, repo entry doc, required worktree/remote source가 없다.
- 필요한 env, Docker, 포트, credential, external dependency가 현재 issue 범위 밖이다.

### Retry Budget

- 기본 budget은 "첫 실패 후 최대 2회의 repair attempt"다.
- 각 repair attempt는 실패 원인을 좁히는 실제 수정 또는 환경 교정 하나와, 그에 대응하는 command 재실행을 함께 남겨야 한다.
- 같은 root cause가 2회 repair 뒤에도 남아 있으면 더 오래 밀어붙이지 말고 `Blocked` 또는 후속 issue split으로 전환한다.
- 새로운 failure class가 추가로 드러나면 budget을 리셋하지 않는다. 현재 issue에서 안전하게 줄일 수 없는 범위 확장은 follow-up으로 넘긴다.

### Re-run Rule

- repair 후에는 최소한 실패했던 required command를 다시 실행한다.
- failure가 baseline command에 걸려 있었으면 그 아래 conditional command를 통과로 간주하지 않는다. 최신 report에서 다시 상태를 적어야 한다.
- reviewer handoff 전에는 latest report 기준으로 모든 required command가 `passed`여야 한다.

### Blocked / Stop Conditions

| Signal | Meaning | Required action |
| --- | --- | --- |
| retry budget exhausted | 같은 issue에서 수리 루프를 더 돌려도 신호가 나아지지 않는다 | `Blocked` 또는 follow-up issue split |
| missing canonical source | 어떤 명령을 정답으로 써야 하는지 source of truth가 없다 | planning 또는 source-of-truth update 먼저 |
| environment prerequisite absent | Docker, env, port, credential, runtime이 현재 범위 밖이다 | 현재 issue는 `Blocked`로 정리 |
| access boundary conflict | 허용되지 않은 저장소/경로/네트워크가 필요하다 | boundary 갱신 또는 issue 분해 |
| evidence mismatch | 명령 결과와 diff 또는 문서 서술이 서로 맞지 않는다 | 재검증 후 report 갱신 |

## Reviewer Handoff Minimum

reviewer에게 넘길 때는 최소한 아래 입력이 함께 있어야 한다.

- exec plan 경로
- latest verification report
- touched diff 요약
- source-of-truth update 목록 또는 업데이트 불필요 사유
- 남은 리스크 또는 conditional command 생략 사유

이 입력은 [dual-agent-review-policy.md](dual-agent-review-policy.md)의 `Reviewer Minimum Context`와 동일한 handoff surface다.

single reviewer뿐 아니라 session-isolated reviewer pool을 쓸 때도 이 handoff surface를 그대로 fan-out한다. role prompt는 이 surface 위에 추가되는 focus일 뿐, minimum context를 없애거나 final verdict owner의 확인 책임을 덜어내는 근거가 아니다.

각 reviewer는 자기 역할에 필요한 subset만 읽을 수 있지만, final verdict owner는 latest verification report와 reviewer finding을 같은 revision 기준으로 정렬해야 한다.

이 입력이 비어 있으면 review 단계로 넘어간 것으로 보지 않는다.
