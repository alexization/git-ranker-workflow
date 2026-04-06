# 2026-04-06-grw-19-harness-issue-pr-template-alignment

- Issue ID: `GRW-19`
- GitHub Issue: `#29`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-19-harness-issue-pr-template-alignment`
- Task Slug: `2026-04-06-grw-19-harness-issue-pr-template-alignment`

## Problem

바로 다음 단계부터 Harness workflow를 issue/PR 단위로 적용하려면, GitHub Issue와 PR이 같은 입력 필드와 완료 기준을 강제해야 한다. 현재 template는 작업 목적과 검증을 받기에는 충분하지만, `request intake`, `write scope`, `verification contract`, `독립 review`, `feedback/guardrail follow-up`을 하네스 기준으로 강제하지 못한다.

이 상태로 후속 작업을 시작하면 source of truth는 새 하네스 흐름을 가리키는데, 실제 GitHub entrypoint는 이전보다 느슨한 양식을 계속 쓰게 된다.

## Why Now

Issue template과 PR template은 이후 모든 작업의 intake와 close-out 형식을 결정한다. 따라서 `GRW-10`, `GRW-11`, `GRW-12`, `GRW-15`, `GRW-16`에 들어가기 전에 먼저 정렬해야 한다.

## Scope

- `GRW-19`를 선행 작업으로 roadmap와 catalog에 반영한다.
- workflow governance에 issue/pr template 필수 항목을 현재 하네스 기준으로 반영한다.
- `.github/ISSUE_TEMPLATE/engineering_task.yml`을 새 intake 기준으로 갱신한다.
- `.github/PULL_REQUEST_TEMPLATE.md`를 verification/review/feedback 기준으로 갱신한다.

## Non-scope

- backend/frontend 앱 코드 변경
- GitHub Actions 구현
- 자동 PR 리뷰 봇 구현
- 신규 skill 작성

## Write Scope

- `.github/`
- `docs/operations/`
- `docs/product/`
- `docs/exec-plans/`

## Outputs

- 갱신된 workflow issue template
- 갱신된 PR template
- governance와 roadmap/catalog의 선행 순서 반영
- `GRW-19` 실행 기록

## Working Decisions

- Issue template은 `문제`, `왜 지금`, `기대 결과`, `범위/비범위`, `write scope`, `context/source of truth`, `verification contract`, `open questions`를 받아야 한다.
- PR template은 `연결된 issue`, `범위/비범위`, `write scope`, `verification 결과`, `독립 review 결과`, `feedback/guardrail follow-up`, `문서 반영`, `리스크`를 받아야 한다.
- 구현 Agent와 review Agent는 동일할 수 없다는 점을 template에 드러낸다.

## Verification

- `sed -n '1,220p' .github/ISSUE_TEMPLATE/engineering_task.yml`
  - 결과: `request_type`, `target_repo`, `problem`, `why_now`, `expected_outcome`, `in_scope`, `out_of_scope`, `write_scope`, `context_sources`, `verification_plan`, `review_expectation`, `open_questions` 필드가 들어간 것을 확인했다.
- `sed -n '1,260p' .github/PULL_REQUEST_TEMPLATE.md`
  - 결과: `Harness Contract`, `Verification Contract`, `Independent Review`, `Feedback / Guardrail Follow-up` 섹션이 들어간 것을 확인했다.
- `rg -n "verification contract|write scope|review Agent|feedback|follow-up|open questions" .github docs/product docs/operations`
  - 결과: `.github` template, `docs/product/*`, `docs/operations/workflow-governance.md`, `GRW-19` exec plan에서 새 하네스 템플릿 핵심 필드가 함께 grep되는 것을 확인했다.

## Evidence

문서/템플릿 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- Issue template의 새 필드 구조
- PR template의 verification/review/feedback 구조
- roadmap/catalog에서 `GRW-19`가 선행 작업으로 반영된 위치

## Risks or Blockers

- `workflow-governance.md`가 아직 이전 evidence 문구를 일부 포함하고 있어, template 개편 후에도 후속 이슈에서 더 세밀한 정렬이 필요할 수 있다.
- 템플릿을 너무 자세하게 만들면 실제 issue 작성 비용이 커질 수 있으므로, 필수 필드는 남기되 중복 필드는 줄여야 한다.

## Next Preconditions

- `GRW-10`: 하네스 기준 정렬
- `GRW-15`: verification contract registry 정의
- `GRW-16`: dual-agent review policy 정의

## Docs Updated

- `.github/ISSUE_TEMPLATE/engineering_task.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/operations/workflow-governance.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/2026-04-06-grw-19-harness-issue-pr-template-alignment.md`

## Skill Consideration

이번 작업은 새 skill 작성 범위는 아니다. 다만 이후 `GRW-S06`과 `GRW-S08`은 이 template가 강제하는 intake/review 필드를 그대로 재사용해야 한다.
