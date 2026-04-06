---
name: issue-to-exec-plan
description: Use this skill when a roadmap item or GitHub issue must be turned into an actionable exec plan before implementation starts.
---

# Issue To Exec Plan

## Purpose

새 Issue나 roadmap 항목을 `docs/exec-plans/active/*.md`의 실행 문서로 고정한다. 목적은 구현 아이디어를 늘리는 것이 아니라, 범위, 비범위, write scope, 검증, evidence, 다음 전제조건을 먼저 잠그는 것이다.

## Trigger

- 새 GitHub Issue를 시작한다.
- `docs/product/work-item-catalog.md`의 항목을 실제 작업으로 착수한다.
- 작업 대상이 여러 저장소나 여러 문서로 퍼질 수 있어 먼저 write scope를 좁혀야 한다.
- 후속 agent에게 같은 범위를 전달할 기준 문서가 아직 없다.

## Inputs and Preconditions

- `AGENTS.md`, `PLANS.md`, `docs/operations/workflow-governance.md`를 먼저 확인한다.
- 관련 `docs/product/*.md`, 완료된 exec plan, source of truth 문서를 읽는다.
- 대상 Issue ID, 저장소, 권장 브랜치/slug, 왜 지금 필요한지 알고 있어야 한다.
- 관련 GitHub Issue가 없으면 governance 규칙에 따라 먼저 만든다.
- 요구사항이나 canonical source가 애매하면 exec plan을 쓰기 전에 사용자에게 질문한다.

## Output and Artifact Location

- 산출물은 `docs/exec-plans/active/YYYY-MM-DD-<issue-id-lower>-<slug>.md` 문서다.
- 문서에는 최소한 아래를 남긴다.
  - Issue ID, GitHub Issue, Status, Repository, Branch Name, Task Slug
  - Problem, Why Now, Scope, Non-scope, Write Scope
  - Outputs, Verification, Evidence, Risks or Blockers
  - Next Preconditions, Docs Updated, Skill Consideration
- 작업이 끝나면 `Completed`로 갱신하고 `docs/exec-plans/completed/`로 이동한다.

## Standard Commands

반복적으로 확인하는 기본 명령 예시:

```bash
rg -n "GRW-S02|GRC-04|GRB-02" docs/product docs/exec-plans
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
cp .codex/skills/issue-to-exec-plan/templates/github-issue-body.md /tmp/<issue-id>-issue-body.md
gh issue create --repo <owner>/<target-repo> --title "[Task] <issue-id> ..." --body-file /tmp/<issue-id>-issue-body.md
gh issue view --repo <owner>/<target-repo> <issue-number> --json body
git checkout -b feat/grw-s02-core-planning-skill-pack
```

명령 자체보다 중요한 것은 "어떤 문서를 읽고 어떤 범위를 고정했는지"를 exec plan에 남기는 것이다.

`gh issue create`의 `--repo`는 항상 대상 저장소와 맞아야 한다. 예를 들어 `GRW-*`는 `alexization/git-ranker-workflow`, `GRB-*`는 `alexization/git-ranker`, `GRC-*`는 `alexization/git-ranker-client`를 쓴다.

workflow 저장소에서 멀티라인 Issue 본문을 만들 때는 `.codex/skills/issue-to-exec-plan/templates/github-issue-body.md`를 복사해 채운다. shell 인라인 `--body`, escaped `\n`, `$'...'` 문자열은 줄바꿈이 깨질 수 있으므로 쓰지 않는다.

## Required Evidence

- 어떤 source of truth 문서를 읽었는지
- 이 Issue의 scope와 non-scope를 어떻게 고정했는지
- 허용 write scope
- 예정된 verification 명령
- 남아 있는 질문이나 blocker
- 관련 GitHub Issue와 branch/slug

## Forbidden Shortcuts

- exec plan 없이 바로 코드나 문서를 수정하지 않는다.
- roadmap 문장을 그대로 복사하고 write scope나 검증을 비워두지 않는다.
- verification을 `문서 확인`, `테스트 실행`처럼 추상적으로 쓰지 않는다.
- 선행조건이 불명확한데 `Ready` 또는 `In Progress`로 올리지 않는다.
- 애매한 요구사항을 임의 해석해 plan 본문에 박지 않는다.
- 멀티라인 GitHub Issue 본문을 `gh issue create --body '...'` 또는 escaped `\n` 문자열로 직접 보내지 않는다.
- Issue 생성 후 `gh issue view --json body` 확인 없이 줄바꿈이 정상이라고 가정하지 않는다.

## Parallel Ownership Rule

- exec plan 파일 편집 ownership은 한 agent만 가진다.
- 다른 agent가 관련 문서를 읽고 요약할 수는 있지만, plan 본문 최종 통합은 plan owner가 한다.
- 동일 작업의 scope/non-scope를 여러 agent가 따로 정의하지 않는다.
- plan owner가 고정한 write scope 없이 병렬 구현 작업을 시작하지 않는다.

## Parallel Execution Don'ts

- 같은 exec plan 파일을 여러 agent가 동시에 수정하지 않는다.
- unanswered question이 남아 있는 상태에서 agent마다 다른 가정을 두고 병렬 탐색하지 않는다.
- GitHub Issue 번호, 브랜치명, slug를 agent별로 다르게 기록하지 않는다.

## Example Input

- Issue: `GRC-04`
- Goal: ranking read Playwright harness 도입
- Relevant docs:
  - `docs/product/work-item-catalog.md`
  - `docs/domain/frontend-data-flows.md`
  - `docs/operations/frontend-runtime-reference.md`
  - `docs/exec-plans/completed/2026-03-25-grw-04-frontend-routes-data-flow-docs.md`

## Example Output

```md
# 2026-03-26-grc-04-ranking-read-playwright-harness

- Issue ID: `GRC-04`
- Status: `Ready`

## Scope
- Playwright config 추가
- ranking read spec 추가
- artifact 규칙 연결

## Non-scope
- 인증 포함 전체 여정 자동화
- 디자인 변경

## Verification
- `npm run playwright -- ranking-read`
- trace/screenshot 생성 확인
```

## Handoff

구현 단계로 넘길 때는 아래를 함께 전달한다.

- active exec plan 경로
- 확정된 write scope
- verification 명령
- 남은 open question 또는 blocker
