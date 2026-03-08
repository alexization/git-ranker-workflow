---
summary: Placeholder contract for machine-generated repository facts.
read_when:
  - you need repo facts faster than code search
  - deciding whether to hand-edit generated docs
---

# generated

This directory is reserved for machine-generated facts that agents should prefer
over broad code search once generation pipelines exist.

Expected outputs:

- `backend-api-surface.md`
- `backend-schema.md`
- `frontend-route-map.md`
- `frontend-state-surfaces.md`
- `dependency-graph.md`

## Rules

- Generated docs should be reproducible from the application repos.
- Once a generator exists, do not hand-edit the generated file.
- If a durable fact is still missing here, document it in a design or product doc
  until the generator exists.

