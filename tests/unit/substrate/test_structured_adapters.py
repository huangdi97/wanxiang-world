"""G55E: Structured adapters — JSON/YAML/CSV/GEDCOM (M52)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.errors import MalformedSourceContent, UnsupportedSource
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.sources.structured import StructuredAdapter


def _record(kind: str, payload: str) -> SourceRecord:
    return SourceRecord(
        source_id="src_struct",
        kind=kind,
        content_hash=payload_hash(payload),
        content_ref="ref://src_struct",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=payload,
        provenance="fixture:g55e",
    )


GEDCOM = """0 @I1@ INDI
1 NAME Alice /Zhang/
1 BIRT
2 DATE 1980-01-01
0 @I2@ INDI
1 NAME Bob /Li/
1 BIRT
2 DATE 1982-03-04
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""


@pytest.mark.unit
def test_handles_structured_kinds() -> None:
    adapter = StructuredAdapter()
    for kind in ("json", "yaml", "csv", "gedcom"):
        assert adapter.can_handle(kind=kind), kind
    assert adapter.can_handle(kind="text", filename="data.csv")
    assert not adapter.can_handle(kind="pdf")


@pytest.mark.unit
def test_json_normalized_canonically() -> None:
    result = StructuredAdapter().ingest(_record("json", '{"b": 1, "a": [3, 2]}'))
    assert result.content == '{"a":[3,2],"b":1}'


@pytest.mark.unit
def test_invalid_json_rejected() -> None:
    with pytest.raises(MalformedSourceContent):
        StructuredAdapter().ingest(_record("json", "{not json"))


@pytest.mark.unit
def test_yaml_normalized() -> None:
    result = StructuredAdapter().ingest(_record("yaml", "name: Alice\nage: 30\n"))
    assert "Alice" in result.content
    assert '"name":"Alice"' in result.content


@pytest.mark.unit
def test_csv_rows_preserved() -> None:
    result = StructuredAdapter().ingest(_record("csv", "id,name\n1,Alice\n2,Bob\n"))
    assert "id\tname" in result.content
    assert "1\tAlice" in result.content
    assert "2\tBob" in result.content


@pytest.mark.unit
def test_gedcom_normalized() -> None:
    result = StructuredAdapter().ingest(_record("gedcom", GEDCOM))
    assert "@I1@" in result.content
    assert "Alice" in result.content
    assert "@F1@" in result.content


@pytest.mark.unit
def test_gedcom_without_records_rejected() -> None:
    with pytest.raises(MalformedSourceContent):
        StructuredAdapter().ingest(_record("gedcom", "0 HEAD\n1 SOUR test\n"))


@pytest.mark.unit
def test_unsupported_kind_rejected() -> None:
    with pytest.raises(UnsupportedSource):
        StructuredAdapter().ingest(_record("pdf", "x"))
