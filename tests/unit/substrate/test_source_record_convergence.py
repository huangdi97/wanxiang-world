"""G55A: SourceRecord convergence — version/checksum/rights/access/reliability/schema."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.sources.errors import DuplicateSource
from wanxiang_substrate.sources.model import (
    RightsEnvelope,
    SourceRecord,
    canonical_json,
    payload_hash,
)
from wanxiang_substrate.sources.registry import SourceRegistry


def _record(
    source_id: str = "src_1",
    *,
    version: str = "1",
    access: str = "private",
    reliability: float = 1.0,
    schema_version: int = 1,
    content: str = "fixture:g55a",
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"ref://{source_id}",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=content,
        provenance="fixture:g55a",
        version=version,
        access=access,  # type: ignore[arg-type]
        reliability=reliability,
        schema_version=schema_version,
    )


@pytest.mark.unit
def test_convergence_fields_roundtrip() -> None:
    record = _record(version="2.1", access="restricted", reliability=0.8, schema_version=2)
    assert record.version == "2.1"
    assert record.access == "restricted"
    assert record.reliability == 0.8
    assert record.schema_version == 2


@pytest.mark.unit
def test_fingerprint_is_stable_and_version_aware() -> None:
    a = _record(content="same")
    b = _record(content="same", version="2")
    assert a.fingerprint() == f"text:{a.content_hash}:1"
    assert a.fingerprint() != b.fingerprint()


@pytest.mark.unit
def test_invalid_access_rejected() -> None:
    with pytest.raises(ContractError):
        _record(access="secret")


@pytest.mark.unit
def test_reliability_bounds_enforced() -> None:
    with pytest.raises(ContractError):
        _record(reliability=1.5)
    with pytest.raises(ContractError):
        _record(reliability=-0.1)


@pytest.mark.unit
def test_schema_version_positive() -> None:
    with pytest.raises(ContractError):
        _record(schema_version=0)


@pytest.mark.unit
def test_canonical_json_includes_convergence_fields() -> None:
    record = _record(version="3", access="public", reliability=0.9)
    payload = canonical_json(record)
    assert '"version":"3"' in payload
    assert '"access":"public"' in payload
    assert '"reliability":0.9' in payload
    assert '"schema_version":1' in payload


@pytest.mark.unit
def test_registry_allows_same_content_new_version() -> None:
    registry = SourceRegistry()
    registry.register(_record(source_id="src_v1", version="1", content="same"))
    registry.register(_record(source_id="src_v2", version="2", content="same"))
    assert registry.require("src_v1").version == "1"
    assert registry.require("src_v2").version == "2"


@pytest.mark.unit
def test_registry_rejects_same_fingerprint_duplicate() -> None:
    registry = SourceRegistry()
    registry.register(_record(source_id="src_v1", version="1", content="same"))
    with pytest.raises(DuplicateSource):
        registry.register(_record(source_id="src_v1_copy", version="1", content="same"))


@pytest.mark.unit
def test_transition_preserves_convergence_fields() -> None:
    registry = SourceRegistry()
    record = _record(version="2", access="restricted", reliability=0.7)
    registry.register(record)
    updated = registry.transition("src_1", "E2", "human", 1)
    assert updated.version == "2"
    assert updated.access == "restricted"
    assert updated.reliability == 0.7
    assert updated.schema_version == 1
