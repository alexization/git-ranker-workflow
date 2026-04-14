---
name: api-contract-sync
description: backend API 계약 변경을 canonical spec, client consumer, workflow 문서와 같은 기준으로 맞춘다. `git-ranker/docs/openapi/openapi.json` 변화가 client 타입, validation, workflow evidence에 영향을 주는지 함께 정리해야 할 때 이 skill을 사용한다.
---

# API Contract Sync

목표는 drift를 같은 순서로 줄이는 것이다.

## 언제 사용하나

- approved spec 또는 명시적 contract drift review 범위가 이미 잠겨 있다.
- `git-ranker/docs/openapi/openapi.json`이 바뀌었다.
- `/api/v1/**` request, response, enum, auth, error envelope가 바뀌었다.
- client 타입이나 validation에서 backend와 drift가 의심된다.
- workflow 문서나 evidence가 현재 계약과 맞지 않을 가능성이 있다.

## 먼저 확인할 것

- canonical backend contract: `git-ranker/docs/openapi/openapi.json`
- 관련 client consumer
- 관련 workflow 문서와 approved spec

## 작업 방식

1. canonical spec에서 바뀐 endpoint, schema, enum을 확인한다.
2. 영향을 받는 client consumer를 찾는다.
3. workflow 문서나 evidence surface가 영향을 받는지 확인한다.
4. 필요한 변경만 반영한다.
5. contract sync evidence를 spec이나 PR에 남긴다.

## 피해야 할 것

- request route를 분류하거나 spec approval을 대신하려는 것
- approved spec 없이 contract drift만 보고 구현 범위를 새로 발명하는 것
- backend contract를 workflow 문서가 canonical source인 것처럼 다루는 것
