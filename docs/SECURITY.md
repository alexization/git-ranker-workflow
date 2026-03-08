---
summary: Security baseline for frontend/backend workflow changes.
read_when:
  - handling user input
  - changing auth, secrets, or external integrations
---

# Security

## Baseline

- validate all untrusted input at the boundary
- keep secrets out of the frontend
- log safely; do not leak secrets or raw credentials
- prefer least-privilege connectors
- treat auth and authorization as explicit requirements, not assumptions

## Required review triggers

Do an explicit security pass when the change touches:

- authentication
- authorization
- user-generated content
- file upload or download
- external webhooks or callbacks
- tokens, API keys, or cookies

## Documentation rule

If a task changes a security-relevant behavior, the relevant doc and ExecPlan
must say what changed and how it was verified.

