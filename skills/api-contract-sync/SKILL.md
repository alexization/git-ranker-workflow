---
name: api-contract-sync
description: Use this skill when a backend API contract change must be synchronized with client types and workflow source-of-truth updates.
---

# API Contract Sync

## Purpose

backend API 계약 변경이 생겼을 때 canonical source, client consumer, workflow 문서/evidence를 같은 기준으로 맞춘다. 목적은 새 자동화를 발명하는 것이 아니라, drift를 같은 절차로 줄이는 것이다.

## Trigger

- `git-ranker/docs/openapi/openapi.json`이 바뀌었다.
- `/api/v1/**` request, response, enum, auth, error envelope가 바뀌었다.
- client 타입이나 validation에서 backend와 drift가 의심된다.
- workflow source of truth 문서가 현재 계약과 맞지 않을 가능성이 있다.

## Inputs and Preconditions

- canonical backend contract는 `git-ranker/docs/openapi/openapi.json`이다.
- backend 쪽 spec regeneration 책임은 `git-ranker`에 있고, workflow는 그 결과를 기준 입력으로 읽는다.
- 관련 client consumer 파일을 확인한다.
  - `git-ranker-client/src/shared/types/api.ts`
  - `git-ranker-client/src/shared/lib/validations.ts`
  - 직접 계약을 소비하는 화면/서비스 파일
- 관련 workflow 문서를 확인한다.
  - `docs/domain/ranking-read-flow.md`
  - `docs/domain/frontend-data-flows.md`
  - 계약을 직접 설명하는 exec plan 또는 source of truth 문서
- 계약 의미가 애매하면 필드 의도나 backward compatibility를 사용자에게 질문한다.

## Output and Artifact Location

- 산출물은 세 가지 중 하나 또는 조합이다.
  - client 타입/validation 업데이트
  - workflow 문서 업데이트
  - exec plan/PR의 contract sync evidence 기록
- 현재 workflow 저장소에는 tracked generated contract mirror가 없으므로, 기본 출력은 “canonical backend spec 확인 + consumer/doc sync 결과”다.
- 향후 `docs/generated/` 아래 파생 artifact가 생기더라도 그것은 derived copy이며 canonical source가 아니다.

## Standard Commands

반복적으로 쓰는 기본 명령 예시:

```bash
rg -n '"/api/v1/ranking"|EMERALD|AuthMeResponse' git-ranker/docs/openapi/openapi.json git-ranker-client/src/shared/types/api.ts git-ranker-client/src/shared/lib/validations.ts
sed -n '1,200p' git-ranker/docs/openapi/README.md
npx tsc --noEmit
rg -n "ranking|auth callback|tier" docs/domain docs/operations docs/exec-plans
```

backend spec freshness 자체는 backend 저장소에서 확인한다. workflow는 canonical spec을 읽고 consumer/doc sync를 확인한다.

## Required Evidence

- canonical spec 경로를 무엇으로 봤는지
- 어떤 endpoint/schema/enum이 바뀌었는지
- 어떤 client file을 확인하거나 수정했는지
- 어떤 workflow 문서를 확인하거나 수정했는지
- 실행한 verification 명령과 결과
- workflow 쪽 generated artifact가 없으면 그 사실과 no-op 사유

## Forbidden Shortcuts

- workflow 복제본이나 기억에 의존해 계약을 해석하지 않는다.
- backend spec을 읽지 않고 client 타입만 먼저 수정하지 않는다.
- `docs/generated/`를 canonical source처럼 다루지 않는다.
- 관련 문서를 확인하지 않고 “문서 변경 없음”이라고 쓰지 않는다.
- 계약 변경과 무관한 대규모 refactor를 sync 작업에 섞지 않는다.

## Parallel Ownership Rule

- backend contract delta 요약 owner, client consumer owner, workflow doc/evidence owner를 나눌 수 있다.
- backend spec이 확정되기 전에는 client/doc owner가 추정치로 수정하지 않는다.
- `git-ranker-client/src/shared/types/api.ts`와 같은 단일 계약 파일은 한 agent만 수정한다.
- 같은 source of truth 문서는 한 agent만 수정하고, 나머지는 review input만 제공한다.

## Parallel Execution Don'ts

- stale spec을 기준으로 client/doc 작업을 병렬 시작하지 않는다.
- backend spec regeneration과 client type 수정이 서로 다른 가정으로 동시에 진행되게 두지 않는다.
- 계약 의미가 미정인데 각 agent가 필드 의미를 따로 정하게 두지 않는다.
- workflow generated artifact가 없는데도 존재하는 것처럼 체크리스트를 작성하지 않는다.

## Example Input

- backend change:
  - `/api/v1/ranking`에 새 query param `size` 추가
  - `RankingUserInfo`에 `country` 필드 추가
- changed canonical file:
  - `git-ranker/docs/openapi/openapi.json`

## Example Output

```md
Contract sync checklist

- Canonical spec: `git-ranker/docs/openapi/openapi.json`
- Client updates:
  - `git-ranker-client/src/shared/types/api.ts`
  - direct ranking consumer review
- Workflow review:
  - `docs/domain/ranking-read-flow.md`
  - `docs/domain/frontend-data-flows.md`
- Verification:
  - `npx tsc --noEmit`
- Note:
  - workflow `docs/generated/`에는 현재 tracked mirror가 없어 no-op
```

## Handoff

sync 작업을 넘길 때는 아래를 함께 전달한다.

- canonical spec 경로와 변경 요약
- client에서 영향 받는 파일 목록
- workflow에서 영향 받는 문서 목록
- “backend freshness”와 “workflow sync freshness” 책임 분리
