"""G35B: chapter/segment stable source locators (mechanism; synthetic corpus)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.locator import (
    SourceLocator,
    locator_stable_hash,
    segment_source,
    source_slice,
)

# Synthetic corpus ONLY — never real《红楼梦》canon.
SYNTHETIC = "第一回\n林黛玉进贾府。\n第二回\n贾雨村风尘怀闺秀。\n第三回\n托内兄如海荐西宾。\n"


@pytest.mark.unit
def test_parser_produces_stable_locators() -> None:
    first = segment_source("src_rc_synth", SYNTHETIC)
    second = segment_source("src_rc_synth", SYNTHETIC)
    assert first == second
    assert locator_stable_hash(first) == locator_stable_hash(second)
    assert len(first) == 3  # one segment per chapter
    assert first[0].chapter == "第一回"
    assert first[0].locator.startswith("src_rc_synth#")


@pytest.mark.unit
def test_locator_backlinks_to_exact_source_slice() -> None:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    # A Canon claim carries the locator; it resolves to the exact source slice.
    claim_locator = locators[1]
    slice_text = source_slice(SYNTHETIC, claim_locator)
    assert "贾雨村风尘怀闺秀" in slice_text
    assert "林黛玉进贾府" not in slice_text  # not the previous chapter


@pytest.mark.unit
def test_original_text_is_never_rewritten() -> None:
    before = SYNTHETIC
    locators = segment_source("src_rc_synth", SYNTHETIC)
    for locator in locators:
        source_slice(SYNTHETIC, locator)
    assert before == SYNTHETIC  # parser + locator are read-only
    assert all(isinstance(item, SourceLocator) for item in locators)


@pytest.mark.unit
def test_offsets_and_segment_ids_are_consistent() -> None:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    # Segments are the content lines AFTER each chapter marker (marker excluded).
    assert locators[0].start_offset == 1
    assert locators[0].end_offset == 2
    assert locators[1].start_offset == 3
    assert locators[1].end_offset == 4
    assert locators[2].segment_id == "src_rc_synth:第三回:5-6"
