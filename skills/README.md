# Skills

이 디렉터리는 `git-ranker-workflow`에서 재사용할 project skill을 관리한다. 여기서 말하는 skill은 source of truth 문서를 대체하는 것이 아니라, 반복 작업을 같은 입력/출력/증거 규칙으로 수행하게 만드는 실행 레시피다.

## 목적

- 병렬 에이전트가 같은 품질 기준으로 작업하게 한다.
- 반복 작업을 매번 자연어로 다시 설명하지 않게 한다.
- 문서, exec plan, evidence 규칙을 실행 절차와 연결한다.

## 기본 구조

- 실제 skill은 `skills/<skill-name>/SKILL.md` 구조를 사용한다.
- 각 skill 폴더의 필수 파일은 `SKILL.md` 하나다.
- `skills/` 루트에는 공통 설명 문서만 둔다. 실제 skill 지원 파일은 가능한 한 각 skill 폴더 안에 둔다.

예시:

```text
skills/
  README.md
  authoring-rules.md
  issue-to-exec-plan/
    SKILL.md
  ranking-read-harness/
    SKILL.md
```

## Naming Rules

- skill 폴더명은 `kebab-case`를 사용한다.
- 한 폴더는 한 skill만 나타낸다.
- skill 이름은 역할 중심으로 짧고 구체적으로 짓는다.
- 프로젝트 전체에 공통인 지원 자산이 실제로 생기기 전까지는 `skills/` 루트에 새 하위 디렉터리를 추가하지 않는다.

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

- `templates/`: 반복해서 복사하는 문서 조각, summary 틀, PR 본문 틀
- `queries/`: PromQL, LogQL, SQL, CLI query 예시
- `examples/`: 입력/출력 예시, 시뮬레이션 예시
- `checklists/`: 단계별 점검표, triage 체크리스트

예시:

```text
skills/promql-logql-evidence/
  SKILL.md
  queries/
  templates/
```

이 디렉터리들은 선택 사항이다. 필요 없는 skill에는 만들지 않는다.

## Registry Status

현재 이 디렉터리에는 authoring 규칙만 있고, 실제 project skill 본문은 아직 추가되지 않았다. 후속 작업에서 아래 skill 후보를 순서대로 채운다.

- `GRW-S02`: `issue-to-exec-plan`, `parallel-work-split`, `api-contract-sync`
- `GRW-S03`: `ranking-read-harness`, `playwright-browser-qa`, `promql-logql-evidence`
- `GRW-S04`: `batch-failure-triage`, `github-rate-limit-investigation`, `doc-gardener`

## Related Docs

- `skills/authoring-rules.md`
- `docs/operations/workflow-governance.md`
- `docs/product/work-item-catalog.md`
