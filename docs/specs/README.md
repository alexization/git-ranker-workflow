# Specs

이 디렉터리는 SDD 기반 작업 spec 문서를 관리한다.

## 목적

- 사용자 요구사항을 소크라테스 방식으로 명확히 정의한다.
- 별도 roadmap/catalog 없이 remaining work도 `Draft` spec으로 같은 surface에 남긴다.
- 각 clarification round에서 왜 물었는지와 어떤 공백이 닫혔는지 남긴다.
- 하위 작업이 필요하면 같은 spec 안에서 분해한다.
- write scope, verification, tracking 결정을 한 문서에 모은다.
- 완료 후에는 completed spec을 historical record로 남긴다.

## 디렉터리 규칙

- [active](active/README.md): 아직 끝나지 않은 spec 문서
- [completed](completed/README.md): 완료되었거나 실행 없이 종료된 spec 문서
- pending requirement seed는 `active/` 아래 `Draft` spec으로 둔다.

## Active Spec 권장 섹션

- Task metadata
- Request
- Problem
- Goals
- Non-goals
- Socratic clarification log
- Approval gate
- Assumptions and constraints
- Write scope
- Acceptance criteria
- Verification
- Delivery and tracking plan
- Detailed subtasks 필요 시
- Risks or open questions

## Completed Spec 권장 섹션

- Task metadata
- Approved requirement summary
- Final change summary
- Final subtasks or delivery summary
- Verification Summary 또는 Verification Report
- Review / feedback 필요 시
- Final user validation
- Docs updated

## 피해야 할 것

- spec 밖에 별도 planning 문서를 만들어 같은 정보를 중복하는 것
- roadmap, backlog, work-item catalog를 spec 밖 stable source로 다시 만드는 것
- 사용자가 승인하지 않은 요구사항을 구현 단계에서 임의로 추가하는 것
- 하위 작업이 필요한데 spec에 분해 없이 구현부터 시작하는 것
- late-discovered spec defect를 clarification log나 재승인 없이 repair 메모로만 덮는 것
