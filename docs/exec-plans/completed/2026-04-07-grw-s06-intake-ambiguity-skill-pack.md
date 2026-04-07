# 2026-04-07-grw-s06-intake-ambiguity-skill-pack

- Issue ID: `GRW-S06`
- GitHub Issue: `#47`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s06-intake-ambiguity-skill-pack`
- Task Slug: `2026-04-07-grw-s06-intake-ambiguity-skill-pack`
- Primary Context Pack: `workflow-docs`
- Verification Contract Profile: `workflow-docs`

## Problem

`GRW-12`에서 request routing과 ambiguity interview 정책은 source of truth로 고정됐지만, 실제 작업자가 같은 입력과 종료 조건으로 intake를 반복 수행하게 만드는 project-local skill은 아직 없다.

이 상태에서는 같은 요청도 작업자별로 `대화`, `모호한 요청`, `즉시 실행 가능한 작업` 분류가 흔들릴 수 있고, ambiguity interview가 범위를 줄이는 절차가 아니라 구현 아이디어를 늘리는 절차로 drift할 수 있다.

## Why Now

`GRW-S06`은 Phase 2 skill pack의 첫 단계다. intake 절차를 먼저 반복 가능한 실행 레시피로 고정해야 이후 `context-pack-selection`, `boundary-check`, `verification-contract-runner`, `reviewer-handoff`도 같은 route taxonomy와 exit condition을 재사용할 수 있다.

또한 workflow issue template과 `issue-to-exec-plan` skill이 이미 intake 필드와 exec plan handoff를 강제하고 있으므로, 이제는 그 입력을 어떻게 읽고 좁히고 종료시키는지를 skill로 연결해야 한다.

## Scope

- `.codex/skills/request-intake/SKILL.md` 작성
- `.codex/skills/ambiguity-interview/SKILL.md` 작성
- `.codex/skills/README.md`에 registry 및 추천 사용 순서 반영
- `.codex/skills/authoring-rules.md`에 policy와 skill의 관리 경계 명시
- `GRW-S06` active exec plan 작성과 완료 기록 정리

## Non-scope

- 신규 에이전트 런타임 구현
- GitHub issue/exec plan 자동 생성 로직 추가
- `GRW-S07`, `GRW-S08`, `GRW-S09` skill 작성
- backend/frontend 앱 코드 변경

## Write Scope

- Primary repo: `git-ranker-workflow`
- Allowed write paths:
  - `.codex/skills/`
  - `docs/exec-plans/`
- Control-plane artifacts:
  - `docs/exec-plans/active/2026-04-07-grw-s06-intake-ambiguity-skill-pack.md`
  - `docs/exec-plans/completed/2026-04-07-grw-s06-intake-ambiguity-skill-pack.md`
- Explicitly forbidden:
  - sibling app repo code tree
  - `docs/operations/`, `docs/architecture/`, `docs/product/`의 unrelated stable source of truth 수정
- Network / external systems:
  - GitHub issue metadata 확인과 생성
- Escalation triggers:
  - 없음

## Outputs

- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `.codex/skills/README.md`
- `docs/exec-plans/completed/2026-04-07-grw-s06-intake-ambiguity-skill-pack.md`

## Working Decisions

- `request-intake`는 route classification, ambiguity signal 확인, 다음 행동 결정을 담당하고 파일 편집이나 issue/exec plan 생성 자체를 소유하지 않는다.
- `ambiguity-interview`는 source of truth 기반 blocker 축소, one-question-at-a-time interview, exit condition 정리를 담당한다.
- `Planned`로 수렴한 뒤 GitHub issue와 exec plan 생성 handoff는 기존 `issue-to-exec-plan` skill을 재사용한다.
- 두 skill 모두 `docs/operations/request-routing-policy.md`를 canonical source로 삼고 새 taxonomy를 발명하지 않는다.

## Verification

- `find .codex/skills -maxdepth 2 -type f | sort`
  - 결과: `.codex/skills/request-intake/SKILL.md`, `.codex/skills/ambiguity-interview/SKILL.md`가 registry 문서와 함께 기대 경로에 생성된 것을 확인했다.
- `sed -n '1,260p' .codex/skills/request-intake/SKILL.md`
  - 결과: route classification, `Rejected` close-out reason 기록, required evidence, forbidden shortcuts, example input/output, `issue-to-exec-plan` handoff가 포함된 것을 확인했다.
- `sed -n '1,280p' .codex/skills/ambiguity-interview/SKILL.md`
  - 결과: blocker 중심 질문 규칙, `Planned`/`Blocked`/`Rejected` exit summary, canonical close-out reason 참조, example interview output이 포함된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/authoring-rules.md`
  - 결과: policy와 skill의 canonical ownership, policy 표 복사 금지, registry 관리 문서의 task ID 금지 규칙이 추가된 것을 확인했다.
- `sed -n '1,220p' .codex/skills/README.md`
  - 결과: skill registry에 `request-intake`, `ambiguity-interview`가 추가되고, canonical ownership section과 intake에서 planning으로 이어지는 추천 사용 순서가 반영되며 task ID가 제거된 것을 확인했다.
- `sed -n '35,140p' .codex/skills/issue-to-exec-plan/SKILL.md` / `sed -n '75,130p' .codex/skills/parallel-work-split/SKILL.md`
  - 결과: 샘플 명령, example input/output, 날짜/issue/slug 예시가 placeholder 기반으로 정리되어 특정 과거 work item을 재사용하지 않는 것을 확인했다.
- `rg -n "request-intake|ambiguity-interview|Recommended Use|Rejected|즉시 실행 가능한 작업|모호한 요청" .codex/skills/README.md .codex/skills/request-intake/SKILL.md .codex/skills/ambiguity-interview/SKILL.md docs/operations/request-routing-policy.md`
  - 결과: 새 skill 문서와 registry가 `request-routing-policy.md`의 route taxonomy, `Rejected` semantics, intake flow 용어와 함께 grep되는 것을 확인했다.
- `rg -n "GRW-|GRB-|GRC-" .codex/skills/README.md .codex/skills/authoring-rules.md .codex/skills/request-intake/SKILL.md .codex/skills/ambiguity-interview/SKILL.md`
  - 결과: 이번에 갱신한 skill registry, authoring rules, `GRW-S06` skill 문서에서는 task ID가 더 이상 남지 않는 것을 확인했다.
- `gh issue view --repo alexization/git-ranker-workflow 47 --json body,title,number`
  - 결과: GitHub Issue `#47` 본문이 template 섹션과 줄바꿈을 유지한 채 생성된 것을 확인했다.
- 예시 요청 2건 수동 시뮬레이션 검토
  - 결과: `request-intake`는 "랭킹 화면 좀 개선해줘"를 `모호한 요청`으로 분류하고 `ambiguity-interview` handoff를 남길 수 있었고, `ambiguity-interview`는 multi-repo 요청을 primary repo 질문 하나로 줄여 `Planned` summary 예시를 만들 수 있었다.
- `git diff --check`
  - 결과: whitespace 또는 conflict marker 문제 없이 통과했다.
- `gh api repos/alexization/git-ranker-workflow/pulls/48/comments`
  - 결과: automated review가 `request-intake`의 `Rejected` close-out 누락을 지적했고, skill output과 handoff에 terminal close-out reason 기록을 추가해 정책과 맞췄다.

## Evidence

문서형 skill 작업이므로 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 skill 본문, registry 갱신, 예시 요청 시뮬레이션, GitHub issue body render 확인 결과를 close-out에 남긴다.

## Independent Review

- Implementer: `Codex`
- Reviewer: `Gemini CLI (gemini-2.5-flash)`
- Reviewer Input:
  - Exec plan: `docs/exec-plans/completed/2026-04-07-grw-s06-intake-ambiguity-skill-pack.md`
  - Latest verification report: `passed`
  - Diff summary: intake skill 2종 추가, skill registry/authoring rules의 policy-skill boundary 정리, 기존 skill 예시의 placeholder 일반화
  - Source-of-truth update: `.codex/skills/README.md`, `.codex/skills/authoring-rules.md`, `.codex/skills/request-intake/SKILL.md`, `.codex/skills/ambiguity-interview/SKILL.md`, `.codex/skills/issue-to-exec-plan/SKILL.md`, `.codex/skills/parallel-work-split/SKILL.md`
  - Remaining risks / skipped checks: 문서형 변경이므로 runtime/build 계열 conditional command 없음
- Review Verdict: `approved`
- Findings / Change Requests:
  - blocking finding 없음
  - non-blocking note였던 `api-contract-sync` 추천 순서 문구는 조건부 hook으로 다시 정리했다.
- Evidence:
- reviewer는 request routing policy, workflow governance, dual-agent review policy, exec plan, changed skill 문서를 기준으로 scope drift, policy contradiction, verification mismatch 여부를 검토했고 `approved` verdict를 남겼다.
- 후속 PR review에서 `request-intake`의 `Rejected` close-out 누락이 지적됐고, 이번 수정으로 `conversation-only`, `cancelled`, `out-of-scope`, `missing-canonical-source` 기록 규칙을 skill output에 반영했다.

## Risks or Blockers

- `request-intake`가 `issue-to-exec-plan`과 책임이 겹치지 않도록, 새 skill 본문에서 issue/exec plan 생성은 handoff 이후 단계로 명시했다.
- `ambiguity-interview`가 질문 수를 늘리는 방향으로 drift하지 않도록 one-question blocker 규칙과 두 라운드 뒤 stop condition을 본문에 명시했다.

## Next Preconditions

- `GRW-S07`: context pack 선택과 boundary 검토를 별도 skill로 고정
- `GRW-S08`: verification/review handoff를 별도 skill로 고정

## Docs Updated

- `.codex/skills/request-intake/SKILL.md`
- `.codex/skills/ambiguity-interview/SKILL.md`
- `.codex/skills/README.md`
- `.codex/skills/authoring-rules.md`
- `.codex/skills/issue-to-exec-plan/SKILL.md`
- `.codex/skills/parallel-work-split/SKILL.md`
- `docs/exec-plans/completed/2026-04-07-grw-s06-intake-ambiguity-skill-pack.md`

## Skill Consideration

이번 Issue 자체가 intake skill pack을 추가하는 작업이다. 새 skill은 정책 문서를 대체하지 않고, route classification과 ambiguity interview를 같은 입력/출력/증거 규칙으로 재현하게 만드는 실행 레시피에 집중한다.
