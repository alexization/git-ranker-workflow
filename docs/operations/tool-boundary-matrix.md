# Tool Boundary Matrix

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Context Ready -> Implementing` 구간에서 어떤 도구와 접근 범위를 허용할지 고정한다. [../architecture/context-pack-registry.md](../architecture/context-pack-registry.md)가 "무엇을 읽기 시작할 수 있는가"를 잠근다면, 이 문서는 "어떤 도구를 어떤 범위로 쓸 수 있는가"를 잠근다.

공통 운영 규칙은 [workflow-governance.md](workflow-governance.md)를 따른다.

## Boundary Invariants

- 도구 경계는 프롬프트의 편의 지시보다 우선한다. 더 넓은 접근이 필요하면 즉흥적으로 진행하지 말고 exec plan 또는 issue 분해로 되돌린다.
- 모든 실행 작업은 하나의 primary repo와 하나의 task type을 가진다. 이 기준이 흔들리면 `cross-repo planning`으로 되돌린다.
- read boundary는 primary context pack과 issue/exec plan의 named input에서 시작한다. 다른 저장소나 다른 pack의 required docs가 필요해지면 boundary를 넓히지 말고 planning을 갱신한다.
- write boundary는 "primary repo의 허용 경로"와 "control-plane artifact"를 분리해서 적는다. app repo 작업이라도 workflow의 exec plan, PR 본문, `.artifacts/<task-slug>/` 같은 control-plane artifact만 예외적으로 함께 쓸 수 있다.
- network는 default allow가 아니다. issue publication, verification contract, evidence query, 공식 문서 확인처럼 목적이 명시된 경우에만 연다.
- escalation은 마지막 수단이다. sandbox나 기본 도구로 충분한데 편의상 올리지 않는다.
- cross-repo 작업은 기본적으로 `workflow 문서 PR`과 `앱 코드 PR`로 분리한다. 한 번의 구현 루프에서 여러 저장소 code diff를 동시에 만들지 않는다.
- prompt, TODO, follow-up 메모가 write scope를 자동으로 넓혀 주지 않는다. 허용 경로는 issue와 exec plan이 canonical source다.

## Access Class Definitions

| Axis | Pass Signal | Fail Signal |
| --- | --- | --- |
| read boundary | primary context pack, named source, nearest hot file까지만 읽는다 | sibling repo 전체나 무관한 stable docs를 "혹시 필요할까" 수준으로 먼저 연다 |
| write boundary | issue/exec plan에 적힌 경로와 control-plane artifact만 수정한다 | 다른 저장소 코드, unrelated stable docs, 선언되지 않은 대량 rewrite를 함께 건드린다 |
| network | 목적이 있는 외부 시스템만 연다 | ad-hoc browsing, 무관한 원격 fetch, 설명 없는 dependency/network call을 실행한다 |
| escalation | sandbox에서 막힌 필수 명령을 좁은 범위로 요청한다 | 더 좁은 대안이 있는데도 broad approval이나 convenience escalation을 요청한다 |

## Task Matrix

| Task type | Read boundary | Write boundary | Network | Escalation | Default denied |
| --- | --- | --- | --- | --- | --- |
| `workflow 문서 수정` | `git-ranker-workflow`의 `docs/`, `.github/`, `.codex/skills/`, active/completed exec plan, issue/exec plan named input까지만 읽는다. sibling app repo code tree는 planning 또는 repo-specific pack 없이 먼저 열지 않는다. | `git-ranker-workflow`의 문서/템플릿/skill 경로와 `docs/exec-plans/`만 쓴다. app repo code, app repo 설정 파일은 쓰지 않는다. | GitHub issue/PR 동기화, 공식 문서 확인, 문서 검증에 필요한 read-only 조회만 허용한다. package install, app runtime endpoint 호출은 기본 금지다. | `gh issue/pr` 발행, 허용 경로 안 문서 편집을 위해 꼭 필요한 명령만 올린다. 포트 바인딩, Docker, GUI 실행은 기본적으로 이 task type의 escalation 사유가 아니다. | sibling app code tree eager load, app repo 수정, repo-wide formatter 실행, destructive git 명령 |
| `backend 수정` | target backend repo entry docs, issue/exec plan에 적힌 모듈/테스트/설정, surface cue에 매칭된 workflow 문서 최소 범위만 읽는다. frontend 내부 구현은 읽지 않는다. | backend repo의 허용 코드/테스트/설정 경로와 control-plane artifact만 쓴다. frontend repo 코드와 workflow stable docs 전체 수정은 금지다. | GitHub/공식 문서 조회, package registry, container/image fetch, verification contract에 적힌 local/runtime endpoint만 허용한다. 목적 없는 웹 탐색은 금지다. | backend build/test, Docker, 로컬 포트, repo write가 sandbox에서 막힐 때만 요청한다. 승인 범위는 backend repo와 declared verification command로 좁힌다. | frontend repo 수정, backend+frontend 동시 구현, secret 조회, broad filesystem write, destructive git 명령 |
| `frontend 수정` | target frontend repo entry docs, issue/exec plan에 적힌 route/component/hook/test, surface cue에 맞는 workflow 문서 최소 범위만 읽는다. backend 내부 구현은 읽지 않는다. | frontend repo의 허용 route/UI/state/config/test 경로와 control-plane artifact만 쓴다. backend repo 코드와 workflow stable docs 전체 수정은 금지다. | GitHub/공식 문서 조회, package registry, verification contract에 적힌 local dev/runtime endpoint만 허용한다. 임의의 외부 자산 의존성 추가는 금지다. | frontend build/typecheck/lint/dev server/browser automation이 sandbox에서 막힐 때만 요청한다. 승인 범위는 frontend repo와 declared verification command로 좁힌다. | backend repo 수정, unrelated UI sweep, remote asset 의존성 추가, secret 조회, destructive git 명령 |
| `cross-repo planning` | workflow planning docs와 영향받는 각 저장소의 entry docs, 필요한 contract 문서까지만 읽는다. 여러 저장소 code tree를 동시에 깊게 읽지 않는다. | workflow repo의 planning 문서, exec plan, issue/PR body file, 필요 시 `.artifacts/`만 쓴다. app repo code는 쓰지 않는다. | GitHub issue/PR metadata, repository inventory, 공식 문서 조회만 허용한다. package install, app runtime endpoint, CI rerun 같은 구현성 네트워크는 금지다. | GitHub issue/PR 생성·조회, read-only repo inspection처럼 planning을 닫는 데 필요한 명령만 올린다. app runtime/test 실행을 위한 escalation은 금지다. | multi-repo code diff 동시 작성, app repo 구현 착수, runtime 실행, destructive git 명령 |

## Dangerous Command Rules

아래는 기본적으로 `dangerous command`로 본다.

- `git reset --hard`, `git checkout --`, `git clean -fd`, branch 삭제, history rewrite, blanket `rm -rf`, force push
- 허용 경로를 넘는 repo-wide formatter, mass replace, bulk delete
- 목적과 출처가 적히지 않은 remote script 실행, credential/secrets 조회, 무단 외부 업로드
- 다른 저장소나 다른 task type 경계까지 한 번에 넓히는 broad automation

예외 규칙:

- 사용자가 직접 요청한 destructive 작업이거나, recoverable cleanup이면서 대상 경로와 이유가 좁게 고정된 경우만 별도 승인 후보가 된다.
- 같은 목표를 read-only 명령, narrower path, non-escalated command로 달성할 수 있으면 dangerous command와 escalation을 선택하지 않는다.

## Escalation Decision Gate

escalation을 요청하기 전 아래 질문에 모두 `yes`여야 한다.

1. 이 명령이 지금 task의 완료 조건이나 verification contract에 직접 필요하다.
2. 명령의 read/write 대상이 현재 issue와 exec plan의 허용 범위 안에 있다.
3. sandbox, local read-only command, connector, 더 좁은 명령으로는 같은 결과를 얻을 수 없다.
4. 승인 요청 문장에 목적과 범위가 한 줄로 설명된다.

하나라도 `no`면 escalation 대신 scope 축소, planning 갱신, 다른 도구 선택으로 되돌린다.

## Write Scope Template

issue와 exec plan에는 최소한 아래 형식으로 write scope를 적는다.

```md
## Write Scope
- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
- Control-plane artifacts:
  - `docs/exec-plans/active/<task-slug>.md`
  - `.artifacts/<task-slug>/` 필요 시
- Explicitly forbidden:
  - sibling app repo code
  - named scope 밖 stable source of truth
- Network / external systems:
  - GitHub issue/PR metadata 확인
  - 공식 문서 조회 필요 시
- Escalation triggers:
  - sandbox가 `gh issue create`를 막을 때
  - declared verification command가 port/Docker 권한을 요구할 때
```

규칙:

- `Allowed write paths`는 디렉터리 또는 파일 단위로 적고, "repo 전체"처럼 넓은 표현은 기본값으로 쓰지 않는다.
- app repo 작업에서도 workflow control-plane artifact를 함께 쓰려면 별도 줄로 분리해서 적는다.
- `Explicitly forbidden`에는 같은 요청에서 헷갈리기 쉬운 sibling repo나 adjacent stable docs를 적는다.
- network가 전혀 필요 없으면 `없음`이라고 적는다. 침묵으로 생략하지 않는다.
- escalation trigger는 실제로 올릴 수 있는 명령 class만 적고, 막연한 "필요 시 권한 요청" 표현은 쓰지 않는다.

## Representative Allow / Deny Cases

| Task type | Allow | Deny | Why |
| --- | --- | --- | --- |
| `workflow 문서 수정` | `docs/operations/tool-boundary-matrix.md`와 `docs/operations/workflow-governance.md`를 수정하고 issue body 렌더링을 확인한다 | `git-ranker-client`의 route 코드를 미리 읽거나 backend README를 같이 수정한다 | workflow-docs pack은 문서/템플릿 범위만 허용한다 |
| `backend 수정` | backend service와 nearest test를 수정하고 workflow exec plan에 verification 결과를 남긴다 | 같은 턴에서 client component를 같이 수정한다 | app code 변경은 저장소별 issue/PR로 분리한다 |
| `frontend 수정` | client route, hook, test를 수정하고 lint/typecheck/build를 실행한다 | backend repository/service 구현을 열어 직접 수정한다 | frontend task는 contract surface까지만 넘겨 읽고 backend 내부 구현은 분리한다 |
| `cross-repo planning` | 두 저장소의 entry docs를 읽고 repo별 첫 issue/PR 분해 문서를 작성한다 | backend와 frontend 코드를 한 branch에서 동시에 수정한다 | planning 단계는 contract와 split을 고정할 뿐 구현을 시작하지 않는다 |

## Boundary Failure Consequences

- read boundary를 넘겼으면 추가 탐색을 멈추고 primary context pack 또는 issue 분해가 맞는지 다시 확인한다.
- write boundary를 넘겼으면 임의로 계속 수정하지 말고, 범위 축소 또는 작업 분리를 먼저 한다.
- network 또는 escalation이 문서화된 목적 없이 필요해지면 verification contract 또는 exec plan을 갱신하기 전에는 실행하지 않는다.
- dangerous command가 필요해 보이면 대안이 없는지 먼저 적고, 사용자 승인 또는 별도 planning 없이는 진행하지 않는다.
