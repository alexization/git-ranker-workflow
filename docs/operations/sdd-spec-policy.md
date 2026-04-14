# SDD Spec Policy

이 문서는 Harness가 모든 즉시 실행 가능한 작업을 Spec-Driven Development 방식으로 수행할 때 따라야 하는 공통 규칙을 고정한다.

## Policy Invariants

- 모든 즉시 실행 가능한 작업은 구현 전에 spec을 먼저 만든다.
- spec은 요구사항, 하위 작업, write scope, verification, tracking 결정을 함께 소유하는 단일 canonical artifact다.
- 추가 planning 문서를 따로 만들지 않는다. 더 자세한 planning이 필요하면 spec을 더 구체화한다.
- 소크라테스 모드의 기본 규칙은 `답 내놓기 금지, 먼저 캐물어라`다.
- 첫 실행 응답은 구현이나 해답이 아니라 질문, 요약, 가정 점검 중 하나여야 한다.
- Harness 판단과 사용자 승인이 모두 있어야 spec을 `Approved`로 고정한다.
- 사용자의 작업 요청 자체는 spec 초안에 대한 승인으로 간주하지 않는다.
- Harness가 approval gate를 채우기에 더 이상 blocker 질문이 없다고 판단한 뒤에만 사용자에게 spec 승인 요청을 할 수 있다.
- approval exit conditions를 통과하기 전까지 spec은 `Draft`로 본다.
- 승인 전에는 구현, issue 분해, 하위 작업 실행, publish를 시작하지 않는다.
- issue 생성은 추적이 필요할 때만 한다. spec 자체가 항상 먼저다.
- 늦게 드러난 spec defect는 repair note로 흡수하지 말고 `Spec Drafting` 또는 `Draft` 상태로 되돌린다.

## Socratic Question Rules

- 질문은 추측을 줄이고 결정이 필요한 공백을 닫는 용도로만 한다.
- source of truth로 닫을 수 있는 사실은 먼저 직접 확인하고, 남는 공백만 묻는다.
- 기본은 한 번에 하나의 blocker 질문이다.
- 같은 답으로 함께 닫히는 공백이 명확할 때만 한 라운드에 최대 세 개까지 묶어 묻는다.
- 각 질문에는 지금 왜 이 정보를 알아야 하는지 짧게 덧붙인다.
- 각 라운드는 숨은 전제, 용어 정의, 또는 범위 framing 중 최소 하나를 점검한다.
- framing 자체가 틀렸을 가능성이 보이면 대안 framing이나 spec split 가능성을 먼저 제기한다.
- 경계, 위험, 검증에 영향이 있는 작업은 예외, 반례, 실패 조건을 질문으로 드러낸다.
- 답을 받은 뒤에는 내부 논리 충돌이나 미잠금 결정을 짧게 요약해 다음 blocker로 넘긴다.
- 용어 정의, 성공 기준, 범위/비범위, 제약, 예외, 검증, publish 필요 여부를 우선 묻는다.
- 질문 없이 바로 설계안이나 코드를 내놓지 않는다.

## Spec Authoring Loop

1. 사용자 요청과 source of truth를 읽는다.
2. 실행 가능한 단일 요구사항인지 먼저 확인한다.
3. blocker 질문을 던질 때는 닫으려는 공백과 왜 지금 필요한지 함께 말한다.
4. 각 라운드마다 확정된 점, 뒤집힌 가정, 남은 공백, 논리 충돌 여부를 짧게 요약한다.
5. approval gate가 비어 있으면 즉답하지 말고 질문 루프를 계속한다.
6. Harness가 approval gate를 채우기에 충분하고 더 이상 blocker 질문이 없다고 판단하면 clarification log와 approval gate를 포함한 spec 초안을 작성한다.
7. 작업 요청 자체를 승인으로 취급하지 말고, 현재 spec 초안에 대한 사용자 승인 요청을 별도로 한다.
8. 사용자가 그 spec 초안에 명시적으로 승인했을 때만 spec 상태를 `Approved`로 올린다.
9. 구현 중 scope가 바뀌거나 verification, review, user validation에서 spec defect가 드러나면 별도 planning 문서를 만들지 말고 spec을 다시 `Draft`로 내려 재승인받아 갱신한다.

## Approval Exit Conditions

아래 조건이 모두 충족되어야 spec을 `Approved`로 본다.

- problem과 goal이 한 spec으로 묶일 만큼 명확하다.
- non-goal이 적혀 있어 scope drift를 막을 수 있다.
- clarification log 또는 summary로 핵심 결정이 왜 필요한지 설명할 수 있다.
- primary repo와 write scope가 잠겨 있다.
- verification 방법을 적을 수 있다.
- 하위 작업이 필요한지와 필요하면 어떻게 쪼갤지 정해졌다.
- tracking issue/PR이 필요한지 결정됐다.
- 남은 blocker가 없거나, 남아 있는 것은 explicit risk/open question으로 승격됐다.
- Harness가 "이제 구현 가능한 spec"이라고 판단했다.
- Harness가 현재 spec 초안에 대해 사용자 승인 요청을 했다.
- 사용자가 작업 요청이 아니라 현재 spec 초안 자체를 명시적으로 승인했다.

## Spec Minimum Shape

모든 spec은 최소한 아래 정보를 가져야 한다.

- task metadata
- request summary
- problem
- goals
- non-goals
- socratic clarification log
- approval gate
- assumptions and constraints
- write scope
- acceptance criteria
- verification
- delivery and tracking plan
- risks or open questions
- approval status

## Detailed Subtask Rules

하위 작업은 아래 중 하나라도 해당하면 spec 안에 명시한다.

- 한 번의 구현 루프로 닫기 어렵다.
- 저장소가 둘 이상 얽힌다.
- verification이나 publish 단위가 나뉜다.
- 위험도나 ownership 분리가 필요하다.

각 하위 작업에는 최소한 아래가 보여야 한다.

- subtask name
- target repo
- goal
- in-scope
- done when
- verification hook
- tracking needed 여부
- dependency 또는 execution order 필요 시

하위 작업을 정의했다고 해서 issue를 자동 생성하지 않는다. issue는 tracking이 필요한 경우에만 만든다.

## Tracking Projection Rules

- spec은 항상 만든다.
- parent issue는 cross-repo planning, 장기 추적, 외부 협업, review focus가 필요한 경우에만 만든다.
- subtask issue는 하위 작업이 독립된 owner, review, publish 단위를 가질 때만 만든다.
- publish가 필요한 구현 결과는 latest verification 뒤 open PR로 공개한다.
- spec만 정의하고 끝난 작업은 issue/PR 없이 종료할 수 있다.

## Write Scope Rules

spec의 `Write Scope` 섹션에는 최소한 아래가 있어야 한다.

- primary repo
- allowed write paths
- control-plane artifact 필요 시
- explicitly forbidden path
- network / external systems
- escalation triggers

이 정보가 없으면 구현으로 가지 않는다.

## Verification and Final Validation

- verification contract profile은 spec 안에 적는다.
- verification evidence는 spec이나 별도 verification artifact에 남긴다.
- review와 feedback은 optional이지만, trigger되면 evidence를 남긴다.
- verification, review, user validation에서 spec defect가 드러나면 repair만 하지 말고 spec을 다시 `Draft`로 내려 clarification과 approval를 반복한다.
- 마지막 완료 판정은 사용자 최종 검증을 포함한다.

## Anti-Patterns

- spec 없이 구현부터 시작하는 것
- 질문 대신 가정으로 빈칸을 채우는 것
- 사용자의 작업 요청을 spec 승인으로 오인하는 것
- blocker 질문이 남아 있는데 승인 요청부터 하는 것
- 하위 작업이 필요한데 spec 밖 TODO나 메모로만 남기는 것
- 추적 issue가 필요하지 않은데 관리용 artifact만 늘리는 것
- 구현 도중 scope가 바뀌었는데 spec을 다시 승인받지 않는 것
- late-discovered spec defect를 code repair만으로 덮고 clarification loop를 다시 열지 않는 것
