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
