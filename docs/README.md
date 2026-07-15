# Harness 구조

이 저장소의 에이전트 harness는 Claude Code 기준으로 구성한다. 헌법은 루트 [CLAUDE.md](../CLAUDE.md)가 소유하고, 이 문서는 구성 요소의 위치만 안내한다.

## 구성 요소 맵

| 위치 | 역할 |
|---|---|
| [CLAUDE.md](../CLAUDE.md) | cross-repo 공통 규약 (작업 원칙, 검증 베이스라인, git 규약) |
| `.claude/settings.json` | Claude Code 훅 등록 (PreToolUse) |
| `.claude/hooks/block-dangerous.sh` | 위험 명령(rm -rf, force push, reset --hard 등) 세션 내 차단 |
| `git-ranker/CLAUDE.md` | backend 작업 규약 |
| `git-ranker/.claude/skills/{red,green,refactor}` | backend TDD 턴 스킬 |
| `git-ranker/.githooks/pre-commit` | 구현-테스트 동반 커밋 검사 (TDD_SKIP=1로 명시적 우회) |
| `git-ranker-client/CLAUDE.md` | frontend 작업 규약 |
| `git-ranker-client/docs/verification-contract.md` | frontend 검증 계약 (lint/typecheck/build) |

## 설계 원칙

- 요구사항 정리와 계획 승인은 Claude Code의 Plan 모드와 AskUserQuestion이 담당한다. 별도의 spec 문서/승인 상태 기계를 두지 않는다.
- 강제는 두 겹이다: Claude 세션 안에서는 PreToolUse 훅, 세션 밖 터미널 작업은 git hooks가 방어한다. force-push의 근본 방어는 GitHub branch protection이다.
- 정책 문서는 짧게 유지한다. 반복 절차는 스킬로, 저장소별 규약은 각 저장소의 CLAUDE.md로 내린다.
