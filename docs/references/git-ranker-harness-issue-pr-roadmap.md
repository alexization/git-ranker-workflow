# Historical: Git Ranker Harness Engineering Issue/PR Roadmap

> 상태: 초기 분해를 남겨두는 역사 문서다. 현재 계획 source of truth는 이 문서가 아니라 `docs/product/`, `docs/operations/`, `docs/exec-plans/`다.
>
> 새 작업은 이 문서보다 아래 문서를 먼저 읽는다.
>
> - [AGENTS.md](../../AGENTS.md)
> - [PLANS.md](../../PLANS.md)
> - [docs/architecture/control-plane-map.md](../architecture/control-plane-map.md)
> - [docs/operations/workflow-governance.md](../operations/workflow-governance.md)
> - [docs/product/harness-roadmap.md](../product/harness-roadmap.md)
> - [docs/product/work-item-catalog.md](../product/work-item-catalog.md)
> - [docs/exec-plans/README.md](../exec-plans/README.md)

- 기준 저장소: `git-ranker-workflow`
- 대상 저장소: `git-ranker-workflow`, `git-ranker`, `git-ranker-client`
- 문서 목적: AI Agent를 바로 크게 투입하기 전에, 코드베이스를 Agent-friendly하게 정비하고 이후 Harness Engineering을 점진적으로 적용하기 위한 상세 작업 분해 문서
- 사용 방식: 이 문서를 기준으로 `Issue 1개 = PR 1개` 단위로 작업을 요청하고, 각 PR은 이 문서의 완료 기준과 검증 기준을 충족해야 한다

---

## 1. 이 문서의 목표

이 문서는 단순한 아이디어 정리 문서가 아니다. 아래 세 가지를 바로 실행 가능한 수준으로 고정하는 문서다.

1. 현재 코드베이스가 AI Agent가 일하기에 얼마나 준비되어 있는지 기준선을 명확히 남긴다.
2. Harness Engineering을 적용하기 전에 무엇부터 정비해야 하는지 Issue/PR 단위로 쪼갠다.
3. 각 작업이 왜 필요한지, 무엇을 바꾸는지, 어떤 결과를 남겨야 하는지, 무엇으로 완료를 판단하는지까지 명확히 적는다.

이 문서의 핵심 전제는 다음과 같다.

- 지금 당장은 자율성이 높은 Agent 운영이 목표가 아니다.
- 먼저 `신뢰할 수 있는 문서`, `신뢰할 수 있는 계약`, `신뢰할 수 있는 검증 신호`, `신뢰할 수 있는 실행 환경`을 만들어야 한다.
- 첫 하네스 대상은 `랭킹 조회`로 고정한다.
- 반복될 가능성이 높은 작업은 단순 문서로만 두지 않고, 이후 `SKILL`로 승격할 수 있도록 설계한다.

---

## 2. 이번 계획에서 고정한 의사결정

### 2.1 준비 수준

- 기준: `균형형`
- 의미: 문서, 가드레일, 핵심 검증을 먼저 고정하고, 통합 테스트와 E2E는 바로 다음 단계에서 강화한다

### 2.2 첫 하네스 축

- 대상: `랭킹 조회`
- 이유:
  - 인증과 배치보다 범위가 작다
  - 프런트엔드와 백엔드 계약을 함께 검증하기 좋다
  - Playwright, LogQL, PromQL을 붙였을 때 가장 작은 성공 루프를 만들 수 있다

### 2.3 source of truth 위치

- 기준: `workflow 중심`
- 의미:
  - `git-ranker-workflow`가 문서, 계획, 증거, 하네스 정의의 컨트롤 플레인 역할을 맡는다
  - `git-ranker`, `git-ranker-client`는 여전히 시스템 오브 레코드이지만, 하네스 운용 규칙과 cross-repo 문맥은 workflow가 소유한다

### 2.4 1단계 런타임 방식

- 기준: `하이브리드`
- 의미:
  - 평소 개발은 각 저장소의 기존 방식대로 해도 된다
  - 다만 하네스 검증용 표준 런타임은 `git-ranker-workflow`가 소유한다
  - 최종 지향점은 `컨테이너 중심`이지만, 첫 단계는 표준 검증 환경부터 만든다

---

## 3. 현재 기준선 요약

### 3.1 `git-ranker` 백엔드

강점:

- `./gradlew test jacocoTestCoverageVerification` 통과
- 단위 테스트, ArchUnit, 배치 코드, 메트릭, 로깅 구성이 이미 존재
- GitHub Actions CI, deploy, quality-gate가 존재
- PR 템플릿에 검증 증거와 관측성 확인 항목이 이미 들어가 있다

약점:

- `./gradlew integrationTest`는 Docker daemon이 없으면 Testcontainers 초기화 실패로 바로 죽는다
- OpenAPI 같은 기계가 읽는 공식 API 계약이 없다
- 문서형 source of truth가 없다
- 정적 가드레일은 구조 검증 외에는 아직 약하다

### 3.2 `git-ranker-client` 프런트엔드

강점:

- `npx tsc --noEmit` 통과
- `npm run build` 통과
- 구조 자체는 `src/app`, `src/features`, `src/shared`로 나뉘어 있어 탐색 가능성은 나쁘지 않다

약점:

- 자동 테스트가 없다
- `npm run lint`는 통과하지만 warning이 많이 누적되어 있어 신호 품질이 낮다
- `README.md`가 기본 Next.js 템플릿 상태다
- `next/font/google` 의존성으로 인해 격리 빌드 재현성이 떨어질 수 있다
- `middleware.ts` deprecated convention이 남아 있다
- `tierSchema`에 `EMERALD`가 빠져 있어 백엔드 계약과 이미 드리프트가 발생했다

### 3.3 `git-ranker-workflow`

현 상태:

- 서브모듈 컨테이너 역할만 한다
- `AGENTS.md`, `PLANS.md`, `docs/`, 표준 검증 명령, 증거 보관 규칙이 없다
- 아직 컨트롤 플레인 저장소라고 부르기 어렵다

---

## 4. 작업 운영 규칙

### 4.1 Issue/PR 단위 규칙

- 원칙적으로 `Issue 1개 = PR 1개`
- 하나의 PR은 하나의 목표만 해결한다
- 한 PR에서 여러 저장소를 동시에 건드리는 경우는 피한다
- cross-repo 작업은 `workflow 문서 PR`과 `앱 코드 PR`로 나눈다

### 4.2 각 PR에 반드시 들어가야 할 내용

- 문제 정의
- 왜 지금 필요한지
- 이번 PR의 범위와 비범위
- 산출물
- 검증 명령과 결과
- 남은 리스크
- 다음 Issue로 넘겨야 할 전제조건

### 4.3 증거 규칙

하네스 관련 PR에서는 가능하면 아래 증거를 남긴다.

- 명령 실행 결과 요약
- 브라우저 증거: screenshot, trace, video
- 로그 증거: LogQL 결과 또는 로그 요약
- 메트릭 증거: PromQL 결과 또는 지표 캡처
- 문서 업데이트: source of truth 반영 여부

### 4.4 브랜치/슬러그 규칙

권장 형식:

- Issue ID: `GRW-01`, `GRB-01`, `GRC-01`
- 브랜치명: `feat/grw-01-workflow-skeleton`
- 작업 슬러그: `2026-03-24-grw-01-workflow-skeleton`

약어:

- `GRW`: `git-ranker-workflow`
- `GRB`: `git-ranker` backend
- `GRC`: `git-ranker-client`

### 4.5 SKILL 운영 규칙

이 roadmap에서는 `문서`, `SKILL`, `exec plan`을 다르게 본다.

- 문서:
  - source of truth
  - 도메인, 계약, 운영 규칙, 수용 기준을 설명한다
- SKILL:
  - 반복 작업을 Agent가 재사용 가능한 절차로 수행하게 만드는 실행 레시피다
  - 병렬 에이전트 운영 시 같은 품질 기준과 증거 규칙을 공유하는 데 쓴다
- exec plan:
  - 현재 한 작업의 목표, 범위, 검증, 증거를 적는 실행 문서다

아래 조건 중 하나라도 만족하면 SKILL 정의 후보로 본다.

- 같은 작업 흐름이 3번 이상 반복될 가능성이 높다
- 병렬 에이전트에게 같은 입력/출력/증거 규칙을 강제해야 한다
- 도메인 문서만 읽어서는 실행 절차가 흔들릴 가능성이 높다
- 로그/메트릭/브라우저 검증처럼 순서가 중요한 루프가 있다

SKILL은 기본적으로 `git-ranker-workflow/.codex/skills/<skill-name>/SKILL.md` 구조로 관리한다.

각 SKILL은 최소한 아래를 포함해야 한다.

- 목적
- 언제 사용하는지
- 입력과 선행조건
- 출력과 산출물 위치
- 표준 명령
- 필수 증거
- 금지 사항
- 병렬 작업 시 ownership 규칙

이번 roadmap에서 우선 검토해야 할 프로젝트 전용 SKILL 후보는 아래와 같다.

- `issue-to-exec-plan`
- `parallel-work-split`
- `api-contract-sync`
- `ranking-read-harness`
- `playwright-browser-qa`
- `promql-logql-evidence`
- `batch-failure-triage`
- `doc-gardener`

---

## 5. 권장 실행 순서

1. `GRW-01` workflow skeleton과 문서 규칙 만들기
2. `GRW-02` 현재 readiness 기준선 문서화
3. `GRW-S01` skill registry와 template 정의
4. `GRB-01` 백엔드 OpenAPI 계약 생성 기반 만들기
5. `GRW-03` 백엔드 도메인/운영 문서 수집
6. `GRC-01` 프런트엔드 계약 타입 단일화
7. `GRW-04` 프런트엔드 구조/데이터 흐름 문서 수집
8. `GRW-S02` core planning/parallel-agent skill pack v1
9. `GRB-02` 백엔드 검증 루프 hardening
10. `GRC-02` 프런트 lint debt 1차 정리
11. `GRC-03` 프런트 build/runtime 하네스 친화화
12. `GRW-05` workflow 표준 검증 런타임 만들기
13. `GRB-03` 랭킹 조회용 결정적 seed 데이터 지원
14. `GRC-04` 랭킹 조회 Playwright 하네스 도입
15. `GRW-06` 랭킹 조회 증거 수집 루프 추가
16. `GRW-S03` ranking harness execution skill pack v1
17. `GRW-07` 문서/계약/플랜 freshness 가드레일 추가
18. `GRW-08` 배지 하네스 계획 문서 작성
19. `GRW-09` 배치 하네스 계획 문서 작성
20. `GRW-S04` reliability/batch skill pack v1

---

## 5.1 AI에게 Issue 단위로 요청할 때 함께 붙일 공통 실행 지시 블록

아래 블록은 앞으로 어떤 Issue를 AI Agent에게 요청하더라도 같이 붙이는 것을 권장한다.

```md
### 공통 실행 지시

- 이 Issue의 목표만 수행한다. 범위를 넓히지 않는다.
- 선행조건이 충족되지 않았으면 임의로 우회 구현하지 말고, 먼저 blocker를 정리한다.
- 허용된 write scope 밖의 파일은 수정하지 않는다.
- source of truth 문서를 함께 업데이트하거나, 업데이트가 불필요한 이유를 남긴다.
- 검증 명령과 결과를 반드시 남긴다.
- 새로 생긴 반복 절차가 있다면 skill 후보로 제안하되, 이번 Issue 범위를 넘는 구현은 하지 않는다.
- 모호한 선택지가 여러 개면 이 문서의 "작업별 추가 고정 정보"를 기본 결정으로 따른다.
- 실행 중 예상치 못한 dirty change가 있으면 되돌리지 말고 영향 여부만 확인한다.
```

이 공통 블록을 붙이는 이유는 다음과 같다.

- Issue 본문마다 같은 안전 수칙을 반복해서 적지 않아도 된다
- Agent가 범위를 넓히거나 조용히 우회 구현하는 것을 줄일 수 있다
- 병렬 작업 시에도 같은 기준으로 움직이게 할 수 있다

---

## 5.2 작업별 추가 고정 정보

아래 표는 각 작업 설명만으로는 남을 수 있는 모호함을 줄이기 위한 기본 결정값이다.

| ID | 선행조건 | 권장 write scope | 기본 결정과 안전장치 |
| --- | --- | --- | --- |
| `GRW-01` | 없음 | 루트, `docs/`, `.gitignore` | 문서 기본 언어는 한국어로 한다. `AGENTS.md`는 짧은 인덱스 문서로 만들고, 상세 규칙은 `docs/`로 보낸다. `PLANS.md`는 실행 계획 상태 규칙과 naming 규칙만 담는다. 실제 스크립트는 추가하지 않는다. |
| `GRW-02` | `GRW-01` | `docs/quality-score`, `docs/references` | readiness 평가는 `1~5 점수 + Low/Medium/High + 핵심 리스크 요약` 형식으로 통일한다. 실제 확인한 명령과 날짜를 함께 남긴다. |
| `GRW-S01` | `GRW-01` | `.codex/skills/` 하위만 | skill은 문서형 자산부터 시작하고, 처음부터 실행 스크립트를 넣지 않는다. 각 skill 폴더의 필수 파일은 `SKILL.md` 하나다. |
| `GRB-01` | 없음 | backend build/config/doc 관련 파일만 | API 동작 변경은 하지 않는다. 목표는 OpenAPI를 생성할 수 있는 기반 추가다. 산출 형식은 가능하면 `JSON`을 기본으로 하고, `YAML`은 비용이 적을 때만 함께 낸다. |
| `GRW-03` | `GRW-01` | workflow 문서만 | 코드 내용을 복붙하지 말고, 규칙과 흐름을 행동 중심으로 요약한다. 필요한 경우 backend 코드 경로를 참조 링크로 남긴다. |
| `GRC-01` | `GRB-01` 권장 | `src/shared/types`, `src/shared/lib/validations`, 직접 소비자 파일만 | 서버 응답 타입은 단일 기준만 남긴다. 이 단계에서는 전체 컴포넌트 리팩터링보다 `계약 중복 제거`가 우선이다. `EMERALD` 누락 같은 enum drift를 먼저 해결한다. |
| `GRW-04` | `GRW-01` | workflow 문서만 | 라우트 문서는 `route`, `사용 API`, `주요 상태`, `env`, `외부 의존성`을 포함한 표 형식으로 정리한다. |
| `GRW-S02` | `GRW-S01`, `GRW-03`, `GRW-04` 권장 | `.codex/skills/` 하위만 | coordination skill만 작성한다. 코드 생성이나 검증 실행 skill은 아직 넣지 않는다. 각 skill에는 병렬 수행 시 ownership 규칙을 반드시 적는다. |
| `GRB-02` | 없음 | Gradle/test/doc 관련 파일만 | Docker가 없을 때 테스트를 조용히 skip하지 말고 명확히 fail-fast 한다. 목표는 "환경 문제인지 코드 문제인지 구분 가능하게 만들기"다. |
| `GRC-02` | `GRC-01` 권장 | ranking/user/badge/auth 관련 파일 우선 | 전체 warning zero를 한 번에 달성하려 하지 않는다. correctness 위험이 큰 경고부터 제거한다. UI 스타일 변경은 목적이 아니다. |
| `GRC-03` | `GRC-02` 권장 | font/runtime config/readme 관련 파일만 | 외부 네트워크 의존성을 줄이는 것이 핵심이다. 디자인 변경보다 build 재현성 확보가 우선이다. |
| `GRW-05` | `GRW-01`, `GRB-02`, `GRC-03` 권장 | workflow runtime 파일만 | 구현 기본값은 `docker compose + 얇은 스크립트`다. 목표는 검증 런타임 표준화이지, 운영 환경 완전 복제는 아니다. |
| `GRB-03` | `GRW-05` 권장 | backend seed/bootstrap 관련 파일만 | GitHub API에 의존하지 않는 결정적 데이터가 핵심이다. seed 방식은 `반복 실행해도 동일 결과가 나오는 방식`을 우선한다. |
| `GRC-04` | `GRW-05`, `GRB-03` | Playwright 설정, 테스트, 필요 최소한의 test hook | Playwright 설정은 client 저장소에 둔다. artifact 위치는 workflow와 연결 가능하게 하되, UI 변경 없이 테스트 가능하면 test id를 남발하지 않는다. |
| `GRW-06` | `GRC-04` | workflow query/template/doc 파일만 | query 저장 위치는 workflow 내부로 고정한다. evidence summary는 브라우저, 로그, 메트릭, 최종 판정을 같은 템플릿으로 남긴다. |
| `GRW-S03` | `GRW-S01`, `GRC-04`, `GRW-06` | `.codex/skills/` 하위만 | 이 단계의 skill은 이미 만들어진 runtime/query/test를 재사용하는 설명서여야 한다. 새 인프라를 발명하지 않는다. |
| `GRW-07` | `GRW-01` | workflow check/script/doc 파일만 | 처음부터 모든 것을 hard fail로 막지 않는다. 다만 broken link, stale contract 같은 명확한 오류는 fail 대상으로 본다. |
| `GRW-08` | `GRW-03` 권장 | planning 문서만 | 구현이 아니라 계획 문서 작성 Issue다. 결과 문서의 기본 섹션은 `목표`, `수용 기준`, `런타임`, `증거`, `리스크`, `다음 구현 단위`로 고정한다. |
| `GRW-09` | `GRW-03` 권장 | planning 문서만 | 구현이 아니라 계획 문서 작성 Issue다. 배치 계획은 `happy path`, `retry/skip`, `partial failure`, `metrics/logs`, `seed/data isolation`까지 적어야 한다. |
| `GRW-S04` | `GRW-S01`, `GRW-09` 권장 | `.codex/skills/` 하위만 | reliability skill은 체크리스트 중심으로 시작한다. 자동 복구나 자동 triage 구현은 이 Issue의 범위가 아니다. |

이 표의 목적은 "이슈 설명은 맞는데 구현 선택지가 여러 갈래로 갈리는 문제"를 줄이는 것이다.

---

## 6. 상세 작업 목록

## GRW-01. workflow skeleton과 문서 규칙 만들기

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: initialize workflow control plane skeleton`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

지금 workflow 저장소는 서브모듈을 담고 있는 컨테이너에 가깝다. AI Agent가 이 저장소를 읽어도 어디에 계획을 써야 하고, 어디에 도메인 문서가 있으며, 어떤 문서가 공식 source of truth인지 알 수 없다.

Harness Engineering의 첫 단계는 모델을 더 똑똑하게 만드는 것이 아니라, 저장소 안에 읽을 수 있는 질서를 만드는 것이다. 이 작업은 그 질서를 만든다.

### 이 PR에서 해야 할 일

- 루트에 `AGENTS.md`를 만든다
- 루트에 `PLANS.md`를 만든다
- 아래 디렉터리 구조를 만든다
  - `docs/architecture`
  - `docs/domain`
  - `docs/product`
  - `docs/operations`
  - `docs/reliability`
  - `docs/security`
  - `docs/quality-score`
  - `docs/exec-plans/active`
  - `docs/exec-plans/completed`
  - `docs/generated`
  - `docs/references`
- `.artifacts/` 디렉터리 규칙을 문서화하고 `.gitignore`에 반영한다
- 작업 슬러그 규칙과 증거 보관 규칙을 문서화한다

### 이번 PR에서 하지 않을 일

- 실제 하네스 스크립트 작성
- 앱 저장소 문서 본문 작성
- PromQL/LogQL 쿼리 추가

### 산출물

- `AGENTS.md`
- `PLANS.md`
- docs 트리
- 아티팩트/슬러그 규칙 문서

### 완료 기준

- 새로운 사람이 저장소 루트만 보고도 “계획은 어디에 두는지”, “도메인 문서는 어디에 적는지”, “증거는 어디에 남기는지”를 알 수 있어야 한다
- 이후 모든 workflow 문서는 새 구조를 따라 추가 가능해야 한다

### 검증

- `find docs -maxdepth 3 -type d | sort`
- `cat AGENTS.md`
- `cat PLANS.md`

### 다음 작업과의 연결

- `GRW-02`, `GRW-03`, `GRW-04`의 기반

---

## GRW-02. 현재 readiness 기준선 문서화

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add current agent readiness baseline`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

무엇을 개선할지 정하려면 먼저 “현재 어떤 상태인지”가 문서로 남아 있어야 한다. 이 기준선이 없으면 이후의 모든 PR이 얼마나 실질적인 개선인지 설명하기 어렵다.

### 이 PR에서 해야 할 일

- 현재 세 저장소 상태를 표로 정리한다
- 최소 항목:
  - 문서화
  - 테스트
  - 정적 가드레일
  - API/타입 계약
  - 운영 재현성
  - 관측 가능성
  - Agent 탐색 가능성
- 현재 확인된 핵심 이슈를 기록한다
  - backend integration test 환경 의존
  - frontend lint warning 누적
  - frontend README 부재
  - contract drift (`EMERALD`)
  - workflow control plane 부재

### 산출물

- readiness review 문서
- 점수표 또는 상태표

### 완료 기준

- 이후 모든 작업이 “어느 기준선 문제를 해결하는지” 연결 가능해야 한다
- 각 저장소별 우선순위가 한눈에 보여야 한다

### 검증

- 문서 리뷰
- readiness 표가 실제 현재 상태와 모순되지 않는지 확인

### 다음 작업과의 연결

- 이후 모든 Issue의 근거 문서

---

## GRW-S01. skill registry와 template 정의

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: define project skill registry and template`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

프로젝트 전용 SKILL이 없으면 병렬 에이전트 운영 시 같은 작업을 매번 자연어로 다시 설명해야 한다. 그러면 작업 품질이 사람 기억과 순간 프롬프트 품질에 의존하게 된다.

먼저 해야 할 일은 개별 skill을 많이 만드는 것이 아니라, skill을 어떤 형식으로 저장하고 어떤 기준으로 관리할지부터 고정하는 것이다.

### 이 PR에서 해야 할 일

- workflow 저장소에 `.codex/skills/` 디렉터리 구조를 만든다
- `.codex/skills/README.md`를 추가한다
- `.codex/skills/authoring-rules.md`를 추가한다
- skill 폴더 내 지원 파일 규칙을 정한다
  - `templates/`
  - `queries/`
  - `examples/`
  - `checklists/`
- skill naming 규칙을 정한다
- skill에 반드시 포함해야 할 항목을 고정한다
  - 목적
  - trigger
  - 입력
  - 출력
  - 표준 명령
  - required evidence
  - forbidden shortcuts
  - parallel ownership rule

### 이번 PR에서 하지 않을 일

- 실제 ranking/batch skill 본문 작성
- Playwright 쿼리나 PromQL 쿼리 추가

### 산출물

- `.codex/skills/README.md`
- `.codex/skills/authoring-rules.md`
- skill authoring 규칙 문서

### 완료 기준

- 이후 어떤 skill이 들어와도 같은 포맷으로 관리할 수 있어야 한다
- 문서와 skill의 역할 차이가 명확히 설명되어 있어야 한다

### 검증

- `find .codex/skills -maxdepth 2 -type f | sort`
- `cat .codex/skills/README.md`
- `cat .codex/skills/authoring-rules.md`

### 다음 작업과의 연결

- `GRW-S02`
- `GRW-S03`
- `GRW-S04`

---

## GRB-01. 백엔드 OpenAPI 계약 생성 기반 만들기

- 저장소: `git-ranker`
- 권장 PR 제목: `build: add generated OpenAPI contract for backend`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

현재 프런트엔드는 API 타입을 수기로 유지하고 있다. 이 방식은 이미 드리프트를 만들었다. Harness Engineering에서 계약은 문장보다 먼저 기계가 읽을 수 있어야 한다.

### 이 PR에서 해야 할 일

- OpenAPI 산출물을 생성할 수 있는 방식 도입
- 아래 엔드포인트가 산출물에 포함되도록 한다
  - `/api/v1/ranking`
  - `/api/v1/users/{username}`
  - `/api/v1/users/{username}/refresh`
  - `/api/v1/auth/*`
  - `/api/v1/badges/*`
- 생성 명령과 산출 위치를 정한다
- workflow가 이 산출물을 가져갈 수 있도록 경로와 버전 관리 정책을 문서화한다

### 이번 PR에서 하지 않을 일

- 프런트엔드 generated client 생성
- 모든 문서를 한 번에 작성

### 산출물

- OpenAPI 생성 설정
- 산출물 경로
- 생성 절차 문서

### 완료 기준

- 한 명령으로 최신 API 계약을 다시 생성할 수 있어야 한다
- 프런트엔드나 workflow가 이 산출물을 기준으로 후속 작업을 할 수 있어야 한다

### 검증

- OpenAPI 생성 명령 실행
- 산출물에 주요 엔드포인트가 포함되는지 확인

### 다음 작업과의 연결

- `GRC-01` 프런트 타입 단일화
- `GRW-03` 계약 문서 수집

---

## GRW-03. 백엔드 도메인/운영 문서를 workflow에 수집

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add backend domain and operations source of truth`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

코드는 동작을 보여주지만, 왜 그 규칙이 필요한지는 설명하지 않는다. Agent는 점수 계산, 티어 판정, 배치 흐름, rate-limit 대응을 코드만 보고 빨리 안전하게 이해하기 어렵다.

### 이 PR에서 해야 할 일

- 다음 문서를 workflow에 작성한다
  - 점수 계산 규칙
  - 티어 판정 규칙
  - 랭킹 조회 흐름
  - 배지 서빙 흐름
  - 수동 갱신 흐름
  - 일일 배치 단계
  - GitHub API 실패/retry/skip/rate-limit 정책
  - 주요 로그 필드와 메트릭 이름
- 가능한 한 “행동”, “입출력”, “실패 모드”, “수용 기준” 중심으로 작성한다

### 산출물

- workflow `docs/domain/*`
- workflow `docs/operations/*`

### 완료 기준

- 랭킹, 배지, 배치 흐름을 코드 탐색 없이 문서로 설명할 수 있어야 한다
- 후속 하네스 문서가 이 내용을 그대로 참조 가능해야 한다

### 검증

- 문서 교차 검토
- 실제 코드와 규칙이 모순되지 않는지 확인

### 다음 작업과의 연결

- `GRW-05`, `GRW-06`, `GRW-08`, `GRW-09`

---

## GRC-01. 프런트엔드 계약 타입 단일화

- 저장소: `git-ranker-client`
- 권장 PR 제목: `refactor: unify frontend API contract types`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

현재 프런트는 같은 계약을 여러 파일에서 다르게 표현한다. 실제로 `EMERALD` 누락이 이미 발생했다. 이런 상태에서는 Agent가 잘못된 타입을 학습해 더 많은 드리프트를 만든다.

### 이 PR에서 해야 할 일

- 서버 응답 타입의 단일 기준을 정한다
- 권장 방향:
  - generated contract type을 서버 응답 기준으로 사용
  - Zod는 사용자 입력 검증에만 사용
- 아래 중복을 정리한다
  - `src/shared/types/api.ts`
  - `src/shared/lib/validations.ts`
- `tier` 값셋을 단일화하고 `EMERALD`를 포함해 정합성을 맞춘다

### 이번 PR에서 하지 않을 일

- 전체 컴포넌트 리팩터링
- Playwright 도입

### 산출물

- 단일 계약 타입 경로
- 드리프트 제거
- 최소한의 문서 또는 주석

### 완료 기준

- `tier`, `user response`, `ranking response`의 정의가 여러 곳에서 중복 선언되지 않아야 한다
- 백엔드 계약과 프런트 타입이 모순되지 않아야 한다

### 검증

- `npx tsc --noEmit`
- 필요한 경우 Zod schema와 generated type 비교

### 다음 작업과의 연결

- `GRC-04` Playwright 하네스
- 랭킹/사용자 페이지 안정화

---

## GRW-04. 프런트엔드 구조와 데이터 흐름 문서 수집

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add frontend routes and data flow source of truth`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

프런트 README가 사실상 비어 있으므로 Agent가 페이지 구조와 상태 흐름을 이해할 공식 문서가 없다. 특히 랭킹 조회 하네스를 붙이려면 어떤 페이지가 어떤 API를 쓰는지 먼저 문서로 고정해야 한다.

### 이 PR에서 해야 할 일

- 라우트 맵 작성
- 랭킹 페이지 상태 흐름 문서화
- 사용자 상세 모달 흐름 문서화
- auth callback 흐름 문서화
- 주요 env 변수와 외부 의존성 정리

### 산출물

- routes 문서
- ranking read data flow 문서
- env reference 문서

### 완료 기준

- “랭킹 페이지는 어디서 데이터를 받고 어떤 상태를 바꾸는가”가 문서로 설명되어야 한다

### 검증

- 문서 리뷰
- 실제 코드 경로와 대조

### 다음 작업과의 연결

- `GRC-04`
- `GRW-06`

---

## GRW-S02. core planning/parallel-agent skill pack v1

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add core planning and parallel-agent skill pack`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

source of truth 문서가 생겨도, 병렬 에이전트가 매번 같은 방식으로 작업을 쪼개고 계약을 동기화하고 실행 계획을 만드는 것은 별도의 문제다. 이 단계에서는 “작업을 시작하는 skill”을 먼저 만든다.

이 skill들은 코드 구현용 skill이 아니라, 병렬 작업과 cross-repo 작업을 흔들림 없이 시작하기 위한 coordination skill이다.

### 이 PR에서 해야 할 일

- 아래 core skill을 v1로 작성한다
  - `issue-to-exec-plan`
    - 목적: issue를 실행 가능한 `docs/exec-plans/active/*.md`로 변환
  - `parallel-work-split`
    - 목적: 여러 agent가 동시에 작업할 때 write set, ownership, merge 위험을 나누기
  - `api-contract-sync`
    - 목적: backend contract 변경 시 workflow docs/generated와 frontend 타입 반영 절차 고정
- 각 skill에 입력/출력 예시를 1개 이상 넣는다
- 각 skill에 “병렬 수행 시 금지 사항”을 적는다
- skill index 문서에 추천 사용 시점을 연결한다

### 이번 PR에서 하지 않을 일

- ranking harness execution skill 작성
- batch triage skill 작성

### 산출물

- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/parallel-work-split/SKILL.md`
- `.codex/skills/api-contract-sync/SKILL.md`

### 완료 기준

- 새로운 issue를 받았을 때 어떤 skill로 exec plan을 만들고, 어떤 skill로 병렬 분할하며, 어떤 skill로 계약 변경을 동기화할지 바로 고를 수 있어야 한다
- skill마다 입력/출력과 금지 사항이 명확해야 한다

### 검증

- skill 문서 리뷰
- 가상의 sample issue로 exec plan 변환 시뮬레이션
- contract-sync 체크리스트 점검

### 다음 작업과의 연결

- `GRB-01`
- `GRC-01`
- 이후 병렬 작업 전반

---

## GRB-02. 백엔드 검증 루프 hardening과 Docker preflight 추가

- 저장소: `git-ranker`
- 권장 PR 제목: `build: harden backend verification loop and docker preflight`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

현재 integration test는 Docker daemon이 없을 때도 단순한 Testcontainers 예외만 남긴다. 사람은 해석할 수 있어도 Agent는 원인을 오판하기 쉽다. “환경 문제”와 “코드 문제”를 분리하는 것이 중요하다.

### 이 PR에서 해야 할 일

- Docker 준비 상태 preflight 추가
- integration test 실패 원인을 더 친절하게 노출
- 검증 명령을 정리한다
  - unit
  - coverage
  - integration
- README 또는 workflow 문서에서 backend verify 절차를 명시한다

### 산출물

- preflight 스크립트 또는 Gradle task
- 검증 절차 문서

### 완료 기준

- Docker가 없을 때 “왜 실패했는지”가 명확히 보인다
- Docker가 준비된 환경에서는 통합 테스트 실행 경로가 분명하다

### 검증

- Docker 미기동 환경에서 메시지 확인
- Docker 기동 환경에서 `./gradlew integrationTest` 재검증

### 다음 작업과의 연결

- `GRW-05`
- `GRB-03`

---

## GRC-02. 프런트엔드 lint debt 1차 정리

- 저장소: `git-ranker-client`
- 권장 PR 제목: `refactor: reduce critical frontend lint debt`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

현재 lint는 통과하지만 핵심 규칙이 warning으로 쌓여 있다. 이렇게 되면 이후 Agent가 새로운 경고를 추가해도 구분이 어렵고, 코드 품질 경계가 모호해진다.

### 이 PR에서 해야 할 일

- 우선순위 높은 경고부터 줄인다
  - `react-hooks/set-state-in-effect`
  - `react-hooks/static-components`
  - `react-hooks/purity`
  - `react-hooks/use-memo`
- 랭킹 조회와 직접 관련된 화면부터 정리한다
  - ranking page
  - user profile
  - badge generator
  - auth hydration
- 명백한 dead import, `any`, impure render 제거

### 이번 PR에서 하지 않을 일

- 디자인 개편
- 테스트 도입

### 산출물

- warning 감소
- 핵심 화면 코드 정리

### 완료 기준

- 랭킹/유저/배지 관련 핵심 경로에서 correctness 관련 warning이 없어야 한다
- lint 신호 품질이 이전보다 명확히 좋아져야 한다

### 검증

- `npm run lint`
- 변경 화면 수동 확인

### 다음 작업과의 연결

- `GRC-03`
- `GRC-04`

---

## GRC-03. 프런트 build/runtime 하네스 친화화

- 저장소: `git-ranker-client`
- 권장 PR 제목: `chore: make frontend build harness-friendly`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

격리 환경이나 CI에서 외부 네트워크 의존성이 있으면 하네스 재현성이 떨어진다. 또한 deprecated runtime convention은 장기 운영 시 noise가 된다.

### 이 PR에서 해야 할 일

- `JetBrains Mono`를 로컬 폰트로 전환
- `middleware.ts`를 `proxy.ts`로 전환
- 빌드에 필요한 전제조건을 README 또는 workflow 문서에 정리
- 외부 의존성 목록을 문서에 반영

### 산출물

- 로컬 폰트 기반 build
- deprecated convention 제거
- 빌드 전제조건 문서

### 완료 기준

- 외부 폰트 fetch 없이 build가 가능해야 한다
- deprecated middleware 경고가 사라져야 한다

### 검증

- `npm run build`
- 관련 runtime warning 확인

### 다음 작업과의 연결

- `GRW-05`
- `GRC-04`

---

## GRW-05. workflow 표준 검증 런타임 만들기

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `feat: add standard verification runtime for workflow`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

하네스는 사람마다 다른 로컬 환경에서 돌면 안 된다. 첫 단계에서는 일상 개발까지 모두 통제하지 않더라도, 적어도 검증 환경은 표준화되어야 한다.

### 이 PR에서 해야 할 일

- 최소 서비스로 구성된 표준 런타임 정의
  - backend
  - client
  - db
  - prometheus
  - loki
- `start`, `stop`, `reset`, `seed`, `verify` 명령 인터페이스를 정의
- 포트와 env 규칙을 문서화
- 런타임을 올리고 내리는 기본 가이드를 작성

### 이번 PR에서 하지 않을 일

- Playwright 시나리오 작성
- 배치 하네스 구현

### 산출물

- compose 또는 script
- runtime usage 문서

### 완료 기준

- 한 명령 흐름으로 랭킹 조회 검증 환경을 올릴 수 있어야 한다
- 이후 Playwright, LogQL, PromQL을 붙일 자리가 명확해야 한다

### 검증

- 서비스 기동 확인
- health endpoint 확인

### 다음 작업과의 연결

- `GRB-03`
- `GRC-04`
- `GRW-06`

---

## GRB-03. 랭킹 조회용 결정적 seed 데이터 지원

- 저장소: `git-ranker`
- 권장 PR 제목: `feat: add deterministic seed data for ranking harness`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

첫 하네스는 GitHub API나 실제 배치에 의존하면 안 된다. Agent가 수정 전후를 비교하려면 항상 같은 데이터로 같은 결과를 볼 수 있어야 한다.

### 이 PR에서 해야 할 일

- 랭킹 조회용 결정적 seed 데이터 도입
- 요구 조건:
  - 여러 티어가 포함될 것
  - 여러 페이지가 생길 정도의 데이터가 있을 것
  - 기대 순위가 문서로 명확할 것
- `ALL` 조회와 `tier` 필터 조회가 모두 검증 가능하도록 한다

### 산출물

- seed 로더
- seed fixture
- expected result 문서

### 완료 기준

- 동일 seed로 항상 동일 ranking order가 나와야 한다
- Playwright와 API smoke에서 이 데이터를 기준으로 검증 가능해야 한다

### 검증

- seed 후 `/api/v1/ranking`
- seed 후 `/api/v1/ranking?tier=...`

### 다음 작업과의 연결

- `GRC-04`
- `GRW-06`

---

## GRC-04. 랭킹 조회 Playwright 하네스 도입

- 저장소: `git-ranker-client`
- 권장 PR 제목: `test: add Playwright harness for ranking read path`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

랭킹 조회를 첫 하네스 대상으로 정한 이유는 작은 범위에서 “브라우저 상태 + API 응답 + 로그/메트릭”을 하나의 루프로 묶기 좋기 때문이다. 이 PR은 그중 브라우저 검증 축을 만든다.

### 이 PR에서 해야 할 일

- Playwright 설정 추가
- 첫 시나리오 구현
  - 랭킹 페이지 진입
  - 초기 목록 렌더링
  - tier filter 변경
  - pagination 이동
  - 사용자 상세 모달 진입
  - console error 없음
  - `/api/v1/ranking` 200 응답 확인
- trace, screenshot, video 보관 규칙을 문서화

### 이번 PR에서 하지 않을 일

- 전체 사용자 여정 자동화
- 인증 포함 시나리오

### 산출물

- Playwright 설정
- ranking read spec
- artifact 규칙

### 완료 기준

- ranking happy path가 자동화되어야 한다
- 최소 1개의 tier filter path가 자동화되어야 한다

### 검증

- Playwright 실행
- trace/screenshot 생성 확인

### 다음 작업과의 연결

- `GRW-06`

---

## GRW-06. 랭킹 조회 증거 수집 루프 추가

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `feat: add evidence loop for ranking harness`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

OpenAI식 하네스의 핵심은 테스트 결과만 보는 것이 아니다. 브라우저, 로그, 메트릭이 함께 맞아야 한다. 이 PR은 첫 하네스에 다중 신호 검증을 붙인다.

### 이 PR에서 해야 할 일

- ranking read 검증용 LogQL 쿼리 정의
- ranking read 검증용 PromQL 쿼리 정의
- Playwright artifact와 로그/메트릭 결과를 한 번에 요약하는 evidence summary 포맷 정의
- `.artifacts/<task-slug>/` 구조에 맞는 예시를 남긴다

### 산출물

- query 파일
- evidence summary 템플릿
- ranking harness verification 문서

### 완료 기준

- 한 번의 ranking harness 실행으로 아래 증거가 모두 남아야 한다
  - 브라우저 screenshot/trace
  - 로그 확인 결과
  - 메트릭 확인 결과
  - 최종 요약 markdown

### 검증

- ranking harness 1회 실행
- `.artifacts` 구조 점검

### 다음 작업과의 연결

- `GRW-07`
- 이후 badge/batch 하네스의 표준 패턴

---

## GRW-S03. ranking harness execution skill pack v1

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add ranking harness execution skill pack`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

랭킹 조회 하네스가 실제로 구성되면, 이 흐름은 앞으로 가장 자주 재실행되는 대표 검증 루프가 된다. 이런 작업은 문서로만 두기보다 skill로 승격해야 병렬 에이전트와 반복 작업에서 동일한 품질을 유지할 수 있다.

### 이 PR에서 해야 할 일

- 아래 skill을 v1로 작성한다
  - `ranking-read-harness`
    - 목적: 표준 런타임 기동, seed 적용, API smoke, Playwright, evidence 수집까지 한 흐름으로 실행
  - `playwright-browser-qa`
    - 목적: 브라우저 상태, 네트워크, console, screenshot/trace 수집 규칙 고정
  - `promql-logql-evidence`
    - 목적: ranking read 검증 시 확인할 쿼리와 결과 요약 형식 고정
- 각 skill에 필수 산출물 위치를 명시한다
- 각 skill에 실패 시 재진입 지점을 적는다
- `.artifacts/<task-slug>/` 구조와 연결되는 예시를 넣는다

### 이번 PR에서 하지 않을 일

- badge/batch skill 작성
- 새로운 Playwright 기능 확대

### 산출물

- `.codex/skills/ranking-read-harness/SKILL.md`
- `.codex/skills/playwright-browser-qa/SKILL.md`
- `.codex/skills/promql-logql-evidence/SKILL.md`

### 완료 기준

- ranking read 관련 반복 작업을 사람이 매번 새로 설명하지 않아도 skill만으로 실행 흐름이 전달되어야 한다
- 병렬 에이전트가 같은 evidence 규칙으로 결과를 남길 수 있어야 한다

### 검증

- skill 문서 리뷰
- ranking harness 1회 실행 후 skill 단계와 실제 산출물 대조

### 다음 작업과의 연결

- 랭킹 조회 회귀 검증 반복
- 이후 badge harness skill 작성의 기준 패턴

---

## GRW-07. 문서/계약/플랜 freshness 가드레일 추가

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `build: add freshness guardrails for docs contracts and plans`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

문서를 만들기만 하고 관리하지 않으면 금방 드리프트가 생긴다. Harness Engineering에서는 문서도 운영 대상이어야 한다.

### 이 PR에서 해야 할 일

- exec plan 필수 항목 검사
- generated contract 최신성 검사
- 문서 링크 유효성 검사
- 아티팩트 인덱스 규칙 정의
- 최소한의 CI 연결점 정의

### 산출물

- freshness check 스크립트
- 정책 문서

### 완료 기준

- stale contract, plan 누락, 링크 깨짐이 자동으로 드러나야 한다

### 검증

- 체크 스크립트 실행
- 일부 의도적 실패 케이스로 동작 확인

### 다음 작업과의 연결

- 이후 자율성 상승을 위한 governance 기반

---

## GRW-08. 배지 하네스 계획 문서 작성

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: define badge harness v1 plan`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

랭킹 조회 다음으로 작은 public read path는 배지 서빙이다. 입력과 출력이 명확하고, SVG와 cache behavior를 검증하기 좋다.

### 이 PR에서 해야 할 일

- badge endpoint 계약 문서화
- SVG 검증 포인트 정리
- cache header 확인 기준 정리
- badge request metric 확인 기준 정리
- failure path 최소 1개 정의

### 산출물

- badge harness v1 계획 문서

### 완료 기준

- 다음 구현 PR이 추가 질문 없이 시작 가능해야 한다

### 검증

- 계획 문서 리뷰

### 다음 작업과의 연결

- badge 하네스 구현 Issue

---

## GRW-09. 배치 하네스 계획 문서 작성

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: define batch harness v1 plan`
- 권장 크기: `S`

### 왜 이 작업을 해야 하는가

배치는 가장 배우고 싶은 영역 중 하나이지만, 첫 하네스로 바로 들어가기에는 복잡도가 높다. 문서로 범위를 먼저 고정하지 않으면 검증 루프가 흐려진다.

### 이 PR에서 해야 할 일

- 일일 배치 단계 문서화
- seed 전략 정의
- retry/skip/partial failure 시나리오 정의
- PromQL/LogQL 체크 포인트 정리
- 무엇을 자동화하고 무엇은 당분간 수동으로 둘지 결정

### 산출물

- batch harness v1 계획 문서
- daily batch runbook 초안

### 완료 기준

- 배치 하네스 구현을 작은 Issue로 다시 쪼갤 수 있는 수준이어야 한다

### 검증

- 문서 리뷰

### 다음 작업과의 연결

- batch harness 구현 Issue들

---

## GRW-S04. reliability/batch skill pack v1

- 저장소: `git-ranker-workflow`
- 권장 PR 제목: `docs: add reliability and batch skill pack`
- 권장 크기: `M`

### 왜 이 작업을 해야 하는가

배치와 장애 대응은 가장 배우고 싶은 영역이지만, 동시에 컨텍스트 손실과 판단 흔들림이 가장 크게 발생하는 영역이다. 배치 실패 분석, rate-limit 조사, 문서 정리 루프는 장기적으로 거의 반드시 반복된다.

따라서 이 단계에서는 reliability 관련 작업을 skill로 승격해, 이후 에이전트가 장애 분석과 문서 정리를 일관되게 수행할 수 있게 해야 한다.

### 이 PR에서 해야 할 일

- 아래 skill을 v1로 작성한다
  - `batch-failure-triage`
    - 목적: 배치 실패 시 로그, 메트릭, skip/retry 상태를 따라가며 원인을 분류
  - `github-rate-limit-investigation`
    - 목적: GitHub API rate-limit, retry, partial failure 조사 절차 고정
  - `doc-gardener`
    - 목적: source of truth 문서와 generated contract, exec plan의 드리프트를 주기적으로 정리
- 각 skill에 확인해야 할 최소 증거를 넣는다
- batch/runbook 문서와 연결 링크를 추가한다

### 이번 PR에서 하지 않을 일

- 실제 batch harness 구현
- 장애 자동 복구 로직 추가

### 산출물

- `.codex/skills/batch-failure-triage/SKILL.md`
- `.codex/skills/github-rate-limit-investigation/SKILL.md`
- `.codex/skills/doc-gardener/SKILL.md`

### 완료 기준

- 배치 실패나 문서 드리프트 같은 반복 운영 작업을 동일한 절차로 재사용할 수 있어야 한다
- 신뢰성 관련 작업을 병렬 에이전트에게 넘길 때 필요한 입력/출력/증거가 고정되어 있어야 한다

### 검증

- skill 문서 리뷰
- 가상의 batch failure 사례를 기준으로 triage checklist 시뮬레이션
- doc-gardener checklist 점검

### 다음 작업과의 연결

- batch harness 구현
- 운영성/드리프트 정리 루프 자동화

---

## 7. 공통 Definition of Done

각 작업은 아래 항목을 최대한 충족해야 한다.

- 왜 이 작업이 필요한지 문서나 PR 본문에 남아 있다
- 변경 범위가 한 가지 목표에 집중되어 있다
- 검증 명령이 PR에 남아 있다
- 후속 작업의 전제조건이 명확하다
- source of truth 문서가 함께 업데이트되었거나, 업데이트 불필요 사유가 명시되어 있다
- 동일 작업이 반복될 가능성이 높다면 skill화 여부가 검토되었거나, 아직 만들지 않는 이유가 남아 있다

하네스 관련 작업은 아래도 추가로 본다.

- 브라우저, 로그, 메트릭 중 이번 PR에서 다룬 신호가 무엇인지 명확하다
- 증거 산출 위치가 정해져 있다
- 실패 시 어떤 루프로 다시 수정할지 문서화되어 있다

---

## 8. 바로 다음에 시작하는 것을 추천하는 작업

현재 시점에서 가장 먼저 시작하기 좋은 작업은 아래 두 개다.

1. `GRW-01`
   - 이유: 모든 문서와 계획의 자리부터 정리해야 이후 작업이 누적될 수 있다
2. `GRW-S01`
   - 이유: 이후 병렬 에이전트 운영과 반복 작업에 사용할 skill의 형식부터 먼저 고정하는 편이 좋다
3. `GRC-01`
   - 이유: 프런트엔드 계약 드리프트는 이미 존재하는 문제라, 나중으로 미루면 이후 하네스 작업 전반을 오염시킬 가능성이 높다

셋 중 하나만 먼저 한다면 `GRW-01`을 우선 추천한다.

이유:

- workflow 저장소가 먼저 컨트롤 플레인 역할을 가져야 이후 작업 결과를 정리할 자리가 생긴다
- 이후의 모든 Issue/PR 설명과 증거 보관 규칙도 여기서 시작된다
- skill도 결국 workflow 저장소 안에서 관리될 것이므로, skeleton이 먼저 있어야 한다

---

## 9. 이후 문서 확장 방향

이 문서는 roadmap 역할을 한다. 이후에는 아래 문서들이 분리되어 추가되는 것이 좋다.

- `docs/exec-plans/active/<task>.md`
- `docs/domain/scoring.md`
- `docs/domain/tiering.md`
- `docs/operations/ranking-read-harness.md`
- `docs/operations/badge-harness.md`
- `docs/operations/batch-harness.md`
- `docs/quality-score/agent-readiness-scorecard.md`
- `.codex/skills/<skill-name>/SKILL.md`

즉, 이 문서는 전체 지도를 제공하고, 개별 작업의 실행 계획은 별도 문서로 분리해가는 구조가 바람직하다.
