---
summary: Useful workflow patterns adapted from steipete repositories.
read_when:
  - refining docs structure
  - deciding how much detail belongs in AGENTS versus docs
---

# steipete workflow analysis

Sources reviewed:

- https://github.com/steipete
- https://raw.githubusercontent.com/steipete/oracle/main/AGENTS.md
- https://raw.githubusercontent.com/steipete/agent-scripts/main/AGENTS.MD
- https://raw.githubusercontent.com/steipete/Peekaboo/main/docs/ARCHITECTURE.md
- https://raw.githubusercontent.com/steipete/Peekaboo/main/docs/testing/tools.md

## Patterns worth reusing

### 1. Short AGENTS, dense docs

steipete keeps `AGENTS` directive-heavy but still points to focused docs rather
than collapsing everything into one file. That supports fast context loading.

### 2. `read_when` front matter

Purpose-driven docs are easier for agents to load when the file itself states
when it should be consulted. This repository adopts that pattern in `docs/`.

### 3. Artifact-oriented testing

The Peekaboo testing docs record exact logs, artifact paths, execution loops, and
pass criteria. That pattern maps well to Playwright, CDP, and local observability
artifacts here.

### 4. Docs are part of the implementation

steipete's repos treat doc updates as part of finishing a feature. This
repository adopts the same rule.

## What was not copied directly

Those repos are optimized for different products and toolchains. The structure
here preserves the transferable workflow ideas while staying aligned to OpenAI's
harness-engineering model as the primary source of truth.

