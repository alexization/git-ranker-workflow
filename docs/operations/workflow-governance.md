# Workflow Governance

이 문서는 workflow 저장소를 기준으로 모든 Issue/PR 작업이 공유해야 하는 운영 규칙을 정의한다.

## Reader-First Body 규칙

- Issue와 PR 본문은 사람이 빠르게 맥락과 판단 포인트를 이해하기 위한 reader-first 문서로 쓴다.
- 본문에는 문제, 배경, 접근, 영향, 검토 포인트, 남은 리스크처럼 사람이 바로 판단할 정보를 우선 적는다.
- 아래 정보는 본문 필수 항목으로 강제하지 않는다.
  - branch 이름, exec plan 파일명, 전체 파일 목록, 업데이트한 문서 inventory
  - raw verification 명령과 명령별 상세 로그
  - reviewer input dump, guardrail ledger field 전체, 내부 운영 체크리스트
- 위 operational evidence는 exec plan, verification report, review comment, feedback ledger 같은 별도 close-out artifact에 남긴다.
- 새 라이브러리, 외부 서비스, 스키마/설정/환경 변경, 마이그레이션, 배포 주의점은 사람이 놓치기 쉬우므로 본문에 명시한다.

## 문서 링크 규칙

- 문서 내부 링크는 절대경로 대신 저장소 기준 상대경로를 사용한다.
- 다른 디렉터리 문서를 가리킬 때도 현재 문서 위치를 기준으로 상대경로를 적는다.
- 로컬 도구나 응답 메시지에서만 절대경로를 사용하고, 저장소 문서 본문에는 넣지 않는다.

## stable source of truth의 task ID 규칙

- `docs/product/`, `docs/exec-plans/`, GitHub Issue/PR 본문, baseline이나 historical snapshot처럼 tracking이 본질인 문서는 work item ID를 직접 써도 된다.
- `docs/architecture/`, `docs/operations/`, `docs/product/` 같은 stable source of truth 문서에는 future work나 follow-up 설명을 위해 직접적인 work item ID를 남기지 않는다.
- stable 문서에서 후속 확장을 가리킬 때는 task ID 대신 정책, registry, skill pack, guardrail 같은 자산 이름을 쓴다.
- task 완료 시 stable 문서에 임시로 넣었던 work item ID는 제거하거나 서술형 이름으로 치환한다.
- Issue ID 형식, 브랜치명 규칙처럼 식별자 형식 자체를 설명하는 문맥은 예외다.

## Runtime Simplification Principles

- 기본값은 `가장 짧은 안전 경로`다. 요청이 명확하고 위험도가 낮으면 issue, exec plan, reviewer handoff, feedback ledger를 모두 기본값처럼 붙이지 않는다.
- workflow가 지켜야 할 최소 공통분모는 `범위 고정 -> 구현 -> 결정론적 검증 -> open PR publish`다.
- independent review와 feedback close-out은 중요한 통제지만, 모든 작업의 publish를 지연시키는 공통 선행조건이 아니다. 위험 신호가 있거나 사용자가 원할 때만 올린다.
- draft PR은 기본 협업 방식이 아니다. 사용자가 명시적으로 요청한 경우에만 쓴다.
- 검증을 끝낸 결과는 가능한 한 빨리 open PR로 공개하고, 추가 review/repair는 그 위에서 이어간다.

## Issue/PR 단위 규칙

- tracked backlog 또는 guarded lane에서는 `Issue 1개 = PR 1개`를 유지한다.
- default lane의 작은 직접 요청은 issue를 생략할 수 있지만, 여전히 `PR 1개 = 목표 1개` 원칙을 지킨다.
- 하나의 PR은 하나의 목표만 해결한다
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다
- cross-repo 작업은 `workflow 문서 PR`과 `앱 코드 PR`로 나눈다
- quality sweep에서 나온 cleanup/refactor/unused code 후보도 원본 issue/PR에 끼워 넣지 않고 별도 issue/PR로 분리한다

## 요청 intake 규칙

- 작업 시작 전 [request-routing-policy.md](request-routing-policy.md)로 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다.
- `즉시 실행 가능한 작업`은 바로 `default lane` 또는 `guarded lane` 중 하나를 고른다.
- `모호한 요청`은 source of truth로 줄일 수 있는 ambiguity를 먼저 제거하고, 남는 blocker만 interview 질문으로 다룬다.
- `대화` 또는 `Rejected` close-out인 요청은 파일 편집을 시작하지 않는다.

## Execution Lane 규칙

| Lane | 언제 쓰나 | 필수 산출물 | 생략 가능한 것 |
| --- | --- | --- | --- |
| `default lane` | 단일 저장소, 명확한 요청, bounded write scope, 검증이 자명한 변경 | 짧은 task brief, latest verification summary, open PR | GitHub issue, active exec plan, sub-agent review, feedback ledger |
| `guarded lane` | tracked backlog, workflow/policy 변경, cross-repo planning, public contract/schema/auth/CI/migration/destructive change, 또는 사용자가 formal plan/review를 원할 때 | GitHub issue, active exec plan, verification report, 필요 시 review evidence | pre-publish draft PR, 불필요한 multi-reviewer pool |

`default lane` task brief에는 최소한 아래 네 가지가 보여야 한다.

- primary repo
- 문제 또는 목표
- write scope
- verification 방법

아래 신호 중 하나라도 있으면 `guarded lane`으로 올린다.

- 요청이 catalog item이거나 기존 issue/exec plan을 기준으로 추적되는 작업
- workflow policy, template, verification contract, CI, permissions, auth, public API/schema를 바꾸는 작업
- cross-repo planning이 필요하거나 write scope가 커질 가능성이 높은 작업
- destructive change, mass delete, migration처럼 rollback cost가 큰 작업
- 사용자가 명시적으로 formal plan, independent review, extra evidence를 요구한 작업

## Context Pack 규칙

- active exec plan이 있는 `guarded lane` 작업은 구현 전 [../architecture/context-pack-registry.md](../architecture/context-pack-registry.md)에서 primary context pack 하나를 고른다.
- `default lane`에서는 active exec plan을 만들지 않는 대신, touched source of truth와 target repo entrypoint만 읽고 시작한다.
- 모든 pack은 required docs만 먼저 읽고, optional docs는 issue, exec plan, hot file 탐색이 trigger를 줄 때만 연다.
- 서로 다른 pack의 required docs까지 동시에 필요해지면 ad-hoc으로 pack을 합치지 말고 issue 분해 또는 exec plan 갱신을 먼저 한다.
- target repo entry 문서나 worktree가 없으면 `Context Ready`를 선언하지 않고 `Blocked` 또는 준비 작업으로 되돌린다.
- `default lane`에서 새 policy 발명, sibling repo 탐색, broad write scope가 필요해지면 즉시 `guarded lane`으로 승격한다.

## Tool Boundary 규칙

- `guarded lane`은 context pack을 고른 뒤 구현 전 [tool-boundary-matrix.md](tool-boundary-matrix.md)로 task type별 read boundary, write boundary, network, escalation class를 잠근다.
- verification 단계에 들어가기 전 [verification-contract-registry.md](verification-contract-registry.md)에서 primary contract profile을 고르고, conditional command나 repo-specific override는 guarded lane의 exec plan에 적는다.
- `guarded lane` exec plan에는 최소한 primary repo, allowed write paths, control-plane artifact, explicitly forbidden path, network 필요 여부, escalation trigger를 적는다.
- `default lane`도 repo boundary와 verification contract는 지키지만, 별도 exec plan 없이 task brief와 PR body에서 scope를 좁게 설명하면 된다.
- prompt나 follow-up 메모로 범위를 넓히지 않는다. task brief, issue, exec plan에 없는 저장소 쓰기나 broad network access가 필요해지면 planning 또는 lane 승격으로 되돌린다.
- cross-repo planning은 여러 저장소를 읽을 수 있어도 app repo code write는 열지 않는다. app 구현이 필요하면 저장소별 issue/PR로 분리한다.
- dangerous command와 broad escalation은 사용자 명시 요청 또는 좁게 복구 가능한 예외가 아니면 허용하지 않는다.

## 각 Issue에 반드시 들어가야 할 내용

- 대상 저장소
- 문제 또는 배경
- 왜 지금 필요한지
- 기대 결과 또는 완료 조건
- 범위와 비범위
- 접근 메모 또는 주요 제약
- 남아 있는 리스크, open question, 참고 자료

## 각 PR에 반드시 들어가야 할 내용

- 연결된 Issue 또는 no-issue reason
- 무엇이 바뀌었는지와 왜 필요한지
- 어떤 과정과 판단으로 결과물을 만들었는지
- 검증 결과 요약과 남은 공백
- 리뷰어가 집중해서 볼 포인트가 있다면 그 지점
- 새 의존성, 외부 영향, 배포/롤백 주의점
- 남은 리스크와 후속 작업

## 증거 규칙

하네스 관련 PR에서는 가능하면 아래 증거를 남긴다.

- human-facing Issue/PR 본문과 운영용 close-out artifact를 분리한다.
- 명령 실행 결과 요약 또는 verification report 위치
- verification report 최소 필드: contract profile, command별 status, 핵심 evidence, failure summary, next action
- review evidence 최소 필드: implementer, reviewer, reviewer input, verdict, blocking finding 또는 no-blocking note
- reviewer pool을 사용했다면 final verdict owner와 역할별 reviewer를 함께 남긴다
- feedback evidence 최소 필드: stage, failure class, promotion decision, follow-up asset 또는 `no new guardrail` 이유, 핵심 evidence
- quality sweep evidence 최소 필드: trigger mode, scan scope, signal class, disposition, follow-up asset 또는 `no-action` 이유, 핵심 evidence
- 문서 업데이트: source of truth 반영 여부

문서 전용 작업도 무엇을 바꿨는지와 어떤 기준으로 확인했는지는 남겨야 한다. 다만 본문에는 판단에 필요한 요약만 적고, raw 명령이나 경로 inventory는 close-out artifact로 내린다.

추가 규칙:

- verification evidence는 모든 publish 대상 작업에서 필수다.
- review evidence는 independent review를 실제로 수행한 경우에만 필수다.
- feedback evidence는 blocker, 반복 실패, guardrail promotion, quality sweep follow-up이 있을 때만 필수다.
- 절차를 수행하지 않았는데 artifact를 형식적으로 채우기 위해 dummy evidence를 만들지 않는다.

## Historical Record 규칙

- `docs/exec-plans/completed/`의 문서는 당시 close-out 근거를 보존하는 historical record다.
- completed exec plan의 reviewer 이름, runtime 설명, 검증 결과, 파일명은 후속 정책 변경에 맞춘다는 이유만으로 rewrite하지 않는다.
- 현재 canonical runtime, 정책, 템플릿은 stable source of truth 문서인 `docs/operations/`, `docs/architecture/`, `docs/product/`, `.github/`, `.codex/skills/`에서 읽는다.
- historical exec plan이 현재 정책과 어휘가 다를 수 있다는 사실 자체는 drift가 아니라 이력이다. 현재 규칙과의 관계는 stable source of truth에서 설명한다.

## 브랜치와 슬러그 규칙

- Issue ID 형식: `GRW-01`, `GRB-01`, `GRC-01`
- 권장 브랜치명: `feat/grw-01-workflow-skeleton`
- 작업 슬러그: `2026-03-24-grw-01-workflow-skeleton`

약어:

- `GRW`: `git-ranker-workflow`
- `GRB`: `git-ranker`
- `GRC`: `git-ranker-client`

## GitHub Issue/PR 운영 규칙

- `guarded lane` 또는 tracked backlog 작업만 대상 저장소에 `gh issue create`로 이슈를 만든다.
- `default lane`의 작은 직접 요청은 issue 없이 진행할 수 있고, 그 경우 PR 본문에 `no-issue reason`과 scope 요약을 남긴다.
- 이슈와 PR 본문은 대상 저장소의 Issue/PR template 형식을 따른다.
- GitHub 본문은 먼저 파일로 작성한 뒤 `gh issue create --body-file <path>` 또는 `gh pr create --body-file <path>`로 보낸다.
- workflow 저장소 Issue 본문은 필요할 때 `.codex/skills/issue-to-exec-plan/assets/github-issue-body.md`를 복사해 채운다.
- workflow 저장소 PR 본문은 `.github/PULL_REQUEST_TEMPLATE.md`를 복사한 임시 파일을 기준으로 채운다.
- PR은 latest verification이 통과한 뒤 open 상태로 생성한다.
- draft PR은 사용자가 명시적으로 요청했을 때만 사용한다.
- verification 전에 막힌 작업은 placeholder draft PR로 공유하지 않는다. blocker는 issue, exec plan, 또는 작업 대화에 남긴다.
- PR은 검증된 결과를 공개하는 기본 협업 surface다. canonical 기본값은 `implement -> verify -> open PR publish`다.
- Issue/PR 본문에는 사람이 확인할 요약만 적고, detailed verification report, review evidence, feedback ledger는 exec plan이나 별도 close-out artifact에 남긴다.
- 성공한 검증은 PR 본문에 고수준 결과만 짧게 적고, 실패, 재시도, 예외, skipped check 같은 운영 상세는 verification report로 내린다.
- review verdict와 feedback decision은 PR 본문에 요약할 수 있지만, canonical evidence는 실제로 review나 feedback이 수행됐을 때만 [dual-agent-review-policy.md](dual-agent-review-policy.md)와 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)가 지정한 artifact에 남긴다.
- independent review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때만 수행한다. 필요 시 current Codex 세션의 session-isolated sub-agent reviewer를 쓸 수 있지만, reviewer pool은 기본값이 아니다.
- 생성 직후에는 `gh issue view --json body` 또는 `gh pr view --json body`로 본문이 예상한 줄바꿈과 섹션을 유지하는지 확인한다.
- Issue template은 최소한 `대상 저장소`, `문제/배경`, `왜 지금`, `완료 조건`, `범위/비범위`, `접근 메모`, `리스크 또는 참고 자료`를 포함해야 한다.
- PR template은 최소한 `요약`, `연결된 issue 또는 no-issue reason`, `접근`, `review guide`, `validation summary`, `dependencies/impact`, `risks/follow-up`을 포함해야 한다.
- 커밋 메시지는 항상 루트의 `.gitmessage.ko.txt` 형식을 따른다.
- 저장소별 작업은 각 저장소마다 별도 branch 또는 worktree에서 수행한다.
- 모든 기능 브랜치는 대상 저장소의 `develop` 브랜치를 기준으로 분기한다.
- cross-repo 작업은 저장소별로 이슈와 PR을 분리한다.
- `git-ranker-workflow`, `git-ranker`, `git-ranker-client`는 서로 다른 작업 트리를 써서 변경 범위를 섞지 않는다.

현재 기준 실행 순서:

1. [request-routing-policy.md](request-routing-policy.md)로 요청을 분류하고, `즉시 실행 가능한 작업`이면 `default lane` 또는 `guarded lane`을 고른다.
2. 대상 저장소의 `develop` 최신 상태를 기준으로 worktree 또는 branch를 만든다.
3. `guarded lane`이면 body file을 준비한 뒤 `gh issue create --body-file ...`로 대상 저장소 이슈를 만들고 active exec plan을 작성한다. `default lane`이면 짧은 task brief만 잠근다.
4. 구현을 수행한다.
5. latest verification report 또는 verification summary를 만든다.
6. PR body file에 작업 요약, 접근, validation summary, 영향, 남은 리스크를 채운 뒤 `gh pr create --base develop --body-file ...`로 open PR을 연다.
7. 생성 직후 `gh issue view --json body` 또는 `gh pr view --json body`로 본문 렌더링을 확인한다.
8. independent review가 필요한 작업이면 open PR 위에서 review를 수행하고, `changes-requested`가 나오면 implementer가 수리 후 영향을 받은 verification을 다시 실행한다.
9. blocker, 반복 실패, guardrail promotion 필요성이 있을 때만 feedback close-out을 남긴다.

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

- 이 Issue 또는 task brief의 목표만 수행한다. 범위를 넓히지 않는다.
- 선행조건이 충족되지 않았으면 임의로 우회 구현하지 말고 blocker를 먼저 정리한다.
- 허용된 write scope 밖의 파일은 수정하지 않는다.
- network나 escalation이 필요하면 목적과 범위를 task brief, exec plan, 또는 최종 close-out에 남긴다.
- verification failure가 나면 registry의 retry budget 안에서만 repair loop를 돌리고, budget 초과나 missing canonical source는 `Blocked` 또는 후속 planning으로 넘긴다.
- issue 없이 시작한 default lane 작업이 policy, contract, CI, cross-repo planning으로 커지면 즉시 guarded lane으로 승격한다.
- review 단계에 들어갈 때만 latest verification report와 reviewer minimum context를 준비한다.
- independent review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때만 수행한다. reviewer가 필요해도 기본값은 한 명의 분리된 reviewer이고, reviewer pool은 security/reliability처럼 추가 눈이 실제로 필요한 경우에만 올린다.
- `changes-requested`가 남아 있는 상태에서도 PR은 open 상태를 유지한다. canonical repair loop는 open PR의 current diff와 latest verification report를 기준으로 닫는다.
- 사용자가 다르게 요청하지 않았다면 latest verification이 통과한 즉시 open PR을 publish하고, review/repair는 그 뒤에 이어간다.
- feedback close-out은 blocker, 반복 실패, guardrail promotion, quality sweep follow-up이 있을 때만 남긴다.
- source of truth 문서를 함께 업데이트하거나, 업데이트가 불필요한 이유를 남긴다.
- 검증 명령과 최종 상태는 close-out artifact에 반드시 남기고, PR 본문에는 필요한 요약만 남긴다.
- quality sweep에서 나온 non-blocking cleanup candidate는 current issue에 섞지 말고 별도 work item으로 넘긴다.
- 새로 생긴 반복 절차가 있다면 skill 후보로 제안하되, 이번 Issue 범위를 넘는 구현은 하지 않는다.
- 모호한 선택지가 여러 개면 [docs/product/work-item-catalog.md](../product/work-item-catalog.md)의 기본 결정을 따른다.
- 실행 중 예상치 못한 dirty change가 있으면 되돌리지 말고 영향 여부만 확인한다.

## 공통 Definition of Done

각 작업은 아래 항목을 최대한 충족해야 한다.

- 왜 이 작업이 필요한지 문서나 PR 본문에 남아 있다
- 변경 범위가 한 가지 목표에 집중되어 있다
- 검증 결과가 PR 본문, exec plan, 또는 다른 close-out artifact에 남아 있다
- latest verification을 반영한 open PR이 생성됐거나, publish를 하지 않은 이유가 명시되어 있다
- 후속 작업의 전제조건이 명확하다
- independent review가 실제로 수행됐다면 그 evidence가 남아 있다
- feedback close-out이 실제로 필요했다면 그 판단과 follow-up이 남아 있다
- source of truth 문서가 함께 업데이트되었거나, 업데이트 불필요 사유가 명시되어 있다
- stable source of truth 문서에 남긴 임시 work item ID가 있다면 close-out 전에 제거되었거나 planning/history 문서로 이동했다
- 동일 작업이 반복될 가능성이 높다면 skill화 여부가 검토되었거나, 아직 만들지 않는 이유가 남아 있다
