# Federated Repo Handoff Contract

이 문서는 workflow control plane이 target repo에 handoff할 때 넘겨야 하는 최소 contract를 고정한다. 목적은 repo-local implementation knowledge를 workflow가 다시 소유하지 않으면서도, 다음 owner가 어디서부터 읽어야 하는지 흔들리지 않게 만드는 것이다.

## Contract Invariants

- workflow handoff는 target repo root entrypoint에서 멈춘다.
- workflow는 route, active spec, active subtask, write boundary, verification hook까지만 넘긴다.
- target repo가 구현 절차, command inventory, bootstrap, verification surface의 canonical source를 소유한다.
- target repo entrypoint가 비어 있으면 workflow는 stable doc으로 대신 메우지 않고 repo-local bootstrap follow-up으로 넘긴다.

## Handoff Summary Minimum

workflow가 target repo를 다음 owner로 지정할 때 handoff summary에는 최소 아래가 보여야 한다.

| Field | Why it is required |
| --- | --- |
| target repo | 다음 owner가 어느 저장소로 이동해야 하는지 잠근다. |
| approved spec path | 현재 결정의 canonical source를 가리킨다. |
| active subtask 또는 current goal | 이번 handoff가 무엇을 닫으려는지 한 줄로 고정한다. |
| allowed write scope와 explicit non-goal | repo-local owner가 범위를 넓히지 않게 한다. |
| verification contract profile 또는 named verification entrypoint | 어떤 검증 surface를 먼저 확인해야 하는지 고정한다. |
| repo entrypoint status | `AGENTS.md`가 로컬/remote source에서 확인됐는지, 아니면 bootstrap gap인지 드러낸다. |
| next source order | handoff 이후 읽을 다음 canonical source를 순서대로 고정한다. |
| open question 또는 blocker | workflow가 닫지 못한 공백을 repo-local follow-up과 분리한다. |

## Target Repo Discovery Order

workflow handoff 뒤 target repo는 아래 순서로 읽는다.

1. root `AGENTS.md`
2. root `README.md` for repo overview only
3. `AGENTS.md`가 지목한 repo-local contract, verification, environment entry docs
4. repo-local `.codex/skills/` 또는 equivalent skill surface
5. current subtask가 직접 건드리는 code, test, config

root `README.md`는 프로젝트 설명과 high-level orientation까지만 기대한다. concrete entrypoint, command inventory, verification sequence는 `AGENTS.md` 또는 named entry docs가 소유한다.

## Local Skill Discovery Order

- local skill은 canonical docs보다 앞서 읽지 않는다.
- `AGENTS.md` 또는 repo-local entry doc이 특정 skill을 지목했을 때만 연다.
- skill은 repo-local canonical source를 대체하지 않고, bootstrap 또는 implementation handoff를 압축하는 절차 layer만 소유한다.
- skill이 없으면 workflow 문서로 되돌아가지 않고 repo-local docs와 code/test를 canonical source로 읽는다.

## Target Repo `AGENTS.md` Requirement

target repo root `AGENTS.md`는 최소 아래를 만족해야 한다.

- repo의 canonical source가 workflow stable docs가 아니라 repo-local 문서와 code/test임을 명시한다.
- 시작 순서에서 `README.md`는 개요 확인용으로만 두고, concrete entrypoint는 named entry docs 기준으로 적는다.
- verification entrypoint 또는 repo manifest surface를 어디서 찾는지 적는다.
- local skill discovery rule과 skill이 canonical docs 뒤에 온다는 점을 적는다.
- workflow handoff가 repo-local command inventory나 troubleshooting playbook를 carry하지 않는다고 적는다.

## Repo Bootstrap Checklist

target repo가 workflow handoff를 안전하게 받을 최소 bootstrap은 아래다.

| Checklist item | Minimum expectation |
| --- | --- |
| root `AGENTS.md` | repo-local start order, source of truth, verification entrypoint, skill discovery rule을 노출한다. |
| root `README.md` | repo 목적과 high-level project description만 제공해도 된다. concrete entrypoint 책임은 지지 않는다. |
| verification entry surface | `build.gradle`, `package.json`, `.env.example`, contract doc처럼 현재 slice가 먼저 읽어야 할 검증/환경 entrypoint가 named source로 존재한다. |
| repo-local contract doc | public API, auth, schema, runtime precondition처럼 repo가 직접 소유해야 하는 surface가 있으면 workflow가 아니라 repo-local 문서가 소유한다. |
| local skill surface | 있으면 repo-local bootstrap 또는 implementation 절차를 thin layer로 제공하고, 없으면 canonical docs와 code/test만으로 onboarding 가능해야 한다. |

## Missing Bootstrap Handling

- `AGENTS.md`가 없으면 workflow handoff는 `bootstrap gap`으로 표시하고 repo-local bootstrap spec을 prerequisite로 건다.
- `README.md`나 verification entry surface가 비어 있으면 workflow는 missing item만 기록하고, 상세 구현 절차를 stable doc으로 추가하지 않는다.
- remote source로만 entrypoint를 확인한 경우에도 같은 minimum을 적용하며, local worktree onboarding은 repo-local follow-up이 닫는다.
