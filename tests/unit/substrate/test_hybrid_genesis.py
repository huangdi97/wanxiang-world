"""G31F: Hybrid Genesis compatibility analysis and safe rejection."""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import WorldDefinitionId
from wanxiang_domain.worldline import WorldDefinition
from wanxiang_substrate.lineage.hybrid_genesis import analyze_hybrid_genesis


def _def(
    definition_id: str,
    *,
    constitution: str = "con_a",
    genesis: str = "gen_a",
    package: str = "pack://a@1.0.0",
) -> WorldDefinition:
    return WorldDefinition(
        definition_id=WorldDefinitionId(definition_id),
        version=1,
        name=definition_id,
        constitution_ref=constitution,
        genesis_ref=genesis,
        package_ref=package,
    ).with_hash()


@pytest.mark.unit
def test_incompatible_constitution_rejected() -> None:
    left = _def("wd_left", constitution="con_x")
    right = _def("wd_right", constitution="con_y")
    report = analyze_hybrid_genesis(left, right)
    assert report.verdict == "rejected"
    names = {c.name for c in report.failing_checks()}
    assert "constitution" in names


@pytest.mark.unit
def test_legacy_constitution_is_compatible() -> None:
    left = _def("wd_left", constitution="con_legacy_v5")
    right = _def("wd_right", constitution="con_x")
    report = analyze_hybrid_genesis(left, right)
    assert report.verdict == "candidate"


@pytest.mark.unit
def test_rights_conflict_rejected() -> None:
    left = _def("wd_left", genesis="gen_a")
    right = _def("wd_right", genesis="gen_b")
    report = analyze_hybrid_genesis(left, right)
    assert report.verdict == "rejected"
    assert "rights" in {c.name for c in report.failing_checks()}


@pytest.mark.unit
def test_compatible_worlds_produce_merge_plan_candidate() -> None:
    left = _def("wd_left", constitution="con_legacy_v5", genesis="gen_a", package="pack://a@1.0.0")
    right = _def(
        "wd_right", constitution="con_legacy_v5", genesis="gen_a", package="pack://a@1.0.0"
    )
    report = analyze_hybrid_genesis(left, right)
    assert report.verdict == "candidate"
    assert not report.failing_checks()


@pytest.mark.unit
def test_analysis_never_rewrites_parent_histories() -> None:
    left = _def("wd_left", constitution="con_legacy_v5")
    right = _def("wd_right", constitution="con_x")
    before_left = left.content_hash
    before_right = right.content_hash
    analyze_hybrid_genesis(left, right)
    # The analysis is read-only: parent world definitions/histories unchanged.
    assert left.content_hash == before_left
    assert right.content_hash == before_right
