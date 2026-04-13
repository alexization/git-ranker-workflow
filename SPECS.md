# SPECS.md

이 문서는 spec 문서의 파일명 규칙과 상태 전이 규칙만 다룬다.

## 파일 위치

- 진행 중이거나 아직 끝나지 않은 spec 문서: [docs/specs/active](docs/specs/active/README.md)
- 완료되었거나 실행 없이 종료된 spec 문서: [docs/specs/completed](docs/specs/completed/README.md)

## 파일명 규칙

- 기본 형식: `YYYY-MM-DD-<slug>.md`
- 예시: `2026-04-13-grw-sdd-socratic-harness-workflow.md`
- slug는 가능하면 primary repo나 work item을 드러내도록 짧고 구체적으로 쓴다.
- GitHub issue가 있더라도 spec 파일명에 issue 번호를 강제하지 않는다. issue/PR 연결 정보는 spec metadata에 적는다.

## 상태 규칙

spec 문서 본문 상단에는 최소한 아래 상태 중 하나를 명시한다.

- `Draft`: 소크라테스 질문과 초안 정리가 진행 중인 상태
- `Approved`: Harness 판단과 사용자 승인이 끝나 구현 또는 추적 단계로 넘어갈 수 있는 상태
- `In Progress`: 구현, 검증, tracking artifact 생성 같은 실행이 진행 중인 상태
- `Blocked`: 선행조건 미충족이나 외부 이슈로 진행이 막힌 상태
- `Completed`: 구현, 검증, 최종 사용자 확인까지 끝난 상태
- `Rejected`: 대화 전환, 취소, 범위 밖 요청 등으로 실행 없이 종료한 상태

## 전이 규칙

- `Draft`, `Approved`, `In Progress`, `Blocked` 상태 문서는 `docs/specs/active/`에 둔다.
- `Completed`, `Rejected` 상태 문서는 `docs/specs/completed/`에 둔다.
- 한 작업의 canonical working artifact는 항상 spec 하나다.
- 추가 planning 문서를 따로 만들지 않는다. 하위 작업 분해, write scope, verification, tracking 결정은 spec 안에 함께 남긴다.
