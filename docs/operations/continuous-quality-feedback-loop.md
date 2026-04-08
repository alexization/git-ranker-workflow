# Continuous Quality Feedback Loop

이 문서는 [../architecture/harness-system-map.md](../architecture/harness-system-map.md)의 `Feedback` 이후에도 품질 저하를 다시 끌어올리기 위한 recurring quality sweep 규칙을 고정한다. [verification-contract-registry.md](verification-contract-registry.md)가 현재 작업의 completion gate를 잠그고, [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)가 close-out 시점의 failure promotion을 잠근다면, 이 문서는 "언제 주기적 또는 targeted quality sweep을 돌리고", "lint drift, duplication, unused code를 어떻게 분류하며", "언제 cleanup PR candidate 또는 guardrail follow-up으로 보내는가"를 잠근다.

관련 운영 규칙은 [workflow-governance.md](workflow-governance.md)를 따른다.

## Policy Invariants

- continuous quality sweep은 verification, review, feedback close-out을 대체하지 않는다. 현재 issue의 완료 판정은 계속 verification contract와 reviewer verdict가 결정한다.
- quality sweep은 `Completed` 뒤의 recurring surface다. 이미 닫힌 issue를 다시 열지 않고, 필요한 경우 새 cleanup work item 또는 guardrail follow-up을 만든다.
- quality sweep은 success path와 failure path 모두에서 실행될 수 있다. 성공 경로에서는 non-blocking quality drift를 찾고, 실패 경로에서는 반복되는 detector gap을 guardrail 후보로 연결한다.
- quality signal entry는 signal class 하나당 하나씩 남긴다. coding rule drift와 unused code를 같은 entry에 섞지 않는다.
- correctness, security, reliability에 직접 영향을 주는 blocking finding은 cleanup candidate로 축소하지 않는다. 이 경우 `repair-now` 또는 새 bug/repair issue로 보낸다.
- workflow control plane은 trigger, taxonomy, evidence, handoff만 소유한다. 저장소별 detector 구현과 명령은 각 repo entry doc, verification contract, build script가 소유한다.
- quality sweep에서 반복적으로 드러나는 detector gap, noisy lint baseline, missing CI gate는 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)의 guardrail promotion으로 다시 연결한다.

## Trigger Modes

| Trigger mode | When to use | Typical owner | Expected output |
| --- | --- | --- | --- |
| `post-closeout` | 특정 issue/PR이 `Completed`로 닫힌 직후, 이번 diff 주변에서 quality drift를 다시 점검해야 할 때 | implementer 또는 reviewer coordinator | quality sweep report, cleanup candidate 여부 |
| `scheduled` | 저장소별 cadence에 따라 주기적으로 lint drift, duplication, unused code를 점검할 때 | repo maintainer, automation runtime, scheduled harness request | quality sweep report, cleanup backlog or PR candidate |
| `targeted` | 특정 경로, 반복 finding, reviewer note를 근거로 한정 스캔이 필요할 때 | implementer, reviewer, maintainer | bounded sweep result and handoff |

추가 규칙:

- workflow control plane은 scheduler 자체를 소유하지 않는다. `scheduled` trigger는 사용자의 요청, repo runtime, CI, 운영자 반복 작업 등 어떤 형태로 들어와도 되지만, 들어온 뒤의 분류와 handoff 규칙은 이 문서를 따른다.
- trigger mode가 무엇이든 original issue의 completion verdict는 그대로 유지하고, 새 follow-up work item을 별도로 만든다.

## Quality Signal Taxonomy

| Signal class | Typical signal | Default question | Preferred follow-up |
| --- | --- | --- | --- |
| `coding-rule-drift` | lint warning 증가, rule suppression 증가, formatter drift, repo rule과 맞지 않는 반복 패턴 | deterministic rule이나 CI gate가 더 일찍 막았어야 하는가 | `cleanup-pr-candidate` 또는 `guardrail-follow-up` |
| `duplication-drift` | copy-paste된 로직, 유사한 patch가 여러 파일로 퍼짐, 같은 handoff/boilerplate 반복 | 구조를 바꾸는 bounded refactor로 줄일 수 있는가 | `cleanup-pr-candidate` |
| `unused-code-drift` | unused export/helper/dependency, stale flag, dead path, 더 이상 호출되지 않는 route or config | 안전하게 제거 가능한 bounded dead code인가 | `cleanup-pr-candidate` 또는 `repair-now` |

추가 규칙:

- signal class는 detector가 아니라 quality drift의 종류를 의미한다.
- blocking runtime regression을 동반하는 dead path나 stale config는 `unused-code-drift`로 기록할 수 있어도 disposition은 `repair-now`일 수 있다.
- 같은 signal class가 반복되는데 detector나 gate가 없으면 quality drift 자체와 detector gap을 별도 root cause로 나눌 수 있다.

## Detection Surface Rule

quality sweep report에는 어떤 detector 또는 inspection surface를 썼는지 반드시 남긴다. 가능한 source는 아래 우선순위를 따른다.

1. impacted repo의 entry doc, package/build script, verification contract에 이미 정의된 deterministic command
2. repo-specific static analysis surface
3. reviewer note, completed exec plan, grep, manual code reading 같은 bounded inspection

추가 규칙:

- workflow 문서는 duplication/unused detector의 정확한 도구 이름을 강제하지 않는다.
- 반복되는 signal class인데 impacted repo에 detector가 전혀 없다면, 그 부재 자체를 `guardrail-follow-up` 후보로 남긴다.
- evidence 없이 "중복 같다", "안 쓰는 것 같다"만 적지 않는다. 최소한 grep, command output, path inventory, review note 중 하나가 있어야 한다.

## Enterprise Execution Pattern

enterprise-grade harness에서는 control plane과 detector runtime을 한 저장소에 몰아넣지 않는다. 기본 실행 패턴은 아래 세 갈래로 나눈다.

1. PR blocking lane
   - repo-local CI에서 빠르고 deterministic한 rule만 gate로 건다.
   - 예: lint, typecheck, build, unused import/variable, low-noise static analysis
2. Scheduled sweep lane
   - heavier duplication, unused export/file/dependency, wide-scope dead code scan은 default branch 기준 scheduled workflow나 maintainer-triggered workflow로 분리한다.
   - 이 lane은 original feature PR completion을 막기보다 cleanup candidate와 guardrail follow-up을 만든다.
3. Autofix lane
   - auto-generated cleanup PR은 semantic risk가 낮고 tool이 deterministic fix를 제공하는 경우에만 허용한다.
   - 예: formatter, lint autofix, unused import/dependency cleanup

추가 규칙:

- duplication refactor는 기본적으로 `cleanup-pr-candidate`다. report는 자동화할 수 있어도 refactor PR 생성은 bounded scope와 reviewability가 잠길 때만 연다.
- backend dead code removal은 framework reflection, Spring wiring, batch/job registration 영향이 있을 수 있으므로 issue-first를 기본으로 한다.
- frontend unused export/file/dependency cleanup은 repo-specific detector가 high-confidence fix를 제공하면 autofix lane 후보가 될 수 있다.
- control plane은 lane 선택, evidence, handoff를 잠그고, lane 실행 자체는 각 repo CI/workflow가 소유한다.

## Disposition Vocabulary

| Disposition | Choose when | Typical output |
| --- | --- | --- |
| `repair-now` | quality sweep이 사실상 correctness, contract, reliability, security bug를 다시 발견한 경우 | 새 bug/repair issue 또는 즉시 repair handoff |
| `cleanup-pr-candidate` | bounded write scope와 deterministic evidence가 있어 별도 cleanup issue/PR로 안전하게 분리 가능한 경우 | quality sweep report, cleanup issue/exec plan 또는 automated cleanup PR handoff |
| `guardrail-follow-up` | root cause가 missing detector, missing policy, weak CI gate, repeated noisy baseline처럼 system asset 부족인 경우 | feedback ledger entry, follow-up docs/skill/test/ci/template asset |
| `no-action` | false positive, duplicate report, 이미 current baseline에서 해소됨, 지금 자산화할 가치가 없는 one-off note인 경우 | explicit rationale only |

## Selection Rules

1. signal이 blocking bug면 `cleanup-pr-candidate`로 축소하지 않고 `repair-now`를 고른다.
2. non-blocking quality drift이고 bounded scope와 evidence가 있으면 `cleanup-pr-candidate`를 우선 검토한다.
3. 같은 signal class가 반복되는데 detector나 gate가 없으면 `guardrail-follow-up`을 검토한다.
4. confidence가 낮거나 write scope를 잠글 수 없으면 바로 cleanup PR을 약속하지 말고 `no-action` 또는 planning follow-up으로 돌린다.
5. quality sweep에서 나온 cleanup candidate는 original issue/PR에 뒤늦게 끼워 넣지 않는다. 새 issue/PR로 분리한다.
6. 하나의 cleanup candidate는 하나의 목표만 가진다. `Issue 1개 = PR 1개` 원칙을 그대로 따른다.

## Cleanup Handoff Rule

`cleanup-pr-candidate`를 선택했으면 최소한 아래를 next work item에 넘긴다.

- 대상 저장소
- bounded scan scope
- signal class
- detector 또는 inspection surface
- 핵심 evidence
- non-scope
- follow-up owner 또는 next action

추가 규칙:

- 현재 runtime이 직접 PR을 만들 수 있어도, scope가 잠겨 있지 않으면 먼저 issue와 exec plan으로 고정한다.
- automated cleanup PR은 allowed write scope, evidence, verification command를 설명할 수 있을 때만 허용한다.
- automated cleanup PR은 semantic risk가 낮고 repo-local autofix surface가 이미 검증된 signal class에만 쓴다.
- cleanup candidate가 여러 개면 path나 root cause별로 issue/PR을 분리한다.

## Quality Sweep Report Minimum

quality sweep 결과는 exec plan close-out, review note, 또는 follow-up artifact 중 최소 한 곳에 [quality-sweep-report-template.md](quality-sweep-report-template.md)의 형식으로 남긴다.

필수 필드:

- trigger mode
- source repo와 source task/PR/baseline
- scan scope
- detection surface
- signal class
- trigger signal
- severity
- disposition
- evidence
- owner / next action

quality sweep report가 없으면 cleanup candidate나 guardrail follow-up handoff가 잠긴 것으로 보지 않는다.

## Relationship To Other Policies

- current issue의 completion gate와 repair budget은 계속 [verification-contract-registry.md](verification-contract-registry.md)가 canonical source다.
- reviewer verdict vocabulary와 blocking review finding은 계속 [dual-agent-review-policy.md](dual-agent-review-policy.md)가 canonical source다.
- close-out 시점의 failure taxonomy, guardrail promotion decision, ledger entry는 계속 [failure-to-guardrail-feedback-loop.md](failure-to-guardrail-feedback-loop.md)가 canonical source다.
- 이 문서는 close-out 이후 recurring quality sweep과 cleanup candidate handoff만 맡는다.
