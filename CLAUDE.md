# CLAUDE.md

`git-ranker-workflow`는 `git-ranker`(backend)와 `git-ranker-client`(frontend) 서브모듈을 묶는 umbrella 저장소다. 이 저장소는 cross-repo 작업의 진입점과 공통 규약만 소유하고, 앱 동작의 source of truth는 각 서브모듈이 직접 소유한다.

## Source Of Truth 순서

1. 이 문서: cross-repo 공통 규약
2. `git-ranker/CLAUDE.md`: backend 작업 규약 (TDD 스킬 포함)
3. `git-ranker-client/CLAUDE.md`: frontend 작업 규약
4. 각 저장소의 코드, 테스트, CI 설정: 실제 앱 동작

앱 동작을 복제한 prose 문서를 이 저장소에 두지 않는다. 앱 계약을 바꾸는 변경은 해당 서브모듈의 문서와 테스트를 함께 갱신한다.

## 작업 원칙

- 비자명한 구현 작업은 Plan 모드로 계획을 세우고 사용자 승인 후 구현한다.
- 요구사항이 모호하면 구현 전에 AskUserQuestion으로 해소한다. 추측으로 범위를 넓히지 않는다.
- 구현 코드 변경에는 대응하는 테스트 변경을 함께 제출한다(`git-ranker`는 JUnit, `git-ranker-client`는 vitest 순수 로직 단위 테스트 — 컴포넌트/E2E는 미도입). 테스트 harness가 없는 영역(예: 프런트 UI 컴포넌트)은 테스트를 생략하고 그 근거를 커밋/PR에 명시한다.
- 작업 완료 보고 전에 해당 저장소의 검증 베이스라인을 통과시킨다.

## 검증 베이스라인

- `git-ranker`: `./gradlew test` → `./gradlew build`
- `git-ranker-client`: `npm run lint` → `npm run typecheck` → `npm run test` → `npm run build` (자세한 계약은 `git-ranker-client/docs/verification-contract.md`)

## Git 규약

- 커밋 메시지는 루트의 `.gitmessage.ko.txt` 형식을 따른다.
- 서브모듈은 독립 저장소다. 서브모듈 변경은 서브모듈에서 먼저 커밋하고, 루트에서 gitlink를 갱신한다.
- NEVER: force push, `git reset --hard`, `rm -rf` 등 destructive 명령을 사용자 확인 없이 실행하지 않는다. (`.claude/hooks/block-dangerous.sh`가 세션 내에서 차단한다.)
- push는 사용자가 요청했을 때만 수행한다.

## Harness 구조

- `.claude/settings.json` + `.claude/hooks/`: 위험 명령 차단 훅 (PreToolUse)
- `docs/README.md`: harness 구조 설명
- `git-ranker/docs/`: STRUCTURE(패키지 구조), DEVELOPMENT(로컬 개발), OPERATIONS(배포·모니터링)
- `git-ranker/.claude/skills/`: TDD 프로세스 스킬(`red`→`green`→`refactor`) + ECC 선별 지식 스킬(Spring Boot/JPA/Security 등)
- `git-ranker/.githooks/pre-commit`: 구현-테스트 동반 커밋 검사 (활성화: `git config core.hooksPath .githooks`)
- `git-ranker-client/docs/`: STRUCTURE(3계층 구조), CONVENTIONS(코드 규약), verification-contract(검증 계약)
- `git-ranker-client/.claude/skills/`: ECC 선별 지식 스킬(React/Next.js/성능/접근성)

## Workflow 오케스트레이션

이 저장소는 요구사항을 FE/BE로 분배하는 오케스트레이터다. 상세 구현 계획은 각 서브모듈의 Plan 모드가 담당하고, 여기서는 역할별 작업 범위만 나눠 GitHub 이슈로 넘긴다. 세 세션이 GitHub 이슈로만 연결된다(로컬 상태 없음).

- `/dispatch <요구사항>`: Plan 모드+AskUserQuestion으로 FE/BE 범위 분해 → 미리보기 승인 → `gh`로 루트 추적 이슈 + 각 서브모듈 이슈 생성. 절차는 `.claude/skills/workflow-dispatch`가 소유한다.
- 각 서브모듈: 자기 이슈를 진입점으로 Plan 모드 → 구현 → PR → merge (각 레포 harness).
- `/sync [추적이슈]`: 머지된 서브모듈 gitlink를 `develop` 최신으로 반영하고 추적 이슈를 닫는다. 절차는 `.claude/skills/workflow-sync`가 소유한다.
- 이슈 형식은 세 저장소 공통 통합 템플릿(`task.yml` / 루트 `tracking.yml`)을 쓴다. 작업 종류(기능/버그/리팩토링/간단한 수정)를 work-type 필드로 흡수한다.
- 서브모듈 remote org는 `alexization`, 추적 브랜치는 `develop`.
