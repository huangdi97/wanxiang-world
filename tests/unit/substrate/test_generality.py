"""M41: cross-domain generality harness (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.generality import (
    black_box_world_pack_gate,
    kernel_diff_guard,
    run_generality_harness,
)


@pytest.mark.unit
def test_generality_harness_four_domains() -> None:
    report = run_generality_harness(
        domains=("family", "heritage", "campaign", "narrative"),
        core_reuse=(
            ("family", ("commit", "replay", "branch")),
            ("heritage", ("commit", "snapshot")),
            ("campaign", ("scheduler", "commit")),
            ("narrative", ("commit", "resolver", "narrative_domain")),
        ),
        kernel_diff_clean=True,
        black_box_pack_ok=True,
        external_blocked=("heritage",),
    )
    assert report.all_domains_pass is True
    assert report.kernel_diff_clean is True
    assert len(report.four_domain_core_reuse) == 4


@pytest.mark.unit
def test_kernel_diff_guard() -> None:
    assert kernel_diff_guard("h1", "h1") is True
    assert kernel_diff_guard("h1", "h2") is False


@pytest.mark.unit
def test_black_box_world_pack_gate() -> None:
    assert black_box_world_pack_gate(package_id="p", content_hash="a" * 64, trusted=True) is True
    assert black_box_world_pack_gate(package_id="p", content_hash="a" * 64, trusted=False) is False
    assert black_box_world_pack_gate(package_id="p", content_hash="short", trusted=True) is False


@pytest.mark.unit
def test_external_blocked_domain_labeled() -> None:
    report = run_generality_harness(
        domains=("family",),
        core_reuse=(("family", ("commit",)),),
        kernel_diff_clean=True,
        black_box_pack_ok=True,
        external_blocked=("family",),
    )
    heritage = report.domains[0]
    assert heritage.external_blocked is True
    assert heritage.acceptance_passed is False
    assert report.all_domains_pass is True
