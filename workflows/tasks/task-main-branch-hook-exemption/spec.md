# main 브랜치 hook 면제 정책 도입

- Task ID: `task-main-branch-hook-exemption`
- Primary Repo: `git-ranker-workflow`
- Status: `draft`

## Request

- `develop` 브랜치에는 `pre-commit`, `pre-push`가 필요하지만, `main` 브랜치는 `develop` 내용을 merge 또는 fast-forward로 반영해 최신 상태를 publish하는 용도이므로 동일한 hook 강제를 적용하지 않도록 control plane 계약을 조정한다.
- 결과적으로 `main` publish 경로가 task artifact 부재 때문에 fail-closed 되는 문제를 제거한다.

## Problem

- 현재 `pre-push`는 unpushed diff를 단일 task scope로 매핑하지 못하면 fail-closed 한다.
- `main` 브랜치에는 여러 완료 이력이 누적되지만 해당 task artifact가 저장소에 남아 있지 않을 수 있어, 단순한 `develop` 동기화 push도 hook에서 차단된다.
- `main`이 배포용 동기화 브랜치라면 `develop`과 동일한 task-bound guard를 유지하는 것이 운영 흐름과 맞지 않는다.

## Goals

- `main` 브랜치에서 `develop` 동기화 publish를 수행할 때 `pre-commit`, `pre-push`가 불필요하게 차단하지 않도록 한다.
- 예외 판별 기준은 `main` tip이 push 시점의 `develop` tip과 동일한 경우로 제한한다.
- `develop` 및 그 외 작업 브랜치에서는 기존 hook guard를 유지한다.
- 변경된 branch-aware policy가 문서, hook wrapper, runtime 테스트에 함께 반영되도록 한다.

## Non-goals

- `develop` 브랜치의 guard 정책을 약화하지 않는다.
- workflow task artifact 모델 자체를 제거하거나 verification guard를 전역 비활성화하지 않는다.
- 앱 저장소(`git-ranker`, `git-ranker-client`)의 동작 계약은 변경하지 않는다.

## Constraints

- workflow 계약 변경이므로 `AGENTS.md`, `docs/`, `.githooks/`, `tests/`까지 같이 맞춰야 한다.
- `main` 예외가 허용되더라도 destructive command guard 같은 안전 장치는 의도치 않게 약화되면 안 된다.
- merge commit 여부, 커밋 메시지, 사람이 의도한 merge 동작 자체는 신뢰하지 않고, git graph에서 관찰 가능한 `main == develop` 상태만 허용 기준으로 사용한다.
- 승인 전에는 phase 생성이나 구현을 시작하지 않는다.

## Acceptance

- `main` 브랜치에서 push 대상 tip이 현재 `develop` tip과 동일하면 `git push origin main` 경로가 branch policy에 따라 허용된다.
- `main` 브랜치라도 tip이 `develop`과 다르면 기존 guard 경로를 계속 탄다.
- `develop` 브랜치에서는 기존처럼 hook guard가 동작해 task binding 및 verification freshness를 계속 검사한다.
- 관련 runtime test가 `main` 예외와 `develop` 유지 동작을 모두 검증한다.
- 문서가 branch-aware hook 정책을 명시한다.

## Socratic Clarification Log

- Q: `main` 브랜치에도 `develop`과 동일한 `pre-commit`/`pre-push` guard를 유지해야 하는가?
- A: `develop` 브랜치는 guard가 필요하지만, `main` 브랜치는 `develop`의 내용을 merge 후 최신화하는 역할이라 굳이 `.githook`이 필요하지 않다.
- Decision: `main` 브랜치는 작업 브랜치와 다른 publish 성격을 가진다는 전제로, branch-aware hook 정책을 검토한다.
- Q: `main` 브랜치 예외를 어떤 기준으로 판별할 것인가?
- A: merge 의도나 커밋 메시지 대신, push 시점의 `main` tip이 `develop` tip과 동일할 때만 예외를 주는 기준이 안전하다.
- Decision: `main == develop`인 동기화 publish에 한해 hook 예외를 허용하고, 그 외 `main` push는 기존 guard를 유지한다.

## Approval

- Actor: `user`
- Timestamp: `2026-04-16T04:34:35+00:00`
- Note: main==develop 동기화 push 예외 기준으로 spec 승인
