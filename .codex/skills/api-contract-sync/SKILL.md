---
name: api-contract-sync
description: backend API 계약 변경을 canonical spec, client consumer, workflow 문서와 같은 기준으로 맞춘다. `git-ranker/docs/openapi/openapi.json` 변화가 client 타입, validation, workflow evidence에 영향을 주는지 함께 정리해야 할 때 이 skill을 사용한다.
---

# API Contract Sync

목표는 새 자동화를 발명하는 것이 아니라 drift를 같은 순서로 줄이는 것이다. backend freshness와 workflow sync freshness는 다른 책임이라는 점을 분명히 둔다.

## 언제 사용하나

- `git-ranker/docs/openapi/openapi.json`이 바뀌었다.
- `/api/v1/**` request, response, enum, auth, error envelope가 바뀌었다.
- client 타입이나 validation에서 backend와 drift가 의심된다.
- workflow 문서나 evidence가 현재 계약과 맞지 않을 가능성이 있다.

## 먼저 확인할 것

- canonical backend contract: `git-ranker/docs/openapi/openapi.json`
- 관련 client consumer
  - `git-ranker-client/src/shared/types/api.ts`
  - `git-ranker-client/src/shared/lib/validations.ts`
  - 직접 계약을 소비하는 화면/서비스 파일
- 관련 workflow 문서와 exec plan

계약 의미가 애매하면 필드 의도나 compatibility를 먼저 확인한다.

## 작업 방식

1. canonical spec에서 바뀐 endpoint, schema, enum을 확인한다.
2. 영향을 받는 client consumer를 찾는다.
3. workflow 문서나 evidence surface가 영향을 받는지 확인한다.
4. 필요한 변경만 반영한다.
5. contract sync evidence를 exec plan이나 PR에 남긴다.

## 결과

산출물은 아래 셋 중 하나 또는 조합이다.

- client 타입/validation 업데이트
- workflow 문서 업데이트
- contract sync evidence 기록

workflow 저장소는 앱 계약 복제본을 소유하지 않으므로, 기본 출력은 canonical spec 확인과 consumer/doc sync 결과다.

## 빠른 점검 명령

```bash
rg -n '"/api/v1/ranking"|EMERALD|AuthMeResponse' git-ranker/docs/openapi/openapi.json git-ranker-client/src/shared/types/api.ts git-ranker-client/src/shared/lib/validations.ts
sed -n '1,200p' git-ranker/docs/openapi/README.md
npx tsc --noEmit -p git-ranker-client/tsconfig.json
rg -n "ranking|auth|tier|contract" docs/operations docs/product docs/exec-plans
```

## 피해야 할 것

- workflow 복제본이나 기억에 의존해 계약을 해석하지 않는다.
- backend spec을 읽지 않고 client 타입만 먼저 수정하지 않는다.
- workflow 저장소에 새 앱 계약 복제본을 임의로 만들지 않는다.
- 관련 문서를 확인하지 않고 “문서 변경 없음”이라고 쓰지 않는다.
- 계약 변경과 무관한 대규모 refactor를 sync 작업에 섞지 않는다.
