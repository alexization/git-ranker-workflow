# Workflow Governance

이 문서는 workflow 저장소를 기준으로 모든 Issue/PR 작업이 공유해야 하는 운영 규칙을 정의한다.

## 문서 링크 규칙

- 문서 내부 링크는 절대경로 대신 저장소 기준 상대경로를 사용한다.
- 다른 디렉터리 문서를 가리킬 때도 현재 문서 위치를 기준으로 상대경로를 적는다.
- 로컬 도구나 응답 메시지에서만 절대경로를 사용하고, 저장소 문서 본문에는 넣지 않는다.

## Issue/PR 단위 규칙

- 원칙적으로 `Issue 1개 = PR 1개`
- 하나의 PR은 하나의 목표만 해결한다
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다
- cross-repo 작업은 `workflow 문서 PR`과 `앱 코드 PR`로 나눈다

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
- 검증 명령과 결과
- 독립 review 결과
- feedback 또는 후속 guardrail 후보
- 남은 리스크
- 다음 Issue로 넘겨야 할 전제조건

## 증거 규칙

하네스 관련 PR에서는 가능하면 아래 증거를 남긴다.

- 명령 실행 결과 요약
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

- 작업 시작 전 대상 저장소에 `gh issue create`로 이슈를 만든다.
- 이슈와 PR 본문은 대상 저장소의 Issue/PR template 형식을 따른다.
- Issue template은 최소한 `문제`, `왜 지금`, `범위/비범위`, `write scope`, `context source`, `verification plan`, `open questions`를 포함해야 한다.
- PR template은 최소한 `연결된 issue`, `범위/비범위`, `write scope`, `verification 결과`, `독립 review 결과`, `feedback follow-up`, `문서 반영`, `리스크`를 포함해야 한다.
- 커밋 메시지는 항상 루트의 `.gitmessage.ko.txt` 형식을 따른다.
- 저장소별 작업은 각 저장소마다 별도 branch 또는 worktree에서 수행한다.
- 모든 기능 브랜치는 대상 저장소의 `develop` 브랜치를 기준으로 분기한다.
- cross-repo 작업은 저장소별로 이슈와 PR을 분리한다.
- `git-ranker-workflow`, `git-ranker`, `git-ranker-client`는 서로 다른 작업 트리를 써서 변경 범위를 섞지 않는다.

현재 기준 실행 순서:

1. 대상 저장소의 `develop` 최신 상태를 기준으로 worktree 또는 branch를 만든다.
2. `gh issue create`로 대상 저장소 이슈를 만든다.
3. 이슈 번호를 브랜치명과 exec plan에 연결한다.
4. 작업 후 `gh pr create --base develop`로 PR을 연다.
5. PR 본문에 검증 결과, 독립 review 결과, 문서 반영 여부, 남은 리스크를 채운다.

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
- source of truth 문서를 함께 업데이트하거나, 업데이트가 불필요한 이유를 남긴다.
- 검증 명령과 결과를 반드시 남긴다.
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
- 동일 작업이 반복될 가능성이 높다면 skill화 여부가 검토되었거나, 아직 만들지 않는 이유가 남아 있다

하네스 관련 작업은 아래 항목도 추가로 본다.

- 브라우저, 로그, 메트릭 중 이번 PR에서 다룬 신호가 무엇인지 명확하다
- 증거 산출 위치가 정해져 있다
- 실패 시 어떤 루프로 다시 수정할지 문서화되어 있다
