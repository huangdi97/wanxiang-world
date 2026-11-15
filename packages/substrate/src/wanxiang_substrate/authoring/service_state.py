"""One product-state rule for a pipeline build (shared by every client surface).

A refusal the client receives and the job status it can poll must never disagree
about *why* a world was not produced. Measured defect (2026-11-13): a bundle whose
sources disagree was refused with `details.product_state == "ZERO_COVERAGE"` while
`GET /studio/jobs/{id}` reported `REVIEW_REQUIRED` for the same job.

Both surfaces therefore derive the state from the same ordered draft facts, and the
refusal adds the viewed reason only where the draft itself cannot explain it.
"""

from __future__ import annotations

from wanxiang_substrate.authoring.model import PipelineBuild

# The state a refusal carries when the draft is ready and only the compiler's own
# pinning/consistency gate failed: nothing in the draft tells the client what to do.
_COMPILER_REFUSED = "COMPILER_REFUSED"


def product_state_for_build(build: PipelineBuild) -> str:
    """The state of one build as the job status surface reports it."""

    draft = build.draft
    if draft.unresolved_rights:
        return "RIGHTS_ACTION_REQUIRED"
    if draft.coverage <= 0.0:
        return "ZERO_COVERAGE"
    if draft.status != "READY_TO_COMPILE":
        return "REVIEW_REQUIRED"
    return "READY"


def product_state_for_refusal(build: PipelineBuild, reasons: tuple[str, ...]) -> str:
    """The state of a refused compile, derived from the same draft facts."""

    if any("rights" in reason for reason in reasons):
        return "RIGHTS_ACTION_REQUIRED"
    state = product_state_for_build(build)
    return state if state != "READY" else _COMPILER_REFUSED


def refusal_details(build: PipelineBuild, reasons: tuple[str, ...]) -> dict[str, str]:
    """Diagnosis payload for a refused compile: the state plus what blocked it."""

    details = {"product_state": product_state_for_refusal(build, reasons)}
    conflicts = len(build.draft.unresolved_conflicts)
    if conflicts:
        details["unresolved_conflicts"] = str(conflicts)
    return details
