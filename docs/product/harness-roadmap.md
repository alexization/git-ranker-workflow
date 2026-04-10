# Harness Roadmap

이 문서는 `git-ranker-workflow`의 현재 기준 하네스 로드맵이다. 여기에는 active/pending work만 남긴다. 완료된 foundation work는 stable source of truth와 `docs/exec-plans/completed/` historical record에서 읽는다.

## 목표

1. `git-ranker-workflow`는 요청 라우팅, exec plan, context pack, boundary, verification/review/feedback orchestration을 소유한다.
2. `git-ranker`, `git-ranker-client`는 각 저장소의 implementation knowledge를 소유한다.
3. backend/frontend 작업은 workflow에서 시작하되, 구현 판단은 target repo `AGENTS.md`, code, test, repo-local skill을 우선 읽는다.
4. cross-repo 요청은 workflow에서 planning으로 분해하고, code change는 저장소별 issue/PR로 나눈다.
5. repo-specific guardrail, CI, quality gate는 각 app repo가 소유하고 workflow는 상위 semantics와 handoff만 고정한다.

## 이번 계획의 고정 결정

- workflow는 monolithic mirror가 아니라 control plane이다.
- workflow가 소유하는 것은 routing, exec plan, context pack, tool boundary, verification/review/feedback/publish ordering 같은 orchestration layer다.
- app repo가 소유하는 것은 entry docs, build/test entrypoint, code/test conventions, repo-local skill, repo-local CI/quality gate다.
- workflow에는 repo-specific 구현 규칙을 장기 보관하지 않는다. 필요하면 thin handoff만 남기고 canonical 내용은 target repo로 이관한다.
- target repo의 canonical entrypoint는 `AGENTS.md`로 고정한다.
- `AGENTS.md`가 없는 repo는 implementation task의 `Context Ready`를 선언하지 않고, 먼저 repo-local bootstrap task에서 `AGENTS.md`를 추가한다.
- completed task는 product 문서에서 제거하고, historical evidence는 completed exec plan에 남긴다.
- 새 federation task는 workflow policy 정렬 -> `AGENTS.md` handoff contract 정리 -> repo-local knowledge bootstrap -> repo-local guardrail 정착 순서로 진행한다.
- 사용자가 다르게 요청하지 않으면 PR은 independent review와 feedback evidence를 먼저 채운 뒤 open 상태로 publish한다.
- draft PR은 canonical review workspace가 아니라 user-request 또는 blocker-sharing exception이다.

## 목표 상태

사용자 요청 처리의 목표 상태는 아래와 같다.

1. 요청이 들어오면 라우터가 요청 유형을 먼저 분류한다.
2. workflow exec plan이 primary repo, task type, write scope를 고정한다.
3. target repo `AGENTS.md`와 repo-local knowledge surface가 구현 단계의 first source가 된다.
4. Implementer Agent는 한 번에 한 저장소만 수정하고, cross-repo 변경은 planning issue로 다시 분해한다.
5. verification contract는 workflow의 상위 semantics와 target repo `AGENTS.md`가 가리키는 repo-local entrypoint를 함께 사용한다.
6. reviewer sub-agent pool과 reviewer coordinator는 [../operations/dual-agent-review-policy.md](../operations/dual-agent-review-policy.md)에 따라 구현 diff와 검증 결과를 검토하고 verdict를 남긴다.
7. feedback과 quality sweep은 가장 가까운 owner repo의 guardrail asset으로 되돌린다.
8. workflow product 문서는 남아 있는 transition work만 보여 주고, 완료된 항목은 historical record로 이동한다.

## 권장 실행 순서

### Phase 1. Current Transition Closeout

1. `GRW-24` product federation roadmap cleanup
2. `GRW-18` workflow pilot and active queue close-out reconciliation
3. `GRB-04` backend verification contract reset
4. `GRB-06` backend test/CI removal
5. `GRC-05` frontend verification contract 정렬

### Phase 2. Federation Source-Of-Truth Alignment

5. `GRW-26` federated ownership model alignment
6. `GRW-27` federated `AGENTS.md` handoff contract

### Phase 3. Repo-Local Knowledge Ownership

7. `GRB-07` backend `AGENTS.md` entrypoint and knowledge bootstrap
8. `GRC-07` frontend `AGENTS.md` entrypoint and knowledge bootstrap

### Phase 4. Repo-Local Guardrail Baselines

9. `GRB-05` backend GC baseline 정렬
10. `GRC-06` frontend GC baseline 정렬

## 바로 다음에 추천하는 작업

1. `GRW-24`
2. `GRW-18`
3. `GRB-04`
4. `GRB-06`
5. `GRC-05`

`GRW-24`를 먼저 publish해야 product 문서 자체가 active/pending backlog, federation ownership, `AGENTS.md` entrypoint 기준으로 정리된다.

그 다음 `GRW-18`, `GRB-04`, `GRB-06`, `GRC-05`를 닫아야 workflow pilot close-out과 repo-local verification surface가 현재 기준으로 정리된다. 이후 `GRW-26`, `GRW-27`에서 ownership과 `AGENTS.md` handoff contract를 federation 기준으로 다시 잠가야 backend/frontend repo-local bootstrap이 중복 문서 없이 이어진다.

## 사용 원칙

- 새 작업은 항상 `docs/exec-plans/active/`에 exec plan을 먼저 만든다.
- 모호한 요청은 구현이나 문서 수정으로 바로 넘기지 않는다.
- 컨텍스트 파일은 task type 기준으로 점진적으로 공개한다.
- 결정론적 검증 없이 Agent의 자기평가를 완료 근거로 삼지 않는다.
- 구현 Agent는 자기 자신의 결과를 최종 승인하지 않는다.
- 같은 실패가 반복되면 다음 턴에서는 가드레일이 하나 더 생겨야 한다.
- `Feedback Pending` close-out에는 guardrail 승격 대상 또는 `no new guardrail` 이유가 남아야 한다.
- quality sweep에서 발견한 non-blocking cleanup candidate는 original issue 완료 여부와 분리해 새 work item으로 넘긴다.
- workflow는 orchestration layer만 소유하고, repo-specific implementation knowledge는 가능한 한 각 app repo로 내린다.
- app repo implementation task는 target repo `AGENTS.md`가 준비되기 전에는 시작하지 않는다.
