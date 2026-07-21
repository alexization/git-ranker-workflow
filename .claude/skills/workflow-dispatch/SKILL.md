---
name: workflow-dispatch
description: 하나의 요구사항을 FE(git-ranker-client)/BE(git-ranker) 작업 범위로 분해해 각 서브모듈에 GitHub 이슈를 생성하고 루트 추적 이슈로 묶을 때 사용한다. 상세 구현 계획은 세우지 않고 역할별 범위만 나눈다.
---

# Workflow Dispatch

요구사항을 받아 **역할별 작업 범위로 분해**하고 각 서브모듈에 GitHub 이슈를 생성한다.

**무엇을 확정하고 무엇을 위임하는가** — 세 세션이 GitHub 이슈로만 연결되므로, 어느 한 레포가 단독으로 결정할 수 없는 것은 dispatch가 확정하고, 각 레포가 스스로 결정할 수 있는 것은 위임한다.

- **dispatch가 확정한다(이슈에 반드시 담는다)**: 공유 계약(FE↔BE 사이 API 응답/요청 JSON 형태), 역할별 작업 범위, 범위 밖(Non-goals), 실행 순서·의존성, 완료·검증 기준. 이 항목들이 없으면 두 세션의 가정이 어긋난다.
- **각 서브모듈 Plan 모드에 위임한다**: 위 계약을 만족하는 *내부 구현 방식*(BE 서비스/영속 계층 설계, FE 컴포넌트/상태 구조 등).

즉 이슈만 읽고도 "무엇을 만들어야 하는지(계약·범위·완료조건)"는 명확해야 하고, "어떻게 만들지"만 열려 있어야 한다.

## 절차

1. **분해 (Plan 모드 + AskUserQuestion)**: 요구사항을 아래 경계 기준으로 FE/BE로 나눈다. 애매하면 AskUserQuestion으로 확정한 뒤 진행한다.
2. **본문 작성**: 각 이슈 본문을 아래 템플릿으로 작성한다(레포별 값 인스턴스화).
3. **미리보기 게이트**: 생성 전 이슈 본문 초안과 gh 명령을 사용자에게 보여주고 승인받는다. 승인 없이 gh 실행 금지.
4. **생성 + 링크**: gh로 추적 이슈 + 해당 서브모듈 이슈를 만들고 상호 링크한다.

## FE/BE 경계 판별 체크리스트

- **BE(git-ranker)**: REST API·엔드포인트, 도메인 로직, 영속성/JPA, 배치, 인증/보안, 관측성.
- **FE(git-ranker-client)**: 라우팅/페이지, 컴포넌트, 클라이언트 상태(Zustand/React Query), API 계약 미러링(`shared/types/api.ts`), 접근성.
- 한쪽만 필요하면 그쪽 이슈만 생성하되 추적 이슈는 항상 생성(해당 없는 역할은 "N/A").
- **공유 계약(API 스키마)은 추적 이슈의 "공유 계약" 섹션에 정본(single source of truth)으로 확정한다.** FE/BE 이슈는 이 계약을 복제하지 말고 링크로 참조한다 — 양쪽에 필드 목록을 중복 기재하면 한쪽이 바뀔 때 조용히 어긋난다. 내부 구현 방식은 확정하지 않고 각 Plan 모드에 위임한다.

## 라벨 보장

이슈 생성 전 대상 저장소에 라벨이 있는지 확인하고 없으면 만든다.
```bash
gh label list --repo alexization/<repo> | grep -q '^task' || gh label create task --repo alexization/<repo>
gh label list --repo alexization/<repo> | grep -q '^triage' || gh label create triage --repo alexization/<repo>
```

## 이슈 본문 템플릿

각 서브모듈 `.github/ISSUE_TEMPLATE/task.yml` 폼과 동일한 섹션을 마크다운으로 재현한다(`gh`는 폼을 자동 채우지 않음). 아래 슬롯은 **모두 채운다** — 빈 채로 두지 않는다. 버그가 아니면 "재현 절차" 섹션만 생략.

```markdown
> 상위 추적: alexization/git-ranker-workflow#<T>
> 연관: alexization/<상대 레포>#<번호>
> 공유 계약: 추적 이슈#<T> "공유 계약" 섹션 참조 (여기 필드 목록을 복제하지 않는다)

## 작업 유형
<BE: feature|bug|refactor|chore|performance|security|observability|docs
 FE: feature|bug|ui-refactor|chore|performance|accessibility|docs>

## 배경 / 문제
<이유. 버그면 증상 요약>

## 작업 내용 / 기대 결과
<무엇을 / 완료 후 기대 동작. 계약의 구체 필드·JSON은 추적 이슈#<T>를 참조하고, 여기서는 이 레포가 그 계약을 어떻게 충족하는지(어느 지점을 바꾸는지)를 적는다>

## 범위 밖 (Non-goals)
<이번 이슈에서 의도적으로 하지 않는 것. 스코프 크립·재검토 방지. 없으면 "없음"이라 명시>

## 재현 절차 / 기대 vs 실제   ← 버그일 때만
재현: 1) ... 2) ...
기대: ...
실제: ...

## 작업 범위
<BE: `domain/...`, `src/test/...`   |   FE: route/component/hook·store>

## 완료 조건
- [ ] <검증 가능한 항목. 주관적 "잘 된다" 금지 — 무엇이 참이면 완료인지>

## 검증 방법
<BE: `./gradlew test`, `./gradlew build -x test`
 FE: `npm run lint`, `npm run typecheck`, `npm run build`,
     브라우저 QA를 구체 시나리오로: (페이지/경로) 접속 → (동작) → (보여야 할 것 / 보이면 안 되는 것)>

## 리스크 / 의존성 / 연관
- 리스크:
- 의존성(상대 레포 이슈):
- 상위 추적:
```

**FE 제약**: 테스트 러너가 없으므로 `작업 유형`에 `testing`을 쓰지 않고 `검증 방법`에 테스트를 넣지 않는다. 대신 브라우저 QA를 위처럼 "경로 → 동작 → 기대/비기대 상태"의 구체 시나리오로 적어 체크 가능하게 만든다.

## 추적 이슈 본문 템플릿

루트 `.github/ISSUE_TEMPLATE/tracking.yml` 폼과 같은 섹션을 마크다운으로 재현한다. **"공유 계약"은 FE↔BE 계약의 정본**이며, 여기서만 필드/JSON을 확정하고 서브모듈 이슈는 이 섹션을 링크로 가리킨다.

````markdown
## 요구사항
<전체 요구사항 요약. 우선순위/식별자(P0-1 등)가 있으면 포함>

## 공유 계약 (FE↔BE 정본 — 서브모듈 이슈는 이 섹션을 참조)
대상: `<METHOD> <경로>`

변경 후 응답(또는 요청) 형태:
```json
{ "<필드>": "<타입>  // 설명", ... }
```
- 포함 필드: <이름:타입 나열>
- 제외/삭제 필드: <이름 — 왜 빼는지>
- 결정과 기각한 대안: <채택안 요약 + "왜 다른 안이 아닌지" 한 줄 — 서브모듈 세션의 재검토 방지>

## 역할 분해
### Backend (git-ranker) — alexization/git-ranker#<N>
- 범위: <한 줄>
### Frontend (git-ranker-client) — alexization/git-ranker-client#<M>
- 범위: <한 줄>
(해당 없는 역할은 "N/A")

## 실행 순서 / 의존성
1. <먼저 배포할 쪽> — 이유
2. <다음 배포할 쪽> — 이유
<순서가 무관하면 "무관"이라 명시>

## 완료 추적
- [ ] BE 머지 (git-ranker#<N>)
- [ ] FE 머지 (git-ranker-client#<M>)
- [ ] 계약 준수 확인: <응답에 제외 필드 없음 등 검증 가능한 항목>
- [ ] gitlink 반영 (루트 커밋)
````

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
