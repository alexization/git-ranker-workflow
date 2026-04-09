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

## Issue/PR 단위 규칙

- 원칙적으로 `Issue 1개 = PR 1개`
- 하나의 PR은 하나의 목표만 해결한다
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다
- cross-repo 작업은 `workflow 문서 PR`과 `앱 코드 PR`로 나눈다
- quality sweep에서 나온 cleanup/refactor/unused code 후보도 원본 issue/PR에 끼워 넣지 않고 별도 issue/PR로 분리한다

## 요청 intake 규칙

- 작업 시작 전 [request-routing-policy.md](request-routing-policy.md)로 요청을 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 분류한다.
- `즉시 실행 가능한 작업`만 GitHub issue와 exec plan을 만든다.
- `모호한 요청`은 source of truth로 줄일 수 있는 ambiguity를 먼저 제거하고, 남는 blocker만 interview 질문으로 다룬다.
- `대화` 또는 `Rejected` close-out인 요청은 파일 편집을 시작하지 않는다.

## Context Pack 규칙

- active exec plan이 생기면 구현 전 [../architecture/context-pack-registry.md](../architecture/context-pack-registry.md)에서 primary context pack 하나를 고른다.
- 모든 pack은 required docs만 먼저 읽고, optional docs는 issue, exec plan, hot file 탐색이 trigger를 줄 때만 연다.
- 서로 다른 pack의 required docs까지 동시에 필요해지면 ad-hoc으로 pack을 합치지 말고 issue 분해 또는 exec plan 갱신을 먼저 한다.
- target repo entry 문서나 worktree가 없으면 `Context Ready`를 선언하지 않고 `Blocked` 또는 준비 작업으로 되돌린다.

## Tool Boundary 규칙

- context pack을 고른 뒤 구현 전 [tool-boundary-matrix.md](tool-boundary-matrix.md)로 task type별 read boundary, write boundary, network, escalation class를 잠근다.
- verification 단계에 들어가기 전 [verification-contract-registry.md](verification-contract-registry.md)에서 primary contract profile을 고르고, conditional command나 repo-specific override는 exec plan에 적는다.
- exec plan에는 최소한 primary repo, allowed write paths, control-plane artifact, explicitly forbidden path, network 필요 여부, escalation trigger를 적는다.
- prompt나 follow-up 메모로 범위를 넓히지 않는다. issue와 exec plan에 없는 저장소 쓰기나 broad network access가 필요해지면 planning으로 되돌린다.
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

- 연결된 Issue
- 무엇이 바뀌었는지와 왜 필요한지
- 어떤 과정과 판단으로 결과물을 만들었는지
- 리뷰어가 집중해서 볼 포인트
- 검증 결과 요약과 남은 공백
- 새 의존성, 외부 영향, 배포/롤백 주의점
- 남은 리스크와 후속 작업

## 증거 규칙

하네스 관련 PR에서는 가능하면 아래 증거를 남긴다.

- human-facing Issue/PR 본문과 운영용 close-out artifact를 분리한다.
- 명령 실행 결과 요약 또는 verification report 위치
- verification report 최소 필드: contract profile, command별 status, 핵심 evidence, failure summary, next action
- review evidence 최소 필드: implementer, reviewer, reviewer input, verdict, blocking finding 또는 no-blocking note
- reviewer pool의 final verdict owner와 역할별 reviewer를 함께 남긴다
- feedback evidence 최소 필드: stage, failure class, promotion decision, follow-up asset 또는 `no new guardrail` 이유, 핵심 evidence
- quality sweep evidence 최소 필드: trigger mode, scan scope, signal class, disposition, follow-up asset 또는 `no-action` 이유, 핵심 evidence
- 문서 업데이트: source of truth 반영 여부

문서 전용 작업도 무엇을 바꿨는지와 어떤 기준으로 확인했는지는 남겨야 한다. 다만 본문에는 판단에 필요한 요약만 적고, raw 명령이나 경로 inventory는 close-out artifact로 내린다.

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

- `즉시 실행 가능한 작업`으로 판정된 뒤 대상 저장소에 `gh issue create`로 이슈를 만든다.
- 이슈와 PR 본문은 대상 저장소의 Issue/PR template 형식을 따른다.
- GitHub 본문은 먼저 파일로 작성한 뒤 `gh issue create --body-file <path>` 또는 `gh pr create --body-file <path>`로 보낸다.
- workflow 저장소 Issue 본문은 `.codex/skills/issue-to-exec-plan/assets/github-issue-body.md`를 복사해 채운다.
- workflow 저장소 PR 본문은 `.github/PULL_REQUEST_TEMPLATE.md`를 복사한 임시 파일을 기준으로 채운다.
- PR은 기본적으로 open으로 생성한다. draft PR은 사용자가 명시적으로 요청했거나, scope-complete 전 공유가 필요한 blocker를 body와 exec plan에 적을 때만 예외적으로 사용한다.
- PR은 review를 받기 위한 작업용 draft workspace가 아니다. canonical 기본값은 local diff와 exec plan artifact에서 verification, independent review, feedback close-out을 먼저 끝내고, 그 최신 결과를 PR에 싣고 publish하는 것이다.
- Issue/PR 본문에는 사람이 확인할 요약만 적고, detailed verification report, review evidence, feedback ledger는 exec plan이나 별도 close-out artifact에 남긴다.
- 성공한 검증은 PR 본문에 고수준 결과만 짧게 적고, 실패, 재시도, 예외, skipped check 같은 운영 상세는 verification report로 내린다.
- review verdict와 feedback decision은 PR 본문에 요약할 수 있지만, canonical evidence는 [dual-agent-review-policy.md](dual-agent-review-policy.md)와 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)가 지정한 artifact에 남긴다.
- independent review는 현재 Codex 세션에서 분리 생성한 session-isolated sub-agent reviewer pool로 수행한다. MCP 기반 외부 reviewer runtime이나 외부 모델 호출은 canonical review 경로가 아니다. reviewer pool의 final verdict owner는 한 명이어야 하며, evidence block은 하나의 canonical verdict로 집계한다.
- 생성 직후에는 `gh issue view --json body` 또는 `gh pr view --json body`로 본문이 예상한 줄바꿈과 섹션을 유지하는지 확인한다.
- Issue template은 최소한 `대상 저장소`, `문제/배경`, `왜 지금`, `완료 조건`, `범위/비범위`, `접근 메모`, `리스크 또는 참고 자료`를 포함해야 한다.
- PR template은 최소한 `요약`, `연결된 issue`, `접근`, `review guide`, `validation summary`, `dependencies/impact`, `risks/follow-up`을 포함해야 한다.
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
5. 작업 후 latest verification report를 만들고, reviewer minimum context를 준비한 뒤 session-isolated sub-agent reviewer pool로 independent review를 먼저 수행한다. 공통 handoff surface를 각 reviewer에 fan-out하되, 역할별 focus에 맞는 subset만 줄 수 있고 final verdict owner 하나를 남긴다.
6. review verdict가 `changes-requested`면 implementer가 in-scope repair를 수행하고, 영향을 받은 verification을 다시 실행한 뒤 reviewer pool을 다시 수행한다. `approved` 또는 declared blocker가 나오기 전에는 PR을 만들지 않는다.
7. latest review verdict와 publish path에 필요한 evidence가 고정된 뒤 PR body file에 작업 요약, 접근, review guide, validation summary, 영향, 남은 리스크를 채우고, detailed verification/review/feedback evidence는 close-out artifact에 정리한다. open path는 feedback outcome을, blocker-sharing draft path는 blocker disclosure를 포함한다.
8. 사용자가 draft를 명시적으로 요청했거나, scope-complete 전 blocker 공유가 필요하면 draft PR을 연다. 그렇지 않다면 `gh pr create --base develop --body-file ...`로 open PR을 연다.
9. 생성 직후 `gh issue view --json body` 또는 `gh pr view --json body`로 본문 렌더링을 확인한다.

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
- reviewer minimum context의 canonical handoff surface는 reviewer pool 전체에 공통이다. 역할별 reviewer는 focus에 맞는 subset만 읽을 수 있지만, implementer가 handoff 항목을 임의로 삭제하거나 final verdict owner의 추적 책임을 줄일 수는 없다.
- independent review는 항상 session-isolated sub-agent reviewer들로 수행하고, implementer와 reviewer의 세션, prompt, output ownership을 섞지 않는다.
- `changes-requested`가 남아 있는 상태에서 draft PR을 먼저 열고 review thread를 canonical repair loop처럼 쓰지 않는다. 기본 repair loop는 local diff, latest verification report, reviewer evidence를 기준으로 닫는다.
- 사용자가 다르게 요청하지 않았다면 independent review와 feedback close-out을 끝낸 뒤 PR을 publish한다.
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
- 검증 결과가 exec plan이나 다른 close-out artifact에 남아 있다
- 후속 작업의 전제조건이 명확하다
- source of truth 문서가 함께 업데이트되었거나, 업데이트 불필요 사유가 명시되어 있다
- stable source of truth 문서에 남긴 임시 work item ID가 있다면 close-out 전에 제거되었거나 planning/history 문서로 이동했다
- 동일 작업이 반복될 가능성이 높다면 skill화 여부가 검토되었거나, 아직 만들지 않는 이유가 남아 있다
