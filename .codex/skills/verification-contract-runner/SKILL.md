---
name: verification-contract-runner
description: 구현이 끝난 뒤 선택된 verification contract profile에 따라 exact command set을 실행하고 latest verification evidence를 남긴다. review 전에 passed, failed, blocked 상태를 canonical 형식으로 잠가야 할 때 이 skill을 사용한다.
---

# Verification Contract Runner

이 skill의 핵심은 새 명령을 발명하지 않는 것이다. exec plan과 registry에 이미 정의된 command set을 그대로 실행하고, reviewer가 바로 읽을 수 있는 latest verification evidence로 묶는다.

## 언제 사용하나

- 구현이나 문서 변경이 끝나서 review 전 검증이 필요하다.
- repair 후 failed command를 다시 실행해 latest evidence를 갱신해야 한다.
- reviewer handoff 전에 command status와 evidence를 한 곳에 정리해야 한다.

## 먼저 확인할 것

- active exec plan
- exec plan에 적힌 verification contract profile
- `docs/operations/verification-contract-registry.md`
- 필요한 runtime, env, credential, worktree

환경이 잠겨 있지 않으면 검증 전에 blocker로 먼저 정리한다.

## 작업 방식

1. selected profile의 required command와 conditional command를 확인한다.
2. required command를 모두 실행한다.
3. conditional command는 trigger 또는 skip reason과 함께 남긴다.
4. 결과를 compact `Verification Summary` 또는 detailed `Verification Report` 중 맞는 형식으로 정리한다.
5. reviewer handoff가 이어질 예정이면 diff summary와 remaining risk 초안도 같이 적어 둔다.

## 결과

산출물은 exec plan이나 verification artifact에 남기는 latest verification evidence다. 최소 아래가 바로 보여야 한다.

- `Contract profile`
- `Overall status`
- `Preconditions` 필요 시
- `Ran` 또는 command별 `Status`
- 핵심 `Evidence`
- `Failure` 또는 `Failure or skipped summary`
- `Next action`

## 빠른 점검 명령

```bash
sed -n '1,320p' docs/operations/verification-contract-registry.md
sed -n '1,260p' docs/exec-plans/active/<plan>.md
git diff --check
./gradlew test
./gradlew build
npm run lint
npx tsc --noEmit
NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_API_URL=http://localhost:8080 npm run build
```

## 피해야 할 것

- selected profile의 required command를 일부만 실행하고 `passed`로 적지 않는다.
- conditional command를 생략하면서 이유를 비워 두지 않는다.
- baseline command가 실패했는데 아래 conditional command 성공을 최신 상태처럼 남기지 않는다.
- all-passed simple case인데 command-by-command report를 불필요하게 길게 늘이지 않는다.
- review 전에 verification evidence 없이 완료를 주장하지 않는다.
- 여러 profile이 필요하다는 이유로 issue 분해 대신 report를 임의로 합치지 않는다.
