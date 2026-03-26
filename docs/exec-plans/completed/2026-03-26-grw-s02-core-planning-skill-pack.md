# 2026-03-26-grw-s02-core-planning-skill-pack

- Issue ID: `GRW-S02`
- GitHub Issue: `#18`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s02-core-planning-skill-pack`
- Task Slug: `2026-03-26-grw-s02-core-planning-skill-pack`

## Problem

workflow 저장소에는 issue를 exec plan으로 고정하고, 병렬 agent ownership을 나누고, backend API 계약 변경을 client/workflow와 동기화하는 coordination skill이 아직 없다. 이 상태에서는 같은 종류의 작업을 시작할 때마다 입력, 산출물, 증거 규칙을 다시 설명해야 하고, 병렬 작업 충돌이나 계약 drift를 일관되게 막기 어렵다.

## Why Now

`GRB-01`, `GRW-03`, `GRW-04`, `GRC-01`까지 기준 문서와 계약 경로가 생겼다. 이제 `GRB-02`, `GRC-02`, `GRC-04`, `GRW-05` 이후 작업을 안정적으로 시작하려면 planning/coordination skill을 먼저 고정해야 한다.

## Scope

- `skills/issue-to-exec-plan/SKILL.md` 작성
- `skills/parallel-work-split/SKILL.md` 작성
- `skills/api-contract-sync/SKILL.md` 작성
- 각 skill에 입력/출력 예시와 병렬 수행 시 금지 사항 추가
- `skills/README.md`에 추천 사용 시점과 현재 skill registry 반영
- `GRW-S02` 실행 기록 남기기

## Non-scope

- ranking harness execution skill 작성
- batch triage skill 작성
- backend/frontend 코드 생성 자동화 추가
- workflow가 backend OpenAPI canonical source를 대체하도록 구조 변경

## Write Scope

- `skills/`
- `docs/exec-plans/`

## Outputs

- `skills/issue-to-exec-plan/SKILL.md`
- `skills/parallel-work-split/SKILL.md`
- `skills/api-contract-sync/SKILL.md`
- `skills/README.md`
- `GRW-S02` 실행/완료 기록

## Working Decisions

- backend OpenAPI canonical source는 계속 `git-ranker/docs/openapi/openapi.json`으로 둔다.
- `git-ranker-client`는 canonical spec의 consumer이며, generated type 또는 manual mirror만 관리한다.
- `git-ranker-workflow`는 canonical spec을 복제해 소유하지 않고, sync 절차, evidence, 필요 시 파생 generated artifact만 관리한다.
- `GRW-07` freshness check는 backend spec regeneration 책임과 workflow sync 책임을 분리하는 방향을 전제로 한다.

## Verification

- `find skills -maxdepth 2 -type f | sort`
  - 결과: `skills/api-contract-sync/SKILL.md`, `skills/issue-to-exec-plan/SKILL.md`, `skills/parallel-work-split/SKILL.md`가 registry 문서와 함께 기대 경로에 생성된 것을 확인했다.
- `cat skills/issue-to-exec-plan/SKILL.md`
  - 결과: exec plan 생성 절차, required evidence, 병렬 수행 금지 사항, `GRC-04` 기준 example input/output이 포함된 것을 확인했다.
- `cat skills/parallel-work-split/SKILL.md`
  - 결과: disjoint write set, cross-repo 분리, critical path 우선 규칙, ownership 표 예시가 포함된 것을 확인했다.
- `cat skills/api-contract-sync/SKILL.md`
  - 결과: canonical backend contract를 `git-ranker/docs/openapi/openapi.json`으로 고정하고, workflow는 sync 절차/evidence만 관리한다는 역할 분리가 명시된 것을 확인했다.
- `rg -n "Recommended Use|issue-to-exec-plan|parallel-work-split|api-contract-sync" skills/README.md skills/issue-to-exec-plan/SKILL.md skills/parallel-work-split/SKILL.md skills/api-contract-sync/SKILL.md`
  - 결과: skill index의 registry entry, 추천 사용 순서, 각 skill의 example/parallel 금지 사항 섹션이 모두 grep 결과에 포함되는 것을 확인했다.
- sample issue를 exec plan으로 바꾸는 시뮬레이션 검토
  - 결과: `issue-to-exec-plan`의 `GRC-04` 예시가 issue metadata, scope/non-scope, verification까지 포함한 exec plan skeleton으로 충분히 변환 가능한 것을 확인했다.
- contract-sync checklist가 backend canonical source 기준으로 동작하는지 문서 리뷰
  - 결과: `api-contract-sync` 예시가 backend canonical spec, client consumer, workflow review, no-op generated note까지 분리해 체크리스트를 만들 수 있음을 확인했다.
- `gh issue create --repo alexization/git-ranker-workflow ...`
  - 결과: `GRW-S02` GitHub issue `#18`을 생성했다.

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 skill 문서 내용, 검증 명령 결과, backend canonical contract에 대한 역할 분리 결정을 이 실행 문서에 남긴다.

- GitHub Issue: `#18`
- canonical backend contract: `git-ranker/docs/openapi/openapi.json`
- workflow role: canonical spec 소유가 아니라 sync 절차와 evidence 관리

## Risks or Blockers

- `api-contract-sync`는 현재 workflow 내부에 tracked generated mirror가 없는 상태를 다뤄야 한다. 따라서 “현재는 no-op인 workflow generated update”와 “실제 drift”를 혼동하지 않게 문구를 정교하게 써야 한다.
- `parallel-work-split`는 cross-repo worktree 규칙과 file ownership 규칙을 함께 다뤄야 하므로, 예시가 너무 추상적이면 재사용 가치가 떨어진다.
- `GRW-07`에서 freshness check를 구현할 때 backend spec freshness와 workflow sync freshness를 하나의 fail 조건으로 뭉개지 않도록 주의해야 한다.

## Next Preconditions

- `GRB-02`, `GRC-02`, `GRC-04`, `GRW-05` 시작 시 새 coordination skill이 실제 진입 절차로 재사용 가능해야 한다.
- `GRW-07`에서는 backend canonical spec freshness와 workflow sync freshness를 분리해 검사해야 한다.

## Docs Updated

- `skills/README.md`
- `skills/issue-to-exec-plan/SKILL.md`
- `skills/parallel-work-split/SKILL.md`
- `skills/api-contract-sync/SKILL.md`
- `docs/exec-plans/completed/2026-03-26-grw-s02-core-planning-skill-pack.md`

## Skill Consideration

이번 Issue 자체가 coordination skill pack을 추가하는 작업이다. 따라서 새 skill의 목적은 구현을 대신하는 것이 아니라, 반복되는 planning/splitting/sync 절차를 같은 입력/출력/증거 규칙으로 고정하는 데 있다. 특히 `api-contract-sync`는 canonical backend spec을 workflow로 복제해 소유하지 않는다는 현재 결정을 명시함으로써, 이후 `GRW-07`의 freshness guardrail 책임 경계를 분명하게 남긴다.
