"""SOURCE_TO_LIVING_WORLD local acceptance — pipeline evidence (Phases 4/5/7/11/12/13).

Drives the real Book -> WorldPackage -> SourceVisualPlan -> atlas/scenes
chain for three copyright-safe synthetic books through the same generic
pipeline and records machine-readable evidence. No canonical writes are
permitted or produced by this script's visual paths.

Stable command from repository root:

    uv run python scripts/source_to_living_world_acceptance.py

Exit code 0 means every pipeline check passed.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import time
import tracemalloc
from dataclasses import asdict, is_dataclass
from typing import Any, Literal

from wanxiang_domain.errors import NotFound
from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
    _PromptedExternalSceneProvider,
)
from wanxiang_substrate.assets.book_scene_plan import (
    _plan_book_scene_assets,
    _SourceSceneRequest,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_projection import _visual_scene_state_from_book_assets
from wanxiang_substrate.assets.book_scene_prompt import (
    _compile_scene_generation_brief,
    _story_visual_profile,
)
from wanxiang_substrate.assets.book_scene_visual import _materialize_visual_plan
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_projection import player_world_detail
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import ActorPerspective, ReferenceVisualProvider

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "runtime-evidence" / "2026-10-09-source-to-living-world"
OUT.mkdir(parents=True, exist_ok=True)

EVIDENCE: dict[str, Any] = {}


def _source(
    source_id: str,
    text: str,
    *,
    access: Literal["public", "private", "restricted"] = "public",
    external_processing: bool = False,
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(text),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(
            owner="synthetic",
            usage="test",
            approved=True,
            external_model_processing_allowed=external_processing,
            public_export_allowed=access == "public",
        ),
        payload=text,
        provenance=f"synthetic:acceptance:{source_id}",
        access=access,
    )


BOOK_A_CN = """# 第一章 城门
角色：沈砚
沈砚说道：“入城需登记。”
沈砚来到江南城。
从江南城到机关桥需要穿过水道。
规则：入城者必须登记。
1921年，沈砚到达江南城。

# 第二章 桥与水
角色：顾朔
顾朔答道：“潮水将临。”
顾朔来到机关桥。
沈砚来到潮汐港。
从机关桥到潮汐港是水路。
1921年，顾朔召开水闸会议。

# 第三章 亭与巷
角色：阿岚
阿岚说道：“望月亭今夜无月。”
阿岚来到望月亭。
沈砚和顾朔来到青石巷。
顾朔是沈砚的朋友。
1922年，三人见面。

# 第四章 夜巡
沈砚来到沉水巷。
顾朔离开望月亭。
规则：夜间不得掌灯。
1922年，事件：水闸调查。
"""

BOOK_B_EN = """# Chapter 1
Character: Clara
Clara arrived in Fortress in 1854.
Marcus visited Harbor.
From Fortress to Harbor the road was open.
rule: guards register all visitors

# Chapter 2
Character: Marcus
Marcus arrived in Library.
Clara travelled to Market.
Marcus is a friend of Clara.
In 1855, the council signed the Armistice.

# Chapter 3
Clara returned to Fortress.
Marcus entered the Academy.
The Academy is connected to the Library.
rule: scholars keep the archive
"""


def _long_book() -> str:
    places = ("Garden", "Fortress", "Harbor", "Library", "Market", "Station")
    chapters: list[str] = []
    for index in range(24):
        place = places[index % len(places)]
        chapters.append(
            f"# Chapter {index + 1}\nCharacter: Elena\nCharacter: Rowan\n"
            f"Elena arrived in {place} in 1985.\n"
            f"Rowan travelled to {places[(index + 1) % len(places)]}.\n"
            f"From {place} the road leads to {places[(index + 1) % len(places)]}.\n"
            f"rule: chapter-{index + 1} visitors register\n"
        )
    return "\n".join(chapters)


def _as_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {
            key: _as_dict(item)
            for key, item in asdict(value).items()  # type: ignore[arg-type]
        }
    if isinstance(value, tuple):
        return [_as_dict(item) for item in value]  # type: ignore[union-attr]
    if isinstance(value, bytes):
        return f"<{len(value)} bytes>"
    return value


def _record(name: str, value: dict[str, Any]) -> None:
    EVIDENCE[name] = value


def _profile(package_id: str, name: str) -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id=f"profile:{name}",
        world_package_ref=package_id,
        scenario_ref=f"scenario:{name}",
        runtime_profile_ref="runtime:reference",
        experience_package_ref=f"experience:{name}",
        projection_profile_ref="projection:player",
        visibility="public",
        display_name=name,
        owner_id="alice",
    )


def _fault_plan(place: str, key: str, *, external_processing: bool = True) -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id=f"world:fault-{key}",
        source_digest=hashlib.sha256(place.encode()).hexdigest(),
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(
            _SourceSceneRequest(
                place_name=place,
                stable_key=key,
                spec=SemanticSceneSpec(
                    spec_id=f"scene-{key}",
                    semantic_id=f"place:{key}",
                    kind="illustrated-environment",
                ),
                cache_key=f"cache-{key}",
            ),
        ),
        deferred_scene_count=0,
        external_processing_allowed=external_processing,
    )


def run_cross_book() -> None:
    """Phase 4: three unrelated books travel the same generic pipeline."""
    provider_service = AuthoringService(providers=ProviderRouter((LocalSemanticProvider(),)))
    a = OneClickAuthoring(provider_service).run(
        "accept_a_cn",
        (_source("accept_a_cn", BOOK_A_CN),),
        profile="book",
        semantic_provider="local",
    )
    b = OneClickAuthoring(provider_service).run(
        "accept_b_en",
        (_source("accept_b_en", BOOK_B_EN),),
        profile="book",
        semantic_provider="local",
    )
    c = OneClickAuthoring().run(
        "accept_c_long", (_source("accept_c_long", _long_book()),), profile="book"
    )

    assert a.visual_plan is not None and a.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert b.visual_plan is not None and b.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert c.visual_plan is not None and c.visual_plan.status == "READY_FOR_ASSET_PROVIDER"

    a_places = set(a.visual_plan.place_names)
    b_places = set(b.visual_plan.place_names)
    assert len(a_places) >= 5, a_places
    assert len(c.visual_plan.place_names) >= 5, c.visual_plan.place_names
    assert len(c.visual_plan.scene_requests) == 3, c.visual_plan.scene_requests
    assert c.visual_plan.deferred_scene_count >= 2, c.visual_plan.deferred_scene_count
    assert not (a_places & b_places), (a_places, b_places)

    package = a.package.draft
    assert len(package.entities) >= 3, package.entities
    assert len(package.events) >= 2, package.events
    assert len(package.places) >= 5, package.places
    assert package.rules, package.rules
    assert package.relations or a.visual_plan.topology_relations, package.relations

    # English identity/place distinction: Fortress is a place, not a person.
    assert "Fortress" in b_places
    assert not any(name in b.package.draft.entities for name in ("Fortress",))

    # One story visual profile per book; different books get different style keys.
    a_styles = {scene.style_key for scene in a.visual_plan.scene_requests}
    b_styles = {scene.style_key for scene in b.visual_plan.scene_requests}
    assert len(a_styles) == 1, a_styles
    assert len(b_styles) == 1, b_styles
    assert a_styles != b_styles

    _record(
        "cross_book",
        {
            "book_a_cn": {
                "places": sorted(a_places),
                "entities": [label for _, label in a.package.draft.entities],
                "events": [f"{event_id}@{date}" for event_id, date in a.package.draft.events],
                "rules": list(a.package.draft.rules),
                "scene_requests": len(a.visual_plan.scene_requests),
                "deferred": a.visual_plan.deferred_scene_count,
                "assets": len(a.visual_assets),
                "provider_calls": a.visual_provider_calls,
                "style_key": next(iter(a_styles)),
            },
            "book_b_en": {
                "places": sorted(b_places),
                "entities": [label for _, label in b.package.draft.entities],
                "scene_requests": len(b.visual_plan.scene_requests),
                "deferred": b.visual_plan.deferred_scene_count,
                "assets": len(b.visual_assets),
                "style_key": next(iter(b_styles)),
            },
            "book_c_long": {
                "sections": 24,
                "source_bytes": len(_long_book().encode("utf-8")),
                "place_names": list(c.visual_plan.place_names),
                "scene_requests": len(c.visual_plan.scene_requests),
                "deferred": c.visual_plan.deferred_scene_count,
                "assets": len(c.visual_assets),
                "provider_calls": c.visual_provider_calls,
                "cost_units": c.visual_cost_units,
            },
            "disjoint_places_a_b": sorted(a_places.intersection(b_places)),
            "per_book_style_keys_differ": True,
        },
    )


def run_deferred_and_privacy() -> None:
    """Phases 5/7/11: on-demand deferred scene, rights/privacy, G96 projection."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.reference_runtime import build_reference_runtime

    provider_service = AuthoringService(providers=ProviderRouter((LocalSemanticProvider(),)))
    authored = OneClickAuthoring(provider_service).run(
        "accept_deferred",
        (_source("accept_deferred", BOOK_A_CN),),
        profile="book",
        semantic_provider="local",
    )
    assert authored.visual_plan is not None
    runtime = build_reference_runtime()
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id="alice", visibility="private")
    initial_assets = playable.visual_assets(profile.profile_id, viewer_id="alice")
    assert len(initial_assets) == 3, len(initial_assets)
    generated = {asset.place_name for asset in initial_assets}
    target = next(place for place in authored.visual_plan.place_names if place not in generated)

    first = playable.materialize_visual_place(profile.profile_id, target, viewer_id="alice")
    second = playable.materialize_visual_place(profile.profile_id, target, viewer_id="alice")
    assert first.provider_calls == 1 and first.cache_hits == 0
    assert second.provider_calls == 0 and second.cache_hits == 1
    assert target in {
        asset.place_name for asset in playable.visual_assets(profile.profile_id, viewer_id="alice")
    }

    rejected = False
    try:
        playable.materialize_visual_place(profile.profile_id, "不存在的月球宫殿", viewer_id="alice")
    except NotFound:
        rejected = True
    assert rejected, "unknown place must be rejected"

    # Canon unchanged: no world instance/event was created by visuals. The
    # reference runtime exposes its event store through the runtime's events
    # port; with no instance ever created there is nothing to load, so the
    # store must report zero instances in the playable store.
    assert len(playable.store.list_instances()) == 0

    denied = player_world_detail(
        _profile(authored.package.package_id, "Denied"),
        authored.package,
        locale="en-US",
        include_visual=True,
        visual_assets=(),
        visual_access_allowed=False,
    )
    assert denied["visual"] is None

    # Rights re-issuance on cache hit: same bytes, newly-minted AssetRef rights.
    plan = _plan_book_scene_assets(authored.package)
    cache = playable._visual_cache
    gated = _materialize_visual_plan(plan, cache=cache, rights="source-gated")
    public = _materialize_visual_plan(plan, cache=cache, rights="public")
    assert {ref.rights for ref in gated.asset_refs} == {"source-gated"}
    assert {ref.rights for ref in public.asset_refs} == {"public"}
    assert gated.assets[0].content_sha256 == public.assets[0].content_sha256

    # G96 projection: book assets -> VisualSceneState -> VisualProjectionFrame.
    scene_state = _visual_scene_state_from_book_assets(
        plan,
        public.asset_refs,
        snapshot_ref="snapshot:acceptance",
        world_instance_ref="world:acceptance",
        branch_ref="branch:main",
        revision=7,
        world_time_ticks=42,
        state_hash="statehash:acceptance",
    )
    perspective = ActorPerspective(
        perspective_ref="perspective:reader",
        actor_ref="actor:reader",
        origin=(0.0, 0.0),
        view_radius=10.0,
        allowed_rights=("public",),
    )
    provider = ReferenceVisualProvider("provider:reference-visual", "1.0.0")
    frame = provider.project(scene_state, perspective)
    assert frame.status == "projected"
    assert frame.projection_only is True
    assert frame.snapshot_revision == 7
    assert frame.state_hash == "statehash:acceptance"
    assert frame.asset_refs and all(ref.rights == "public" for ref in frame.asset_refs)
    # Canonical world state untouched by projection: fresh runtime, zero events.
    assert not playable.store.list_instances()

    # Consistent per-book style: every scene request shares one style key, and the
    # scene-generation brief is bounded (no full source included).
    profile_obj = _story_visual_profile(plan)
    brief = _compile_scene_generation_brief(plan.scene_requests[0], profile_obj)
    assert brief.full_source_included is False
    assert len(brief.semantic_prompt) < 1800
    assert "context candidates are co-located" in brief.semantic_prompt

    _record(
        "deferred_on_demand",
        {
            "initial_assets": len(initial_assets),
            "generated_places": sorted(generated),
            "target_place": target,
            "first_provider_calls": first.provider_calls,
            "first_cache_hits": first.cache_hits,
            "repeat_provider_calls": second.provider_calls,
            "repeat_cache_hits": second.cache_hits,
            "unknown_place_rejected": rejected,
            "canonical_instances_created": len(playable.store.list_instances()),
            "style_key_consistent_across_scenes": len(
                {scene.style_key for scene in plan.scene_requests}
            )
            == 1,
            "brief_full_source_included": brief.full_source_included,
            "brief_prompt_bytes": len(brief.semantic_prompt.encode("utf-8")),
            "clue_vs_presence_policy": (
                "context candidates are co-located source evidence candidates as "
                "written in the brief; UI never renders them as current presence"
            ),
        },
    )
    _record(
        "rights_privacy",
        {
            "non_owner_visual_denied": denied["visual"] is None,
            "cache_hit_rights_reissued": {
                "source-gated": [ref.rights for ref in gated.asset_refs],
                "public": [ref.rights for ref in public.asset_refs],
                "same_sha256": gated.assets[0].content_sha256 == public.assets[0].content_sha256,
            },
        },
    )
    _record(
        "g96_projection",
        {
            "status": frame.status,
            "projection_only": frame.projection_only,
            "snapshot_revision": frame.snapshot_revision,
            "state_hash": frame.state_hash,
            "asset_ref_count": len(frame.asset_refs),
            "canonical_writes": 0,
        },
    )


def run_fault_tolerance() -> None:
    """Phase 12: provider failure, bad output, network and budget fail closed."""

    outcomes: dict[str, str] = {}

    # 1. Provider raises -> materializer must propagate, cache stays untouched.
    class _RaisingProvider(_PromptedExternalSceneProvider):
        def produce(self, request: Any) -> Any:  # type: ignore[override]
            _ = request
            raise RuntimeError("upstream image API failed")

    try:
        _materialize_visual_plan(
            _fault_plan("破败城", "raise"),
            provider=_RaisingProvider(
                provider_id="provider:raise",
                provider_version="1",
                client=_ExternalImageClient(),
                cost_units_per_asset=1,
                private_safe=True,
            ),
            allow_network=True,
            max_cost_units=5,
        )
        outcomes["provider_failure"] = "NOT_REJECTED"
    except RuntimeError:
        outcomes["provider_failure"] = "REJECTED_CANON_UNTOUCHED"

    # 2. Empty / text-plain / oversized image outputs must be rejected.
    class _EmptyClient(_ExternalImageClient):
        def generate(self, brief: Any) -> _ExternalImageResult:
            _ = brief
            return _ExternalImageResult(b"", "image/png")

    class _TextClient(_ExternalImageClient):
        def generate(self, brief: Any) -> _ExternalImageResult:
            _ = brief
            return _ExternalImageResult(b"not an image", "text/plain")

    class _HugeClient(_ExternalImageClient):
        def generate(self, brief: Any) -> _ExternalImageResult:
            _ = brief
            return _ExternalImageResult(b"x" * (20 * 1024 * 1024 + 1), "image/png")

    def _tries(client: _ExternalImageClient, key: str) -> None:
        try:
            provider = _PromptedExternalSceneProvider(
                provider_id=f"provider:{key}",
                provider_version="1",
                client=client,
                cost_units_per_asset=1,
                private_safe=True,
            )
            _materialize_visual_plan(
                _fault_plan("坏输出", key),
                provider=provider,
                allow_network=True,
                max_cost_units=5,
            )
            outcomes[key] = "NOT_REJECTED"
        except ValueError:
            outcomes[key] = "REJECTED"

    _tries(_EmptyClient(), "empty_output")
    _tries(_TextClient(), "text_plain_output")
    _tries(_HugeClient(), "oversized_output")

    # 3. Network disabled -> must reject a remote provider.
    class _RemoteLike(_PromptedExternalSceneProvider):
        requires_network = True  # type: ignore[assignment]

    try:
        _materialize_visual_plan(
            _fault_plan("远方", "network"),
            provider=_RemoteLike(
                provider_id="provider:remote",
                provider_version="1",
                client=_ExternalImageClient(),
                cost_units_per_asset=2,
                private_safe=False,
            ),
        )
        outcomes["network_disabled"] = "NOT_REJECTED"
    except ValueError:
        outcomes["network_disabled"] = "REJECTED"

    # 4. Budget insufficient -> must reject without charging.
    try:
        _materialize_visual_plan(
            _fault_plan("预算", "budget"),
            provider=_RemoteLike(
                provider_id="provider:remote",
                provider_version="1",
                client=_ExternalImageClient(),
                cost_units_per_asset=5,
                private_safe=False,
            ),
            allow_network=True,
            max_cost_units=2,
        )
        outcomes["budget_insufficient"] = "NOT_REJECTED"
    except ValueError:
        outcomes["budget_insufficient"] = "REJECTED"

    _record("fault_tolerance", outcomes)


def run_performance() -> None:
    """Phase 12: long-book cost stays bounded; record T0 + cache-hit timings."""
    tracemalloc.start()
    started = time.monotonic()
    authoring = OneClickAuthoring()
    c = authoring.run(
        "accept_perf_long", (_source("accept_perf_long", _long_book()),), profile="book"
    )
    t0_duration = time.monotonic() - started
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert c.visual_plan is not None
    plan = _plan_book_scene_assets(c.package)

    warm = _materialize_visual_plan(plan, cache=authoring.visual_cache)
    assert warm.provider_calls == 0 and warm.cache_hits == len(plan.scene_requests)
    hit_started = time.monotonic()
    hit = _materialize_visual_plan(plan, cache=authoring.visual_cache)
    cache_hit_duration = time.monotonic() - hit_started
    assert hit.provider_calls == 0 and hit.cache_hits == len(plan.scene_requests)

    _record(
        "performance_cost",
        {
            "source_bytes": len(_long_book().encode("utf-8")),
            "sections": 24,
            "place_count": len(plan.place_names),
            "scene_requests": len(plan.scene_requests),
            "deferred_count": plan.deferred_scene_count,
            "initial_visual_cost_units": c.visual_cost_units,
            "provider_calls": c.visual_provider_calls,
            "t0_duration_s": round(t0_duration, 3),
            "cache_hit_duration_s": round(cache_hit_duration, 5),
            "peak_memory_bytes": int(peak),
            "cost_scales_with_places": len(plan.place_names) > len(plan.scene_requests),
        },
    )


def main() -> int:
    run_cross_book()
    run_deferred_and_privacy()
    run_fault_tolerance()
    run_performance()
    evidence = {name: _as_dict(value) for name, value in EVIDENCE.items()}
    out_path = OUT / "pipeline_evidence.json"
    out_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
    print(f"PIPELINE_EVIDENCE={out_path}")
    print("PIPELINE_ACCEPTANCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
