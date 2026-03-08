---
summary: Intake contract for feature requests before implementation begins.
read_when:
  - before starting any new feature
  - when the request is vague or spans frontend and backend
---

# Feature Request Intake

Before implementation begins, rewrite every request in the following shape.

## 1. Problem

What user problem or business problem is being solved?

## 2. User-visible outcome

What can the user do after this change that they could not do before?

## 3. Affected repos

- `git-ranker`
- `git-ranker-client`
- `knowledge-store only`

## 4. Contract surface

List any API, schema, event, route, or copy changes.

## 5. Acceptance checks

Describe the exact behavior to observe when the change works.

## 6. QA evidence

List the minimum required evidence:

- test commands
- Playwright journey names
- CDP checks
- log queries
- performance or trace checks when relevant

## 7. Non-goals

State what this request is not trying to solve.

## 8. Risks

List migration, compatibility, reliability, or security risks.

## Output format

Use this checklist at the top of an ExecPlan or task note:

```text
Problem:
User-visible outcome:
Affected repos:
Contract surface:
Acceptance checks:
QA evidence:
Non-goals:
Risks:
```

