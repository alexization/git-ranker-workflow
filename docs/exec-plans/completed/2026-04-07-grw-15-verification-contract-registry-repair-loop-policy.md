# 2026-04-07-grw-15-verification-contract-registry-repair-loop-policy

- Issue ID: `GRW-15`
- GitHub Issue: `#39`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-15-verification-contract-registry-repair-loop-policy`
- Task Slug: `2026-04-07-grw-15-verification-contract-registry-repair-loop-policy`

## Problem

`GRW-11`은 `Verifying`, `Repairing`, `Blocked` 상태의 상위 의미와 retry budget 필요성을 정의했고, `GRW-14`는 task type별 도구 경계와 escalation 규칙을 고정했다. 하지만 실제 작업에서 어떤 명령이 완료 판정을 내리는지, 실패 시 implementer가 reviewer에게 넘길 수 있는 repair loop 입력 형식이 무엇인지, 언제 `Blocked`로 멈춰야 하는지에 대한 registry는 아직 없다.

이 공백이 남아 있으면 workflow 문서 작업과 backend/frontend 앱 작업이 서로 다른 검증 명령과 실패 해석을 사용하게 되고, review 이전에 필요한 verification report shape도 task마다 흔들린다. 후속 `GRW-16`, `GRW-17`, `GRW-S08`, `GRB-04`, `GRC-05`가 공유할 결정론적 완료 기준을 먼저 잠가야 한다.

## Why Now

하네스의 통제력은 "무엇을 읽는가"와 "무엇을 수정하는가"만으로는 완성되지 않는다. `Implementing -> Verifying -> Reviewing` 전이에서 어떤 명령을 통과해야 다음 상태로 넘어가는지, 실패하면 어떤 정보로 재작업을 지시할지를 먼저 고정해야 implementer와 reviewer의 역할 분리가 실제로 작동한다.

또한 현재 workflow 저장소에는 cross-repo runtime 검증 기준이 일부 있고, backend/frontend 저장소에는 각자 build/test entrypoint가 존재할 수 있다. 이를 registry 형태로 먼저 정리해야 이후 repo-specific verification contract 정규화가 동일한 상위 규약을 재사용할 수 있다.

## Scope

- `docs/operations/`에 verification contract registry source of truth를 추가한다.
- `workflow`, `backend`, `frontend` 기본 verification entrypoint, pass/fail semantics, evidence 필드를 정의한다.
- repair loop 입력 형식, retry budget, `Blocked` 전환 기준, stop condition을 문서화한다.
- 관련 architecture/operations/product 문서가 새 verification policy를 참조하도록 갱신한다.
- `GRW-15` close-out을 기록한다.

## Non-scope

- backend/frontend 앱 코드 변경
- 테스트 프레임워크 추가
- dual-agent review policy 상세 설계
- verification/review-loop skill pack 작성

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/` 필요 시
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-07-grw-15-verification-contract-registry-repair-loop-policy.md`
  - `.artifacts/2026-04-07-grw-15-verification-contract-registry-repair-loop-policy/` 필요 시
- Explicitly forbidden:
  - sibling app repo code write
  - declared scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue body render 확인
  - sibling repo remote source inspection 필요 시
- Escalation triggers:
  - 없음. 문서 작업과 read-only inspection 범위에서 처리한다.

## Outputs

- `docs/operations/verification-contract-registry.md`
- verification report minimum shape와 repair loop policy
- architecture/governance/product hook 갱신
- `GRW-15` 실행 기록

## Working Decisions

- 이번 작업의 primary write repo는 `git-ranker-workflow`지만, read boundary는 `cross-repo planning`처럼 다뤄 backend/frontend의 current verification entrypoint를 확인한다.
- sibling 저장소는 entry 문서, build/test script, verification 관련 공식 문서나 remote source까지만 읽고 구현 코드 수정으로는 확장하지 않는다.
- registry는 repo-specific contract를 대체하지 않고, 각 저장소가 따라야 할 상위 completion semantics와 기본 entrypoint만 정의한다.
- repair loop는 무한 재시도를 허용하지 않으며, retry budget 초과, canonical source 부재, 환경 선행조건 부재는 `Blocked`로 전환한다.
- verification 결과는 reviewer가 diff와 함께 읽을 수 있도록 `command`, `final status`, `evidence`, `failure summary`, `next action`을 최소 필드로 가진다.

## Verification

- `sed -n '1,360p' docs/operations/verification-contract-registry.md`
  - 결과: registry invariants, status vocabulary, contract selection rule, `workflow-docs`/`cross-repo-planning`/`workflow-runtime`/`backend-change`/`frontend-change` profile, verification report shape, repair loop policy가 한 문서에 정리된 것을 확인했다.
- `rg -n "workflow-docs|backend-change|frontend-change|verification report|repair loop|retry budget|stop condition|Blocked" docs/operations/verification-contract-registry.md docs/architecture/harness-system-map.md docs/operations/workflow-governance.md docs/operations/tool-boundary-matrix.md docs/operations/README.md docs/product/work-item-catalog.md`
  - 결과: verification contract registry의 핵심 용어와 architecture/governance/product hook이 함께 grep되는 것을 확인했다.
- backend/frontend/workflow representative contract 수동 검토
  - 결과: backend는 `../git-ranker/build.gradle`, `../git-ranker/docs/openapi/README.md`, 완료된 `GRB-02` exec plan을 기준으로 baseline/conditional command를 설명할 수 있었다.
  - 결과: frontend는 `git-ranker-client` 원격 `README.md`, `package.json`, `.env.example`, 완료된 `GRC-03` exec plan과 `docs/operations/frontend-runtime-reference.md`를 기준으로 `lint`, `typecheck`, env 포함 `build` contract를 설명할 수 있었다.
  - 결과: workflow는 `docs/operations/workflow-verification-runtime.md`와 완료된 `GRW-05` exec plan을 기준으로 runtime contract를 설명할 수 있었다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- GitHub Issue `#39` body render 확인
  - 결과: issue 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- verification contract registry 본문
- repo/task type별 기본 검증 명령과 evidence 필드
- repair loop 입력 형식과 retry budget 기준
- 관련 architecture/governance/product 연결 결과
- backend local source: `../git-ranker/README.md`, `../git-ranker/build.gradle`, `../git-ranker/docs/openapi/README.md`
- frontend remote source: `alexization/git-ranker-client`의 `develop` branch `README.md`, `package.json`, `.env.example`
- GitHub Issue `#39` body 검증 결과

## Risks or Blockers

- 로컬에 `git-ranker-client` worktree가 없을 수 있으므로, frontend verification entrypoint는 remote source inspection과 existing workflow docs를 함께 대조해야 할 수 있다.
- backend/frontend의 현재 명령이 repo 내부에서 일관되지 않다면, 이번 작업은 상위 registry를 먼저 고정하고 세부 정규화는 `GRB-04`, `GRC-05`로 넘겨야 한다.

## Next Preconditions

- `GRW-16`: dual-agent review policy 정의
- `GRW-17`: failure-to-guardrail feedback loop 정의
- `GRW-S08`: verification/review-loop skill pack
- `GRB-04`: backend verification contract 정규화
- `GRC-05`: frontend verification contract 정규화

## Docs Updated

- `docs/operations/verification-contract-registry.md`
- `docs/operations/README.md`
- `docs/operations/workflow-governance.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/2026-04-07-grw-15-verification-contract-registry-repair-loop-policy.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 대신 후속 `verification-contract-runner`, `repair-loop-triage`, `reviewer-handoff` skill이 재사용할 수 있도록 verification report shape와 retry/blocked semantics를 source of truth로 먼저 고정한다.
