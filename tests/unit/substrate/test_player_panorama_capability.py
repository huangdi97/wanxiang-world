"""T2 panorama capability fails closed on invalid third-party provider pricing."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest
from fastapi import Request
from tests.unit.substrate.test_book_scene_plan import package_from_book
from wanxiang_substrate.assets.book_scene_panorama_budget import PanoramaBudgetLedger
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.playable import PlayableService

from wanxiang_api.player_panorama_views import panorama_generation_view


class _ServiceStub:
    def __init__(self) -> None:
        self.packages = {"profile": package_from_book("panorama-cost", ("观景台",))}

    def visual_assets(
        self,
        profile_id: str,
        *,
        viewer_id: str,
    ) -> tuple[object, ...]:
        _ = (profile_id, viewer_id)
        return ()


@pytest.mark.parametrize("invalid_cost", [True, -1, 1.5, "4"])
def test_panorama_capability_rejects_invalid_provider_cost(invalid_cost: object) -> None:
    provider = cast(
        SceneImageProvider,
        SimpleNamespace(
            provider_id="provider:bad-cost",
            provider_version="1",
            presentation_kind="panorama",
            generation_is_idempotent=True,
            cost_units_per_asset=invalid_cost,
            requires_network=False,
            private_safe=True,
        ),
    )
    state = SimpleNamespace(
        panorama_asset_provider=provider,
        panorama_asset_max_cost_units=10,
        panorama_budget_ledger=PanoramaBudgetLedger(),
        panorama_asset_allow_network=False,
    )
    request = cast(Request, SimpleNamespace(app=SimpleNamespace(state=state)))
    service = cast(PlayableService, _ServiceStub())

    result = panorama_generation_view(
        request,
        service,
        "profile",
        viewer_id="owner",
        place_name="观景台",
    )
    generation = cast(dict[str, object], result["generation"])

    assert generation["available"] is False
    assert generation["reason"] == "budget_insufficient"
    assert generation["cost_units"] == 0
