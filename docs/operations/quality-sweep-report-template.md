# Quality Sweep Report Template

이 문서는 [continuous-quality-feedback-loop.md](continuous-quality-feedback-loop.md)의 canonical quality sweep report 형식을 제공한다. cleanup candidate, guardrail follow-up, repair-now handoff는 최소한 아래 필드를 포함한 report 하나로 남긴다.

## Report Template

```md
## Quality Sweep Report
- Date:
- Trigger mode:
  - `post-closeout | scheduled | targeted`
- Source repo:
- Source task / PR / baseline:
- Scan scope:
- Detection surface:
- Signal class:
  - `coding-rule-drift | duplication-drift | unused-code-drift`
- Trigger signal:
- Root cause hypothesis:
- Severity:
  - `blocking | non-blocking`
- Existing guardrail:
- Disposition:
  - `repair-now | cleanup-pr-candidate | guardrail-follow-up | no-action`
- Follow-up asset / issue / PR:
- Owner / next action:
- Evidence:
- Notes:
```

## Writing Rules

- report 하나에는 signal class 하나만 적는다.
- `Trigger signal`은 symptom이고, `Root cause hypothesis`는 왜 이 quality drift가 다시 생길 수 있는지에 대한 가설이다.
- `Detection surface`에는 command, grep, review note, repo-specific detector 중 실제로 쓴 경로를 적는다.
- `Existing guardrail`에는 이미 있던 lint rule, docs rule, CI gate, detector가 있으면 적고, 없으면 `없음`이라고 적는다.
- `cleanup-pr-candidate`를 고르면 follow-up asset에 대상 issue, PR candidate, spec path 중 최소 하나를 적는다.
- `no-action`을 고르면 `Notes`에 왜 지금은 follow-up을 만들지 않는지 적는다.

## Minimal Example

```md
## Quality Sweep Report
- Date: `2026-04-08`
- Trigger mode:
  - `post-closeout`
- Source repo: `git-ranker-client`
- Source task / PR / baseline: `docs/specs/completed/2026-04-08-sample.md`
- Scan scope: `src/features/ranking`
- Detection surface: `npm run lint` warning summary와 reviewer note
- Signal class:
  - `unused-code-drift`
- Trigger signal: unused ranking prefetch helper가 current route tree에서 더 이상 호출되지 않는다.
- Root cause hypothesis: route refactor 이후 stale helper cleanup이 follow-up 없이 남았다.
- Severity:
  - `non-blocking`
- Existing guardrail: `없음`
- Disposition:
  - `cleanup-pr-candidate`
- Follow-up asset / issue / PR: cleanup issue 초안
- Owner / next action: request-intake로 새 cleanup issue를 시작한다.
- Evidence: lint warning, grep path inventory, reviewer note
- Notes: current issue completion verdict는 유지한다.
```
