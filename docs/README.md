# Docs Index

이 저장소의 공식 문서는 `AGENTS.md`를 헌법으로 두고, `docs/`는 그 헌법을 설명하는 보조 문서만 유지한다.

## 먼저 읽을 문서

1. [AGENTS.md](../AGENTS.md)
2. [docs/artifact-model.md](artifact-model.md)
3. [docs/runtime.md](runtime.md)
4. [docs/hooks.md](hooks.md)
5. [docs/runbook.md](runbook.md)

## 문서 맵

- [artifact-model.md](artifact-model.md): `tasks/`와 `system/` artifact 구조, spec과 phase 적재 위치
- [runtime.md](runtime.md): 승인, phase 실행, verification, review, reopen 순서와 내부 런타임 구조
- [hooks.md](hooks.md): TDD, write scope, dangerous command, verification freshness, circuit breaker
- [runbook.md](runbook.md): 초기화, 새 task 생성, 점검 명령

## 우선순위

- 헌법과 강제 규칙은 `AGENTS.md`가 소유한다.
- 현재 작업의 상태와 증거는 `workflows/tasks/<task-id>/`가 소유한다.
- 전역 guard 정책은 `workflows/system/hooks.json`이 소유한다.
- 앱 동작의 source of truth는 각 앱 저장소의 문서, 코드, 테스트다.
