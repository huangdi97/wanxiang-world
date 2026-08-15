"""Shared evidence review rules for source-bound candidates (G35D).

M32: one rule set shared by the identity review gate (G35C) and the
place/object/organization review gate (G35D) so evidence rules never drift
between candidate kinds. Pure functions only; no state, no write path.
"""

from __future__ import annotations

from wanxiang_substrate.sources.locator import SourceLocator, source_slice

AUTHORIZED_REVIEWERS = ("human", "reviewer")


def evidence_ok(
    *,
    locators_per_claim: tuple[tuple[SourceLocator, ...], ...],
    source_text: str,
    min_evidence_locators: int,
) -> tuple[bool, str]:
    """True iff every claim has >= min resolvable locators.

    Returns (ok, reason). A claim without evidence, or whose locator cannot
    resolve to a non-empty source slice, is rejected. Candidates never enter
    Canon through this helper: it only decides eligibility of a candidate.
    """
    if not locators_per_claim:
        return False, "candidate lacks evidence-backed claims"
    for locators in locators_per_claim:
        if len(locators) < min_evidence_locators:
            return False, "claim lacks required evidence"
        for locator in locators:
            if not source_slice(source_text, locator).strip():
                return False, "claim locator does not resolve"
    return True, ""
