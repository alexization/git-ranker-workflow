# Skills

이 디렉터리는 `git-ranker-workflow`에서만 쓰는 project-local skill을 관리한다. 여기서 말하는 skill은 source of truth 문서를 대체하는 것이 아니라, 반복 작업을 같은 입력/출력/증거 규칙으로 수행하게 만드는 실행 레시피다.

## 목적

- 병렬 에이전트가 같은 품질 기준으로 작업하게 한다.
- 반복 작업을 매번 자연어로 다시 설명하지 않게 한다.
- 문서, exec plan, evidence 규칙을 실행 절차와 연결한다.

## Canonical Ownership

- 정책, vocabulary, 상태 전이, 종료 조건, evidence minimum은 `docs/operations/`, `docs/architecture/`, `docs/product/`의 source of truth가 관리한다.
- skill은 그 정책을 대체하지 않고, 한 단계의 반복 실행 절차와 handoff만 다룬다.
- registry 문서는 "지금 어떤 skill이 있고 어떤 순서로 쓰는가"만 관리한다. roadmap task ID나 진행 상태는 여기서 추적하지 않는다.
- policy와 skill이 충돌하면 skill에 새 규칙을 더하지 말고 canonical policy를 먼저 수정한 뒤 skill을 맞춘다.

## 기본 구조

- 실제 skill은 `.codex/skills/<skill-name>/SKILL.md` 구조를 사용한다.
- 각 skill 폴더의 필수 파일은 `SKILL.md` 하나다.
- 공통 설명 문서가 필요하면 `.codex/skills/` 루트에 두고, 실제 skill 지원 파일은 가능한 한 각 skill 폴더 안에 둔다.

예시:

```text
.codex/skills/
  README.md
  skill-creator/
    SKILL.md
    references/
  issue-to-exec-plan/
    SKILL.md
    assets/
```

## Naming Rules

- skill 폴더명은 `kebab-case`를 사용한다.
- 한 폴더는 한 skill만 나타낸다.
- skill 이름은 역할 중심으로 짧고 구체적으로 짓는다.
- 프로젝트 전체에 공통인 지원 자산이 실제로 생기기 전까지는 `.codex/skills/` 루트에 새 하위 디렉터리를 추가하지 않는다.

권장 예시:

- `issue-to-exec-plan`
- `parallel-work-split`
- `api-contract-sync`
- `ranking-read-harness`

피해야 할 예시:

- `skill1`
- `misc`
- `ranking`
- `agent-helper-final`

## Optional Support Directories

실제 skill에 지원 파일이 필요할 때만 각 skill 폴더 아래에 아래 이름을 추가한다.

- `references/`: 길고 상세한 참고 문서, schema, variant별 가이드
- `scripts/`: 반복되는 결정론적 작업을 위한 실행 코드
- `assets/`: 템플릿, boilerplate, 재사용 파일

예시:

```text
.codex/skills/skill-creator/
  SKILL.md
  references/
  scripts/
```

이 디렉터리들은 선택 사항이다. 필요 없는 skill에는 만들지 않는다.

## Registry Status

현재 등록된 project skill은 아래와 같다.

- `skill-creator`: 새 skill 생성, 기존 skill 리팩터링, trigger/structure/resource 설계에 사용
- `request-intake`: 새 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류하고 `default`/`guarded` lane을 고를 때 사용
- `ambiguity-interview`: `모호한 요청`을 executable issue, `Blocked`, `Rejected` 중 하나로 수렴시킬 때 사용
- `issue-to-exec-plan`: guarded lane의 issue를 active exec plan으로 바꾸고 write scope와 verification을 잠글 때 사용
- `context-pack-selection`: active exec plan 뒤에 primary context pack과 required docs, forbidden context를 잠글 때 사용
- `boundary-check`: 구현 전에 read/write/network/escalation 경계와 write scope completeness를 다시 확인할 때 사용
- `parallel-work-split`: 여러 agent를 투입하기 전에 ownership과 disjoint write set을 고정할 때 사용
- `api-contract-sync`: backend API 계약 변화가 client consumer와 workflow evidence에 미치는 영향을 맞출 때 사용
- `verification-contract-runner`: selected verification contract profile을 실행하고 latest verification report를 쓸 때 사용
- `repair-loop-triage`: verification 실패나 review 수리 요청 뒤 rerun, `Blocked`, split 중 하나를 정할 때 사용
- `reviewer-handoff`: review가 실제로 필요할 때 reviewer minimum context를 넘기고 review evidence를 남길 때 사용
- `publish-after-review`: legacy 이름이지만 current policy에서는 latest verification 뒤 open PR을 publish하는 단계에 사용
- `guardrail-ledger-update`: feedback close-out에서 guardrail ledger entry를 작성할 때 사용
- `failure-to-policy`: normalized failure를 가장 작은 guardrail asset으로 연결할 때 사용
- `quality-sweep-triage`: quality sweep signal을 cleanup candidate, guardrail follow-up, repair-now, no-action으로 분류할 때 사용
- `red`: failing test 하나로 behavior slice를 잠글 때 사용
- `green`: failing test를 production-side 최소 변경으로 green으로 만들 때 사용
- `refactor`: green을 유지한 채 구조만 정리할 때 사용

## Recommended Use

새 skill을 만들거나 기존 skill을 리팩터링할 때는 항상 `skill-creator`부터 사용한다.

새 요청을 처음 받을 때의 기본 순서는 아래와 같다.

1. `request-intake`
2. `ambiguity-interview` if route is `모호한 요청`
3. `issue-to-exec-plan` if selected lane is `guarded` or interview exits `Planned`
4. `context-pack-selection` once active exec plan exists
5. `boundary-check` before guarded-lane implementation
6. `parallel-work-split` if more than one agent will work on the same issue

아래 skill은 기본 진입 순서가 아니라 조건부 hook으로 사용한다.

- `api-contract-sync` if backend contract changed

close-out이 `Rejected`이거나 route가 `대화`로 끝나면 issue, exec plan, 파일 편집을 시작하지 않는다.

범위가 이미 issue/exec plan 수준으로 잠긴 작업은 `issue-to-exec-plan`부터 시작해도 된다.

구현 skill은 그 다음 slice에 맞춰 쓴다.

1. `red`
2. `green`
3. `refactor`

구현 뒤 close-out 순서는 아래 hook을 따른다.

1. `verification-contract-runner`
2. `publish-after-review` once latest verification report is `passed` and the open PR must be created
3. `reviewer-handoff` if independent review is required after publish
4. `repair-loop-triage` if verification failed or review requested changes
5. `guardrail-ledger-update` once feedback close-out is actually triggered
6. `failure-to-policy` when feedback close-out must choose a guardrail promotion target or `no-new-guardrail`
7. `quality-sweep-triage` when periodic or targeted quality scan is in scope

`api-contract-sync`의 canonical backend contract는 `git-ranker/docs/openapi/openapi.json`이다. workflow는 canonical spec을 복제해 소유하지 않고, sync 절차와 evidence를 관리한다.

새 skill을 추가할 때는 roadmap item이나 task ID가 아니라 asset 이름과 workflow 역할만 registry에 남긴다.

구현 결과의 publish 기준은 latest verification이다. merge-level approval이 추가로 필요하면 별도 reviewer가 담당한다.

## Related Docs

- `.codex/skills/skill-creator/SKILL.md`
- `docs/operations/workflow-governance.md`
- `docs/product/work-item-catalog.md`
