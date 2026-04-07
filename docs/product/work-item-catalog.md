# Work Item Catalog

이 문서는 현재 하네스 시스템 구축을 위한 작업 카탈로그다. 모든 작업은 `요청 라우팅`, `컨텍스트 제한`, `도구 경계`, `결정론적 검증`, `구현/리뷰 Agent 분리`, `실패의 가드레일화`를 차례로 고정하는 방향으로 진행한다.

## 사용 순서

1. [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 읽는다.
2. 아래에서 해당 Issue 항목의 선행조건, write scope, 기본 결정을 확인한다.
3. `docs/exec-plans/active/YYYY-MM-DD-<issue-id-lower>-<slug>.md`를 만든다.
4. 작업 후에는 문서를 `docs/exec-plans/completed/`로 이동한다.

## Workflow Track

### GRW-19. Harness issue/PR template 정렬

- 저장소: `git-ranker-workflow`
- 선행조건: 없음
- 권장 write scope: `.github/`, `docs/operations/`, `docs/product/`, `docs/exec-plans/`
- 기본 결정: Issue/PR template은 앞으로 사용할 하네스 기준만 담는다. 요청 intake, write scope, verification contract, 독립 review, feedback follow-up을 공통 필드로 강제한다.
- 핵심 작업: workflow Issue template, PR template, governance 문서, roadmap/catalog 선행 순서를 현재 하네스 기준으로 정렬한다.
- 비범위: backend/frontend 코드 변경, GitHub Actions 구현
- 산출물: 업데이트된 GitHub templates, 관련 governance/source of truth 반영
- 검증: template 본문 리뷰와 필수 섹션 grep 확인

### GRW-10. 하네스 기준 정렬

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-19`
- 권장 write scope: `docs/product`, `docs/architecture`, `docs/operations`, `.codex/skills/README`, `docs/exec-plans`
- 기본 결정: 현재 기준 문서는 앞으로 사용할 하네스 흐름만 설명한다. 구현 Agent와 review Agent의 역할 분리를 초기 기준으로 넣는다.
- 핵심 작업: roadmap, catalog, index, 운영 문서의 방향을 현재 하네스 기준으로 정렬하고 다음 Issue 진입 기준을 고정한다.
- 비범위: backend/frontend 코드 변경, CI 구현
- 산출물: 업데이트된 source of truth와 후속 Issue 진입 기준
- 검증: 관련 문서 간 용어와 흐름 정렬 검토

### GRW-11. 하네스 시스템 맵과 상태 머신 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-10`
- 권장 write scope: `docs/architecture`, 필요 시 `docs/README.md`
- 기본 결정: 목표 흐름은 `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback`으로 고정한다.
- 핵심 작업: 시스템 구성요소, 상태 전이, stop condition, pass/fail semantics, 역할 분리 원칙을 문서화한다.
- 비범위: skill 작성, CI 구현
- 산출물: 하네스 시스템 맵 문서, 상태 머신 정의
- 검증: flow와 state가 issue/PR workflow에 그대로 투영 가능한지 문서 리뷰

### GRW-12. 요청 라우팅과 ambiguity interview 정책 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-11`
- 권장 write scope: `docs/operations`, 필요 시 루트 운영 문서
- 기본 결정: 모호한 요청은 바로 구현으로 보내지 않는다. 인터뷰는 요구사항을 줄이는 방향으로 수행한다.
- 핵심 작업: 요청 분류 기준, 모호성 판단 규칙, 인터뷰 종료 조건, 일반 대화 fallback, 즉시 실행 가능한 작업의 기준을 문서화한다.
- 비범위: 새로운 에이전트 런타임 구현
- 산출물: request routing policy, ambiguity interview policy
- 검증: 예시 요청 3~5개를 분류해 정책이 일관되게 적용되는지 검토

### GRW-13. context pack registry와 task-to-context 매핑 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-11`, `GRW-12`
- 권장 write scope: `docs/architecture`, `docs/domain`, `docs/operations`
- 기본 결정: 컨텍스트는 task type 기준으로 최소 공개한다. `backend 수정`, `frontend 수정`, `workflow 문서 수정`, `cross-repo planning`은 서로 다른 context pack을 사용한다.
- 핵심 작업: task type별 필수 문서, 선택 문서, 금지 컨텍스트, hot file 탐색 기준을 정의한다.
- 비범위: 자동 context loader 구현
- 산출물: context pack registry, task-to-context mapping 표
- 검증: 대표 task에 대해 과도한 문서 로딩 없이 필요한 판단이 가능한지 시뮬레이션

### GRW-14. tool boundary matrix와 write scope 거버넌스 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-11`, `GRW-13`
- 권장 write scope: `docs/operations`, `docs/architecture`, 필요 시 `AGENTS.md`
- 기본 결정: 프롬프트 제약보다 도구 경계를 우선한다. cross-repo 작업은 기본적으로 문서 PR과 앱 코드 PR로 분리한다.
- 핵심 작업: task type별 read/write/network/escalation 허용 범위, 위험 명령 금지 규칙, write scope 템플릿을 정의한다.
- 비범위: 샌드박스 구현 변경
- 산출물: tool boundary matrix, 갱신된 write scope 규칙
- 검증: 대표 task별 허용/금지 사례 검토

### GRW-15. verification contract registry와 repair loop 기준 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-11`
- 권장 write scope: `docs/operations`, `docs/architecture`, 필요 시 `docs/product`
- 기본 결정: 완료 판정은 저장소별 명시된 명령이 내린다. 검증 결과는 review Agent에게 전달 가능한 형식으로 남겨야 한다.
- 핵심 작업: `workflow`, `backend`, `frontend`별 기본 검증 명령, 실패 시 repair loop 입력 형식, 최대 재시도 기준, stop condition을 정의한다.
- 비범위: 테스트 프레임워크 추가
- 산출물: verification contract registry, repair loop policy
- 검증: 각 저장소의 현재 명령으로 registry 초안을 채울 수 있는지 확인

### GRW-16. dual-agent review policy 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-11`, `GRW-15`
- 권장 write scope: `docs/operations`, `docs/architecture`, `.codex/skills` 필요 시
- 기본 결정: 구현 Agent는 자기 자신의 결과를 최종 승인할 수 없다. review Agent는 구현 컨텍스트와 분리된 검토 관점으로 동작한다.
- 핵심 작업: implementer/reviewer 책임 분리, reviewer 입력 형식, review 통과 조건, 수정 요청 루프, review evidence 규칙을 정의한다.
- 비범위: 자동 PR 리뷰 봇 구현
- 산출물: dual-agent review policy, review checklist 초안
- 검증: 샘플 diff와 검증 결과를 기준으로 reviewer 흐름 시뮬레이션

### GRW-17. failure-to-guardrail feedback loop 정의

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-12`, `GRW-14`, `GRW-15`, `GRW-16`
- 권장 write scope: `docs/operations`, `.codex/skills`, 필요 시 `docs/references`
- 기본 결정: 반복 실패는 반드시 `문서 규칙`, `skill`, `테스트`, `CI`, `template` 중 하나로 승격할지 판단한다.
- 핵심 작업: 실패 taxonomy, feedback ledger 포맷, 가드레일 후보 승격 규칙, no-op 기준을 정의한다.
- 비범위: 자동 PR 생성, 자동 복구
- 산출물: feedback loop policy, guardrail ledger template
- 검증: 과거 실패 사례 2~3개를 분류해 ledger에 적합한지 확인

### GRW-18. workflow repo pilot issue로 새 흐름 1회 검증

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-12`, `GRW-13`, `GRW-14`, `GRW-15`, `GRW-16`
- 권장 write scope: pilot 대상 문서, `docs/exec-plans`, `.artifacts/` 필요 시
- 기본 결정: 첫 pilot은 문서 또는 규칙 변경처럼 브라우저 자동화가 없어도 되는 작업으로 시작한다.
- 핵심 작업: 실제 Issue 하나를 새 라우팅, context pack, boundary, verification, review, feedback 흐름으로 끝까지 수행한다.
- 비범위: backend/frontend 기능 개발
- 산출물: pilot exec plan, verification 결과, review 결과, feedback ledger entry
- 검증: 새 흐름만으로 작업이 끝까지 닫히는지 확인

## Skill Track

### GRW-S06. intake/ambiguity skill pack

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-12`
- 권장 write scope: `.codex/skills/` 하위만
- 기본 결정: skill은 라우팅과 인터뷰 절차를 고정하는 문서형 자산으로 시작한다.
- 핵심 작업: `request-intake`, `ambiguity-interview` skill 작성
- 비범위: 실행 런타임 추가
- 산출물: skill 문서 2개, 갱신된 skill registry
- 검증: 예시 요청을 skill 입력/출력 형식에 맞춰 시뮬레이션

### GRW-S07. context-pack/boundary skill pack

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-13`, `GRW-14`
- 권장 write scope: `.codex/skills/` 하위만
- 기본 결정: context pack 선택과 write scope 검토를 분리된 반복 절차로 만든다.
- 핵심 작업: `context-pack-selection`, `boundary-check` skill 작성
- 비범위: 자동 context 수집기 구현
- 산출물: skill 문서 2개
- 검증: 대표 task에서 필요한 문서와 금지 범위를 일관되게 뽑는지 검토

### GRW-S08. verification/review-loop skill pack

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-15`, `GRW-16`
- 권장 write scope: `.codex/skills/` 하위만
- 기본 결정: 구현 완료 선언보다 검증과 review handoff를 우선한다. 저장소별 명령은 contract registry가 canonical source다.
- 핵심 작업: `verification-contract-runner`, `repair-loop-triage`, `reviewer-handoff` skill 작성
- 비범위: 테스트 프레임워크 추가
- 산출물: skill 문서 3개
- 검증: 실패 로그와 diff를 입력으로 triage와 review handoff가 재현되는지 확인

### GRW-S09. guardrail-hardening skill pack

- 저장소: `git-ranker-workflow`
- 선행조건: `GRW-17`
- 권장 write scope: `.codex/skills/` 하위만
- 기본 결정: 같은 실패가 2번 이상 반복되면 가드레일 승격을 우선 검토한다.
- 핵심 작업: `guardrail-ledger-update`, `failure-to-policy` skill 작성
- 비범위: 자동 CI 생성
- 산출물: skill 문서 2개, ledger update checklist
- 검증: 과거 실패 사례를 기준으로 승격 판단이 가능한지 검토

## Backend Track

### GRB-04. backend verification contract 정규화

- 저장소: `git-ranker`
- 선행조건: `GRW-15`
- 권장 write scope: backend 검증 문서, build/test entrypoint, 필요 최소한의 preflight
- 기본 결정: 행동 변경 없이 검증 명령과 실패 의미를 명확히 하는 것이 우선이다. 상위 completion semantics는 verification contract registry를 따른다.
- 핵심 작업: 현재 backend 검증 명령, fail-fast 조건, 환경 전제, 결과 해석 기준을 contract에 맞게 정리한다.
- 비범위: 새 기능 구현
- 산출물: backend verification contract, 필요한 문서/스크립트 정리
- 검증: contract에 적힌 명령과 실제 실행 결과 대조

## Client Track

### GRC-05. frontend verification contract 정규화

- 저장소: `git-ranker-client`
- 선행조건: `GRW-15`
- 권장 write scope: frontend 검증 문서, build/lint/typecheck entrypoint
- 기본 결정: `lint`, `typecheck`, `build`를 안정적인 완료 조건으로 먼저 고정한다. 상위 completion semantics는 verification contract registry를 따른다.
- 핵심 작업: 현재 frontend 검증 명령, 필수 env, 실패 의미, 수동 확인이 필요한 공백을 contract에 맞게 정리한다.
- 비범위: UI 개편
- 산출물: frontend verification contract, 필요한 문서/스크립트 정리
- 검증: contract에 적힌 명령과 실제 실행 결과 대조

## 참고

- 공통 운영 규칙과 Definition of Done은 [docs/operations/workflow-governance.md](../operations/workflow-governance.md)를 따른다.
- 새 작업의 기본 지시는 이 카탈로그와 active exec plan에서 읽는다.
