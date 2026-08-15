"""M42: production release readiness (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.release import (
    build_release_bundle,
    certify_release,
    freeze_sdk,
)


@pytest.mark.unit
def test_sdk_freeze() -> None:
    freeze = freeze_sdk(17, 5, 1169)
    assert freeze.sdk_routes == 17
    assert freeze.api_frozen is True
    assert "additive-only" in freeze.compat_policy


@pytest.mark.unit
def test_release_bundle_metadata() -> None:
    bundle = build_release_bundle(
        bundle_id="rc001_bundle",
        content_hash="a" * 64,
        rights_refs=("worldpack:literary-historical",),
        source_metadata=("edition:EXTERNAL_BLOCKED",),
        scenario_catalog=("arrival", "illness"),
        release_notes="RC-001 synthetic release notes",
    )
    assert bundle.content_hash == "a" * 64
    assert bundle.scenario_catalog == ("arrival", "illness")
    assert "synthetic" in bundle.release_notes


@pytest.mark.unit
def test_final_certification_gates() -> None:
    cert = certify_release(
        version="v5.2.0",
        quality_passed=978,
        quality_skipped=1,
        red_chamber_real="EXTERNAL_BLOCKED",
        tag="m42-v5.2-production",
    )
    assert cert.status.startswith("V5_2_PRODUCTION_PASS")
    assert cert.red_chamber_real == "EXTERNAL_BLOCKED"
    assert cert.tag == "m42-v5.2-production"


@pytest.mark.unit
def test_certification_refused_when_gates_red() -> None:
    from wanxiang_domain.errors import ContractError

    with pytest.raises(ContractError):
        certify_release(
            version="v5.2.0",
            quality_passed=978,
            quality_skipped=1,
            red_chamber_real="EXTERNAL_BLOCKED",
            tag="m42",
            kernel_guard_ok=False,
        )
