---
summary: Reliability expectations and evidence rules for runtime behavior.
read_when:
  - changing startup flow
  - touching async jobs, APIs, or critical user journeys
---

# Reliability

## Principle

Reliability requirements must be phrased as observable behavior, not vague
intent.

## Every reliability-sensitive task should answer

- which journey matters?
- what latency or failure budget matters?
- how will logs and metrics prove compliance?

## Default expectations

- startup should be measured, not assumed
- critical journeys should have named owners and evidence
- no regression claim is valid without an artifact path

## Evidence examples

- `LogQL`: service startup completed without retries or fatal errors
- `PromQL`: request or job latency remained under the target threshold

Exact thresholds belong in the relevant ExecPlan until stable enough to promote
into a permanent doc.
