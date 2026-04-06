# 2026-04-06-grw-11-harness-system-map

- Issue ID: `GRW-11`
- GitHub Issue: `#31`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-11-harness-system-map`
- Task Slug: `2026-04-06-grw-11-harness-system-map`

## Problem

현재 하네스 canonical flow는 roadmap와 work item catalog 수준에서만 표현되어 있어, 시스템 구성요소와 상태 전이와 stop condition을 한 문서에서 읽을 수 없다. 이 상태로 `GRW-12`, `GRW-13`, `GRW-14`, `GRW-15`, `GRW-16`을 이어서 작성하면 같은 흐름을 서로 다른 용어와 완료 조건으로 설명할 위험이 있다.

또한 과거 전체 분해 문서가 `docs/plans/`에 남아 있어, 현재 계획 source of truth인 `docs/product/`와 `docs/exec-plans/` 체계와 위치가 충돌한다. 이번 작업에서는 architecture 문서와 함께 역사 문서 위치도 정리해 planning source를 하나로 고정한다.

작업 중 GitHub issue body를 CLI 인라인 문자열로 만들면 줄바꿈이 literal `\n`로 깨질 수 있다는 운영 문제도 드러났다. 같은 문제가 반복되지 않게 issue/PR 작성 가드레일도 source of truth와 planning skill에 반영해야 한다.

## Why Now

`GRW-11`은 request routing, context pack, tool boundary, verification contract, dual-agent review policy가 공유해야 하는 공통 상태 모델을 제공한다. 상태와 전이 규칙을 먼저 고정하지 않으면 후속 policy 문서가 phase 이름만 공유하고 실제 통제 의미는 달라질 수 있다.

사용자도 `docs/product/harness-roadmap.md`를 기준으로 하네스 구성을 진행하려고 하고 있다. 따라서 과거 roadmap는 source of truth 경계 밖으로 이동시켜 문서 체계를 명확히 해야 한다.

동시에 하네스 작업의 entrypoint인 GitHub issue/PR 본문이 깨지면 이후 exec plan과 review handoff의 품질도 같이 떨어진다. 따라서 body-file 규칙과 생성 직후 검증 루프를 함께 고정한다.

## Scope

- 하네스 시스템 구성요소와 책임을 `docs/architecture/`에 문서화한다.
- `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback` 흐름의 상태 전이와 역할 분리를 정의한다.
- stop condition, pass/fail semantics, repair loop의 상위 규칙을 정의한다.
- 역사 roadmap 문서를 `docs/references/` 체계로 정리하고 관련 인덱스를 갱신한다.
- GitHub issue/PR 멀티라인 본문 생성 규칙을 `--body-file` 중심으로 정리하고 재사용 템플릿을 추가한다.

## Non-scope

- request routing 세부 정책 정의
- context pack registry 상세 작성
- verification 명령 registry와 retry budget 수치 확정
- backend/frontend 앱 코드 변경
- skill 신규 작성

## Write Scope

- `docs/architecture/`
- `docs/README.md`
- `docs/operations/`
- `docs/references/`
- `docs/exec-plans/`
- `.codex/skills/issue-to-exec-plan/`

## Outputs

- `docs/architecture/harness-system-map.md`
- 갱신된 architecture/docs/reference 인덱스
- `docs/references/`로 이관된 역사 roadmap 문서
- GitHub issue body 재발 방지 규칙과 템플릿

## Working Decisions

- 현재 planning source of truth는 `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, `docs/exec-plans/`로 고정한다.
- `GRW-11`은 상태 머신의 상위 semantics만 정의하고, stage별 세부 정책은 후속 Issue에서 확장한다.
- verification/review 실패는 곧바로 완료 불가를 의미하며, 성공 경로와 실패 경로 모두 feedback 단계에서 close-out 또는 guardrail 후보 판단을 거친다.
- GitHub issue/PR 멀티라인 본문은 shell 인라인 문자열 대신 body file을 canonical 작성 방식으로 사용한다.

## Verification

- `sed -n '1,260p' docs/architecture/harness-system-map.md`
  - 결과: 시스템 구성요소, canonical state machine, pass/fail semantics, stop condition, role separation, issue/PR projection이 한 문서에 정리된 것을 확인했다.
- `rg -n "Router|Interview|Context Pack|Implementer|Verification|Reviewer|Feedback|stop condition|pass/fail|repair loop" docs/architecture docs/README.md docs/references`
  - 결과: `docs/architecture/harness-system-map.md`에서 canonical flow와 stage semantics가 grep되는 것을 확인했다.
- `find docs/references -maxdepth 1 -type f | sort`
  - 결과: `docs/references/git-ranker-harness-issue-pr-roadmap.md`가 history 문서로 존재하는 것을 확인했다.
- `rg -n "docs/plans/" docs/README.md docs/architecture docs/references`
  - 결과: 현재 source of truth 인덱스와 reference 인덱스에는 `docs/plans/` 참조가 남아 있지 않은 것을 확인했다.
- `sed -n '67,92p' docs/operations/workflow-governance.md`
  - 결과: GitHub issue/PR 본문은 `--body-file`로 만들고 생성 직후 `gh issue view --json body` 또는 `gh pr view --json body`로 확인하는 규칙이 반영된 것을 확인했다.
- `sed -n '39,78p' .codex/skills/issue-to-exec-plan/SKILL.md`
  - 결과: `issue-to-exec-plan` skill의 기본 명령이 body file 기반 issue 생성과 body 확인 루프로 바뀐 것을 확인했다.
- `sed -n '1,220p' .codex/skills/issue-to-exec-plan/templates/github-issue-body.md`
  - 결과: workflow 저장소 issue 본문을 파일로 작성할 때 바로 복사해 쓸 수 있는 템플릿이 추가된 것을 확인했다.
- 문서 링크 검토
  - 결과: `docs/README.md`, `docs/architecture/control-plane-map.md`, `docs/references/README.md`가 새 architecture 문서와 history 문서 위치를 올바르게 가리키는 것을 확인했다.

## Evidence

문서 작업이므로 별도 artifact는 만들지 않는다. 대신 아래를 근거로 남긴다.

- 시스템 맵 문서에서 정의한 canonical state와 transition
- planning source of truth와 historical reference의 분리 결과
- GitHub issue body 재발 방지 규칙과 템플릿
- verification 명령 요약

## Risks or Blockers

- verification contract의 retry budget 수치와 repair loop 최대 횟수는 `GRW-15`에서 더 구체화해야 한다.
- ambiguity interview 종료 기준은 `GRW-12`에서 세부화해야 하므로 이번 문서는 상위 상태 의미만 다룬다.

## Next Preconditions

- `GRW-12`: 요청 라우팅과 ambiguity interview 정책 정의
- `GRW-13`: context pack registry와 task-to-context 매핑 정의
- `GRW-14`: tool boundary matrix와 write scope 거버넌스 정의
- `GRW-15`: verification contract registry와 repair loop 기준 정의
- `GRW-16`: dual-agent review policy 정의
- `GRW-17`: failure-to-guardrail feedback loop 정의

## Docs Updated

- `docs/architecture/harness-system-map.md`
- `docs/architecture/control-plane-map.md`
- `docs/architecture/README.md`
- `docs/README.md`
- `docs/operations/workflow-governance.md`
- `docs/references/README.md`
- `docs/references/git-ranker-harness-issue-pr-roadmap.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/issue-to-exec-plan/templates/github-issue-body.md`
- `docs/exec-plans/completed/2026-04-06-grw-11-harness-system-map.md`

## Skill Consideration

이번 작업은 신규 skill을 만드는 단계는 아니다. 다만 상태 머신이 고정되면 후속 `GRW-S06`, `GRW-S07`, `GRW-S08`, `GRW-S09`가 각각 어느 transition을 자동화하는지 더 명확해진다. 이번 턴에서는 기존 `issue-to-exec-plan` skill에 issue body 생성 가드레일만 추가했다.
