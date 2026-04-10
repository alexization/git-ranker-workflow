---
name: issue-to-exec-plan
description: guarded lane의 GitHub issue나 roadmap item을 실행 가능한 exec plan으로 바꾸고, 구현 전에 범위와 verification을 잠근다. write scope, non-scope, 검증 명령을 먼저 고정해야 할 planning 단계에서 이 skill을 사용한다.
---

# Issue To Exec Plan

이 skill은 issue를 문서화하는 것이 아니라 구현 가능한 범위로 잠그는 데 초점을 둔다. exec plan이 준비되면 이후 agent들이 같은 scope와 같은 verification을 재사용할 수 있어야 한다.

## 언제 사용하나

- 새 GitHub issue를 시작한다.
- `docs/product/work-item-catalog.md` 항목을 실제 작업으로 착수한다.
- 후속 agent에게 넘길 기준 문서가 아직 없다.
- 작업이 여러 문서나 여러 저장소로 번질 위험이 있어 먼저 write scope를 잠가야 한다.
- selected lane이 `guarded`다.

## 먼저 확인할 것

- `AGENTS.md`
- `PLANS.md`
- `docs/operations/workflow-governance.md`
- 관련 `docs/product/*.md`, source of truth, 완료된 exec plan

요구사항이나 canonical source가 애매하면 plan을 쓰기 전에 질문부터 다시 정리한다.

## 작업 방식

1. 문제, why now, scope, non-scope를 먼저 고정한다.
2. 허용 write scope와 forbidden path를 적는다.
3. verification 명령과 evidence surface를 미리 적는다.
4. GitHub issue가 없으면 먼저 만들고 줄바꿈까지 확인한다.
5. `docs/exec-plans/active/YYYY-MM-DD-<issue-id-lower>-<slug>.md`를 작성한다.

## 결과

산출물은 active exec plan 문서다. 최소한 아래가 바로 읽혀야 한다.

- Issue ID, GitHub issue, 저장소, 브랜치명, task slug
- Problem, Why Now, Scope, Non-scope, Write Scope
- Outputs, Verification, Evidence, Risks or Blockers
- Next Preconditions, Docs Updated, Skill Consideration

작업이 끝나면 `Completed`로 갱신하고 `docs/exec-plans/completed/`로 옮긴다.

## 빠른 점검 명령

```bash
rg -n "<issue-id|task-slug|surface noun>" docs/product docs/exec-plans
find docs/exec-plans/active docs/exec-plans/completed -maxdepth 1 -type f | sort
cp .codex/skills/issue-to-exec-plan/assets/github-issue-body.md /tmp/<issue-id>-issue-body.md
gh issue create --repo <owner>/<target-repo> --title "[Task] <issue-id> ..." --body-file /tmp/<issue-id>-issue-body.md
gh issue view --repo <owner>/<target-repo> <issue-number> --json body
git checkout -b feat/<issue-id-lower>-<slug>
```

workflow 저장소에서 멀티라인 issue body를 만들 때는 [github-issue-body.md](assets/github-issue-body.md)를 복사해 채운다.

## 피해야 할 것

- guarded lane인데 exec plan 없이 바로 코드나 문서를 수정하지 않는다.
- roadmap 문장을 그대로 복사하고 write scope나 검증을 비워두지 않는다.
- verification을 `문서 확인`, `테스트 실행`처럼 추상적으로 쓰지 않는다.
- 선행조건이 불명확한데 `Ready` 또는 `In Progress`로 올리지 않는다.
- 애매한 요구사항을 임의 해석해 plan 본문에 박지 않는다.
- `docs/architecture/`, `docs/operations/`, `docs/product/` 같은 stable source of truth 문서에 현재/후속 work item ID를 설명용 문장으로 남기지 않는다.
- 멀티라인 GitHub Issue 본문을 `gh issue create --body '...'` 또는 escaped `\n` 문자열로 직접 보내지 않는다.
- Issue 생성 후 `gh issue view --json body` 확인 없이 줄바꿈이 정상이라고 가정하지 않는다.
