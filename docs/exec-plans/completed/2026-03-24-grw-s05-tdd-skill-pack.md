# 2026-03-24-grw-s05-tdd-skill-pack

- Issue ID: `GRW-S05`
- GitHub Issue: `#7`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s05-tdd-skill-pack`
- Task Slug: `2026-03-24-grw-s05-tdd-skill-pack`

## Problem

기능 구현을 TDD로 반복 수행할 계획이지만, `red`, `green`, `refactor` 각 턴에서 무엇을 만들고 무엇을 금지하는지에 대한 project skill이 없다. 이 상태에서는 테스트 작성, 최소 구현, 리팩터링의 경계가 작업자마다 달라질 수 있다.

## Why Now

backend와 client 저장소에서 앞으로 기능 구현 작업이 이어질 예정이므로, 구현 전에 TDD 턴 기준을 먼저 고정해 두는 편이 낫다. 지금 skill로 분리해 두면 이후 기능 요청에서 같은 절차를 반복 설명하지 않아도 된다.

## Scope

- `red`, `green`, `refactor` skill 작성
- 각 skill에 목적, trigger, 입력, 출력, 검증, 금지 사항, ownership rule 정의
- `.codex/skills/README.md`에 새 skill pack 등록
- `docs/product/`에 `GRW-S05` 작업 추가
- `GRW-S05` 실행/완료 기록 남기기

## Non-scope

- 특정 기능 자체 구현
- 테스트 프레임워크 선택 강제
- coverage automation 또는 CI 추가
- 기존 roadmap 역사 문서 정리

## Write Scope

- `.codex/skills/`
- `docs/product/`
- `docs/exec-plans/`

## Outputs

- `.codex/skills/red/SKILL.md`
- `.codex/skills/green/SKILL.md`
- `.codex/skills/refactor/SKILL.md`
- `.codex/skills/README.md`
- `.codex/skills/authoring-rules.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `GRW-S05` 실행/완료 기록

## Verification

- `find .codex/skills -maxdepth 2 -type f | sort`
  - 결과: `.codex/skills/README.md`, `.codex/skills/authoring-rules.md`, `.codex/skills/red/SKILL.md`, `.codex/skills/green/SKILL.md`, `.codex/skills/refactor/SKILL.md`를 확인했다.
- `cat .codex/skills/red/SKILL.md`
  - 결과: red 턴의 산출물을 failing test file 하나로 고정하고 production code 변경 금지를 확인했다.
- `cat .codex/skills/green/SKILL.md`
  - 결과: green 턴에서 test file 수정 없이 최소 구현으로 targeted test를 green으로 만드는 기준을 확인했다.
- `cat .codex/skills/refactor/SKILL.md`
  - 결과: refactor 턴에서 test file cleanup은 허용하되 assertion 의미와 behavior contract 변경은 금지하는 기준을 확인했다.
- `rg -n "GRW-S05|name: red|name: green|name: refactor" docs/product .codex/skills docs/exec-plans/completed/2026-03-24-grw-s05-tdd-skill-pack.md`
  - 결과: 새 skill pack과 skill 이름이 `.codex/skills/README.md`, `docs/product/harness-roadmap.md`, `docs/product/work-item-catalog.md`, 완료 기록에 반영된 것을 확인했다.

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 검증 명령 결과와 갱신된 source of truth 문서 경로를 exec plan에 남긴다.

## Risks or Blockers

- 현재 skill은 repo-agnostic하게 작성돼 있어, 실제 backend/client 작업에서 반복되는 프레임워크별 패턴은 후속 skill이나 examples로 보완할 수 있다.
- red/green/refactor 경계를 강하게 잡았기 때문에, 예외 상황이 반복되면 별도 보완 규칙을 추가해야 한다.

## Next Preconditions

- 이후 backend/client 기능 구현 작업에서 이 skill pack을 실제로 사용해 보고 보완 포인트를 수집한다.
- 반복되는 프레임워크별 예시가 쌓이면 `examples/` 또는 후속 skill pack으로 분리한다.

## Docs Updated

- `.codex/skills/README.md`
- `.codex/skills/authoring-rules.md`
- `.codex/skills/red/SKILL.md`
- `.codex/skills/green/SKILL.md`
- `.codex/skills/refactor/SKILL.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/2026-03-24-grw-s05-tdd-skill-pack.md`

## Skill Consideration

이번 Issue는 구현용 공용 TDD 절차를 project skill로 고정하는 작업이다. 이후 실제 기능 작업에서는 이 skill pack을 그대로 재사용하고, 특정 저장소 패턴이 반복될 때만 repo-specific 보조 skill을 추가한다.
