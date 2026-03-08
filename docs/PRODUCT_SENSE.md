---
summary: Product framing rules that convert requests into stable acceptance criteria.
read_when:
  - clarifying scope
  - deciding whether a change is complete
---

# Product Sense

## Principle

Do not implement from ambiguous desire statements. Convert requests into stable,
testable behavior statements first.

## Required questions

- Who benefits from the change?
- What exact workflow improves?
- What is the smallest observable version of the outcome?
- What must remain unchanged?
- How will we know the feature actually works?

## Completion test

A feature is not complete when the code exists. It is complete when:

- the user-visible outcome is real
- the acceptance checks pass
- the QA evidence exists
- the docs explain the new durable behavior

