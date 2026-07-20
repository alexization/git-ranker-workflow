# Workflow 오케스트레이션 (분해 → dispatch → 반영) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 루트 `git-ranker-workflow`에 요구사항을 FE/BE 작업으로 분해해 각 서브모듈에 GitHub 이슈를 생성하고(`/dispatch`), 머지 후 gitlink를 반영하는(`/sync`) 오케스트레이션 harness를 추가하고, 작업 종류를 가리지 않는 통합 이슈 템플릿으로 세 저장소를 통일한다.

**Architecture:** 세 개의 독립 Claude Code 세션(루트 dispatch / 각 서브모듈 실행 / 루트 sync)이 GitHub 이슈만으로 연결된다. 로컬 상태 기계 없이 루트 추적 이슈를 원장으로 삼는다. 신규 커맨드·스킬은 전부 루트에, 통합 이슈 템플릿은 루트 추적 폼 + 두 서브모듈 폼에 적용한다.

**Tech Stack:** Claude Code slash commands(`.claude/commands/*.md`) + skills(`.claude/skills/*/SKILL.md`), GitHub 이슈 폼(YAML), `gh` CLI, git submodule.

**참조 스펙:** `docs/superpowers/specs/2026-07-20-workflow-orchestration-dispatch-design.md`

## Global Constraints

- 커밋 메시지는 `.gitmessage.ko.txt` 형식 `<type>: <핵심 작업 내용>`, 전체 한국어, 마침표 생략. 사용 type: feat, fix, docs, refactor, test, chore, perf, build, ci, revert.
- push는 사용자가 요청했을 때만 수행한다. 서브모듈을 push할 때는 서브모듈 먼저, 루트 나중.
- destructive 명령(`rm -rf`, `git reset --hard`, force push 등) 금지 — `.claude/hooks/block-dangerous.sh`가 세션 내 차단한다. 파일 삭제는 `git rm`, 디렉터리 정리는 `rm -r`(‑f 없이) 사용.
- 서브모듈은 독립 저장소다. 서브모듈 변경은 서브모듈에서 먼저 커밋하고, 루트에서 gitlink를 갱신한다.
- 서브모듈 remote org: `alexization`. 머지 대상 및 gitlink 추적 브랜치: `develop`.
- 스킬 파일(`SKILL.md`)은 YAML frontmatter에 `name`, `description`이 필수다.
- YAML 유효성 검증은 ruby 사용: `ruby -ryaml -e "YAML.load_file('<path>'); puts 'valid'"` → 기대 출력 `valid`.
- GitHub 이슈 폼의 `labels`는 해당 저장소에 라벨이 존재해야 적용된다. 없으면 `gh label create`로 만든다.

---

## 통합 이슈 템플릿 구조 (Task 1·2·4에서 재사용)

세 저장소가 공유하는 섹션 구조: 작업 유형 / 배경·문제 / 작업 내용·기대 결과 / 재현 절차(버그 시) / 작업 범위 / 완료 조건 / 검증 방법 / 리스크·의존·연관. 레포별로 `작업 유형 옵션`, `작업 범위 힌트`, `검증 명령`만 다르다.

---

### Task 1: 백엔드 통합 이슈 템플릿 (`git-ranker` 서브모듈)

**Files:**
- Create: `git-ranker/.github/ISSUE_TEMPLATE/task.yml`
- Delete: `git-ranker/.github/ISSUE_TEMPLATE/engineering_task.yml`, `git-ranker/.github/ISSUE_TEMPLATE/bug_report.yml`, `git-ranker/.github/ISSUE_TEMPLATE/feature_request.yml`
- Keep: `git-ranker/.github/ISSUE_TEMPLATE/config.yml`

**Interfaces:**
- Produces: `task` 라벨을 쓰는 백엔드 작업 이슈 폼. dispatch 본문(Task 5)과 동일 섹션 구조.

- [ ] **Step 1: 통합 폼 파일 작성**

Create `git-ranker/.github/ISSUE_TEMPLATE/task.yml`:

```yaml
name: "📋 작업 (Work Item)"
description: 기능·버그·리팩토링·간단한 수정 등 모든 백엔드 작업을 하나의 형식으로 기록합니다.
title: "[작업] "
labels: ["task", "triage"]
body:
  - type: dropdown
    id: work_type
    attributes:
      label: 작업 유형
      options:
        - feature
        - bug
        - refactor
        - chore
        - performance
        - security
        - observability
        - docs
    validations:
      required: true
  - type: textarea
    id: background
    attributes:
      label: 배경 / 문제
      description: 이 작업이 필요한 이유. 버그면 증상, 기능이면 필요, 리팩토링이면 현재 구조의 문제.
    validations:
      required: true
  - type: textarea
    id: what
    attributes:
      label: 작업 내용 / 기대 결과
      description: 무엇을 해야 하는지와 완료 후 기대 동작.
    validations:
      required: true
  - type: textarea
    id: bug_detail
    attributes:
      label: 재현 절차 / 기대 vs 실제 (버그인 경우)
      placeholder: |
        재현: 1) ... 2) ...
        기대: ...
        실제: ...
    validations:
      required: false
  - type: textarea
    id: scope
    attributes:
      label: 작업 범위
      placeholder: |
        - `domain/ranking`
        - `global/logging`
        - `src/test/...`
    validations:
      required: true
  - type: textarea
    id: done
    attributes:
      label: 완료 조건
      placeholder: |
        - [ ] ...
        - [ ] ...
    validations:
      required: true
  - type: textarea
    id: validation
    attributes:
      label: 검증 방법
      placeholder: |
        - `./gradlew test`
        - `./gradlew build -x test`
        - 로그/메트릭 확인
    validations:
      required: true
  - type: textarea
    id: links
    attributes:
      label: 리스크 / 의존성 / 연관
      placeholder: |
        - 리스크:
        - 의존성(상대 레포 이슈):
        - 상위 추적:
    validations:
      required: false
```

- [ ] **Step 2: 레거시 3종 삭제 스테이징**

Run:
```bash
git -C git-ranker rm .github/ISSUE_TEMPLATE/engineering_task.yml .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/feature_request.yml
```
Expected: `rm '.github/ISSUE_TEMPLATE/...'` 3줄.

- [ ] **Step 3: 폼 YAML 유효성 + 잔여 파일 확인**

Run:
```bash
ruby -ryaml -e "YAML.load_file('git-ranker/.github/ISSUE_TEMPLATE/task.yml'); puts 'valid'" && ls git-ranker/.github/ISSUE_TEMPLATE/
```
Expected: `valid` 다음 줄에 `config.yml  task.yml` (레거시 3종 없음).

- [ ] **Step 4: 서브모듈에서 커밋**

```bash
git -C git-ranker add .github/ISSUE_TEMPLATE/task.yml
git -C git-ranker commit -m "chore: 통합 작업 이슈 템플릿으로 정리" -m "- work-type 필드로 기능/버그/리팩토링/간단한 수정 통합
- 레거시 engineering_task/bug_report/feature_request 제거"
```
Expected: 4 files changed (1 create, 3 delete).

---

### Task 2: 프론트엔드 통합 이슈 템플릿 (`git-ranker-client` 서브모듈)

**Files:**
- Create: `git-ranker-client/.github/ISSUE_TEMPLATE/task.yml`
- Delete: `git-ranker-client/.github/ISSUE_TEMPLATE/engineering_task.yml`, `.../bug_report.yml`, `.../feature_request.yml`
- Keep: `git-ranker-client/.github/ISSUE_TEMPLATE/config.yml`

**Interfaces:**
- Produces: `task` 라벨을 쓰는 프론트 작업 이슈 폼. 백엔드와 동일 구조이나 `작업 유형`에 `testing` 없음(러너 부재), 검증은 npm 명령.

- [ ] **Step 1: 통합 폼 파일 작성**

Create `git-ranker-client/.github/ISSUE_TEMPLATE/task.yml`:

```yaml
name: "📋 작업 (Work Item)"
description: 기능·버그·리팩토링·간단한 수정 등 모든 프론트엔드 작업을 하나의 형식으로 기록합니다.
title: "[작업] "
labels: ["task", "triage"]
body:
  - type: dropdown
    id: work_type
    attributes:
      label: 작업 유형
      options:
        - feature
        - bug
        - ui-refactor
        - chore
        - performance
        - accessibility
        - docs
    validations:
      required: true
  - type: textarea
    id: background
    attributes:
      label: 배경 / 문제
      description: 이 작업이 필요한 이유. 버그면 증상, 기능이면 필요, 리팩토링이면 현재 구조의 문제.
    validations:
      required: true
  - type: textarea
    id: what
    attributes:
      label: 작업 내용 / 기대 결과
      description: 무엇을 해야 하는지와 완료 후 기대 동작.
    validations:
      required: true
  - type: textarea
    id: bug_detail
    attributes:
      label: 재현 절차 / 기대 vs 실제 (버그인 경우)
      placeholder: |
        재현: 1) ... 2) ...
        기대: ...
        실제: ...
    validations:
      required: false
  - type: textarea
    id: scope
    attributes:
      label: 작업 범위
      placeholder: |
        - route:
        - component:
        - hook/store:
    validations:
      required: true
  - type: textarea
    id: done
    attributes:
      label: 완료 조건
      placeholder: |
        - [ ] ...
        - [ ] ...
    validations:
      required: true
  - type: textarea
    id: validation
    attributes:
      label: 검증 방법
      placeholder: |
        - `npm run lint`
        - `npm run typecheck`
        - `npm run build`
        - 스크린샷 / 브라우저 QA
    validations:
      required: true
  - type: textarea
    id: links
    attributes:
      label: 리스크 / 의존성 / 연관
      placeholder: |
        - 리스크:
        - 백엔드 의존성:
        - 상위 추적:
    validations:
      required: false
```

- [ ] **Step 2: 레거시 3종 삭제 스테이징**

Run:
```bash
git -C git-ranker-client rm .github/ISSUE_TEMPLATE/engineering_task.yml .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/feature_request.yml
```
Expected: `rm '.github/ISSUE_TEMPLATE/...'` 3줄.

- [ ] **Step 3: 폼 YAML 유효성 + 잔여 파일 확인**

Run:
```bash
ruby -ryaml -e "YAML.load_file('git-ranker-client/.github/ISSUE_TEMPLATE/task.yml'); puts 'valid'" && ls git-ranker-client/.github/ISSUE_TEMPLATE/
```
Expected: `valid` 다음 줄에 `config.yml  task.yml`.

- [ ] **Step 4: 서브모듈에서 커밋**

```bash
git -C git-ranker-client add .github/ISSUE_TEMPLATE/task.yml
git -C git-ranker-client commit -m "chore: 통합 작업 이슈 템플릿으로 정리" -m "- work-type 필드로 기능/버그/리팩토링/간단한 수정 통합
- 레거시 engineering_task/bug_report/feature_request 제거"
```
Expected: 4 files changed (1 create, 3 delete).

---

### Task 3: 서브모듈 gitlink 반영 (루트)

**Files:**
- Modify (gitlink): `git-ranker`, `git-ranker-client` 포인터

**Interfaces:**
- Consumes: Task 1·2의 서브모듈 커밋 SHA.

- [ ] **Step 1: gitlink 변경 스테이징**

Run:
```bash
git add git-ranker git-ranker-client
git status --short
```
Expected: `M git-ranker` `M git-ranker-client` (두 gitlink 갱신).

- [ ] **Step 2: 서브모듈 포인터가 새 커밋을 가리키는지 확인**

Run:
```bash
git diff --cached --submodule=log
```
Expected: 두 서브모듈 모두 `> chore: 통합 작업 이슈 템플릿으로 정리` 라인이 보인다.

- [ ] **Step 3: 커밋**

```bash
git commit -m "chore: 서브모듈 통합 이슈 템플릿 gitlink 반영"
```
Expected: 2 files changed.

---

### Task 4: 루트 요구사항 추적 이슈 템플릿 (`tracking.yml`)

**Files:**
- Create: `.github/ISSUE_TEMPLATE/tracking.yml`

**Interfaces:**
- Produces: `tracking` 라벨을 쓰는 추적 이슈 폼(요구사항 / 역할 분해 / 완료 추적). sync(Task 6)가 이 구조를 파싱한다.

- [ ] **Step 1: 추적 폼 파일 작성**

Create `.github/ISSUE_TEMPLATE/tracking.yml`:

```yaml
name: "🧭 요구사항 추적 (Tracking)"
description: 하나의 요구사항을 FE/BE 작업으로 분해해 추적합니다. 보통 /dispatch가 자동 생성합니다.
title: "[추적] "
labels: ["tracking"]
body:
  - type: textarea
    id: requirement
    attributes:
      label: 요구사항
      description: 전체 요구사항 요약.
    validations:
      required: true
  - type: textarea
    id: breakdown
    attributes:
      label: 역할 분해
      placeholder: |
        ### Backend (git-ranker) — 이슈 alexization/git-ranker#N
        - 범위: ...
        ### Frontend (git-ranker-client) — 이슈 alexization/git-ranker-client#M
        - 범위: ...
    validations:
      required: true
  - type: textarea
    id: tracking
    attributes:
      label: 완료 추적
      placeholder: |
        - [ ] BE 머지 (git-ranker#N)
        - [ ] FE 머지 (git-ranker-client#M)
        - [ ] gitlink 반영 (루트 커밋)
    validations:
      required: true
```

- [ ] **Step 2: YAML 유효성 확인**

Run:
```bash
ruby -ryaml -e "YAML.load_file('.github/ISSUE_TEMPLATE/tracking.yml'); puts 'valid'"
```
Expected: `valid`.

- [ ] **Step 3: 루트에 `tracking` 라벨 보장**

Run:
```bash
gh label list --repo alexization/git-ranker-workflow | grep -q '^tracking' || gh label create tracking --repo alexization/git-ranker-workflow --color 0E8A16 --description "요구사항 추적 이슈"
gh label list --repo alexization/git-ranker-workflow | grep tracking
```
Expected: `tracking` 라벨이 출력된다. (gh 미인증 시 `gh auth status`로 안내 후 중단.)

- [ ] **Step 4: 커밋**

```bash
git add .github/ISSUE_TEMPLATE/tracking.yml
git commit -m "feat: 루트 요구사항 추적 이슈 템플릿 추가"
```
Expected: 1 file changed.

---

### Task 5: `workflow-dispatch` 스킬

**Files:**
- Create: `.claude/skills/workflow-dispatch/SKILL.md`

**Interfaces:**
- Produces: `/dispatch` 커맨드(Task 7)가 호출하는 분해·이슈생성 절차 지식.

- [ ] **Step 1: 스킬 파일 작성**

Create `.claude/skills/workflow-dispatch/SKILL.md`:

````markdown
---
name: workflow-dispatch
description: 하나의 요구사항을 FE(git-ranker-client)/BE(git-ranker) 작업 범위로 분해해 각 서브모듈에 GitHub 이슈를 생성하고 루트 추적 이슈로 묶을 때 사용한다. 상세 구현 계획은 세우지 않고 역할별 범위만 나눈다.
---

# Workflow Dispatch

요구사항을 받아 **역할별 작업 범위로 분해**하고 각 서브모듈에 GitHub 이슈를 생성한다. 상세 구현 계획은 각 서브모듈의 Plan 모드가 담당하므로, 여기서는 "무엇을/어디까지"만 정한다.

## 절차

1. **분해 (Plan 모드 + AskUserQuestion)**: 요구사항을 아래 경계 기준으로 FE/BE로 나눈다. 애매하면 AskUserQuestion으로 확정한 뒤 진행한다.
2. **본문 작성**: 각 이슈 본문을 아래 템플릿으로 작성한다(레포별 값 인스턴스화).
3. **미리보기 게이트**: 생성 전 이슈 본문 초안과 gh 명령을 사용자에게 보여주고 승인받는다. 승인 없이 gh 실행 금지.
4. **생성 + 링크**: gh로 추적 이슈 + 해당 서브모듈 이슈를 만들고 상호 링크한다.

## FE/BE 경계 판별 체크리스트

- **BE(git-ranker)**: REST API·엔드포인트, 도메인 로직, 영속성/JPA, 배치, 인증/보안, 관측성.
- **FE(git-ranker-client)**: 라우팅/페이지, 컴포넌트, 클라이언트 상태(Zustand/React Query), API 계약 미러링(`shared/types/api.ts`), 접근성.
- 한쪽만 필요하면 그쪽 이슈만 생성하되 추적 이슈는 항상 생성(해당 없는 역할은 "N/A").
- 계약(API 스키마)은 확정하지 않는다 — 범위만 나누고 두 이슈를 상호 링크한다.

## 라벨 보장

이슈 생성 전 대상 저장소에 라벨이 있는지 확인하고 없으면 만든다.
```bash
gh label list --repo alexization/<repo> | grep -q '^task' || gh label create task --repo alexization/<repo>
gh label list --repo alexization/<repo> | grep -q '^triage' || gh label create triage --repo alexization/<repo>
```

## 이슈 본문 템플릿

각 서브모듈 `.github/ISSUE_TEMPLATE/task.yml` 폼과 동일한 섹션을 마크다운으로 재현한다(`gh`는 폼을 자동 채우지 않음). 버그가 아니면 "재현 절차" 섹션은 생략.

```markdown
> 상위 추적: alexization/git-ranker-workflow#<T>
> 연관: alexization/<상대 레포>#<번호>

## 작업 유형
<BE: feature|bug|refactor|chore|performance|security|observability|docs
 FE: feature|bug|ui-refactor|chore|performance|accessibility|docs>

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

## 검증 방법
<BE: `./gradlew test`, `./gradlew build -x test`
 FE: `npm run lint`, `npm run typecheck`, `npm run build`, 브라우저 QA>

## 리스크 / 의존성 / 연관
- 리스크:
- 의존성(상대 레포 이슈):
- 상위 추적:
```

**FE 제약**: 테스트 러너가 없으므로 `작업 유형`에 `testing`을 쓰지 않고 `검증 방법`에 테스트를 넣지 않는다.

## gh 명령 (제목 규칙: `[<work_type>] <요약>`)

```bash
# 1) 서브모듈 이슈 생성 (본문은 --body-file로)
gh issue create --repo alexization/git-ranker        --title "[bug] ..." --body-file be.md  --label task,triage
gh issue create --repo alexization/git-ranker-client --title "[feature] ..." --body-file fe.md --label task,triage
# 2) 확보한 번호로 루트 추적 이슈 생성
gh issue create --repo alexization/git-ranker-workflow --title "[추적] ..." --body-file tracking.md --label tracking
# 3) 상호 링크 보정 (필요 시)
gh issue edit <번호> --repo alexization/<repo> --body-file <보정본>
```

## 오류 처리

- gh 실패 시 이미 생성된 이슈 번호를 보고하고(부분 생성 은폐 금지) 재시도/수동 보정 안내.
- `gh auth status` 미인증 시 인증 방법을 안내하고 중단.
````

- [ ] **Step 2: frontmatter 필수 필드 확인**

Run:
```bash
head -4 .claude/skills/workflow-dispatch/SKILL.md
```
Expected: `---` / `name: workflow-dispatch` / `description: ...` / (본문 시작 전).

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/workflow-dispatch/SKILL.md
git commit -m "feat: workflow-dispatch 스킬 추가"
```
Expected: 1 file changed.

---

### Task 6: `workflow-sync` 스킬

**Files:**
- Create: `.claude/skills/workflow-sync/SKILL.md`

**Interfaces:**
- Consumes: Task 4의 추적 이슈 포맷, Task 5가 만든 이슈 링크.
- Produces: `/sync` 커맨드(Task 7)가 호출하는 merge-back 절차 지식.

- [ ] **Step 1: 스킬 파일 작성**

Create `.claude/skills/workflow-sync/SKILL.md`:

````markdown
---
name: workflow-sync
description: 서브모듈 PR 머지 상태를 확인해 루트 gitlink를 갱신하고 요구사항 추적 이슈를 닫을 때 사용한다. destructive 명령 없이 gitlink만 develop 최신으로 반영한다.
---

# Workflow Sync

`/dispatch`가 만든 추적 이슈를 원장으로, 머지된 서브모듈 작업을 루트 gitlink에 반영한다.

## 절차

1. **추적 이슈 선택**: 인자로 번호/URL이 오면 그것을, 없으면 `gh issue list --repo alexization/git-ranker-workflow --label tracking --state open`에서 고른다.
2. **머지 상태 확인**: 추적 이슈 본문의 서브모듈 이슈 번호를 파싱하고, 각 이슈에 연결된 PR의 머지 여부를 확인한다.
   ```bash
   gh issue view <번호> --repo alexization/<repo> --json title,state,body
   gh pr list --repo alexization/<repo> --search "<이슈참조>" --state merged --json number,mergedAt
   ```
3. **gitlink 갱신 (머지된 쪽만)**: destructive 규약 준수.
   ```bash
   git -C <sub> fetch origin develop
   git submodule update --remote <sub>   # 또는: git -C <sub> checkout <merge-sha>
   git add <sub>
   ```
   - 파일 discard용 `git checkout --`가 아닌 브랜치/커밋 checkout만 사용.
   - 서브모듈에 uncommitted 변경이 있으면 중단하고 사용자에게 보고(덮어쓰기 금지).
4. **커밋 초안**: `.gitmessage.ko.txt` 형식으로 gitlink 커밋을 만든다. **push는 사용자 요청 시만.**
   ```bash
   git commit -m "chore: <요구사항> 서브모듈 gitlink 반영"
   ```
5. **추적 이슈 갱신**: 완료 체크박스를 갱신한다. 두 서브모듈 모두 머지·반영되면 사용자 확인 후 닫는다.
   ```bash
   gh issue edit <T> --repo alexization/git-ranker-workflow --body-file <갱신본>
   gh issue close <T> --repo alexization/git-ranker-workflow
   ```

## 부분 진행

- 아직 머지되지 않은 PR은 skip하고 상태만 보고한다.
- 한쪽만 머지되면 그쪽 gitlink만 갱신하고 체크박스도 부분 갱신한다. 나머지는 다음 `/sync`에서 처리.

## 오류 처리

- `gh auth status` 미인증 시 안내 후 중단.
- 연결된 PR을 찾지 못하면(이슈 본문에 `Closes #` 누락 등) 이슈 상태만 보고하고 사용자에게 수동 확인 요청.
````

- [ ] **Step 2: frontmatter 필수 필드 확인**

Run:
```bash
head -4 .claude/skills/workflow-sync/SKILL.md
```
Expected: `---` / `name: workflow-sync` / `description: ...`.

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/workflow-sync/SKILL.md
git commit -m "feat: workflow-sync 스킬 추가"
```
Expected: 1 file changed.

---

### Task 7: `/dispatch` · `/sync` 슬래시 커맨드

**Files:**
- Create: `.claude/commands/dispatch.md`, `.claude/commands/sync.md`

**Interfaces:**
- Consumes: Task 5(`workflow-dispatch`), Task 6(`workflow-sync`) 스킬.

- [ ] **Step 1: `/dispatch` 커맨드 작성**

Create `.claude/commands/dispatch.md`:

```markdown
---
description: 요구사항을 FE/BE 작업으로 분해해 각 서브모듈에 GitHub 이슈를 생성
argument-hint: <요구사항 설명>
---

`workflow-dispatch` 스킬을 먼저 로드해 그 절차를 그대로 따르라.

요구사항: $ARGUMENTS

1. Plan 모드 + AskUserQuestion으로 요구사항을 FE(git-ranker-client) / BE(git-ranker) 작업 범위로 분해한다. 상세 구현 계획은 세우지 않고 범위만 나눈다.
2. 각 이슈 본문 초안과 gh 명령을 미리보기로 제시하고 사용자 승인을 받는다.
3. 승인 후 gh로 루트 추적 이슈 + 해당 서브모듈 이슈를 생성하고 상호 링크한다.
```

- [ ] **Step 2: `/sync` 커맨드 작성**

Create `.claude/commands/sync.md`:

```markdown
---
description: 서브모듈 PR 머지 상태를 확인해 gitlink를 갱신하고 추적 이슈를 닫는다
argument-hint: <추적 이슈 번호 또는 URL (선택)>
---

`workflow-sync` 스킬을 먼저 로드해 그 절차를 그대로 따르라.

대상 추적 이슈: $ARGUMENTS (없으면 열린 `tracking` 라벨 이슈를 조회해 선택)

1. 추적 이슈를 읽어 연결된 서브모듈 이슈/PR 머지 상태를 gh로 확인한다.
2. 머지된 서브모듈만 gitlink를 갱신한다(destructive 금지 규약 준수).
3. `.gitmessage.ko.txt` 형식으로 gitlink 커밋 초안을 만든다. push는 사용자 요청 시만.
4. 추적 이슈 체크박스를 갱신하고, 모두 완료되면 사용자 확인 후 닫는다.
```

- [ ] **Step 3: 존재·frontmatter 확인**

Run:
```bash
head -3 .claude/commands/dispatch.md && echo "---" && head -3 .claude/commands/sync.md
```
Expected: 두 파일 모두 `---` / `description: ...` / `argument-hint: ...`.

- [ ] **Step 4: 커밋**

```bash
git add .claude/commands/dispatch.md .claude/commands/sync.md
git commit -m "feat: /dispatch, /sync 슬래시 커맨드 추가"
```
Expected: 2 files changed.

---

### Task 8: 루트 `CLAUDE.md`에 오케스트레이션 규약 반영

**Files:**
- Modify: `CLAUDE.md` (`## Harness 구조` 섹션 뒤에 새 섹션 추가)

**Interfaces:**
- Consumes: Task 5·6·7의 커맨드/스킬 이름.

- [ ] **Step 1: 오케스트레이션 섹션 추가**

`CLAUDE.md`의 `## Harness 구조` 섹션 마지막 항목 뒤, 파일 끝에 아래를 추가한다:

```markdown

## Workflow 오케스트레이션

이 저장소는 요구사항을 FE/BE로 분배하는 오케스트레이터다. 상세 구현 계획은 각 서브모듈의 Plan 모드가 담당하고, 여기서는 역할별 작업 범위만 나눠 GitHub 이슈로 넘긴다. 세 세션이 GitHub 이슈로만 연결된다(로컬 상태 없음).

- `/dispatch <요구사항>`: Plan 모드+AskUserQuestion으로 FE/BE 범위 분해 → 미리보기 승인 → `gh`로 루트 추적 이슈 + 각 서브모듈 이슈 생성. 절차는 `.claude/skills/workflow-dispatch`가 소유한다.
- 각 서브모듈: 자기 이슈를 진입점으로 Plan 모드 → 구현 → PR → merge (각 레포 harness).
- `/sync [추적이슈]`: 머지된 서브모듈 gitlink를 `develop` 최신으로 반영하고 추적 이슈를 닫는다. 절차는 `.claude/skills/workflow-sync`가 소유한다.
- 이슈 형식은 세 저장소 공통 통합 템플릿(`task.yml` / 루트 `tracking.yml`)을 쓴다. 작업 종류(기능/버그/리팩토링/간단한 수정)를 work-type 필드로 흡수한다.
- 서브모듈 remote org는 `alexization`, 추적 브랜치는 `develop`.
```

- [ ] **Step 2: 링크 정합성 확인**

Run:
```bash
grep -n "workflow-dispatch\|workflow-sync\|/dispatch\|/sync" CLAUDE.md
```
Expected: 위에서 추가한 참조들이 출력되고, 이름이 실제 스킬/커맨드 경로와 일치한다.

- [ ] **Step 3: 커밋**

```bash
git add CLAUDE.md
git commit -m "docs: workflow 오케스트레이션 규약 CLAUDE.md 반영"
```
Expected: 1 file changed.

---

### Task 9: refactor 잔재 정리 + 최종 검증

**Files:**
- Modify: `.gitignore` (stale 라인 제거)
- Delete (디스크): `.pytest_cache/`

- [ ] **Step 1: `.gitignore`에서 stale 라인 제거**

`.gitignore`의 `workflows/system/circuit-breaker.json` 라인을 삭제한다(삭제된 `workflows/` 트리를 가리키는 잔재). 최종 `.gitignore`:

```
.gitignore
.idea/
__pycache__/
```

- [ ] **Step 2: `.pytest_cache/` 디스크 정리**

Run (‑f 없이 — block-dangerous 규약 준수):
```bash
rm -r .pytest_cache && echo "removed" || echo "already gone"
```
Expected: `removed` (또는 `already gone`).

- [ ] **Step 3: 커밋 (.gitignore 변경만)**

```bash
git add .gitignore
git commit -m "chore: refactor 잔재 gitignore 참조 정리"
```
Expected: 1 file changed.

- [ ] **Step 4: 최종 정합성 검증**

Run:
```bash
# (a) 모든 신규 폼 YAML 유효
for f in .github/ISSUE_TEMPLATE/tracking.yml git-ranker/.github/ISSUE_TEMPLATE/task.yml git-ranker-client/.github/ISSUE_TEMPLATE/task.yml; do ruby -ryaml -e "YAML.load_file('$f'); puts '$f valid'"; done
# (b) 스킬/커맨드 존재
ls .claude/skills/workflow-dispatch/SKILL.md .claude/skills/workflow-sync/SKILL.md .claude/commands/dispatch.md .claude/commands/sync.md
# (c) 스킬에 dangling 상대링크 없음(존재하지 않는 파일 참조 여부 육안 확인)
grep -rn "\](\.\./" .claude/skills/workflow-dispatch .claude/skills/workflow-sync || echo "no relative cross-refs"
# (d) 워킹트리 깨끗
git status --short
```
Expected: (a) 세 폼 모두 `valid`, (b) 네 파일 모두 존재, (c) `no relative cross-refs`, (d) 출력 없음(깨끗).

- [ ] **Step 5: dispatch dry-run 리허설 (수동)**

새 세션 또는 현재 세션에서 `/dispatch 샘플 요구사항(예: 사용자 프로필 페이지에 뱃지 표시)`을 실행한다. 확인 사항:
- `workflow-dispatch` 스킬이 로드되고 Plan 모드로 FE/BE 범위 분해가 시작되는가.
- 이슈 본문 초안이 통합 템플릿 섹션 구조로 나오고, BE=gradlew·FE=npm 검증으로 채워지는가.
- **미리보기 단계에서 멈추고 승인을 요청**하는가(실제 gh 생성 전).
기대: 위 3개 모두 충족. (실제 이슈 생성 없이 미리보기에서 중단 확인.)

---

## Self-Review

**1. Spec coverage:**
- 3-세션 흐름·`/dispatch`·`/sync` → Task 5·6·7·8 ✔
- 통합 이슈 템플릿(서브모듈 교체 + 레거시 삭제) → Task 1·2 ✔
- 루트 추적 이슈 원장 → Task 4 ✔
- gitlink 반영(sync 절차 + 구현 시 초기 반영) → Task 3·6 ✔
- 미리보기 게이트·오류/부분 진행 처리 → Task 5·6 스킬 본문 ✔
- refactor 잔재 정리 → Task 9 ✔
- 검증(폼 유효성·훅 정합·문서 정합·위생·dry-run) → Task 9 ✔
- 스코프 제외(FE 러너/BE 훅) → 계획에서 다루지 않음(의도적) ✔

**2. Placeholder scan:** 코드블록의 `<T>`,`<번호>`,`<sub>`,`<repo>`,`<merge-sha>`,`$ARGUMENTS`는 커맨드/스킬 런타임에 채워지는 의도된 파라미터이며 계획 자체의 미완성 항목(TBD/TODO)은 없다.

**3. Type consistency:** 스킬 이름(`workflow-dispatch`/`workflow-sync`), 커맨드(`/dispatch`/`/sync`), 파일 경로, org(`alexization`), 브랜치(`develop`), 라벨(`task`/`triage`/`tracking`)이 전 task에서 일관.

## 실행 시 주의 (push 순서)

이 계획은 로컬 커밋까지만 수행한다. 사용자가 push를 요청하면 **서브모듈(git-ranker, git-ranker-client) 먼저 push한 뒤 루트를 push**해야 gitlink가 원격에서 유효하다.

## 열린 참고 (스코프 밖)

루트 `.github/ISSUE_TEMPLATE/engineering_task.yml`(target_repo 드롭다운의 수동 라우팅 폼)은 이번 스코프에서 건드리지 않는다. `/dispatch` 자동화와 역할이 겹치므로, 별도 후속에서 제거 또는 통합을 검토할 수 있다.
