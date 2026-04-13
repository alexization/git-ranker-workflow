# AGENTS.md

`git-ranker-workflow`는 `git-ranker-workflow`, `git-ranker`, `git-ranker-client`를 묶는 하네스 컨트롤 플레인 저장소다.

## 시작 순서

1. [docs/README.md](docs/README.md)를 읽고 문서 구조를 확인한다.
2. [SPECS.md](SPECS.md)에서 spec 파일명과 상태 규칙을 확인한다.
3. [docs/operations/sdd-spec-policy.md](docs/operations/sdd-spec-policy.md)에서 SDD와 소크라테스 기반 spec 규칙을 확인한다.
4. [docs/operations/workflow-governance.md](docs/operations/workflow-governance.md)에서 공통 작업 운영 규칙과 증거 규칙을 확인한다.
5. 해당 작업과 관련된 디렉터리의 `README.md`와 본문 문서를 읽는다.
6. 현재 작업 문서는 `docs/specs/active/`, 완료된 작업 문서는 `docs/specs/completed/`에서 찾는다.

## source of truth 위치

- [docs/architecture](docs/architecture/README.md): 컨트롤 플레인 구조와 cross-repo 경계
- [docs/operations](docs/operations/README.md): 작업 운영 규칙, evidence, runbook
- [docs/specs](docs/specs/README.md): SDD 기반 작업 spec 문서와 남은 요구사항 queue

앱 동작의 canonical source는 workflow 복제 문서가 아니라 각 앱 저장소의 엔트리 문서와 코드/테스트에 둔다.

## 운영 원칙

- 루트 문서는 인덱스만 맡는다. 상세 규칙은 `docs/` 아래에 둔다.
- 새 작업은 원칙적으로 stable source of truth 문서를 먼저 읽고, 남은 작업은 `docs/specs/active/`의 draft/approved spec으로 확인한다.
- 모든 즉시 실행 가능한 작업은 구현 전에 소크라테스 방식으로 spec을 먼저 만든다.
- spec은 요구사항, 하위 작업, write scope, verification, tracking 결정을 함께 소유한다.
- 변경이 생기면 코드만이 아니라 관련 source of truth 문서도 함께 갱신한다.
- 커밋 메시지는 항상 루트의 `.gitmessage.ko.txt` 형식을 따른다.
