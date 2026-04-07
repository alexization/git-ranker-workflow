# 2026-04-07-grw-16-dual-agent-review-policy

- Issue ID: `GRW-16`
- GitHub Issue: `#41`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-16-dual-agent-review-policy`
- Task Slug: `2026-04-07-grw-16-dual-agent-review-policy`

## Problem

`GRW-11`은 `Reviewing` 상태와 implementer/reviewer 분리 원칙을 정의했고, `GRW-15`는 reviewer handoff 전에 필요한 verification report minimum을 고정했다. 하지만 reviewer가 정확히 어떤 입력을 받아야 하는지, 어떤 기준으로 승인, 수정 요청, `Blocked`를 판단하는지, review 결과를 어디에 어떤 evidence 형태로 남겨야 하는지는 아직 source of truth로 잠겨 있지 않다.

이 공백이 남아 있으면 implementer와 reviewer가 같은 diff를 두고도 서로 다른 승인 기준을 쓰게 되고, PR template의 `Independent Review` 섹션과 이후 `GRW-S08` skill pack이 재사용할 canonical handoff 규칙도 흔들린다. 구현 Agent가 자기 결과를 승인하지 못하게 하려면 reviewer의 입력, 판단 기준, 수정 요청 루프를 먼저 고정해야 한다.

## Why Now

하네스의 `Implementing -> Verifying -> Reviewing -> Feedback` 흐름은 verification contract만으로 완성되지 않는다. verification이 통과한 뒤에도 reviewer가 무엇을 확인해야 하는지, 어떤 경우에 repair로 되돌리고 어떤 경우에 feedback close-out으로 넘기는지가 문서로 잠겨 있어야 실제로 dual-agent review가 운영된다.

또한 이미 PR template과 verification registry에는 reviewer input과 독립 review 섹션이 들어가 있다. `GRW-16`은 이 필드들이 참조할 canonical review policy를 제공해, 이후 `reviewer-handoff` skill과 pilot issue가 같은 handoff shape와 verdict semantics를 사용하게 만드는 선행 작업이다.

## Scope

- `docs/operations/`에 dual-agent review policy source of truth를 추가한다.
- implementer/reviewer 책임 분리, reviewer minimum input, review verdict 종류와 pass/fail semantics를 정의한다.
- 수정 요청 loop, self-approval 금지, review evidence 규칙과 draft checklist를 문서화한다.
- 관련 architecture/operations/product 문서가 새 review policy를 참조하도록 갱신한다.
- `GRW-16` close-out을 기록한다.

## Non-scope

- 자동 PR review bot 구현
- `GRW-S08` skill pack 작성
- backend/frontend 앱 코드 변경
- verification contract 자체 변경
- `.github/` template 구조 변경

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `docs/operations/`
  - `docs/architecture/`
  - `docs/product/` 필요 시
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/completed/2026-04-07-grw-16-dual-agent-review-policy.md`
  - `.artifacts/2026-04-07-grw-16-dual-agent-review-policy/` 필요 시
- Explicitly forbidden:
  - `.github/` template 구조 변경
  - sibling app repo code write
  - scope 밖 stable source of truth mass update
- Network / external systems:
  - GitHub Issue body render 확인
- Escalation triggers:
  - 없음. 문서 작업 범위에서 처리한다.

## Outputs

- `docs/operations/dual-agent-review-policy.md`
- reviewer handoff minimum, verdict semantics, review evidence rule, draft checklist
- architecture/operations/product hook 갱신
- `GRW-16` 실행 기록

## Working Decisions

- 이번 작업의 primary context pack은 `workflow-docs`다.
- dual-agent review의 canonical source는 `docs/operations/dual-agent-review-policy.md`에 두고, skill이나 template는 후속 `GRW-S08`에서 이 문서를 참조하는 thin layer로만 만든다.
- reviewer verdict vocabulary는 state machine과 직접 대응되도록 `approved`, `changes-requested`, `blocked` 세 가지로 고정한다.
- review-driven repair loop는 `GRW-15`의 latest verification report discipline과 retry/blocked semantics를 재사용한다.
- `.github/PULL_REQUEST_TEMPLATE.md`는 이미 필요한 필드를 갖추고 있으므로, 이번 이슈에서는 template 구조를 바꾸지 않는다.

## Verification

- `sed -n '1,320p' docs/operations/dual-agent-review-policy.md`
  - 결과: review invariants, 역할 분리, `Reviewer Minimum Context`, verdict semantics, review repair loop, evidence rule, draft checklist가 한 문서에 정리된 것을 확인했다.
- `rg -n "dual-agent|review verdict|review evidence|self-approval|Reviewer Minimum Context|repair loop|Independent Review" docs/operations/dual-agent-review-policy.md docs/architecture/harness-system-map.md docs/operations/workflow-governance.md docs/operations/verification-contract-registry.md docs/operations/README.md docs/product/harness-roadmap.md .github/PULL_REQUEST_TEMPLATE.md`
  - 결과: 새 review policy의 핵심 용어와 architecture/operations/product/template hook이 함께 grep되는 것을 확인했다.
- sample reviewer handoff와 verdict 흐름 수동 검토
  - 결과: reviewer가 exec plan, latest verification report, diff summary, remaining risks만으로 `approved`, `changes-requested`, `blocked` 분기 조건을 판별할 수 있음을 확인했다.
- `git diff --check`
  - 결과: whitespace 또는 patch formatting 오류가 없음을 확인했다.
- GitHub Issue `#41` body render 확인
  - 결과: issue 본문이 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.

## Evidence

문서 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 아래를 근거로 남긴다.

- dual-agent review policy 본문
- reviewer minimum context와 verdict rule
- review evidence 규칙과 draft checklist
- architecture/operations/product 연결 결과
- GitHub Issue `#41` body 검증 결과

## Risks or Blockers

- review verdict를 너무 세분화하면 PR template과 후속 skill의 재사용성이 떨어질 수 있으므로, 이번 작업은 상태 머신과 직접 연결되는 최소 vocabulary만 유지해야 한다.
- verification registry와 review policy가 서로 다른 retry semantics를 가지면 repair loop가 흔들릴 수 있으므로, review-driven repair는 `GRW-15`와 충돌 없이 연결되어야 한다.

## Next Preconditions

- `GRW-17`: failure-to-guardrail feedback loop 정의
- `GRW-18`: workflow repo pilot issue로 새 흐름 1회 검증
- `GRW-S08`: verification/review-loop skill pack

## Docs Updated

- `docs/operations/dual-agent-review-policy.md`
- `docs/operations/README.md`
- `docs/operations/workflow-governance.md`
- `docs/operations/verification-contract-registry.md`
- `docs/architecture/harness-system-map.md`
- `docs/product/harness-roadmap.md`
- `docs/exec-plans/completed/2026-04-07-grw-16-dual-agent-review-policy.md`

## Skill Consideration

이번 작업은 skill을 직접 작성하는 단계는 아니다. 대신 후속 `reviewer-handoff`, `repair-loop-triage`, `verification-contract-runner`가 그대로 재사용할 수 있도록 reviewer minimum context, verdict vocabulary, review evidence rule을 source of truth로 먼저 고정한다.
