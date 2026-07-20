# Workflow 오케스트레이션: 분해 → dispatch → 반영 설계

- 작성일: 2026-07-20
- 대상 저장소: `git-ranker-workflow` (루트 umbrella) + 서브모듈 이슈 템플릿
- 상태: 설계 승인됨 (구현 계획 수립 전)

## Context

`git-ranker-workflow`는 backend(`git-ranker`)와 frontend(`git-ranker-client`) 서브모듈을 묶는 umbrella 저장소로, "요구사항을 받아 역할별로 작업을 나눠 각 레포에 지시하는 오케스트레이터"로 설계되었다. 그러나 현재 루트 레포에는 이 오케스트레이션을 수행하는 **실행 가능한 메커니즘이 없다.** 존재하는 것은 (1) `CLAUDE.md`/`docs/README.md`의 prose 규약, (2) 위험 명령 차단 훅(`block-dangerous.sh`), (3) 이슈/PR 템플릿뿐이다. 직전 커밋(`1e52772`)에서 Codex 기반 단일-레포 상태 기계를 걷어내며 "요구사항 정리·계획 승인은 Plan 모드/AskUserQuestion이 담당한다"로 방향을 잡았지만, **FE/BE 분해 + 각 서브모듈 Issue 생성 + 결과 반영**이라는 핵심 흐름은 어느 버전에서도 구현된 적이 없다.

또한 각 서브모듈의 기존 이슈 템플릿(`engineering_task.yml`, `bug_report.yml`, `feature_request.yml`)은 레거시 잔재로, 작업 유형별로 흩어져 있고 "각 레포가 무슨 작업을 해야 하는지"를 일관되게 전달하지 못한다.

이 설계는 그 격차를 메운다. workflow의 역할은 **상세 구현 계획 수립이 아니라 "역할별 작업 범위 분해 + 각 레포로의 핸드오프 + 머지 후 반영"** 이며, 상세 구현 계획은 각 서브모듈이 자신의 harness와 Plan 모드로 독립 수행한다. 핸드오프의 매개는 **작업 종류(기능/버그/간단한 수정/리팩토링)를 가리지 않는 통합 이슈 템플릿** 하나로 통일한다.

## Goals

- 루트에서 요구사항을 받아 Plan 모드 + AskUserQuestion으로 FE/BE 작업 범위를 분해한다.
- 작업 종류(feature/bug/refactor/chore 등)와 무관하게 "무엇을 해야 하는지"를 명확히 전달하는 **통합 단일 이슈 템플릿**을 정의하고, dispatch 본문과 각 서브모듈 폼을 모두 이 구조로 통일한다(레거시 3종 템플릿 대체).
- 분해 결과를 각 서브모듈의 GitHub Issue로 자동 생성(`gh`)하고, 요구사항 전체를 대표하는 루트 추적 이슈로 묶는다.
- 각 서브모듈은 자신의 Issue를 진입점으로 기존 실행 harness에서 독립적으로 작업한다.
- 두 PR이 머지되면 루트에서 gitlink를 갱신해 결과를 반영하고, 추적 이슈로 루프를 닫는다.
- 이 과정을 슬래시 커맨드 + 스킬로 코드화해 반복 재현 가능하게 한다.

## Non-Goals

- 상세 구현 계획 수립 (각 서브모듈의 Plan 모드가 담당).
- FE/BE 공유 API 계약의 확정 (각 레포 재량; workflow는 범위만 분리하고 두 이슈를 상호 링크).
- 삭제된 것과 같은 로컬 JSON 상태 기계/spec 승인 상태 기계의 재도입 (GitHub이 source of truth).
- 서브모듈의 **실행** harness(스킬, docs, CI, `red/green/refactor` 등) 변경 — 이번 스코프는 이슈 템플릿 통일까지다.
- 프론트엔드 테스트 러너 도입, 백엔드 pre-commit 훅 자동 활성화 (독립 후속 과제; 아래 "스코프에서 제외" 참조).

## 핵심 설계 결정 (승인됨)

| 결정 | 선택 | 근거 |
|---|---|---|
| 핸드오프 방식 | Claude가 `gh issue create --repo`로 각 서브모듈에 Issue 자동 생성 | Plan 모드 승인 후 사람 개입 최소화, 각 레포 진입점이 GitHub Issue로 통일 |
| 계약/의존 | workflow는 **범위만 분리** + 두 이슈 상호 링크, 계약은 각 레포 재량 | workflow 부담 최소화, 프론트의 기존 수동 미러링 절차가 divergence 흡수 |
| 코드화 | 루트 `.claude/commands/` 슬래시 커맨드 + `.claude/skills/` 스킬 | 각 서브모듈 harness 철학과 일관, 반복 재현성 |
| 머지 반영 | 가벼운 `/sync` 커맨드로 gitlink 갱신까지 포함 | 루프를 닫아 "결과가 workflow에 반영" 요건 충족 |
| dispatch↔sync 연결 | **루트 추적 이슈를 원장(ledger)으로** | GitHub이 source of truth, 로컬 상태 없음, 요구사항 전체가 한 곳에 |
| 이슈 템플릿 | **통합 단일 템플릿**(work-type 필드 포함)으로 통일, dispatch 본문 + 서브모듈 폼 모두 교체, 레거시 3종 정리 | 작업 종류 무관하게 "무엇을 할지" 일관 전달, 사람·workflow 생성 이슈 동일 구조 |

## 아키텍처 — GitHub을 조율 substrate로 삼는 3-세션 흐름

세 개의 독립 Claude Code 세션이 GitHub Issue로만 연결된다(공유 로컬 상태 없음).

```
[루트 workflow 세션]  /dispatch
  요구사항 → Plan모드+AskUserQuestion으로 FE/BE 범위 분해 → 승인 → 미리보기
  → gh로 ① 루트 추적 이슈 1개  ② 각 서브모듈 이슈 생성 (통합 템플릿, 상호 링크)
       │
       ├──▶ [git-ranker 세션]        이슈 읽고 Plan모드 → TDD 구현 → PR → merge
       └──▶ [git-ranker-client 세션] 이슈 읽고 Plan모드 → 구현 → PR → merge
       │
[루트 sync 세션]  /sync
  추적 이슈 읽음 → 두 서브모듈 PR 머지 상태 확인
  → 머지된 서브모듈 gitlink 갱신 → 루트 커밋 초안 → 추적 이슈 체크박스 갱신
```

가운데(서브모듈 실행)의 스킬·docs·CI 등 **실행 harness는 변경 대상이 아니나, 이슈 템플릿은 통합 구조로 교체**한다. 신규 커맨드·스킬은 전부 루트에, 템플릿 교체는 루트 추적 이슈 폼 + 두 서브모듈 폼에 걸친다.

## Components

### 루트 `git-ranker-workflow`

| 파일 | 유형 | 역할 |
|---|---|---|
| `.claude/commands/dispatch.md` | 신규 | `/dispatch` 진입점. 요구사항 → 분해 스킬 호출 → 미리보기 → gh 이슈 생성 안내 |
| `.claude/commands/sync.md` | 신규 | `/sync` 진입점. 추적 이슈 기반 머지 반영 |
| `.claude/skills/workflow-dispatch/SKILL.md` | 신규 | 분해 절차 + 통합 이슈 본문 작성 지식(아래 상세) |
| `.claude/skills/workflow-sync/SKILL.md` | 신규 | merge-back 절차 지식(아래 상세) |
| `.github/ISSUE_TEMPLATE/tracking.yml` | 신규 | 루트 추적 이슈 폼(수동 생성 대비; dispatch는 gh로 본문 직접 작성) |
| `CLAUDE.md` | 갱신 | workflow 정체성·3-세션 흐름·커맨드 사용법·통합 템플릿 규약 명문화 |
| `.gitignore` | 갱신 | stale `workflows/system/circuit-breaker.json` 참조 제거 |
| `.pytest_cache/` | 삭제 | refactor 잔재 정리 |

### 서브모듈 (각 레포에서 커밋 후 루트 gitlink 반영)

| 파일 | 유형 | 역할 |
|---|---|---|
| `git-ranker/.github/ISSUE_TEMPLATE/task.yml` | 신규 | 통합 단일 이슈 폼(백엔드 인스턴스) |
| `git-ranker/.github/ISSUE_TEMPLATE/{engineering_task,bug_report,feature_request}.yml` | 삭제 | 레거시 3종 정리 |
| `git-ranker-client/.github/ISSUE_TEMPLATE/task.yml` | 신규 | 통합 단일 이슈 폼(프론트 인스턴스) |
| `git-ranker-client/.github/ISSUE_TEMPLATE/{engineering_task,bug_report,feature_request}.yml` | 삭제 | 레거시 3종 정리 |

각 서브모듈의 `config.yml`(`blank_issues_enabled: false`, 보안 신고 링크)은 유지한다. 서브모듈 변경은 서브모듈에서 먼저 커밋하고 루트에서 gitlink를 갱신한다.

### `workflow-dispatch` 스킬이 담는 지식

- **FE/BE 경계 판별 체크리스트**: 요구사항의 어느 부분이 API/도메인/배치/영속성(BE)인지, UI/라우팅/상태/접근성(FE)인지 가르는 질문 목록. 애매하면 AskUserQuestion으로 확정.
- **통합 이슈 본문 작성**: 부록 A의 통합 템플릿 구조(작업 유형 / 배경·문제 / 작업 내용 / 재현 상세(버그 시) / 작업 범위 / 완료 조건 / 검증 방법 / 리스크·의존·연관)를 본문 마크다운으로 작성. `gh issue create`는 이슈 폼을 자동 채우지 않으므로 동일 섹션 구조를 본문으로 재현한다.
- **레포별 인스턴스 값**: 작업 유형 옵션, 작업 범위 힌트, 검증 방법을 레포별로 채운다.
  - BE(`git-ranker`): 검증 `./gradlew test` → `./gradlew build -x test`
  - FE(`git-ranker-client`): 검증 `npm run lint` → `npm run typecheck` → `npm run build` + 브라우저 QA (테스트 러너 없음 → `test` 유형/검증 미사용)
- **제목 규칙**: `--title "[<work_type>] <요약>"` (예: `[bug] 랭킹 갱신 누락`).
- **gh 명령 템플릿**: `gh issue create --repo alexization/<repo> --title "..." --body-file <tmp> --label task,triage`.
- **추적 이슈 포맷** 및 **상호 링크 규칙**(아래 데이터 흐름 참조).
- **미리보기 게이트**: 실제 생성 전 이슈 본문 초안과 gh 명령을 사용자에게 보여주고 승인받는다.

### `workflow-sync` 스킬이 담는 지식

- 추적 이슈 파싱(체크리스트에서 서브모듈 이슈 번호 추출).
- `gh`로 각 서브모듈 이슈에 연결된 PR의 머지 상태 확인.
- gitlink 갱신 절차(아래 상세)와 안전장치.
- 부분 진행 처리(한쪽만 머지되면 그쪽만 반영).

## 데이터 흐름 — 추적 이슈 포맷

루트 추적 이슈 본문:

```
## 요구사항
<요약>

## 역할 분해
### Backend (git-ranker) — 이슈 alexization/git-ranker#N
- 범위: ...
### Frontend (git-ranker-client) — 이슈 alexization/git-ranker-client#M
- 범위: ...

## 완료 추적
- [ ] BE 머지 (git-ranker#N)
- [ ] FE 머지 (git-ranker-client#M)
- [ ] gitlink 반영 (루트 커밋)
```

각 서브모듈 이슈 본문 상단에 역참조를 삽입한다:

```
> 상위 추적: alexization/git-ranker-workflow#T
> 연관: alexization/<상대 레포>#<번호>
```

한쪽 역할만 필요한 요구사항이면 그쪽 서브모듈 이슈만 생성하되, 추적 이슈는 일관성을 위해 생성한다(해당 없는 역할은 "N/A"로 표기).

## gitlink 갱신 절차 (sync) — destructive 규약 준수

1. 서브모듈에서 `git -C <sub> fetch`.
2. 머지된 커밋으로 이동: `git submodule update --remote <sub>` 또는 `git -C <sub> checkout <merge-sha>`.
   - 파일 discard용 `git checkout --`가 아닌 브랜치/커밋 checkout만 사용(`block-dangerous.sh`와 정합).
3. 루트에서 `git add <sub>` → `.gitmessage.ko.txt` 형식으로 커밋 초안.
4. **push는 사용자가 요청했을 때만** 수행.

안전장치:
- 서브모듈에 uncommitted 변경이 있으면 중단하고 사용자에게 보고(임의 덮어쓰기 금지).
- `git reset --hard`, force push 등 destructive 명령 사용 금지(`block-dangerous.sh`가 세션 내 차단).

## 에러 처리 / 부분 진행

- **dispatch**
  - 범위가 애매하면 AskUserQuestion으로 확정한 뒤에만 이슈 생성.
  - 미리보기 승인 없이는 gh 실행 금지.
  - gh 실패 시 이미 생성된 이슈를 보고하고 재시도/수동 보정 안내(부분 생성 상태를 숨기지 않음).
  - `gh auth status` 미인증 시 명확히 안내.
- **sync**
  - 아직 머지되지 않은 PR은 skip하고 상태만 보고.
  - 한쪽만 머지된 부분 진행 지원(머지된 쪽만 gitlink 갱신, 추적 이슈 체크박스 부분 갱신).
  - 두 서브모듈 모두 머지·반영되면 추적 이슈를 닫는다(사용자 확인 후).

## 검증 방법

루트는 앱 코드가 아니라 harness 문서·커맨드·스킬이므로 유닛 테스트 대상이 아니다. 대신:

1. **dry-run 리허설**: 샘플 요구사항으로 `/dispatch`를 실행해 이슈 본문 초안이 통합 템플릿 규격대로 나오고 gh 명령의 repo/제목/라벨/본문 구조가 올바른지 미리보기 단계에서 확인(실제 생성 전).
2. **템플릿 유효성**: 새 `task.yml` 폼이 GitHub 이슈 폼 문법에 맞는지, 레거시 3종 삭제 후 각 서브모듈에서 이슈 생성 UI가 통합 템플릿 하나만 노출하는지 확인.
3. **훅 정합성**: `block-dangerous.sh`가 sync의 gitlink 명령(브랜치/커밋 checkout, `submodule update`)을 오차단하지 않는지 확인.
4. **문서 정합성**: 스킬에 dangling reference 없음, `CLAUDE.md` 서사와 실제 커맨드/스킬/템플릿이 일치.
5. **위생**: 잔재 제거 후 `git status`가 깨끗하고 `.gitignore`에 stale 참조가 없는지 확인.

## 스코프에서 제외 (독립 후속 과제)

- 프론트엔드 테스트 러너(vitest/Playwright) 도입 및 verification-contract에 test 단계 추가.
- 백엔드 `.githooks/pre-commit` 자동 활성화.
- 이 항목들은 dispatch 설계와 독립이며, dispatch는 "검증 방법 정합성"으로 각 레포의 현재 계약을 존중해 우회한다. (프론트 통합 템플릿에서 `test` 유형/검증을 쓰지 않음.)

## 부록 A: 통합 이슈 템플릿

작업 종류(feature/bug/refactor/chore 등)와 무관하게 "무엇을 해야 하는지"를 전달하는 단일 구조다. 같은 구조를 (1) 각 서브모듈 GitHub 이슈 폼(`task.yml`), (2) dispatch가 `gh --body-file`로 넘기는 본문 마크다운 양쪽에 적용한다.

### A-1. 통합 이슈 폼 (`task.yml`, 서브모듈)

레포별로 `<work_type 옵션>`, `<작업 범위 힌트>`, `<검증 명령>`만 인스턴스화한다.

```yaml
name: "📋 작업 (Work Item)"
description: 기능·버그·리팩토링·간단한 수정 등 모든 작업을 하나의 형식으로 기록합니다.
title: "[작업] "
labels: ["task", "triage"]
body:
  - type: dropdown
    id: work_type
    attributes:
      label: 작업 유형
      options: [feature, bug, refactor, chore, performance, docs]   # BE는 +security/observability, FE는 +accessibility
    validations: { required: true }
  - type: textarea
    id: background
    attributes:
      label: 배경 / 문제
      description: 이 작업이 필요한 이유. 버그면 증상, 기능이면 필요, 리팩토링이면 현재 구조의 문제.
    validations: { required: true }
  - type: textarea
    id: what
    attributes:
      label: 작업 내용 / 기대 결과
      description: 무엇을 해야 하는지와 완료 후 기대 동작.
    validations: { required: true }
  - type: textarea
    id: bug_detail
    attributes:
      label: 재현 절차 / 기대 vs 실제 (버그인 경우)
      placeholder: |
        재현: 1) ... 2) ...
        기대: ...
        실제: ...
    validations: { required: false }
  - type: textarea
    id: scope
    attributes:
      label: 작업 범위
      placeholder: |
        <BE: - `domain/...` / - `global/...` / - `src/test/...`>
        <FE: - route: / - component: / - hook/store:>
    validations: { required: true }
  - type: textarea
    id: done
    attributes:
      label: 완료 조건
      placeholder: |
        - [ ] ...
        - [ ] ...
    validations: { required: true }
  - type: textarea
    id: validation
    attributes:
      label: 검증 방법
      placeholder: |
        <BE: - `./gradlew test` / - `./gradlew build -x test`>
        <FE: - `npm run lint` / - `npm run typecheck` / - `npm run build` / - 브라우저 QA>
    validations: { required: true }
  - type: textarea
    id: links
    attributes:
      label: 리스크 / 의존성 / 연관
      placeholder: |
        - 리스크:
        - 의존성(상대 레포 이슈):
        - 상위 추적:
    validations: { required: false }
```

### A-2. dispatch 본문 마크다운 (gh `--body-file`)

폼과 동일 섹션을 마크다운으로 재현하고, 상단에 추적/연관 역참조를 넣는다. 버그가 아니면 "재현 절차" 섹션은 생략한다.

```markdown
> 상위 추적: alexization/git-ranker-workflow#<T>
> 연관: alexization/<상대 레포>#<번호>

## 작업 유형
<feature | bug | refactor | chore | performance | docs | (BE) security/observability | (FE) accessibility>

## 배경 / 문제
<이유. 버그면 증상 요약>

## 작업 내용 / 기대 결과
<무엇을 / 완료 후 기대 동작>

## 재현 절차 / 기대 vs 실제   ← 버그일 때만
재현: 1) ... 2) ...
기대: ...
실제: ...

## 작업 범위
<BE: `domain/...`, `src/test/...`   |   FE: route/component/hook·store>

## 완료 조건
- [ ] ...
- [ ] ...

## 검증 방법
<BE: `./gradlew test`, `./gradlew build -x test`   |   FE: `npm run lint`, `npm run typecheck`, `npm run build`, 브라우저 QA>

## 리스크 / 의존성 / 연관
- 리스크:
- 의존성(상대 레포 이슈):
- 상위 추적:
```

### A-3. 루트 추적 이슈 (`tracking.yml`)

"데이터 흐름 — 추적 이슈 포맷" 섹션의 포맷을 폼(요구사항 / 역할 분해 / 완료 추적)으로 재현한다. dispatch는 이 구조의 본문을 gh로 생성한다.

**링크 순서 규칙**: 서브모듈 이슈를 먼저 생성해 번호(`#N`,`#M`)를 확보한 뒤 추적 이슈를 만들거나, 추적 이슈를 먼저 만들어 `#T`를 확보한 뒤 서브모듈 이슈에 역참조를 넣는다. 어느 순서든 생성 직후 나머지 본문/체크리스트를 `gh issue edit`으로 링크 보정한다.

### 확정 사항 (리뷰 완료)

- 레거시 `bug_report.yml`/`feature_request.yml`이 겸하던 외부 신고 창구는 **별도로 남기지 않는다.** 통합 `task.yml` 하나로 대체하며, 외부 신고자도 동일 폼을 사용한다.
- 서브모듈 remote org는 `alexization`, 머지 대상 및 gitlink 추적 브랜치는 `develop`.
