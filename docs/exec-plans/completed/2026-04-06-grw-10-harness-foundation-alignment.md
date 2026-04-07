# 2026-04-06-grw-10-harness-foundation-alignment

- Issue ID: `GRW-10`
- GitHub Issue: `#30`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-10-harness-foundation-alignment`
- Task Slug: `2026-04-06-grw-10-harness-foundation-alignment`

## Problem

현재 workflow source of truth는 앞으로 적용할 하네스 시스템의 canonical flow, 역할 분리, 완료 판정을 한 문장으로 묶어 보여주지 못하고 있다. 바로 다음 턴부터 issue/PR 단위 작업을 시작할 계획이라면, 모든 후속 작업이 같은 기준을 읽을 수 있도록 foundation 문서를 먼저 정렬해야 한다.

이번 기준에서 하네스의 핵심은 `라우팅`, `컨텍스트 제한`, `도구 경계`, `결정론적 검증`, `구현/리뷰 Agent 분리`, `실패의 가드레일화`다. 따라서 첫 작업은 이 여섯 축을 current source of truth에 명시하는 것이다.

## Why Now

사용자가 바로 다음 턴부터 issue/PR 단위로 새 Harness workflow를 적용할 계획이다. 따라서 시작점인 `roadmap`, `catalog`, `governance`, `index`가 먼저 현재 기준으로 정렬되어 있어야 이후 exec plan과 PR 운영 규칙이 흔들리지 않는다.

이 작업은 실제 구현 작업에 들어가기 전, 앞으로의 공식 계획과 운영 용어를 잠그는 foundation 단계다.

## Scope

- roadmap, catalog, index, 운영 문서를 현재 하네스 기준으로 정렬한다.
- canonical flow와 역할 분리 기준을 source of truth에 반영한다.
- 구현 Agent와 review Agent를 분리하는 정책을 후속 Issue가 바로 이어받을 수 있도록 기준점을 만든다.
- 새 하네스 기준의 후속 Issue 순서를 고정한다.
- 현재 Harness 범위에 포함하지 않는 디렉터리와 문서를 source of truth에서 제거한다.

## Non-scope

- backend/frontend 앱 코드 변경
- CI 파이프라인 구현
- skill 본문 신규 작성

## Write Scope

- `AGENTS.md`
- `.gitignore`
- `.artifacts/`
- `docs/README.md`
- `docs/product/`
- `docs/architecture/`
- `docs/domain/`
- `docs/generated/`
- `docs/operations/`
- `docs/quality-score/`
- `docs/references/`
- `docs/reliability/`
- `docs/security/`
- `.codex/skills/`
- `docs/exec-plans/`
- `runtime/`

## Outputs

- 새 하네스 기준으로 갱신된 roadmap와 work item catalog
- 관련 index/governance 문서의 방향성 정렬
- 후속 Issue 진입 기준
- 현재 Harness 범위 밖의 디렉터리와 문서 제거

## Working Decisions

- 현재 control plane source of truth는 `docs/architecture/`, `docs/operations/`, `docs/product/`, `docs/exec-plans/`, 루트 인덱스로 한정한다.
- 앱 동작 설명은 workflow 복제 문서 대신 각 앱 저장소 엔트리 문서와 코드/테스트를 직접 읽는다.
- 완료된 exec plan은 historical evidence로 유지한다.
- 이후 하네스의 canonical flow는 `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback`이다.
- 완료 판정은 `결정론적 검증 통과`와 `별도 review Agent 승인`을 함께 요구한다.

## Verification

- `cat docs/product/harness-roadmap.md`
  - 결과: `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback` 흐름, current source of truth 범위, repo-specific contract 순서가 현재 계획과 맞게 정리된 것을 확인했다.
- `cat docs/product/work-item-catalog.md`
  - 결과: `GRW-10`, `GRW-13`, `GRW-15`, `GRW-17`, `GRW-18`의 범위와 write scope가 현재 control plane 축소 방향과 맞게 정리된 것을 확인했다.
- `rg -n "Router|Interview|Context Pack|Implementer|Verification|Reviewer|Feedback|control plane source of truth|앱 동작의 canonical source" AGENTS.md docs/README.md docs/architecture docs/operations docs/product .codex/skills`
  - 결과: canonical flow, control plane source of truth, app repo canonical source 원칙이 인덱스와 정책 문서 전반에 반영된 것을 확인했다.
- `find docs -maxdepth 2 -type d | sort`
  - 결과: `docs/architecture`, `docs/operations`, `docs/product`, `docs/exec-plans`만 현재 workflow 문서 트리로 남아 있는 것을 확인했다.
- 상대 링크 검토
  - 결과: `AGENTS.md`, `docs/README.md`, `docs/architecture/*.md`, `docs/operations/*.md`, `docs/product/*.md`, active exec plan의 상대 링크가 모두 유효한 것을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.

## Verification Report

- Contract profile: `workflow-docs`
- Overall status: `passed`
- Preconditions:
  - docs-only cleanup
  - app runtime/build checks not required for this issue
- Command: `rg -n "Router|Interview|Context Pack|Implementer|Verification|Reviewer|Feedback|control plane source of truth|앱 동작의 canonical source" AGENTS.md docs/README.md docs/architecture docs/operations docs/product .codex/skills`
  - Status: `passed`
  - Evidence: canonical flow, control-plane source of truth, app repo canonical source 원칙이 surviving docs 전반에 남아 있다.
- Command: `find docs -maxdepth 2 -type d | sort`
  - Status: `passed`
  - Evidence: `docs/architecture`, `docs/operations`, `docs/product`, `docs/exec-plans`만 현재 workflow 문서 트리로 남아 있다.
- Command: relative link check on `AGENTS.md`, `docs/README.md`, `docs/architecture/*.md`, `docs/operations/*.md`, `docs/product/*.md`, active exec plan surfaces
  - Status: `passed`
  - Evidence: surviving live docs에서 broken relative link가 없었다.
- Command: `git diff --check`
  - Status: `passed`
  - Evidence: whitespace 또는 patch formatting 오류가 없었다.
- Failure summary: 없음
- Next action: reviewer handoff

## Evidence

문서 정렬 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- 새 canonical flow가 어디에 적혔는지
- 구현 Agent와 review Agent 분리 기준이 어디에 적혔는지
- 바로 다음 Issue가 무엇인지
- retired 문서군과 실제로 남은 문서 트리 비교 결과

## Risks or Blockers

- `workflow-governance.md`와 `control-plane-map.md`는 후속 Issue에서 더 정밀한 용어 정리가 필요할 수 있다.
- 구현/리뷰 Agent 분리를 문서에 적는 것과 실제 작업 절차에 녹이는 것은 다르므로, `GRW-16`에서 운영 규칙까지 닫아야 한다.

## Next Preconditions

- `GRW-11`: 하네스 시스템 맵과 상태 머신 정의
- `GRW-12`: 요청 라우팅과 ambiguity interview 정책 정의
- `GRW-15`: verification contract registry 정의
- `GRW-16`: dual-agent review policy 정의

## Docs Updated

- `AGENTS.md`
- `.gitignore`
- `docs/README.md`
- `docs/architecture/`
- `docs/operations/`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/api-contract-sync/SKILL.md`
- `docs/exec-plans/completed/2026-04-06-grw-10-harness-foundation-alignment.md`

## Current Outcome

- 현재 workflow source of truth를 `docs/architecture/`, `docs/operations/`, `docs/product/`, `docs/exec-plans/`, 루트 인덱스로 축소했다.
- `docs/domain`, `docs/generated`, `docs/quality-score`, `docs/references`, `docs/reliability`, `docs/security`, `runtime`, `.artifacts`와 현재 Harness 범위 밖의 app/runtime 세부 문서를 제거했다.
- 앱 동작과 계약은 workflow 복제 문서 대신 각 앱 저장소의 엔트리 문서와 코드/테스트를 canonical source로 읽도록 정책을 정렬했다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `Nash (reviewer-pool-coordinator)`
- Additional Reviewers:
  - `scope-and-governance`: `Archimedes`
  - `verification-and-regression`: `Ramanujan`
  - `security-and-reliability`: `Gibbs`
- Reviewer Roles / Prompt Focus: `scope-and-governance`, `verification-and-regression`, `security-and-reliability`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/completed/2026-04-06-grw-10-harness-foundation-alignment.md`
  - Latest verification report: `passed`
  - Diff summary: control-plane docs를 `docs/architecture`, `docs/operations`, `docs/product`, `docs/exec-plans`와 루트 인덱스로 축소하고, 현재 Harness 범위 밖의 문서/디렉터리를 제거했다.
  - Source-of-truth update: `AGENTS.md`, `docs/README.md`, `docs/architecture/*`, `docs/operations/*`, `docs/product/*`, `.codex/skills/*`, `docs/exec-plans/*`
  - Remaining risks / skipped checks: 문서형 cleanup이므로 app runtime/build 계열 검사는 생략했다.
- Review Verdict: `approved`
- Findings / Change Requests:
  - `no blocking findings`
- Evidence:
  - `scope-and-governance`, `verification-and-regression`, `security-and-reliability` reviewer가 모두 `approved`를 반환했다.
  - coordinator `Nash`가 aggregation 규칙에 따라 overall verdict를 `approved`로 잠갔다.
  - write scope를 삭제 대상까지 확장한 뒤 surviving live docs의 broken link가 없음을 다시 확인했다.
  - retained control-plane docs만으로 backend/frontend/cross-repo planning guidance가 계속 설명 가능하다는 reviewer 합의가 있었다.

## Feedback / Guardrail Follow-up

- Latest verification status: `passed`
- Latest review verdict: `approved`
- Promotion decision: `no-new-guardrail`
- Decision rationale: 이번 정리는 기존 routing, boundary, verification, review 규칙 안에서 닫혔고, 같은 종류의 반복 실패를 새 guardrail로 승격해야 할 신호는 관측되지 않았다.
- Follow-up asset or issue: `없음`

## Skill Consideration

이번 작업은 새 skill을 만드는 단계가 아니다. 다만 이후 `GRW-S08`에는 verification 이후 review handoff와 repair loop를 함께 다루는 skill이 포함되어야 한다.
