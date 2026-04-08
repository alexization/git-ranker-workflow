---
name: context-pack-selection
description: active exec plan 뒤에 task type별 primary context pack을 고르고, required docs와 optional trigger와 forbidden context를 잠가야 할 때 사용한다. `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 중 하나로 시작 surface를 좁히고 eager load를 막는 작업에 적용한다.
---

# Context Pack Selection

이 skill의 목적은 더 많은 문서를 읽는 것이 아니라, 지금 task에 필요한 최소 컨텍스트만 고정하는 것이다.

## 언제 사용하나

- active exec plan이 준비됐고 구현 전에 primary context pack을 정해야 한다.
- task type은 이미 `workflow 문서 수정`, `backend 수정`, `frontend 수정`, `cross-repo planning` 중 하나로 좁혀졌다.
- hot file 탐색을 시작하기 전에 required docs와 forbidden context를 먼저 잠가야 한다.

primary repo나 task type이 아직 하나로 잠기지 않았다면 이 skill로 덮지 말고 planning으로 되돌린다.

## 먼저 확인할 것

- active exec plan
- request record 또는 GitHub issue
- `AGENTS.md`
- `docs/README.md`
- `PLANS.md`
- `docs/operations/workflow-governance.md`
- `docs/architecture/context-pack-registry.md`
- workflow repo가 아닌 저장소가 primary면 target repo entry 문서

## 작업 방식

1. issue와 exec plan에서 primary repo와 task type이 하나로 잠겼는지 먼저 확인한다.
2. `docs/architecture/context-pack-registry.md`의 mapping으로 primary context pack 하나를 고른다.
3. common base context와 선택한 pack의 required docs만 먼저 연다.
4. optional docs는 trigger와 함께 적고, forbidden context는 eager load 금지 surface로 분리한다.
5. hot file 탐색은 issue noun과 write scope를 기준으로 시작하고 한 hop씩만 확장한다.
6. 다른 pack의 required docs까지 필요해지거나 target repo entry 문서가 없으면 `Context Ready`를 선언하지 말고 planning 또는 `Blocked`로 되돌린다.

## 결과

산출물은 짧은 context selection summary다. 아래가 바로 보여야 한다.

- primary repo
- task type
- primary context pack
- required docs
- optional docs trigger
- forbidden context
- first-ring hot file cue
- stop signal 또는 planning return 조건

## 빠른 점검 명령

```bash
sed -n '1,260p' docs/architecture/context-pack-registry.md
sed -n '1,220p' docs/exec-plans/active/<plan>.md
rg -n "<task type|repo name|issue noun>" docs .codex/skills
sed -n '1,220p' <target-repo-entry-doc>
```

## 피해야 할 것

- required docs를 잠그기 전에 sibling repo나 다른 pack의 문서를 먼저 열지 않는다.
- optional docs를 default 읽기 목록처럼 취급하지 않는다.
- 여러 pack의 required docs가 동시에 필요해졌는데 임의로 합치지 않는다.
- target repo entry 문서나 공식 remote source 없이 `Context Ready`를 선언하지 않는다.
- workflow 문서에 앱 동작 canonical source를 새로 복제하지 않는다.
