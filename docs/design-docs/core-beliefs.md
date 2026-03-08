---
summary: Core beliefs for an agent-first repository.
read_when:
  - making architecture or workflow decisions
  - deciding whether a rule belongs in code, docs, or a prompt
---

# Core Beliefs

## 1. Repository-local knowledge wins

If a fact matters to future work, it must live in versioned files inside this
repository or the application repos. Chat logs, memory, and oral tradition do
not count.

## 2. Legibility beats cleverness

Prefer technologies, abstractions, and folder structures that a stateless agent
can inspect, understand, and modify without hidden context.

## 3. AGENTS is a map, not the encyclopedia

Keep `AGENTS.md` concise. Promote durable instructions into purpose-built docs or
mechanical checks.

## 4. Boundaries are leverage

Strict layering, naming, and evidence requirements are not bureaucracy. They are
what lets agents move quickly without spreading architectural drift.

## 5. Behavior matters more than code motion

Every change must end in observable behavior: a journey that passes, an error
that disappears, a metric that stays below target, or a trace that no longer
regresses.

## 6. Feedback loops are part of the product

Playwright specs, CDP inspection, logs, metrics, traces, and review loops are
first-class system components. If they are missing, the workflow is incomplete.

## 7. Continuous cleanup is mandatory

Bad patterns compound quickly in an AI-heavy codebase. Capture taste once,
enforce it repeatedly, and keep the debt surface small.

