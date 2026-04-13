---
name: verification-contract-runner
description: 구현이 끝난 뒤 선택된 verification contract profile에 따라 exact command set을 실행하고 latest verification evidence를 남긴다.
---

# Verification Contract Runner

이 skill의 핵심은 새 명령을 발명하지 않는 것이다.

## 언제 사용하나

- 구현이나 문서 변경이 끝나서 검증이 필요하다.
- repair 후 failed command를 다시 실행해야 한다.

## 먼저 확인할 것

- approved spec
- spec에 적힌 verification contract profile
- `docs/operations/verification-contract-registry.md`

## 작업 방식

1. selected profile의 required command와 conditional command를 확인한다.
2. required command를 모두 실행한다.
3. conditional command는 trigger 또는 skip reason과 함께 남긴다.
4. 결과를 compact `Verification Summary` 또는 detailed `Verification Report`로 정리한다.

## 결과

- `Contract profile`
- `Overall status`
- `Preconditions` 필요 시
- `Ran` 또는 command별 `Status`
- 핵심 `Evidence`
- `Failure` 또는 `Failure or skipped summary`
- `Next action`
