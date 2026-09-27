"""Knowledge and promotion level vocabulary and the automation ceiling."""

from __future__ import annotations

import pytest
from wanxiang_foundry.levels import (
    AUTOMATION_MAX_PROMOTION,
    KnowledgeLevel,
    PromotionLevel,
    is_automation_grantable,
)


@pytest.mark.unit
def test_knowledge_levels_span_k0_to_k3() -> None:
    assert list(KnowledgeLevel) == [
        KnowledgeLevel.K0_TEXT,
        KnowledgeLevel.K1_STRUCTURED,
        KnowledgeLevel.K2_EXECUTABLE,
        KnowledgeLevel.K3_VERIFIED_ENVIRONMENTAL,
    ]


@pytest.mark.unit
def test_promotion_levels_span_c0_to_c5() -> None:
    assert list(PromotionLevel) == [
        PromotionLevel.C0_RAW,
        PromotionLevel.C1_BUILT,
        PromotionLevel.C2_RUNNABLE,
        PromotionLevel.C3_VERIFIED,
        PromotionLevel.C4_DOMAIN_APPROVED,
        PromotionLevel.C5_ACCREDITED,
    ]


@pytest.mark.unit
def test_automation_may_grant_only_up_to_c3() -> None:
    assert is_automation_grantable(PromotionLevel.C3_VERIFIED)
    assert not is_automation_grantable(PromotionLevel.C4_DOMAIN_APPROVED)
    assert not is_automation_grantable(PromotionLevel.C5_ACCREDITED)


@pytest.mark.unit
def test_automation_ceiling_is_c3() -> None:
    assert AUTOMATION_MAX_PROMOTION is PromotionLevel.C3_VERIFIED
