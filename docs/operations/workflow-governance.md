# Workflow Governance

이 문서는 workflow 저장소를 기준으로 모든 Issue/PR 작업이 공유해야 하는 운영 규칙을 정의한다.

## 문서 링크 규칙

- 문서 내부 링크는 절대경로 대신 저장소 기준 상대경로를 사용한다.
- 다른 디렉터리 문서를 가리킬 때도 현재 문서 위치를 기준으로 상대경로를 적는다.
- 로컬 도구나 응답 메시지에서만 절대경로를 사용하고, 저장소 문서 본문에는 넣지 않는다.

## stable source of truth의 task ID 규칙

- `docs/product/`, `docs/exec-plans/`, GitHub Issue/PR 본문, baseline이나 historical snapshot처럼 tracking이 본질인 문서는 work item ID를 직접 써도 된다.
- `docs/architecture/`, `docs/operations/`, `docs/domain/`, `docs/reliability/`, `docs/security/`, `docs/quality-score/` 같은 stable source of truth 문서에는 future work나 follow-up 설명을 위해 직접적인 work item ID를 남기지 않는다.
- stable 문서에서 후속 확장을 가리킬 때는 task ID 대신 정책, registry, skill pack, guardrail 같은 자산 이름을 쓴다.
- task 완료 시 stable 문서에 임시로 넣었던 work item ID는 제거하거나 서술형 이름으로 치환한다.
- Issue ID 형식, 브랜치명 규칙처럼 식별자 형식 자체를 설명하는 문맥은 예외다.

## Issue/PR 단위 규칙

- 원칙적으로 `Issue 1개 = PR 1개`
- 하나의 PR은 하나의 목표만 해결한다
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다
- cross-repo 작업은 `workflow 문서 PR`과 `앱 코드 PR`로 나눈다

## 요청 intake 규칙

- 작업 시작 전 [request-routing-policy.md](request-routing-policy.md)로 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다.
- `즉시 실행 가능한 작업`만 GitHub issue와 exec plan을 만든다.
- `모호한 요청`은 source of truth로 줄일 수 있는 ambiguity를 먼저 제거하고, 남는 blocker만 interview 질문으로 다룬다.
- `대화` 또는 `Rejected` close-out인 요청은 파일 편집을 시작하지 않는다.

## Context Pack 규칙

- active exec plan이 생기면 구현 전 [../architecture/context-pack-registry.md](../architecture/context-pack-registry.md)에서 primary context pack 하나를 고른다.
- 모든 pack은 required docs만 먼저 읽고, optional docs는 issue, exec plan, hot file 탐색이 trigger를 줄 때만 연다.
- 서로 다른 pack의 required docs까지 동시에 필요해지면 ad-hoc으로 pack을 합치지 말고 issue 분해 또는 exec plan 갱신을 먼저 한다.
- `docs/references/`와 generated snapshot은 default context가 아니다. 현재 source of truth가 부족하거나 생성 계약을 확인할 때만 연다.
- target repo entry 문서나 worktree가 없으면 `Context Ready`를 선언하지 않고 `Blocked` 또는 준비 작업으로 되돌린다.

## Tool Boundary 규칙

- context pack을 고른 뒤 구현 전 [tool-boundary-matrix.md](tool-boundary-matrix.md)로 task type별 read boundary, write boundary, network, escalation class를 잠근다.
- verification 단계에 들어가기 전 [verification-contract-registry.md](verification-contract-registry.md)에서 primary contract profile을 고르고, conditional command나 repo-specific override는 exec plan에 적는다.
- exec plan에는 최소한 primary repo, allowed write paths, control-plane artifact, explicitly forbidden path, network 필요 여부, escalation trigger를 적는다.
- prompt나 follow-up 메모로 범위를 넓히지 않는다. issue와 exec plan에 없는 저장소 쓰기나 broad network access가 필요해지면 planning으로 되돌린다.
- cross-repo planning은 여러 저장소를 읽을 수 있어도 app repo code write는 열지 않는다. app 구현이 필요하면 저장소별 issue/PR로 분리한다.
- dangerous command와 broad escalation은 사용자 명시 요청 또는 좁게 복구 가능한 예외가 아니면 허용하지 않는다.

## 각 Issue에 반드시 들어가야 할 내용

- 문제 정의
- 왜 지금 필요한지
- 기대 결과 또는 완료 조건
- 범위와 비범위
- 대상 저장소와 write scope
- 참조할 source of truth 또는 context source
- verification contract 또는 검증 계획
- 남아 있는 open question 또는 blocker

## 각 PR에 반드시 들어가야 할 내용

- 연결된 Issue
- 문제 정의
- 왜 지금 필요한지
- 이번 PR의 범위와 비범위
- write scope
- 산출물
- 검증 명령, 최종 상태, 핵심 evidence
- 독립 review 결과
- feedback ledger entry 또는 `no new guardrail` 판단
- 남은 리스크
- 다음 Issue로 넘겨야 할 전제조건

## 증거 규칙

하네스 관련 PR에서는 가능하면 아래 증거를 남긴다.

- 명령 실행 결과 요약 또는 artifact 위치
- verification report 최소 필드: contract profile, command별 status, 핵심 evidence, failure summary, next action
- review evidence 최소 필드: implementer, reviewer, reviewer input, verdict, blocking finding 또는 no-blocking note
- feedback evidence 최소 필드: stage, failure class, promotion decision, follow-up asset 또는 `no new guardrail` 이유, 핵심 evidence
- 브라우저 증거: screenshot, trace, video
- 로그 증거: LogQL 결과 또는 로그 요약
- 메트릭 증거: PromQL 결과 또는 지표 캡처
- 문서 업데이트: source of truth 반영 여부

문서 전용 Issue에서는 브라우저, 로그, 메트릭 증거가 필수는 아니다. 대신 어떤 문서를 바꿨고 무엇으로 검증했는지를 남긴다.

## 브랜치와 슬러그 규칙

- Issue ID 형식: `GRW-01`, `GRB-01`, `GRC-01`
- 권장 브랜치명: `feat/grw-01-workflow-skeleton`
- 작업 슬러그: `2026-03-24-grw-01-workflow-skeleton`

약어:

- `GRW`: `git-ranker-workflow`
- `GRB`: `git-ranker`
- `GRC`: `git-ranker-client`

## GitHub Issue/PR 운영 규칙

- `즉시 실행 가능한 작업`으로 판정된 뒤 대상 저장소에 `gh issue create`로 이슈를 만든다.
- 이슈와 PR 본문은 대상 저장소의 Issue/PR template 형식을 따른다.
- GitHub 본문은 먼저 파일로 작성한 뒤 `gh issue create --body-file <path>` 또는 `gh pr create --body-file <path>`로 보낸다.
- workflow 저장소 Issue 본문은 `.codex/skills/issue-to-exec-plan/templates/github-issue-body.md`를 복사해 채운다.
- workflow 저장소 PR 본문은 `.github/PULL_REQUEST_TEMPLATE.md`를 복사한 임시 파일을 기준으로 채운다.
- PR은 기본적으로 open으로 생성한다. draft PR은 사용자가 명시적으로 요청했거나, scope-complete 전 공유가 필요한 blocker를 body와 exec plan에 적을 때만 예외적으로 사용한다.
- PR의 `6) Verification Contract`는 카테고리별 section 아래에 check별 block 형식으로 작성한다.
- 성공한 검증은 최종 상태와 핵심 evidence만 짧게 적고, 실패, 재시도, 예외만 상세히 남긴다.
- PR의 `7) Independent Review`는 [dual-agent-review-policy.md](dual-agent-review-policy.md)의 reviewer minimum context와 verdict vocabulary를 따른다.
- PR의 `9) Feedback / Guardrail Follow-up`는 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)와 [guardrail-ledger-template.md](guardrail-ledger-template.md)의 vocabulary와 최소 필드를 따른다.
- 생성 직후에는 `gh issue view --json body` 또는 `gh pr view --json body`로 본문이 예상한 줄바꿈과 섹션을 유지하는지 확인한다.
- Issue template은 최소한 `문제`, `왜 지금`, `범위/비범위`, `write scope`, `context source`, `verification plan`, `open questions`를 포함해야 한다.
- PR template은 최소한 `연결된 issue`, `범위/비범위`, `write scope`, `verification 결과`, `독립 review 결과`, `feedback follow-up`, `문서 반영`, `리스크`를 포함해야 한다.
- 커밋 메시지는 항상 루트의 `.gitmessage.ko.txt` 형식을 따른다.
- 저장소별 작업은 각 저장소마다 별도 branch 또는 worktree에서 수행한다.
- 모든 기능 브랜치는 대상 저장소의 `develop` 브랜치를 기준으로 분기한다.
- cross-repo 작업은 저장소별로 이슈와 PR을 분리한다.
- `git-ranker-workflow`, `git-ranker`, `git-ranker-client`는 서로 다른 작업 트리를 써서 변경 범위를 섞지 않는다.

현재 기준 실행 순서:

1. [request-routing-policy.md](request-routing-policy.md)로 요청을 분류하고, `즉시 실행 가능한 작업`만 다음 단계로 보낸다.
2. 대상 저장소의 `develop` 최신 상태를 기준으로 worktree 또는 branch를 만든다.
3. body file을 준비한 뒤 `gh issue create --body-file ...`로 대상 저장소 이슈를 만든다.
4. 이슈 번호를 브랜치명과 exec plan에 연결한다.
5. 작업 후 latest verification report를 만들고, reviewer minimum context를 준비한 뒤 independent review를 먼저 수행한다.
6. PR body file에 검증 결과, independent review 결과, 문서 반영 여부, 남은 리스크를 먼저 채운다.
7. 사용자가 draft를 명시적으로 요청했거나, scope-complete 전 blocker 공유가 필요하면 draft PR을 연다. 그렇지 않다면 `gh pr create --base develop --body-file ...`로 open PR을 연다.
8. 생성 직후 `gh issue view --json body` 또는 `gh pr view --json body`로 본문 렌더링을 확인한다.

## 문서, SKILL, exec plan의 역할

- 문서: source of truth다. 도메인, 계약, 운영 규칙, 수용 기준을 설명한다.
- SKILL: 반복 작업을 Agent가 재사용 가능한 절차로 수행하게 만드는 실행 레시피다.
- exec plan: 현재 한 작업의 목표, 범위, 검증, 증거를 적는 실행 문서다.

아래 조건 중 하나라도 만족하면 SKILL 후보로 검토한다.

- 같은 작업 흐름이 3번 이상 반복될 가능성이 높다
- 병렬 에이전트에게 같은 입력, 출력, 증거 규칙을 강제해야 한다
- 도메인 문서만 읽어서는 실행 절차가 흔들릴 가능성이 높다
- 로그, 메트릭, 브라우저 검증처럼 순서가 중요한 루프가 있다

## 공통 실행 지시

- 이 Issue의 목표만 수행한다. 범위를 넓히지 않는다.
- 선행조건이 충족되지 않았으면 임의로 우회 구현하지 말고 blocker를 먼저 정리한다.
- 허용된 write scope 밖의 파일은 수정하지 않는다.
- network나 escalation이 필요하면 목적과 범위를 exec plan 또는 최종 close-out에 남긴다.
- verification failure가 나면 registry의 retry budget 안에서만 repair loop를 돌리고, budget 초과나 missing canonical source는 `Blocked` 또는 후속 planning으로 넘긴다.
- review 단계에 들어가기 전 latest verification report와 reviewer minimum context를 준비한다.
- 사용자가 다르게 요청하지 않았다면 independent review를 끝낸 뒤 PR을 publish한다.
- source of truth 문서를 함께 업데이트하거나, 업데이트가 불필요한 이유를 남긴다.
- 검증 명령과 최종 상태를 반드시 남기고, 실패나 예외가 있었다면 요약을 남긴다.
- 새로 생긴 반복 절차가 있다면 skill 후보로 제안하되, 이번 Issue 범위를 넘는 구현은 하지 않는다.
- 모호한 선택지가 여러 개면 [docs/product/work-item-catalog.md](../product/work-item-catalog.md)의 기본 결정을 따른다.
- 실행 중 예상치 못한 dirty change가 있으면 되돌리지 말고 영향 여부만 확인한다.

## `.artifacts/` 보관 규칙

작업 증거는 기본적으로 `.artifacts/<task-slug>/` 아래에 남긴다.

권장 구조:

- `.artifacts/<task-slug>/browser/`
- `.artifacts/<task-slug>/logs/`
- `.artifacts/<task-slug>/metrics/`
- `.artifacts/<task-slug>/summary.md`

보관 원칙:

- 산출물은 로컬 증거로 취급하고 git에는 커밋하지 않는다
- exec plan 또는 PR에는 산출 위치와 핵심 요약만 남긴다
- 문서 전용 작업은 `.artifacts/` 없이 명령 결과 요약만 남겨도 된다

## 공통 Definition of Done

각 작업은 아래 항목을 최대한 충족해야 한다.

- 왜 이 작업이 필요한지 문서나 PR 본문에 남아 있다
- 변경 범위가 한 가지 목표에 집중되어 있다
- 검증 명령이 PR이나 exec plan에 남아 있다
- 후속 작업의 전제조건이 명확하다
- source of truth 문서가 함께 업데이트되었거나, 업데이트 불필요 사유가 명시되어 있다
- stable source of truth 문서에 남긴 임시 work item ID가 있다면 close-out 전에 제거되었거나 planning/history 문서로 이동했다
- 동일 작업이 반복될 가능성이 높다면 skill화 여부가 검토되었거나, 아직 만들지 않는 이유가 남아 있다

하네스 관련 작업은 아래 항목도 추가로 본다.

- 브라우저, 로그, 메트릭 중 이번 PR에서 다룬 신호가 무엇인지 명확하다
- 증거 산출 위치가 정해져 있다
- 실패 시 어떤 루프로 다시 수정할지 문서화되어 있다
