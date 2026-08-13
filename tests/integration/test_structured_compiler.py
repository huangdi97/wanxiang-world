"""G04C: structured compiler MVP.

Covers safe readers (json/yaml/markdown/text), deterministic golden hashes,
negative/unsupported-format handling and provenance tracing.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.compiler.compiler import StructuredCompiler
from wanxiang_substrate.compiler.errors import UnsupportedFormat
from wanxiang_substrate.compiler.fixture import (
    json_source,
    malformed_json_source,
    markdown_source,
    oversized_source,
    pdf_source,
    text_source,
    yaml_source,
)
from wanxiang_substrate.compiler.model import CompileResult
from wanxiang_substrate.compiler.readers import read_source
from wanxiang_substrate.sources.model import SourceRecord


def _compile(*sources: SourceRecord) -> CompileResult:
    compiler = StructuredCompiler()
    return compiler.compile("job_1", {s.source_id: s for s in sources})


@pytest.mark.unit
def test_json_source_compiles_entity() -> None:
    result = _compile(json_source())
    assert result.ok is True
    town = next(c for c in result.candidates if c.object_id == "town")
    assert town.kind == "entity"
    assert town.payload["entity_type"] == "spatial.place"
    assert town.source_refs == ("src_objects_json",)


@pytest.mark.unit
def test_yaml_source_compiles_entity() -> None:
    result = _compile(yaml_source())
    assert result.ok is True
    town = next(c for c in result.candidates if c.object_id == "town")
    assert town.payload["name"] == "Town"


@pytest.mark.unit
def test_markdown_source_compiles_entity() -> None:
    result = _compile(markdown_source())
    assert result.ok is True
    town = next(c for c in result.candidates if c.object_id == "town")
    assert town.payload["entity_id"] == "town"
    assert town.provenance.startswith("markdown:")


@pytest.mark.unit
def test_text_source_compiles_fact() -> None:
    result = _compile(text_source())
    assert result.ok is True
    fact = next(c for c in result.candidates if c.kind == "fact")
    assert "historical note" in str(fact.payload["text"])


@pytest.mark.unit
def test_golden_hash_deterministic() -> None:
    first = _compile(json_source(), yaml_source())
    second = _compile(json_source(), yaml_source())
    assert first.result_hash() == second.result_hash()


@pytest.mark.unit
def test_malformed_json_fails_safely() -> None:
    result = _compile(malformed_json_source())
    assert result.ok is False
    assert any(d.code == "read_failed" for d in result.diagnostics)


@pytest.mark.unit
def test_oversized_source_fails_safely() -> None:
    result = _compile(oversized_source())
    assert result.ok is False
    assert any(d.code == "read_failed" for d in result.diagnostics)


@pytest.mark.unit
def test_pdf_is_explicitly_unsupported_not_faked() -> None:
    result = _compile(pdf_source())
    assert result.ok is False
    assert any(d.code == "unsupported_format" for d in result.diagnostics)
    assert not result.candidates
    # The reader itself raises the structured error (no fake extraction).
    with pytest.raises(UnsupportedFormat):
        read_source(pdf_source())


@pytest.mark.unit
def test_every_candidate_has_provenance() -> None:
    result = _compile(json_source(), yaml_source(), markdown_source(), text_source())
    assert result.ok is True
    for candidate in result.candidates:
        assert candidate.source_refs
        assert candidate.provenance


@pytest.mark.unit
def test_export_package_candidate_is_review_ready() -> None:
    from wanxiang_substrate.compiler.export import export_package_candidate

    result = _compile(json_source())
    exported = export_package_candidate(result)
    assert exported["compiler_version"] == 1
    assert exported["hash"] == result.result_hash()
    assert isinstance(exported["candidates"], list)
    assert isinstance(exported["diagnostics"], list)
