# Runbook

## 초기 설정

```bash
python3 scripts/workflow.py init
python3 scripts/workflow.py doctor
python3 -m unittest discover -s tests -v
```

`init`가 로컬 git 저장소의 `core.hooksPath`를 `.githooks`로 맞추고 `.githooks/*`, `workflows/system/hooks.json`을 source 기준으로 다시 동기화한다. `doctor`는 이 값이나 runtime surface가 어긋나면 실패한다.

## 새 작업 시작

```bash
python3 scripts/workflow.py new task-001 --title "..." --primary-repo git-ranker-workflow
```

이후 `workflows/tasks/task-001/spec.md`를 소크라테스 질문으로 잠근다. `Socratic Clarification Log`는 아래처럼 `Q/A/Decision` triplet만 사용한다.

```md
- Q: phase canonical source는 무엇인가?
- A: executable plan은 prose가 아니라 JSON이어야 한다.
- Decision: `phases.json`만 canonical plan으로 쓴다.
```

사용자가 현재 spec 초안에 명시적으로 동의하면 approve 한다. 이때 `approve`가 `spec.md`를 `task.json.intake`로 잠근다.

```bash
python3 scripts/workflow.py approve task-001 --note "사용자 승인 요약"
```

## Phase 고정

phase 정의는 명시적 JSON 입력으로만 적재한다.

```bash
python3 scripts/workflow.py plan task-001 --from /tmp/task-001-phases.json
cat /tmp/task-001-phases.json | python3 scripts/workflow.py plan task-001 --stdin
```

## 실행과 검증

`verify`는 `run --complete`로 닫힌 phase에 대해서만 실행한다.

```bash
python3 scripts/workflow.py run task-001 --start
python3 scripts/workflow.py run task-001 --complete --changed-path scripts/workflow.py --changed-path tests/test_workflow_cli.py
python3 scripts/workflow.py verify task-001
python3 scripts/workflow.py review task-001 --note "review ready"
python3 scripts/workflow.py review task-001 --close --user-validation-note "validated"
```

## Repair / Reopen

실패, block, review follow-up, 추가 요구사항이 들어오면 `reopen`으로 다시 `approved` 상태로 되돌린다. `reopen`은 target phase를 `pending`으로 복구해서 바로 `run --start`로 재개할 수 있게 만든다. 추가 요구사항이면 `spec.md`를 다시 잠근 뒤 `approve`를 다시 실행하고, 그 다음 `plan`으로 phase를 갱신한다.

```bash
python3 scripts/workflow.py reopen task-001 --note "추가 요구사항 반영"
python3 scripts/workflow.py approve task-001 --note "변경된 spec 재승인"
```

## 점검 명령

```bash
python3 scripts/workflow.py status task-001
python3 scripts/workflow.py status --all --check
python3 scripts/workflow.py doctor
python3 scripts/workflow.py hook pre_command --command-text "git push origin feature"
python3 scripts/workflow.py hook pre_commit --staged
python3 scripts/workflow.py hook pre_push --command-text "git push origin feature"
```

`pre_commit`은 active task가 여러 개라면 자동 추론을 중단하고 실패한다. 이 경우 `WORKFLOW_TASK_ID` 또는 `--task-id`로 명시적으로 task binding을 넣는다.
`pre_push`는 먼저 unpushed diff를 task scope에 매핑한다. active task가 없어도 completed task scope 하나로 매핑되면 그 task를 재사용하고, 단일 task로 정해지지 않으면 실패한다.
