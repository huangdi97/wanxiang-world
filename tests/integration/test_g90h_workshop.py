"""G90H qualification: three creation modes share preview and playable paths."""

from __future__ import annotations

from scripts.reference_runtime import build_reference_runtime
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.workshop import CreatorIntent, LocalPromptGenesisProvider, WorkshopService


def _source(source_id: str, version: str = "1") -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
        "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
        "relationship: Alice -> Bob\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(
            owner="fixture",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance=f"fixture:g90h:{source_id}",
        version=version,
        access="private",
    )


def test_source_prompt_hybrid_qualify_to_preview_playable_and_publish_gates() -> None:
    router = ProviderRouter((LocalSemanticProvider(), LocalPromptGenesisProvider()))
    authoring = AuthoringService(providers=router)
    workshops = WorkshopService(authoring, providers=router)
    source = _source("g90h_source")

    source_build = workshops.create_from_source(
        "g90h_source_world",
        owner_id="alice",
        sources=(source,),
        visibility="private",
        semantic_provider="local_semantic_v1",
    )
    assert source_build.package.evidence_coverage > 0.0
    assert source_build.preview.scoped_ref.startswith("preview://")
    assert source_build.publishing.publishable is True
    assert source_build.publishing.visible_in_plaza is False
    assert workshops.evidence_audit("g90h_source_world")["all_prompt_claims_e5"] is True

    prompt_build = workshops.create_from_prompt(
        "g90h_prompt_world",
        owner_id="alice",
        intent=CreatorIntent(
            "g90h_intent",
            "alice",
            "setting: river city\nactor: archivist\ngoal: preserve records",
        ),
        visibility="public",
    )
    assert prompt_build.package.evidence_coverage > 0.0
    assert prompt_build.publishing.publishable is False
    prompt_audit = workshops.evidence_audit("g90h_prompt_world")
    assert prompt_audit["all_prompt_claims_e5"] is True
    for action in ("review_e5", "accept_constraints", "preview"):
        prompt_build = workshops.accept_prompt_review("g90h_prompt_world", action)
    assert prompt_build.publishing.publishable is True
    assert prompt_build.publishing.visible_in_plaza is True

    hybrid_build = workshops.create_hybrid(
        "g90h_hybrid_world",
        owner_id="alice",
        sources=(_source("g90h_hybrid_source", version="2"),),
        intent=CreatorIntent(
            "g90h_hybrid_intent",
            "alice",
            "setting: river city\nactor: archivist\ngoal: inspect archives",
        ),
        visibility="private",
        semantic_provider="local_semantic_v1",
    )
    assert hybrid_build.package.evidence_coverage > 0.0
    hybrid_audit = workshops.evidence_audit("g90h_hybrid_world")
    assert hybrid_audit["all_hybrid_prompt_traces_e5"] is True
    assert hybrid_audit["hybrid_prompt_trace_ids"]

    playable = PlayableService(build_reference_runtime())
    for index, build in enumerate((source_build, prompt_build, hybrid_build), start=1):
        profile = playable.register_package(
            build.package,
            owner_id="alice",
            visibility="private",
        )
        entered = playable.enter(
            profile.profile_id,
            viewer_id="alice",
            mode="observer",
            session_id=f"g90h_session_{index}",
        )
        assert entered["instance"]
        assert entered["state_hash"]
