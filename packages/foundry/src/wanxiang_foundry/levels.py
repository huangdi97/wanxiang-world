"""Knowledge and promotion levels for capability packages.

A knowledge level describes *how a capability's behaviour is known*. A promotion
level describes *how far the capability has been admitted*, from raw artifact to
accredited capability.

INVARIANT: no knowledge or promotion level implies world truth. A K3/C3 package
is verified in an environment, not guaranteed correct about the world; only a
commit authority (outside this package) can turn a proposal into canonical state.

C3 is the highest level the foundry automation may grant on its own. C4 and C5
require a human or organisational decision and are never produced by automation.
"""

from __future__ import annotations

from enum import StrEnum


class KnowledgeLevel(StrEnum):
    """How a capability's behaviour is known."""

    K0_TEXT = "k0_text"
    K1_STRUCTURED = "k1_structured"
    K2_EXECUTABLE = "k2_executable"
    K3_VERIFIED_ENVIRONMENTAL = "k3_verified_environmental"


class PromotionLevel(StrEnum):
    """How far a capability has been admitted by the foundry."""

    C0_RAW = "c0_raw"
    C1_BUILT = "c1_built"
    C2_RUNNABLE = "c2_runnable"
    C3_VERIFIED = "c3_verified"
    C4_DOMAIN_APPROVED = "c4_domain_approved"
    C5_ACCREDITED = "c5_accredited"


AUTOMATION_MAX_PROMOTION = PromotionLevel.C3_VERIFIED
"""Highest promotion level the foundry automation may grant on its own."""


def is_automation_grantable(level: PromotionLevel) -> bool:
    """Return True when automation (not a human/organisation) may grant level.

    Args:
        level: Promotion level to test.

    Returns:
        True for C0 through C3, False for C4 and C5.
    """
    order = list(PromotionLevel)
    return order.index(level) <= order.index(AUTOMATION_MAX_PROMOTION)
