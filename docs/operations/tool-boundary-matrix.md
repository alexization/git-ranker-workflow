# Tool Boundary Matrix

이 문서는 `Context Ready -> Implementing` 구간에서 어떤 도구와 접근 범위를 허용할지 고정한다.

## Boundary Invariants

- 도구 경계는 프롬프트의 편의 지시보다 우선한다.
- 더 넓은 접근이 필요하면 즉흥적으로 진행하지 말고 spec을 갱신하고 다시 승인받는다.
- 모든 실행 작업은 하나의 primary repo와 하나의 active subtask를 가진다.
- read boundary는 primary context pack과 approved spec의 named input에서 시작한다.
- write boundary는 approved spec의 `Write Scope`가 canonical source다.
- network는 default allow가 아니다.
- escalation은 마지막 수단이다.
- cross-repo 작업은 기본적으로 workflow 문서 PR과 앱 코드 PR로 분리한다.

## Task Matrix

| Task type | Read boundary | Write boundary | Network | Escalation | Default denied |
| --- | --- | --- | --- | --- | --- |
| `workflow 문서 수정` | `git-ranker-workflow`의 `docs/`, `.github/`, `.codex/skills/`, `docs/specs/`, approved spec named input까지만 읽는다 | `git-ranker-workflow`의 문서/템플릿/skill/spec 경로만 쓴다 | GitHub issue/PR 동기화와 공식 문서 확인만 허용한다 | `gh issue/pr` 발행이나 허용 경로 안 검증 명령이 막힐 때만 | sibling app code tree eager load, app repo 수정 |
| `backend 수정` | target backend repo entry docs, approved spec에 적힌 모듈/테스트/설정까지만 읽는다 | backend repo의 허용 코드/테스트/설정 경로와 control-plane artifact만 쓴다 | GitHub/공식 문서 조회, package registry, declared verification endpoint만 허용한다 | backend build/test가 sandbox에서 막힐 때만 | frontend repo 수정, backend+frontend 동시 구현 |
| `frontend 수정` | target frontend repo entry docs, approved spec에 적힌 route/component/hook/test까지만 읽는다 | frontend repo의 허용 route/UI/state/config/test 경로와 control-plane artifact만 쓴다 | GitHub/공식 문서 조회, package registry, declared verification endpoint만 허용한다 | frontend build/typecheck/lint/dev server가 sandbox에서 막힐 때만 | backend repo 수정, unrelated UI sweep |
| `cross-repo planning` | workflow planning docs와 영향받는 각 저장소의 entry docs, 필요한 contract 문서까지만 읽는다 | workflow repo의 planning 문서, spec, issue/PR body file만 쓴다 | GitHub metadata와 공식 문서 조회만 허용한다 | planning을 닫는 데 필요한 read-only inspection만 | multi-repo code diff 동시 작성, app 구현 착수 |

## Dangerous Command Rules

아래는 기본적으로 dangerous command다.

- `git reset --hard`, `git checkout --`, `git clean -fd`, branch 삭제, history rewrite, blanket `rm -rf`, force push
- 허용 경로를 넘는 repo-wide formatter, mass replace, bulk delete
- 목적과 출처가 적히지 않은 remote script 실행

사용자가 직접 요청한 경우가 아니면 실행하지 않는다.

## Escalation Decision Gate

escalation 전 아래가 모두 `yes`여야 한다.

1. 이 명령이 현재 subtask의 완료 조건이나 verification contract에 직접 필요하다.
2. 명령 대상이 approved spec의 허용 범위 안에 있다.
3. 더 좁은 non-escalated 대안이 없다.
4. 승인 요청 문장에 목적과 범위가 한 줄로 설명된다.

## Write Scope Template

approved spec에는 최소한 아래 형식의 write scope가 있어야 한다.

```md
## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
- Control-plane artifacts:
  - `docs/specs/active/<spec>.md`
- Explicitly forbidden:
  - sibling app repo code
  - named scope 밖 stable source of truth
- Network / external systems:
  - GitHub issue/PR metadata 확인
- Escalation triggers:
  - sandbox가 declared verification command를 막을 때
```

## Boundary Failure Consequences

- read boundary를 넘겼으면 추가 탐색을 멈추고 context pack이나 spec split이 맞는지 다시 확인한다.
- write boundary를 넘겼으면 임의로 계속 수정하지 말고 범위 축소 또는 task 분리를 먼저 한다.
- network 또는 escalation이 문서화된 목적 없이 필요해지면 spec을 갱신하기 전에는 실행하지 않는다.
