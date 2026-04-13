# Skills

이 디렉터리는 `git-ranker-workflow`에서만 쓰는 project-local skill을 관리한다.

## 목적

- 병렬 에이전트가 같은 품질 기준으로 작업하게 한다.
- 반복 작업을 매번 자연어로 다시 설명하지 않게 한다.
- 문서, spec, evidence 규칙을 실행 절차와 연결한다.

## Canonical Ownership

- 정책, vocabulary, 상태 전이, 종료 조건, evidence minimum은 `docs/operations/`, `docs/architecture/`, `docs/specs/`가 관리한다.
- skill은 그 정책을 대체하지 않고, 한 단계의 반복 실행 절차와 handoff만 다룬다.
- policy와 skill이 충돌하면 skill에 새 규칙을 더하지 말고 canonical policy를 먼저 수정한 뒤 skill을 맞춘다.

## Registry Status

- `skill-creator`: 새 skill 생성, 기존 skill 리팩터링
- `request-intake`: 새 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류
- `ambiguity-interview`: `모호한 요청`을 single spec 후보, `Blocked`, `Rejected`로 수렴
- `socratic-spec-authoring`: 소크라테스 질문으로 spec을 작성하고 승인 상태까지 고정
- `context-pack-selection`: approved spec 뒤에 primary context pack과 required docs를 고정
- `boundary-check`: 구현 전에 read/write/network/escalation 경계를 다시 확인
- `parallel-work-split`: 여러 agent를 투입하기 전에 ownership과 disjoint write set을 고정
- `api-contract-sync`: backend API 계약 변화가 client consumer와 workflow evidence에 미치는 영향을 맞춤
- `verification-contract-runner`: selected verification contract profile을 실행하고 latest verification evidence를 남김
- `repair-loop-triage`: verification 실패나 review 수리 요청 뒤 rerun, `Blocked`, split 중 하나를 정함
- `reviewer-handoff`: review가 실제로 필요할 때 reviewer minimum context를 넘김
- `publish-after-review`: legacy 이름이지만 current policy에서는 latest verification 뒤 open PR을 publish
- `guardrail-ledger-update`: feedback close-out에서 guardrail ledger entry 작성
- `failure-to-policy`: normalized failure를 가장 작은 guardrail asset으로 연결
- `quality-sweep-triage`: quality sweep signal을 cleanup candidate, guardrail follow-up, repair-now, no-action으로 분류
- `red`
- `green`
- `refactor`

## Recommended Use

새 요청을 처음 받을 때의 기본 순서는 아래와 같다.

1. `request-intake`
2. `ambiguity-interview` if route is `모호한 요청`
3. `socratic-spec-authoring`
4. `context-pack-selection`
5. `boundary-check`
6. `parallel-work-split` if more than one agent will work on the same spec

구현 뒤 close-out 순서는 아래 hook을 따른다.

1. `verification-contract-runner`
2. `publish-after-review` once latest verification evidence is `passed`
3. `reviewer-handoff` if independent review is required after publish
4. `repair-loop-triage` if verification failed or review requested changes
5. `guardrail-ledger-update` once feedback close-out is triggered
6. `failure-to-policy` when feedback close-out must choose a guardrail promotion target
7. `quality-sweep-triage` when periodic or targeted quality scan is in scope

구현 skill은 그 다음 slice에 맞춰 쓴다.

1. `red`
2. `green`
3. `refactor`

`api-contract-sync`의 canonical backend contract는 `git-ranker/docs/openapi/openapi.json`이다. workflow는 canonical spec을 복제해 소유하지 않고, sync 절차와 evidence를 관리한다.
