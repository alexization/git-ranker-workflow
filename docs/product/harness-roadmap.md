# Harness Roadmap

이 문서는 `git-ranker-workflow`의 현재 기준 하네스 로드맵이다. 목표는 AI Agent가 issue/PR 단위 작업을 수행할 때, 출발 조건과 읽을 정보와 수정 가능한 범위와 완료 판정이 모두 시스템으로 고정된 상태를 만드는 것이다.

## 목표

1. 사용자 요청이 들어오면 먼저 `대화`, `모호한 요청`, `즉시 실행 가능한 작업`으로 라우팅한다.
2. 실행 가능한 작업은 task type에 맞는 최소 컨텍스트와 명시적 write scope를 가진다.
3. 구현 Agent는 결정론적 검증 명령을 통과하기 전까지 작업 완료를 주장할 수 없다.
4. 코드 검토는 구현 Agent 자신이 아니라 별도의 review Agent가 수행한다.
5. 실패는 다음 문서, skill, 테스트, CI 가드레일로 축적된다.

## 이번 계획의 고정 결정

- 하네스의 중심 흐름은 `Router -> Interview -> Context Pack -> Implementer -> Verification -> Reviewer -> Feedback`이다.
- 모호한 요청은 구현 단계로 보내지 않고 인터뷰 정책으로 되돌린다.
- task type마다 읽을 문서와 수정 가능한 범위를 별도 context pack으로 고정한다.
- 완료 판정은 `결정론적 검증 통과`와 `별도 review Agent 승인`이 함께 있어야 한다.
- 구현 Agent와 review Agent는 역할을 분리한다.
- source of truth는 `workflow 중심`으로 유지하되, 앱 동작의 canonical source는 각 앱 저장소 코드와 테스트에 둔다.
- 새 작업은 항상 exec plan으로 고정한 뒤 시작한다.

## 목표 상태

사용자 요청 처리의 목표 상태는 아래와 같다.

1. 요청이 들어오면 라우터가 요청 유형을 먼저 분류한다.
2. 모호한 요청은 ambiguity interview 정책에 따라 정제한다.
3. 실행 가능한 작업만 exec plan으로 고정하고, 저장소와 write scope를 명시한다.
4. task type에 맞는 context pack만 Agent에 제공한다.
5. Implementer Agent는 허용된 도구 경계 안에서만 작업한다.
6. verification contract registry에 정의된 명령이 통과해야 다음 단계로 넘어간다.
7. Reviewer Agent는 [../operations/dual-agent-review-policy.md](../operations/dual-agent-review-policy.md)에 따라 구현 diff와 검증 결과를 검토하고, 통과 또는 수정 요청을 결정한다.
8. 실패한 작업은 feedback ledger에 남기고 다음 가드레일 후보로 전환한다.

## 권장 실행 순서

### Phase 1. Core Harness Control Plane

1. `GRW-19` Harness issue/PR template 정렬
2. `GRW-10` 하네스 기준 정렬
3. `GRW-11` 하네스 시스템 맵과 상태 머신 정의
4. `GRW-12` 요청 라우팅과 ambiguity interview 정책 정의
5. `GRW-13` context pack registry와 task-to-context 매핑 정의
6. `GRW-14` tool boundary matrix와 write scope 거버넌스 정의
7. `GRW-15` verification contract registry와 repair loop 기준 정의
8. `GRW-16` dual-agent review policy 정의
9. `GRW-17` failure-to-guardrail feedback loop 정의

### Phase 2. Skills and Pilot

10. `GRW-S06` intake/ambiguity skill pack
11. `GRW-S07` context-pack/boundary skill pack
12. `GRW-S08` verification/review-loop skill pack
13. `GRW-S09` guardrail-hardening skill pack
14. `GRW-18` workflow repo pilot issue로 새 흐름 1회 검증

### Phase 3. Repo-Specific Contracts

15. `GRB-04` backend verification contract 정규화
16. `GRC-05` frontend verification contract 정규화

## 바로 다음에 추천하는 작업

1. `GRW-10`
2. `GRW-11`
3. `GRW-12`
4. `GRW-15`
5. `GRW-16`

`GRW-10`을 먼저 권장하는 이유는 template 정렬 이후의 공식 용어와 운영 기준을 source of truth 전반에 맞춰야 이후 issue/PR workflow가 흔들리지 않기 때문이다.

`GRW-15`와 `GRW-16`을 초반에 올려둔 이유는, 실제 하네스 통제력은 "무엇이 완료인지"와 "누가 승인하는지"를 먼저 고정해야 생기기 때문이다.

## 사용 원칙

- 새 작업은 항상 `docs/exec-plans/active/`에 exec plan을 먼저 만든다.
- 모호한 요청은 구현이나 문서 수정으로 바로 넘기지 않는다.
- 컨텍스트 파일은 task type 기준으로 점진적으로 공개한다.
- 결정론적 검증 없이 Agent의 자기평가를 완료 근거로 삼지 않는다.
- 구현 Agent는 자기 자신의 결과를 최종 승인하지 않는다.
- 같은 실패가 반복되면 다음 턴에서는 가드레일이 하나 더 생겨야 한다.
