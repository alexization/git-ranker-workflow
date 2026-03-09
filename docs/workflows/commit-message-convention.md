---
summary: Shared Korean commit-message convention for the control-plane repo and both application repos.
read_when:
  - preparing a commit in this repository
  - preparing a commit in git-ranker or git-ranker-client
  - deciding which commit type and message shape to use
---

# Commit Message Convention

Use the same commit-message format in:

- `git-ranker-workflow`
- `git-ranker`
- `git-ranker-client`

## Language rule

제목과 본문을 포함한 커밋 메시지 전체를 한국어로 작성한다.

## Subject format

The first line must use this shape:

```text
<type>: <핵심적인 작업 내용>
```

Example:

```text
feat: 랭킹 필터 상태를 URL 쿼리와 동기화
```

## Allowed types

- `feat`: 사용자 기능 추가 또는 동작 확장
- `fix`: 버그 수정, 회귀 수정, 잘못된 동작 복구
- `docs`: 문서, 가이드, 템플릿, 주석성 규칙 변경
- `refactor`: 동작 변경 없이 구조 개선
- `test`: 테스트 추가, 수정, 안정화
- `chore`: 유지보수성 작업, 설정 정리, 의존성 관리
- `perf`: 성능 개선
- `build`: 빌드 시스템, 패키지, 배포 산출물 관련 변경
- `ci`: CI/CD 파이프라인 관련 변경
- `revert`: 기존 커밋 되돌리기

## Subject rules

- 커밋 메시지 전체가 한국어여야 한다.
- 제목은 한 줄로 끝낸다.
- 가장 중요한 결과를 먼저 쓴다.
- 마침표를 붙이지 않는다.
- 모호한 표현보다 변경된 핵심 행동이나 산출물을 쓴다.

Good:

```text
docs: 워크플로우 검증에서 1회성 서브모듈 체크 분리
fix: 로그인 콜백에서 누락된 state 검증 추가
refactor: GitHub 분석 서비스와 컨트롤러 의존성 정리
```

Avoid:

```text
feat: 수정
chore: 이것저것 정리
fix: 문제 해결 완료.
```

## Body format

제목 아래 한 줄을 비우고, 세부 작업은 bullet list로 짧게 쓴다.

```text
docs: 커밋 메시지 규칙 문서화

- 공통 커밋 타입과 한국어 제목 규칙 추가
- 루트 리포와 두 서브모듈에 동일하게 적용하도록 명시
- git commit template로 재사용 가능한 템플릿 파일 추가
```

## Body rules

- 각 bullet은 하나의 작업 단위를 설명한다.
- bullet과 추가 설명도 모두 한국어로 작성한다.
- 구현 세부보다 결과와 의도를 우선한다.
- 불필요하게 긴 배경 설명은 넣지 않는다.
- 제목만으로 충분한 아주 작은 커밋은 본문을 생략할 수 있다.

## Usage with git commit template

This repository provides a reusable template file at
[`/.gitmessage.ko.txt`](/Users/hyoseok/Desktop/git-ranker-workflow/.gitmessage.ko.txt).

Examples:

- Root repo:
  `git config commit.template .gitmessage.ko.txt`
- From `git-ranker`:
  `git config commit.template ../.gitmessage.ko.txt`
- From `git-ranker-client`:
  `git config commit.template ../.gitmessage.ko.txt`

If a developer prefers a global setup, an absolute path is also acceptable as
long as the same format is used.
