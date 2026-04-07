# 2026-04-07-grw-20-pr-publish-review-order

- Issue ID: `GRW-20`
- GitHub Issue: `#45`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-20-pr-publish-review-order`
- Task Slug: `2026-04-07-grw-20-pr-publish-review-order`

## Problem

현재 workflow source of truth는 PR 생성 순서를 `작업 후 PR 생성 -> PR 본문에 review 결과 채우기`처럼 읽히게 적고 있으며, PR을 언제 draft로 만들고 언제 open으로 만들어야 하는지도 명시하지 않는다.

이 상태에서는 사용자가 open PR을 원해도 실행자가 draft를 기본값으로 적용하거나, independent review를 PR 생성 이후의 절차처럼 다루는 drift가 생길 수 있다. dual-agent review의 목적이 "publish 전 독립 검토"라면, review는 기본적으로 PR publish 전에 끝나야 하고 PR에는 이미 latest verification/review evidence가 실린 상태여야 한다.

## Why Now

실제 작업에서 open PR 요청과 draft 기본값이 충돌했고, reviewer 수행 시점도 사용자 기대와 현재 문서 해석 사이에 차이가 드러났다. 이 공백을 그대로 두면 같은 publish/review ordering 혼선이 반복된다.

또한 `Issue 1개 = PR 1개`, `verification`, `independent review`, `feedback`을 하네스 핵심 통제로 두고 있으므로, PR publication semantics와 review ordering을 source of truth로 바로 잠가야 이후 작업이 일관되게 따른다.

## Scope

- PR publish의 기본값을 `open`으로 고정하고, draft는 사용자 명시 요청 또는 선언된 blocker가 있을 때만 허용한다.
- independent review의 기본 수행 시점을 `pre-PR publish`로 정렬한다.
- 관련 governance, review policy, architecture, roadmap hook을 갱신한다.
- 이번 작업 자체는 새 규칙에 맞게 PR publish 전에 독립 review를 먼저 수행한다.

## Non-scope

- GitHub Actions, branch protection, reviewer auto-assignment 구현
- backend/frontend 앱 코드 변경
- 기존 `GRW-17` PR 내용 수정
- `.github/` template 구조 대수선

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/` 필요 시
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-07-grw-20-pr-publish-review-order.md`
  - `.artifacts/2026-04-07-grw-20-pr-publish-review-order/` 필요 시
- Explicitly forbidden:
  - sibling app repo code write
  - 기존 `GRW-17` PR 본문 수정
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue/PR create/view
- Escalation triggers:
  - sandbox가 git stage/commit/push를 막을 때

## Outputs

- PR publication semantics와 pre-PR review ordering을 반영한 source of truth
- independent review evidence를 포함한 `GRW-20` exec plan
- open PR default 규칙을 반영한 publish 결과

## Working Decisions

- 이번 작업의 primary context pack은 `workflow-docs`다.
- PR publication은 기본적으로 review 이후에 수행한다. PR은 review를 받기 위한 초안이 아니라, 최신 verification/review evidence를 publish하는 컨테이너로 본다.
- draft PR은 기본값이 아니다. 사용자 명시 요청 또는 scope-complete 전 공유가 필요한 blocker가 있을 때만 예외적으로 사용한다.
- independent review evidence는 PR 생성 전에 먼저 만들고, PR에는 그 결과를 싣는다.

## Verification

- `sed -n '1,260p' docs/operations/workflow-governance.md`
  - 결과: PR은 기본적으로 open으로 생성하고, independent review 이후 PR body를 채운 뒤 publish하는 순서가 반영된 것을 확인했다.
- `sed -n '1,260p' docs/operations/dual-agent-review-policy.md`
  - 결과: PR 존재 여부가 review 선행조건이 아니며, latest review verdict를 PR publish 시점에 싣는다는 규칙이 반영된 것을 확인했다.
- `sed -n '1,180p' docs/architecture/harness-system-map.md`
  - 결과: PR projection이 local verification/review/feedback 결과를 정리한 뒤 publish하는 컨테이너로 읽히도록 갱신된 것을 확인했다.
- `sed -n '1,90p' docs/product/harness-roadmap.md`
  - 결과: roadmap의 고정 결정에 open-by-default와 pre-PR review publish 순서가 추가된 것을 확인했다.
- `rg -n "draft PR|open PR|open으로 생성|independent review를 먼저|PR 존재 여부|publish|gh pr create|Independent Review" docs/operations docs/architecture docs/product docs/exec-plans`
  - 결과: touched 문서의 용어와 순서가 같은 의미로 grep되는 것을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- GitHub Issue `#45` body render 확인
  - 결과: issue 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- independent review
  - 결과: `Gemini CLI (gemini-2.5-flash)` reviewer가 diff와 touched policy 문서를 검토했고 `approved` verdict를 남겼다. blocking inconsistency는 없고, open-by-default와 pre-PR review semantics가 일관되게 반영됐다고 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- publish/review ordering policy 본문
- hook 문서 갱신 결과
- independent review evidence
- `git diff --check` 결과
- GitHub issue body render 확인 결과

## Independent Review

- Implementer: `Codex`
- Reviewer: `Gemini CLI (gemini-2.5-flash)`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/completed/2026-04-07-grw-20-pr-publish-review-order.md`
  - Latest verification report: `passed`
  - Diff summary: governance, review policy, architecture, roadmap에 `open-by-default`와 `pre-PR independent review` semantics 반영
  - Source-of-truth update: `docs/operations/workflow-governance.md`, `docs/operations/dual-agent-review-policy.md`, `docs/architecture/harness-system-map.md`, `docs/product/harness-roadmap.md`
  - Remaining risks / skipped checks: publish skill/template 후속 정렬 필요 가능성
- Review Verdict: `approved`
- Findings / Change Requests:
  - blocking finding 없음
- Evidence:
  - reviewer는 touched 문서 전반에서 `draft는 예외`, `review는 PR 선행 가능`, `PR은 review/evidence를 싣고 publish` 세 규칙이 서로 충돌 없이 반영됐다고 확인했다.

## Risks or Blockers

- 기존 문서가 PR을 review 진행 중 컨테이너처럼 읽히게 적혀 있어, 한두 문서만 바꾸면 순서가 다시 충돌할 수 있다.
- open-by-default 규칙을 적더라도 publish skill이나 관성적 절차가 draft를 계속 기본값처럼 쓰면 drift가 남을 수 있다.
- repo 밖 publish skill 문서나 외부 개인 습관은 이번 수정만으로 자동 정렬되지 않는다.

## Next Preconditions

- 필요 시 publish skill 또는 template 가이드의 후속 정렬

## Docs Updated

- `docs/exec-plans/completed/2026-04-07-grw-20-pr-publish-review-order.md`
- `docs/operations/workflow-governance.md`
- `docs/operations/dual-agent-review-policy.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 대신 PR publish와 reviewer handoff 순서가 반복적으로 흔들리면 후속 publish/reviewer-handoff skill에서 재사용할 수 있도록 policy와 evidence rule을 먼저 고정한다.
