# Continuous Quality Feedback Loop

이 문서는 recurring quality sweep 규칙을 고정한다.

## Policy Invariants

- quality sweep은 verification, review, feedback close-out을 대체하지 않는다.
- quality sweep은 `Completed` 뒤의 recurring surface다.
- quality signal entry는 signal class 하나당 하나씩 남긴다.
- correctness, security, reliability에 직접 영향을 주는 finding은 cleanup candidate로 축소하지 않는다.
- workflow control plane은 trigger, taxonomy, evidence, handoff만 소유한다.

## Trigger Modes

| Trigger mode | When to use | Expected output |
| --- | --- | --- |
| `post-closeout` | 특정 task가 닫힌 직후 quality drift를 다시 점검할 때 | quality sweep report |
| `scheduled` | 저장소별 cadence에 따라 주기적으로 점검할 때 | quality sweep report |
| `targeted` | 특정 경로나 reviewer note를 근거로 한정 스캔이 필요할 때 | bounded sweep result |

## Quality Signal Taxonomy

| Signal class | Typical signal | Preferred follow-up |
| --- | --- | --- |
| `coding-rule-drift` | lint warning 증가, rule suppression 증가, formatter drift | `cleanup-pr-candidate` 또는 `guardrail-follow-up` |
| `duplication-drift` | copy-paste된 로직, 유사 patch 반복 | `cleanup-pr-candidate` |
| `unused-code-drift` | unused export/helper/dependency, stale flag, dead path | `cleanup-pr-candidate` 또는 `repair-now` |

## Detection Surface Rule

quality sweep report에는 어떤 detector 또는 inspection surface를 썼는지 반드시 남긴다. 가능한 source는 아래 우선순위를 따른다.

1. impacted repo의 entry doc, package/build script, verification contract에 이미 정의된 deterministic command
2. repo-specific static analysis surface
3. reviewer note, completed spec, grep, manual code reading 같은 bounded inspection

## Disposition Vocabulary

| Disposition | Choose when | Typical output |
| --- | --- | --- |
| `repair-now` | 사실상 correctness, contract, reliability, security bug를 다시 발견한 경우 | 새 bug/repair issue 또는 즉시 repair handoff |
| `cleanup-pr-candidate` | bounded write scope와 deterministic evidence가 있어 별도 cleanup issue/PR로 안전하게 분리 가능한 경우 | quality sweep report, cleanup handoff |
| `guardrail-follow-up` | root cause가 missing detector, missing policy, weak CI gate 같은 system asset 부족인 경우 | feedback ledger entry, follow-up asset |
| `no-action` | false positive, duplicate report, 이미 해소됨, 지금 자산화할 가치가 낮은 경우 | explicit rationale only |

## Cleanup Handoff Rule

`cleanup-pr-candidate`를 선택했으면 최소한 아래를 next work item에 넘긴다.

- 대상 저장소
- bounded scan scope
- signal class
- detector 또는 inspection surface
- 핵심 evidence
- non-scope
- follow-up owner 또는 next action

## Quality Sweep Report Minimum

quality sweep 결과는 spec close-out, review note, 또는 follow-up artifact 중 최소 한 곳에 [quality-sweep-report-template.md](quality-sweep-report-template.md) 형식으로 남긴다.
