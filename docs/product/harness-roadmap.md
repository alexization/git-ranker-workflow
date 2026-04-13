# Harness Roadmap

이 문서는 `git-ranker-workflow`의 현재 기준 하네스 로드맵이다. 여기에는 active/pending work만 남긴다.

## 목표

1. `git-ranker-workflow`는 요청 라우팅, Socratic spec 작성, tracking orchestration, context/boundary, verification/review/feedback orchestration을 소유한다.
2. `git-ranker`, `git-ranker-client`는 각 저장소의 implementation knowledge를 소유한다.
3. backend/frontend 작업은 workflow에서 시작하되, 구현 판단은 target repo `AGENTS.md`, code, test, repo-local skill을 우선 읽는다.
4. cross-repo 요청은 workflow에서 spec과 tracking으로 분해하고, code change는 저장소별 issue/PR로 나눈다.
5. repo-specific guardrail, CI, quality gate는 각 app repo가 소유하고 workflow는 상위 semantics와 handoff만 고정한다.

## 이번 계획의 고정 결정

- workflow는 monolithic mirror가 아니라 control plane이다.
- 모든 즉시 실행 가능한 작업은 구현 전에 승인된 spec을 먼저 가진다.
- spec은 요구사항, 하위 작업, write scope, verification, tracking 결정을 함께 소유한다.
- issue는 spec이 추적 surface를 요구할 때만 만든다.
- 기본 publish 순서는 `implement -> verify -> open PR`이다.
- independent review는 guarded lane, high-risk change, 또는 사용자 요청이 있을 때만 수행한다.
- 마지막 완료 판정은 사용자 최종 검증을 포함한다.

## 목표 상태

1. 요청이 들어오면 라우터가 요청 유형을 먼저 분류한다.
2. workflow는 즉시 실행 가능한 작업마다 소크라테스 질문으로 spec을 먼저 만든다.
3. approved spec이 lane, subtask, tracking, write scope, verification을 함께 고정한다.
4. target repo `AGENTS.md`와 repo-local knowledge surface가 구현 단계의 first source가 된다.
5. Implementer Agent는 한 번에 한 저장소의 한 subtask만 수정한다.
6. verification contract는 workflow의 상위 semantics와 target repo `AGENTS.md`가 가리키는 repo-local entrypoint를 함께 사용한다.
7. latest verification이 끝나면 open PR을 먼저 publish하고, review는 필요할 때 그 위에서 수행한다.
8. feedback과 quality sweep은 가장 가까운 owner repo의 guardrail asset으로 되돌린다.

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

## 사용 원칙

- 모든 실행 작업은 먼저 `docs/specs/active/`에 active spec을 가진다.
- 모호한 요청은 구현이나 문서 수정으로 바로 넘기지 않는다.
- 컨텍스트 파일은 task type 기준으로 점진적으로 공개한다.
- 결정론적 검증 없이 Agent의 자기평가를 완료 근거로 삼지 않는다.
- open PR publish는 latest verification 뒤에 바로 수행한다.
- quality sweep에서 발견한 non-blocking cleanup candidate는 original task에 섞지 않는다.
