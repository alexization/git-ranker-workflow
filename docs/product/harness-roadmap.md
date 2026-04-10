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
- 기본 publish 순서는 `implement -> verify -> open PR`이다.
- independent review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때만 수행한다.
- draft PR은 canonical 기본값이 아니며, 사용자가 명시적으로 요청한 경우에만 사용한다.
- feedback close-out은 blocker, 반복 실패, guardrail promotion 필요성이 있을 때만 수행한다.

## 목표 상태

사용자 요청 처리의 목표 상태는 아래와 같다.

1. 요청이 들어오면 라우터가 요청 유형을 먼저 분류한다.
2. workflow는 요청을 `default lane` 또는 `guarded lane`으로 나눠 non-critical overhead를 줄인다.
3. guarded lane만 exec plan, context pack, boundary lock을 formal하게 수행한다.
4. target repo `AGENTS.md`와 repo-local knowledge surface가 구현 단계의 first source가 된다.
5. Implementer Agent는 한 번에 한 저장소만 수정하고, cross-repo 변경은 planning issue로 다시 분해한다.
6. verification contract는 workflow의 상위 semantics와 target repo `AGENTS.md`가 가리키는 repo-local entrypoint를 함께 사용한다.
7. latest verification이 끝나면 open PR을 먼저 publish하고, review는 필요할 때 그 위에서 수행한다.
8. feedback과 quality sweep은 가장 가까운 owner repo의 guardrail asset으로 되돌린다.
9. workflow product 문서는 남아 있는 transition work만 보여 주고, 완료된 항목은 historical record로 이동한다.

## 권장 실행 순서

### Phase 1. Current Transition Closeout

1. `GRB-04` backend verification contract reset
2. `GRB-06` backend test/CI removal
3. `GRC-05` frontend verification contract 정렬

### Phase 2. Federation Source-Of-Truth Alignment

4. `GRW-26` federated ownership model alignment
5. `GRW-27` federated `AGENTS.md` handoff contract

### Phase 3. Repo-Local Knowledge Ownership

6. `GRB-07` backend `AGENTS.md` entrypoint and knowledge bootstrap
7. `GRC-07` frontend `AGENTS.md` entrypoint and knowledge bootstrap

### Phase 4. Repo-Local Guardrail Baselines

8. `GRB-05` backend GC baseline 정렬
9. `GRC-06` frontend GC baseline 정렬

## 바로 다음에 추천하는 작업

1. `GRB-04`
2. `GRB-06`
3. `GRC-05`
4. `GRW-26`
5. `GRW-27`

이제 `GRB-04`, `GRB-06`, `GRC-05`를 닫아야 repo-local verification surface가 현재 기준으로 정리된다. 이후 `GRW-26`, `GRW-27`에서 ownership과 `AGENTS.md` handoff contract를 federation 기준으로 다시 잠가야 backend/frontend repo-local bootstrap이 중복 문서 없이 이어진다.

## 사용 원칙

- guarded lane 또는 catalog item만 `docs/exec-plans/active/`에 exec plan을 먼저 만든다.
- 모호한 요청은 구현이나 문서 수정으로 바로 넘기지 않는다.
- 컨텍스트 파일은 task type 기준으로 점진적으로 공개한다.
- 결정론적 검증 없이 Agent의 자기평가를 완료 근거로 삼지 않는다.
- open PR publish는 latest verification 뒤에 바로 수행한다.
- independent review는 필요한 경우에만 수행하고, 기본값은 reviewer 한 명이다.
- 같은 실패가 반복되면 다음 턴에서는 가드레일이 하나 더 생겨야 한다.
- `Feedback Pending` close-out은 실제로 feedback이 trigger됐을 때만 남긴다.
- quality sweep에서 발견한 non-blocking cleanup candidate는 original issue 완료 여부와 분리해 새 work item으로 넘긴다.
- workflow는 orchestration layer만 소유하고, repo-specific implementation knowledge는 가능한 한 각 app repo로 내린다.
- app repo implementation task는 target repo `AGENTS.md`가 준비되기 전에는 시작하지 않는다.
