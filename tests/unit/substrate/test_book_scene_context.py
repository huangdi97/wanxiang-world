"""Direct boundary tests for bounded scene-context selection."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_context import _context_candidates


def _rows(*items: object) -> list[dict[str, object]]:
    return [{"cooccurring_candidates": list(items)}]


def test_context_candidates_bound_labels_and_skip_blanks() -> None:
    candidates = _context_candidates(
        _rows(
            {"kind": "event", "label": "x" * 500},
            {"kind": "object", "label": "   "},
            {"kind": "object"},
        )
    )

    assert len(candidates) == 1
    assert candidates[0] == "event:" + "x" * 160


def test_context_candidates_skip_concrete_owners_in_any_field() -> None:
    candidates = _context_candidates(
        _rows(
            {"kind": "object", "label": "Key", "actor": "Alice"},
            {"kind": "object", "label": "Ledger", "owner": "Alice"},
            {"kind": "object", "label": "Chest", "custodian": "Bob"},
            {"kind": "object", "label": "Sign", "actor": " none "},
            {"kind": "object", "label": "Clock", "actor": "N/A"},
            {"kind": "object", "label": "Box", "owner": "unknown"},
        )
    )

    assert candidates == ["object:Sign", "object:Clock", "object:Box"]


def test_context_candidates_dedupe_case_and_unicode() -> None:
    candidates = _context_candidates(
        _rows(
            {"kind": "object", "label": "Lamp"},
            {"kind": "object", "label": "lamp"},
            {"kind": "object", "label": "Café"},
            {"kind": "object", "label": "Cafe\u0301"},
        )
    )

    assert candidates == ["object:Lamp", "object:Café"]


def test_context_candidates_cap_at_eight() -> None:
    candidates = _context_candidates(
        _rows(*({"kind": "object", "label": f"Item{index}"} for index in range(12)))
    )

    assert len(candidates) == 8


def test_context_candidates_ignore_non_list_payloads() -> None:
    rows: list[dict[str, object]] = [
        {"cooccurring_candidates": "not-a-list"},
        {"cooccurring_candidates": [None, 7, {"kind": "event", "label": "Festival"}]},
    ]

    assert _context_candidates(rows) == ["event:Festival"]
