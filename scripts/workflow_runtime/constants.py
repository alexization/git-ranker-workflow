from __future__ import annotations

CURRENT_TASK_CONTRACT_VERSION = 4

TASK_STATES = {"draft", "approved", "in_progress", "failed", "review_ready", "completed"}
IMPLEMENTATION_STATES = {"pending", "in_progress", "completed", "failed"}
VERIFICATION_STATES = {"not_run", "passed", "failed", "skipped"}

SPEC_REQUIRED_SECTIONS = [
    "Request",
    "Problem",
    "Goals",
    "Non-goals",
    "Constraints",
    "Acceptance",
    "Implementation Scopes",
    "Socratic Clarification Log",
]

EVENT_LIMIT = 50
