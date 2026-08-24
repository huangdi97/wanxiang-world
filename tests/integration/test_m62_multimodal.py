"""M62 provider-port, subtitle, connector, and bundle-rights contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.multimodal import (
    BundleEntry,
    ExternalSourceRequest,
    MediaLocator,
    ReferenceExternalConnector,
    SourceBundleManifest,
    SubtitleAdapter,
)
from wanxiang_substrate.authoring.providers import (
    ProviderCapability,
    ProviderRouter,
    ReferenceProvider,
)
from wanxiang_substrate.sources.errors import CapabilityUnavailable, OcrRequired


@pytest.mark.integration
def test_optional_provider_ports_fail_explicitly_without_fabrication() -> None:
    router = ProviderRouter()
    with pytest.raises(OcrRequired, match="OCR_REQUIRED"):
        router.propose("ocr", ("scan#1",), "image")
    with pytest.raises(CapabilityUnavailable, match="CAPABILITY_UNAVAILABLE"):
        router.propose("asr", ("audio#1",), "audio")
    with pytest.raises(CapabilityUnavailable, match="vision"):
        router.require("vision", ("image#1",))

    provider = ReferenceProvider(ProviderCapability("offline_vision", "vision", "1"))
    proposals = ProviderRouter((provider,)).propose("vision", ("image#1",), "pixels")
    assert proposals[0].kind == "candidate"
    assert not hasattr(proposals[0], "commit")


@pytest.mark.integration
def test_subtitle_adapter_and_media_locator_are_stable() -> None:
    srt = """1
00:00:01,000 --> 00:00:02,500
Hello world.

2
00:00:03,000 --> 00:00:04,000
Second cue.
"""
    cues = SubtitleAdapter().parse("video_1", srt)
    assert [(cue.cue_id, cue.start_ms, cue.end_ms) for cue in cues] == [
        ("1", 1000, 2500),
        ("2", 3000, 4000),
    ]
    assert MediaLocator("video_1", "audio", 1000, 2500, page=1).to_string() == (
        "audio://video_1@1000-2500/page/1"
    )
    with pytest.raises(ValueError):
        SubtitleAdapter().parse("video_1", "1\n00:00:01,000 --> 00:00:00,500\ninvalid")


@pytest.mark.unit
def test_iiif_reference_connector_is_a_non_network_observation_port() -> None:
    observation = ReferenceExternalConnector().observe(
        ExternalSourceRequest("iiif_1", "iiif://manifest/1", "a" * 64)
    )
    assert observation.available is False
    assert observation.content_hash == "a" * 64
    assert observation.diagnostics == ("EXTERNAL_FETCH_DISABLED_REFERENCE",)


@pytest.mark.integration
def test_bundle_manifest_is_deterministic_and_rights_private_aware() -> None:
    entries = (
        BundleEntry("family_private", "image", "b" * 64, True, private=True),
        BundleEntry("caption", "text", "a" * 64, False),
    )
    first = SourceBundleManifest.build("bundle_m62", entries)
    second = SourceBundleManifest.build("bundle_m62", tuple(reversed(entries)))
    assert first.manifest_hash == second.manifest_hash
    assert first.rights_ok is False
    assert first.rights_blockers == ("caption",)
    assert first.private_source_ids == ("family_private",)
    with pytest.raises(ValueError, match="unique"):
        SourceBundleManifest.build("duplicate", (entries[0], entries[0]))
