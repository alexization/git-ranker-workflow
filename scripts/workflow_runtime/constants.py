from __future__ import annotations

from pathlib import Path

TASK_STATES = {"draft", "approved", "in_progress", "failed", "blocked", "review_ready", "completed"}
PHASE_STATES = {"pending", "in_progress", "completed", "failed", "blocked"}

TASK_TRANSITIONS = {
    "draft": {"approved"},
    "approved": {"in_progress", "blocked"},
    "in_progress": {"approved", "failed", "blocked", "review_ready", "completed"},
    "failed": {"approved", "in_progress", "blocked"},
    "blocked": {"approved", "in_progress"},
    "review_ready": {"completed", "blocked"},
    "completed": set(),
}

PHASE_TRANSITIONS = {
    "pending": {"in_progress", "blocked"},
    "in_progress": {"completed", "failed", "blocked"},
    "failed": {"pending", "in_progress", "blocked"},
    "blocked": {"pending", "in_progress"},
    "completed": {"pending", "failed", "blocked"},
}

SPEC_REQUIRED_SECTIONS = [
    "Request",
    "Problem",
    "Goals",
    "Non-goals",
    "Constraints",
    "Acceptance",
    "Socratic Clarification Log",
]

AGENTS_REQUIRED_HEADINGS = [
    "## Mission",
    "## Start Here",
    "## CRITICAL Rules",
    "## Architecture Boundaries",
    "## Workflow Contract",
    "## TDD Contract",
    "## Command Contract",
    "## Source Of Truth Order",
    "## Forbidden Actions",
    "## Change Discipline",
]

AGENTS_REQUIRED_KEYWORDS = [
    "CRITICAL:",
    "ALWAYS:",
    "NEVER:",
]

DOC_FILES = [
    "docs/README.md",
    "docs/artifact-model.md",
    "docs/runtime.md",
    "docs/hooks.md",
    "docs/runbook.md",
]

DOC_REQUIRED_MARKERS = {
    "docs/README.md": ["AGENTS.md", "docs/runtime.md", "docs/artifact-model.md"],
    "docs/artifact-model.md": ["task.json", "intake", "clarifications"],
    "docs/runtime.md": ["소크라테스 질문", "approve", "plan", "review --close"],
    "docs/hooks.md": [".githooks/", "TDD Guard", "Dangerous Command Guard", "Circuit Breaker", "workflow.py hook"],
    "docs/runbook.md": ["사용자가 현재 spec 초안에 명시적으로 동의하면 approve 한다.", "approve", "plan"],
}

STALE_REFERENCE_PATTERNS = [
    "docs/workflow/",
    "SPECS.md",
    "docs/specs/",
    "docs/operations/",
    "docs/architecture/",
    "workflows/config/",
    "workflows/runtime/",
    "workflows/schemas/",
    "scripts/hooks/",
    "workflow_lib.py",
]

STALE_REFERENCE_SCAN_EXCLUDES = {
    Path("scripts/workflow_runtime/constants.py"),
    Path("scripts/workflow_runtime/doctor.py"),
    Path(".github/workflows/workflow-control-plane.yml"),
}
