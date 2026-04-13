# Docs Index

이 저장소의 공식 문서는 목적별 디렉터리로 나뉜다. 새 작업은 이 문서와 각 디렉터리 `README.md`를 진입점으로 삼는다.

## 먼저 읽을 문서

1. [AGENTS.md](../AGENTS.md)
2. [SPECS.md](../SPECS.md)
3. [docs/architecture/control-plane-map.md](architecture/control-plane-map.md)
4. [docs/architecture/harness-system-map.md](architecture/harness-system-map.md)
5. [docs/operations/sdd-spec-policy.md](operations/sdd-spec-policy.md)
6. [docs/operations/workflow-governance.md](operations/workflow-governance.md)
7. [docs/specs/README.md](specs/README.md)
8. [docs/specs/active/README.md](specs/active/README.md)

## 디렉터리 맵

- [docs/architecture](architecture/README.md): 저장소 구조, cross-repo 경계, 문서 배치 규칙
- [docs/operations](operations/README.md): 작업 운영 규칙, evidence, 실행 runbook
- [docs/specs](specs/README.md): SDD 기반 작업 spec 문서, draft requirement, completed history

## 우선순위

- 현재 workflow는 Harness control plane 문서만 유지한다.
- 모든 즉시 실행 가능한 작업은 구현 전에 승인된 spec을 먼저 만든다.
- 별도 roadmap/catalog source는 유지하지 않고, 남은 작업은 `docs/specs/active/`의 draft/approved spec으로 관리한다.
- 앱 동작과 계약의 canonical source는 각 앱 저장소의 `AGENTS.md`, `README.md`, 코드, 테스트를 우선한다.
