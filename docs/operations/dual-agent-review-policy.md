# Dual-Agent Review Policy

이 문서는 open PR 이후 independent review를 언제 수행하고, 어떤 입력으로 verdict를 남기며, 어떤 경우에 repair 또는 `Blocked`로 되돌리는지를 고정한다.

## Policy Invariants

- independent review는 중요한 통제지만, 모든 작업의 publish 선행조건은 아니다.
- canonical 기본 흐름은 `implement -> verify -> open PR publish`다.
- independent review를 수행할 때만 implementer와 reviewer는 반드시 서로 다른 agent 또는 사람이어야 한다.
- review는 latest verification evidence가 최신이고 reviewer minimum context가 채워진 뒤에만 시작할 수 있다.
- reviewer는 diff만 보지 않고 approved spec, verification 결과, 남은 리스크를 함께 읽어야 한다.

## Review Trigger Rules

아래 중 하나라도 해당하면 independent review를 수행한다.

- 작업이 `guarded lane`이다.
- public API/schema, auth/permission, security, CI, migration, destructive change를 포함한다.
- 사용자가 reviewer 또는 sub-agent 검토를 명시적으로 요청했다.
- verification은 통과했지만 residual risk가 높다.

## Reviewer Minimum Context

- open PR link 또는 latest diff reference
- latest verification report 또는 summary
- approved spec 요약 또는 경로
- touched diff summary
- source-of-truth update 목록 또는 업데이트 불필요 사유
- 남은 리스크, skipped conditional command, follow-up 필요 사항

아래 중 하나라도 있으면 verdict는 `blocked`다.

- latest verification evidence가 없거나 latest가 아니다
- approved spec이 없어 scope를 고정할 수 없다
- diff summary와 실제 변경 범위가 맞지 않는다
- canonical source가 없어 reviewer가 새 정책을 발명해야 한다

## Verdict Vocabulary

| Verdict | Meaning | Required Consequence |
| --- | --- | --- |
| `approved` | latest verification과 current diff를 기준으로 blocking finding이 없다 | merge 또는 후속 handoff로 진행할 수 있다 |
| `changes-requested` | 현재 PR 범위 안에서 수리 가능한 blocking finding이 있다 | implementer가 repair 후 affected verification을 다시 실행한다 |
| `blocked` | missing reviewer input, missing canonical source, boundary conflict처럼 현재 PR 안에서 review를 닫을 수 없다 | `Blocked` 또는 follow-up planning으로 전환한다 |

## Review Evidence Rule

canonical review evidence는 review comment, PR comment, spec close-out 중 최소 한 곳에 아래 필드를 남긴다.

```md
## Independent Review
- Implementer:
- Reviewer:
- Reviewer Input:
  - PR or diff:
  - Latest verification report:
  - Approved spec:
  - Source-of-truth update:
  - Remaining risks / skipped checks:
- Review Verdict:
- Findings / Change Requests:
- Evidence:
```

## Review Repair Loop

- `changes-requested` verdict에는 blocking finding, 기대 next action, 다시 확인할 command 또는 문서가 들어가야 한다.
- implementer는 current diff에서 수정을 남기고 영향을 받은 command를 다시 실행한 뒤 verification evidence를 갱신한다.
- 같은 root cause가 두 번의 repair 뒤에도 남으면 `blocked` 또는 follow-up split로 전환한다.
