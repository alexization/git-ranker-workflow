# Skill Authoring Rules

이 문서는 `git-ranker-workflow` 전용 skill을 새로 추가할 때 따라야 할 최소 작성 기준을 정리한다. 목표는 구조를 과하게 고정하는 것이 아니라, 어떤 skill이 들어와도 입력/출력/증거 규칙이 빠지지 않게 만드는 것이다.

## Authoring Principles

- skill은 문서형 자산부터 시작한다. 처음부터 스크립트나 자동화를 넣지 않는다.
- skill은 source of truth를 대체하지 않는다. 필요한 도메인 문서와 운영 문서를 먼저 읽게 해야 한다.
- 한 skill은 한 작업 흐름만 다룬다.
- 후속 에이전트가 같은 절차를 재사용할 수 있을 정도로만 구체적으로 쓴다.
- 구조보다 판단 기준과 금지 사항을 우선 명확히 쓴다.

## Required Coverage

각 `SKILL.md`는 섹션 이름이 완전히 같을 필요는 없지만, 아래 항목을 반드시 다뤄야 한다.

- 목적: 이 skill이 해결하는 반복 작업
- Trigger: 언제 이 skill을 써야 하는지
- 입력과 선행조건: 필요한 문서, 저장소 상태, 의존 작업
- 출력과 산출물 위치: 무엇을 남기고 어디에 두는지
- 표준 명령: 기본 검증 명령이나 확인 절차
- Required evidence: 확인해야 할 로그, 문서, 아티팩트, 명령 결과
- Forbidden shortcuts: 우회 구현, 생략하면 안 되는 단계
- Parallel ownership rule: 병렬 에이전트 사용 시 파일/책임 분리 규칙

## Writing Guidance

- 서두에서 관련 source of truth 문서를 먼저 읽게 한다.
- 명령은 실제로 반복 실행 가능한 수준으로 구체적으로 적는다.
- 증거 규칙은 "가능하면"이 아니라 "최소 무엇은 남겨야 한다" 수준으로 적는다.
- 금지 사항은 모호하게 쓰지 말고, 어떤 우회를 막는지 분명히 적는다.
- 후속 작업의 재진입 지점이 있다면 함께 적는다.

## File Layout Rules

- 기본 레이아웃은 `skills/<skill-name>/SKILL.md`다.
- 지원 파일은 각 skill 폴더 안에 둔다.
- 아래 디렉터리는 필요할 때만 추가한다.
  - `templates/`
  - `queries/`
  - `examples/`
  - `checklists/`
- 공통 지원 자산이 정말 생기기 전까지는 `skills/` 루트에 별도 shared 디렉터리를 만들지 않는다.

## Scope Guardrails

- 아직 존재하지 않는 런타임, 쿼리, 테스트 인프라를 skill에서 발명하지 않는다.
- 현재 Issue의 write scope를 넘는 파일 변경을 skill에서 정당화하지 않는다.
- "언젠가 필요할 수도 있는" 절차까지 미리 넣지 않는다.
- source of truth 문서 업데이트가 필요한 경우, 해당 문서 반영 또는 반영 불필요 사유를 함께 남긴다.

## Review Checklist

- 이 skill이 반복 가능성이 높은 하나의 흐름에 집중하는가
- 필요한 입력과 선행조건이 빠지지 않았는가
- 산출물 위치와 required evidence가 명확한가
- forbidden shortcuts와 ownership rule이 실제 위험을 막는가
- 관련 source of truth 문서 링크가 포함되어 있는가
