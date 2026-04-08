# 2026-04-08-grw-s07-context-pack-boundary-skill-pack

- Issue ID: `GRW-S07`
- GitHub Issue: `#68`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s07-context-pack-boundary-skill-pack`
- Task Slug: `2026-04-08-grw-s07-context-pack-boundary-skill-pack`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`GRW-13`에서 task type별 primary context pack, required docs, optional docs, forbidden context, hot file exploration 규칙이 source of truth로 고정됐다. `GRW-14`에서는 같은 task type 분류를 기준으로 read/write/network/escalation boundary와 write scope template까지 문서화됐다. 하지만 implementer가 실제 작업 착수 전에 이 두 문서를 같은 순서와 같은 stop signal로 재사용하게 만드는 project-local skill pack은 아직 없다.

이 공백이 남아 있으면 같은 `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 작업도 누군가는 sibling repo를 먼저 열고, 누군가는 required docs 대신 optional docs를 먼저 읽고, 누군가는 write scope와 escalation trigger를 exec plan에 느슨하게 적는 drift가 생길 수 있다.

## Why Now

`GRW-S06`은 intake와 ambiguity narrowing을 operationalize했고, `GRW-S08`, `GRW-S09`는 verification 이후 close-out loop를 thin layer로 고정했다. implementer 단계 앞단에 해당하는 `Context Pack -> Boundary Check`가 빠져 있으면 Phase 2 skill pack은 시작과 종료만 있고, 실제 착수 조건을 잠그는 반복 절차가 비어 있게 된다.

또한 `GRW-13`, `GRW-14` completed exec plan이 후속 자산으로 직접 `context-pack-selection`, `boundary-check` skill을 남겨 두었다. canonical policy는 이미 있으므로 이번 작업은 새 policy를 발명하는 것이 아니라, 그 규칙을 실제 구현 전에 재현하는 thin-layer skill 2종을 추가하는 데 집중한다.

## Scope

- `.codex/skills/context-pack-selection/SKILL.md` 작성
- `.codex/skills/boundary-check/SKILL.md` 작성
- `.codex/skills/README.md`에 새 skill registry와 recommended use hook 반영
- `GRW-S07` exec plan 작성과 close-out 기록 정리

## Non-scope

- `docs/architecture/context-pack-registry.md` 또는 `docs/operations/tool-boundary-matrix.md`의 policy 재설계
- backend/frontend 앱 코드 변경
- 자동 context loader, runtime enforcement, sandbox 구현
- verification/review/feedback skill 또는 policy 재작업
- stable source of truth에 task ID를 설명용으로 추가하는 문서 개편

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-08-grw-s07-context-pack-boundary-skill-pack.md`
  - `docs/exec-plans/completed/2026-04-08-grw-s07-context-pack-boundary-skill-pack.md`
  - `/tmp/grw-s07-issue-body.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/architecture/`, `docs/operations/`, `docs/product/`의 policy 재설계
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue create/view
- Escalation triggers:
  - 없음

## Outputs

- `.codex/skills/context-pack-selection/SKILL.md`
- `.codex/skills/boundary-check/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-s07-context-pack-boundary-skill-pack.md`

## Working Decisions

- `context-pack-selection`은 `docs/architecture/context-pack-registry.md`를 canonical source로 두고, request/issue/exec plan에서 primary repo와 task type이 잠긴 뒤 required docs, optional trigger, forbidden context, hot file stop signal을 정리하는 역할만 맡는다.
- `boundary-check`는 `docs/operations/tool-boundary-matrix.md`, `docs/operations/workflow-governance.md`, active exec plan의 write scope를 canonical source로 두고, read/write/network/escalation 경계와 write scope completeness를 다시 점검하는 역할만 맡는다.
- 두 skill 모두 policy 표를 복사하지 않고, "무엇을 먼저 확인하고 어떤 경우에 planning 또는 blocker로 되돌릴지"를 얇은 workflow로만 제공한다.
- `.codex/skills/README.md`에는 task ID가 아니라 asset 이름과 implementer 단계 hook만 반영한다.

## Verification

- `find .codex/skills -maxdepth 2 -type f | sort`
  - 결과: `.codex/skills/context-pack-selection/SKILL.md`, `.codex/skills/boundary-check/SKILL.md`가 registry 아래 기대 경로에 추가된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/context-pack-selection/SKILL.md`
  - 결과: primary repo/task type 잠금, single-pack selection, required docs, optional trigger, forbidden context, hot file stop signal이 포함된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/boundary-check/SKILL.md`
  - 결과: read/write/network/escalation 경계, write scope completeness, convenience escalation 금지, boundary conflict return signal이 포함된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/README.md`
  - 결과: 새 skill registry와 `issue-to-exec-plan -> context-pack-selection -> boundary-check` 추천 순서가 반영된 것을 확인했다.
- `rg -n "context-pack-selection|boundary-check|workflow-docs|backend-change|frontend-change|cross-repo-planning|read boundary|write scope|forbidden context|escalation" .codex/skills docs/architecture docs/operations`
  - 결과: skill 본문과 canonical source가 `workflow-docs`, `backend-change`, `frontend-change`, `cross-repo-planning`, read/write boundary, forbidden context, escalation vocabulary를 함께 재사용하는 것을 확인했다.
- representative task 수동 시뮬레이션 2건
  - 결과: "하네스 정책 문서를 정리한다" surface는 `workflow-docs` pack과 workflow-only write boundary로, "backend verification command를 정리한다" surface는 `backend-change` pack과 backend-only write boundary로 각각 좁혀져 두 skill의 역할 분리가 유지되는 것을 확인했다.
- `gh issue view --repo alexization/git-ranker-workflow 68 --json body,title,number`
  - 결과: Issue `#68` 본문이 템플릿 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - workflow 저장소의 skill/doc 전용 변경
  - GitHub Issue `#68`, feature branch, exec plan이 준비됨
- Command: `find .codex/skills -maxdepth 2 -type f | sort`
  - Status: `passed`
  - Evidence: 새 skill 2종이 기대 경로에 추가됐다.
- Command: `sed -n '1,260p' .codex/skills/context-pack-selection/SKILL.md`
  - Status: `passed`
  - Evidence: primary pack selection, required/optional/forbidden context, stop signal이 포함됐다.
- Command: `sed -n '1,260p' .codex/skills/boundary-check/SKILL.md`
  - Status: `passed`
  - Evidence: read/write/network/escalation boundary와 write scope completeness 점검이 포함됐다.
- Command: `sed -n '1,260p' .codex/skills/README.md`
  - Status: `passed`
  - Evidence: registry와 recommended use가 새 implementer-start hook을 반영한다.
- Command: `rg -n "context-pack-selection|boundary-check|workflow-docs|backend-change|frontend-change|cross-repo-planning|read boundary|write scope|forbidden context|escalation" .codex/skills docs/architecture docs/operations`
  - Status: `passed`
  - Evidence: 새 skill과 canonical source가 같은 vocabulary와 hook을 공유한다.
- Command: `gh issue view --repo alexization/git-ranker-workflow 68 --json body,title,number`
  - Status: `passed`
  - Evidence: Issue `#68` 본문이 기대한 섹션과 줄바꿈을 유지한다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: formatting 오류가 없다.
- Failure summary: 없음
- Next action: `Context Pack -> Boundary Check` handoff를 pilot 또는 repo-specific task에서 재사용

## Evidence

- skill 본문 2종
- registry 업데이트 결과
- representative task simulation 메모
- GitHub Issue `#68` body 확인 결과
- `git diff --check` 결과

## Independent Review

- Not run
- Reason: 이번 턴은 로컬 skill authoring과 close-out 정리까지만 범위에 포함했고, session-isolated reviewer pool handoff는 별도 요청하지 않았다.

## Risks or Blockers

- skill이 context pack registry나 tool boundary matrix를 과도하게 재서술하면 source of truth drift가 생길 수 있다.
- `context-pack-selection`과 `boundary-check`의 책임이 겹치면 planning/implementation 경계가 다시 흐려질 수 있다.
- repo-specific 예시를 너무 많이 넣으면 thin-layer skill보다 mini policy 복제가 될 수 있다.
- 실제 runtime에서의 재사용성은 `GRW-18` pilot이나 repo-specific task에서 다시 검증해야 한다.

## Next Preconditions

- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증
- repo-specific 구현 작업에서 `Context Pack -> Boundary Check` handoff를 실제로 재사용

## Docs Updated

- `.codex/skills/context-pack-selection/SKILL.md`
- `.codex/skills/boundary-check/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-08-grw-s07-context-pack-boundary-skill-pack.md`

## Skill Consideration

이번 Issue 자체가 implementer 시작 단계 thin-layer skill pack을 추가하는 작업이다. 새 skill은 policy를 대체하지 않고, context selection과 boundary check를 같은 입력/출력/증거 규칙으로 재사용하게 만드는 실행 레시피에 집중한다.
