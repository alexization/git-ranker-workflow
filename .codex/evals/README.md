# Evals

Use this directory for repo-local eval definitions that measure whether the AI
workflow and the product behavior are improving or regressing.

Recommended layout:

```text
.codex/evals/
  templates/
  <feature-name>.md
  <feature-name>.log
```

For non-trivial changes, define:

- capability evals for the new behavior
- regression evals for the old behavior that must keep working
- clear pass or fail evidence

