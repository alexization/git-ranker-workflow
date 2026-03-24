# Work Item Catalog

이 문서는 초기 roadmap의 상세 작업 목록을 디렉터리 구조에 맞게 다시 정리한 1차 작업 카탈로그다. 이후 작업은 이 문서와 관련 source of truth 문서를 읽고 `docs/exec-plans/active/`에 개별 실행 문서를 만든 뒤 진행한다.

## 사용 순서

1. [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 읽는다.
2. 아래에서 해당 Issue 항목을 읽고 선행조건, write scope, 기본 결정을 확인한다.
3. `docs/exec-plans/active/YYYY-MM-DD-<issue-id-lower>-<slug>.md`를 만든다.
4. 작업 후에는 문서를 `docs/exec-plans/completed/`로 이동한다.

## Workflow Track

### GRW-01. workflow skeleton과 문서 규칙 만들기

- 저장소: `git-ranker-workflow`
- 선행조건: 없음
- 권장 write scope: 루트, `docs/`, `.gitignore`
- 기본 결정: 문서 기본 언어는 한국어로 한다. `AGENTS.md`는 짧은 인덱스 문서로 만들고, 상세 규칙은 `docs/`로 보낸다. `PLANS.md`는 실행 계획 상태 규칙과 naming 규칙만 담는다. 실제 스크립트는 추가하지 않는다.
- 핵심 작업: 루트 인덱스 문서 추가, docs 트리 생성, `.artifacts/` 규칙 문서화, 작업 슬러그와 evidence 규칙 정리
- 비범위: 실제 하네스 스크립트 작성, 앱 저장소 문서 본문 작성, PromQL/LogQL 쿼리 추가
- 산출물: `AGENTS.md`, `PLANS.md`, docs 트리, 아티팩트/슬러그 규칙 문서
- 검증: `find docs -maxdepth 3 -type d | sort`, `cat AGENTS.md`, `cat PLANS.md`

### GRW-02. 현재 readiness 기준선 문서화

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`
- 권장 write scope: `docs/quality-score`, `docs/references`
- 기본 결정: readiness 평가는 `1~5 점수 + Low/Medium/High + 핵심 리스크 요약` 형식으로 통일한다. 실제 확인한 명령과 날짜를 함께 남긴다.
- 핵심 작업: 세 저장소 상태를 문서화, 문서화/테스트/정적 가드레일/API 계약/운영 재현성/관측 가능성/Agent 탐색 가능성 점검
- 비범위: 코드 수정
- 산출물: readiness review 문서, 점수표 또는 상태표
- 검증: 문서 리뷰와 실제 명령 결과 대조

### GRW-03. 백엔드 도메인/운영 문서를 workflow에 수집

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`
- 권장 write scope: workflow 문서만
- 기본 결정: 코드 내용을 복붙하지 말고, 규칙과 흐름을 행동 중심으로 요약한다. 필요한 경우 backend 코드 경로를 참조 링크로 남긴다.
- 핵심 작업: 점수 계산, 티어 판정, 랭킹 조회, 배지 서빙, 수동 갱신, 일일 배치, GitHub API 실패 정책, 주요 로그/메트릭 문서화
- 비범위: backend 코드 수정
- 산출물: `docs/domain/*`, `docs/operations/*`
- 검증: 문서와 실제 코드 경로 교차 검토

### GRW-04. 프런트엔드 구조와 데이터 흐름 문서 수집

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`
- 권장 write scope: workflow 문서만
- 기본 결정: 라우트 문서는 `route`, `사용 API`, `주요 상태`, `env`, `외부 의존성`을 포함한 표 형식으로 정리한다.
- 핵심 작업: 라우트 맵, 랭킹 페이지 상태 흐름, 사용자 상세 모달 흐름, auth callback 흐름, 주요 env와 외부 의존성 정리
- 비범위: 프런트엔드 코드 수정
- 산출물: routes 문서, ranking read data flow 문서, env reference 문서
- 검증: 문서 리뷰와 실제 코드 경로 대조

### GRW-05. workflow 표준 검증 런타임 만들기

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`, `GRB-02`, `GRC-03` 권장
- 권장 write scope: workflow runtime 파일만
- 기본 결정: 구현 기본값은 `docker compose + 얇은 스크립트`다. 목표는 검증 런타임 표준화이지, 운영 환경 완전 복제는 아니다.
- 핵심 작업: backend/client/db/prometheus/loki 최소 런타임 정의, `start/stop/reset/seed/verify` 인터페이스 정의, 포트와 env 규칙 문서화
- 비범위: Playwright 시나리오 작성, 배치 하네스 구현
- 산출물: compose 또는 script, runtime usage 문서
- 검증: 서비스 기동과 health endpoint 확인

### GRW-06. 랭킹 조회 증거 수집 루프 추가

- 저장소: `git-ranker-workflow`
- 선행조건: `GRC-04`
- 권장 write scope: workflow query/template/doc 파일만
- 기본 결정: query 저장 위치는 workflow 내부로 고정한다. evidence summary는 브라우저, 로그, 메트릭, 최종 판정을 같은 템플릿으로 남긴다.
- 핵심 작업: LogQL/PromQL 쿼리 정의, evidence summary 포맷 정의, `.artifacts/<task-slug>/` 예시 정리
- 비범위: 새 런타임 발명
- 산출물: query 파일, evidence summary 템플릿, ranking harness verification 문서
- 검증: ranking harness 1회 실행 후 `.artifacts` 구조 점검

### GRW-07. 문서/계약/플랜 freshness 가드레일 추가

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`
- 권장 write scope: workflow check/script/doc 파일만
- 기본 결정: 처음부터 모든 것을 hard fail로 막지 않는다. 다만 broken link, stale contract 같은 명확한 오류는 fail 대상으로 본다.
- 핵심 작업: exec plan 필수 항목 검사, generated contract 최신성 검사, 문서 링크 검사, 아티팩트 인덱스 규칙, 최소 CI 연결점 정의
- 비범위: 과도한 governance 자동화
- 산출물: freshness check 스크립트, 정책 문서
- 검증: 체크 스크립트 실행과 의도적 실패 케이스 확인

### GRW-08. 배지 하네스 계획 문서 작성

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-03` 권장
- 권장 write scope: planning 문서만
- 기본 결정: 구현이 아니라 계획 문서 작성 Issue다. 결과 문서의 기본 섹션은 `목표`, `수용 기준`, `런타임`, `증거`, `리스크`, `다음 구현 단위`로 고정한다.
- 핵심 작업: badge endpoint 계약, SVG 검증 포인트, cache header 기준, metric 확인 기준, failure path 1개 정의
- 비범위: 구현
- 산출물: badge harness v1 계획 문서
- 검증: 계획 문서 리뷰

### GRW-09. 배치 하네스 계획 문서 작성

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-03` 권장
- 권장 write scope: planning 문서만
- 기본 결정: 구현이 아니라 계획 문서 작성 Issue다. 배치 계획은 `happy path`, `retry/skip`, `partial failure`, `metrics/logs`, `seed/data isolation`까지 적어야 한다.
- 핵심 작업: 일일 배치 단계, seed 전략, retry/skip/partial failure 시나리오, PromQL/LogQL 체크 포인트, 자동화/수동 범위 결정
- 비범위: 구현
- 산출물: batch harness v1 계획 문서, daily batch runbook 초안
- 검증: 문서 리뷰

## Skill Track

### GRW-S01. skill registry와 template 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-01`
- 권장 write scope: `skills/` 하위만
- 기본 결정: skill은 문서형 자산부터 시작하고, 처음부터 실행 스크립트를 넣지 않는다. 각 skill 폴더의 필수 파일은 `SKILL.md` 하나다.
- 핵심 작업: `skills/` 구조, `skills/README.md`, `skills/_template/SKILL.md`, 지원 파일 규칙과 naming 규칙 정의
- 비범위: ranking/batch skill 본문 작성
- 산출물: skill index, template, authoring 규칙 문서
- 검증: `find skills -maxdepth 2 -type f | sort`, 핵심 문서 내용 확인

### GRW-S02. core planning/parallel-agent skill pack v1

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-S01`, `GRW-03`, `GRW-04` 권장
- 권장 write scope: `skills/` 하위만
- 기본 결정: coordination skill만 작성한다. 코드 생성이나 검증 실행 skill은 아직 넣지 않는다. 각 skill에는 병렬 수행 시 ownership 규칙을 반드시 적는다.
- 핵심 작업: `issue-to-exec-plan`, `parallel-work-split`, `api-contract-sync` 문서 작성과 예시 추가
- 비범위: ranking harness execution skill 작성
- 산출물: 세 개의 core skill 문서
- 검증: 문서 리뷰와 sample issue 시뮬레이션

### GRW-S03. ranking harness execution skill pack v1

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-S01`, `GRC-04`, `GRW-06`
- 권장 write scope: `skills/` 하위만
- 기본 결정: 이미 만들어진 runtime/query/test를 재사용하는 설명서여야 한다. 새 인프라를 발명하지 않는다.
- 핵심 작업: `ranking-read-harness`, `playwright-browser-qa`, `promql-logql-evidence` skill 문서 작성
- 비범위: badge/batch skill 작성
- 산출물: 세 개의 ranking harness skill 문서
- 검증: skill 단계와 실제 산출물 대조

### GRW-S04. reliability/batch skill pack v1

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-S01`, `GRW-09` 권장
- 권장 write scope: `skills/` 하위만
- 기본 결정: reliability skill은 체크리스트 중심으로 시작한다. 자동 복구나 자동 triage 구현은 이 Issue의 범위가 아니다.
- 핵심 작업: `batch-failure-triage`, `github-rate-limit-investigation`, `doc-gardener` skill 문서 작성
- 비범위: 실제 batch harness 구현, 장애 자동 복구
- 산출물: reliability/batch skill 문서
- 검증: 가상 failure 사례와 checklist 시뮬레이션

## Backend Track

### GRB-01. 백엔드 OpenAPI 계약 생성 기반 만들기

- 저장소: `git-ranker`
- 선행조건: 없음
- 권장 write scope: backend build/config/doc 관련 파일만
- 기본 결정: API 동작 변경은 하지 않는다. 목표는 OpenAPI를 생성할 수 있는 기반 추가다. 산출 형식은 가능하면 `JSON`을 기본으로 하고, `YAML`은 비용이 적을 때만 함께 낸다.
- 핵심 작업: `/api/v1/ranking`, `/api/v1/users/{username}`, `/api/v1/users/{username}/refresh`, `/api/v1/auth/*`, `/api/v1/badges/*`를 포함한 OpenAPI 생성 기반 추가
- 비범위: 프런트엔드 generated client 생성
- 산출물: OpenAPI 생성 설정, 산출물 경로, 생성 절차 문서
- 검증: OpenAPI 생성 명령 실행과 주요 엔드포인트 확인

### GRB-02. 백엔드 검증 루프 hardening과 Docker preflight 추가

- 저장소: `git-ranker`
- 선행조건: 없음
- 권장 write scope: Gradle/test/doc 관련 파일만
- 기본 결정: Docker가 없을 때 테스트를 조용히 skip하지 말고 명확히 fail-fast 한다. 목표는 환경 문제와 코드 문제를 구분 가능하게 만드는 것이다.
- 핵심 작업: Docker preflight 추가, integration test 오류 메시지 개선, unit/coverage/integration 검증 절차 정리
- 비범위: 기능 변경
- 산출물: preflight 스크립트 또는 Gradle task, 검증 절차 문서
- 검증: Docker 미기동/기동 환경 각각 확인

### GRB-03. 랭킹 조회용 결정적 seed 데이터 지원

- 저장소: `git-ranker`
- 선행조건: `GRW-05` 권장
- 권장 write scope: backend seed/bootstrap 관련 파일만
- 기본 결정: GitHub API에 의존하지 않는 결정적 데이터가 핵심이다. seed 방식은 반복 실행해도 동일 결과가 나오는 방식을 우선한다.
- 핵심 작업: 여러 티어와 여러 페이지를 포함하는 결정적 seed 데이터와 기대 순위 문서화
- 비범위: 실제 GitHub 연동 검증
- 산출물: seed 로더, seed fixture, expected result 문서
- 검증: `/api/v1/ranking`과 tier 필터 응답 확인

## Client Track

### GRC-01. 프런트엔드 계약 타입 단일화

- 저장소: `git-ranker-client`
- 선행조건: `GRB-01` 권장
- 권장 write scope: `src/shared/types`, `src/shared/lib/validations`, 직접 소비자 파일만
- 기본 결정: 서버 응답 타입은 단일 기준만 남긴다. 이 단계에서는 전체 컴포넌트 리팩터링보다 계약 중복 제거가 우선이다. `EMERALD` 누락 같은 enum drift를 먼저 해결한다.
- 핵심 작업: `src/shared/types/api.ts`, `src/shared/lib/validations.ts`의 중복 제거와 단일 계약 경로 정리
- 비범위: 전체 컴포넌트 리팩터링, Playwright 도입
- 산출물: 단일 계약 타입 경로, drift 제거
- 검증: `npx tsc --noEmit`

### GRC-02. 프런트엔드 lint debt 1차 정리

- 저장소: `git-ranker-client`
- 선행조건: `GRC-01` 권장
- 권장 write scope: ranking/user/badge/auth 관련 파일 우선
- 기본 결정: 전체 warning zero를 한 번에 달성하려 하지 않는다. correctness 위험이 큰 경고부터 제거한다. UI 스타일 변경은 목적이 아니다.
- 핵심 작업: `react-hooks/set-state-in-effect`, `react-hooks/static-components`, `react-hooks/purity`, `react-hooks/use-memo` 등 우선순위 높은 경고 감소
- 비범위: 디자인 개편, 테스트 도입
- 산출물: warning 감소, 핵심 화면 코드 정리
- 검증: `npm run lint`, 변경 화면 수동 확인

### GRC-03. 프런트 build/runtime 하네스 친화화

- 저장소: `git-ranker-client`
- 선행조건: `GRC-02` 권장
- 권장 write scope: font/runtime config/readme 관련 파일만
- 기본 결정: 외부 네트워크 의존성을 줄이는 것이 핵심이다. 디자인 변경보다 build 재현성 확보가 우선이다.
- 핵심 작업: 로컬 폰트 전환, `middleware.ts`를 `proxy.ts`로 전환, 빌드 전제조건과 외부 의존성 문서화
- 비범위: UI 개편
- 산출물: 로컬 폰트 기반 build, deprecated convention 제거, 빌드 전제조건 문서
- 검증: `npm run build`

### GRC-04. 랭킹 조회 Playwright 하네스 도입

- 저장소: `git-ranker-client`
- 선행조건: `GRW-05`, `GRB-03`
- 권장 write scope: Playwright 설정, 테스트, 필요 최소한의 test hook
- 기본 결정: Playwright 설정은 client 저장소에 둔다. artifact 위치는 workflow와 연결 가능하게 하되, UI 변경 없이 테스트 가능하면 test id를 남발하지 않는다.
- 핵심 작업: 랭킹 페이지 진입, 초기 목록 렌더링, tier filter 변경, pagination 이동, 사용자 상세 모달 진입, console error 없음, `/api/v1/ranking` 200 응답 확인
- 비범위: 전체 사용자 여정 자동화, 인증 포함 시나리오
- 산출물: Playwright 설정, ranking read spec, artifact 규칙
- 검증: Playwright 실행과 trace/screenshot 생성 확인

## 참고

- 공통 운영 규칙과 Definition of Done은 [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.
- 이 카탈로그는 1차 정규화 버전이다. 실제 작업 착수 시에는 issue별 exec plan에 범위와 리스크를 다시 고정한다.
