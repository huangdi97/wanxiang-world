"""G90F: visibility and rights publication boundaries."""

from __future__ import annotations

from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.workshop import (
    PackageMetadata,
    PublishingPolicy,
    PublishingProfile,
    RightsSummary,
    SafetyExtensionPoints,
)


def _metadata() -> PackageMetadata:
    return PackageMetadata(
        "world:publish",
        "1.0.0",
        "Publishable World",
        categories=("literary",),
        tags=("reference",),
        compatibility=("v5.4",),
        provenance_refs=("source:approved",),
    )


def test_private_publish_is_not_a_plaza_listing() -> None:
    profile = PublishingProfile(
        "publish_private",
        "private",
        "alice",
        _metadata(),
        RightsSummary.creator_intent("intent_private"),
        SafetyExtensionPoints("moderation:v1"),
    )
    decision = PublishingPolicy().assess(profile)
    assert decision.publishable is True
    assert decision.visible_in_plaza is False


def test_blocked_source_cannot_publish_publicly() -> None:
    content = "private source"
    source = SourceRecord(
        "blocked_source",
        "text",
        payload_hash(content),
        "memory://blocked_source",
        stage="E2",
        rights=RightsEnvelope("owner", "review", approved=False),
        payload=content,
    )
    profile = PublishingProfile(
        "publish_blocked",
        "public",
        "alice",
        _metadata(),
        RightsSummary.from_sources((source,)),
    )
    decision = PublishingPolicy().assess(profile)
    assert decision.publishable is False
    assert "rights" in " ".join(decision.reasons)
    assert decision.visible_in_plaza is False
