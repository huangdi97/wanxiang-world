"""Bounded visual prompt compilation for book-derived scene asset providers.

The compiler carries structured evidence references and creative style choices.
It never receives or serializes an entire source book.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan


@dataclass(frozen=True, slots=True)
class _StoryVisualProfile:
    """Versioned creative projection shared by all scenes in one world."""

    profile_id: str
    style_key: str
    medium: str
    palette: tuple[str, ...]
    lighting: str
    camera_language: str
    negative_constraints: tuple[str, ...]
    creative_projection: bool = True
    version: int = 1


@dataclass(frozen=True, slots=True)
class _SceneGenerationBrief:
    """Minimal provider-facing scene brief; source text remains outside this record."""

    brief_id: str
    scene_key: str
    place_name: str
    style_profile_id: str
    style_key: str
    semantic_prompt: str
    source_refs: tuple[str, ...]
    source_context_candidates: tuple[str, ...]
    negative_constraints: tuple[str, ...]
    full_source_included: bool = False
    version: int = 1


_PALETTES = (
    ("mist-jade", "ink-blue", "warm-paper"),
    ("cinder-amber", "slate", "ivory"),
    ("moss", "river-blue", "clay"),
    ("moon-silver", "deep-indigo", "muted-gold"),
)
_LIGHTING = ("soft-overcast", "late-afternoon", "diffuse-interior", "misty-dawn")
_CAMERA = ("human-eye-wide", "cinematic-wide", "illustrated-diorama", "quiet-observer")


def _story_visual_profile(plan: _SourceVisualPlan) -> _StoryVisualProfile:
    """Create one deterministic creative style seed per source world."""
    style_key = (
        plan.scene_requests[0].style_key
        if plan.scene_requests and plan.scene_requests[0].style_key
        else hashlib.sha256(
            f"{plan.source_digest}:story-visual-profile:v1".encode("utf-8")
        ).hexdigest()[:24]
    )
    digest = hashlib.sha256(style_key.encode("utf-8")).digest()
    return _StoryVisualProfile(
        profile_id=f"story-visual:{style_key}",
        style_key=style_key,
        medium="illustrated-environment",
        palette=_PALETTES[digest[0] % len(_PALETTES)],
        lighting=_LIGHTING[digest[1] % len(_LIGHTING)],
        camera_language=_CAMERA[digest[2] % len(_CAMERA)],
        negative_constraints=(
            "do-not-invent-named-characters",
            "do-not-invent-geographic-topology",
            "no-readable-source-paragraphs",
            "no-canonical-claims-from-generated-pixels",
        ),
    )


def _compile_scene_generation_brief(
    request: _SourceSceneRequest,
    profile: _StoryVisualProfile,
) -> _SceneGenerationBrief:
    """Compile a bounded prompt using structured scene evidence, not full source text."""
    context = tuple(
        requirement.split(":", 1)[1]
        for requirement in request.spec.requirements
        if requirement.startswith("source_context_candidate:")
        and ":" in requirement
    )[:8]
    payload = {
        "task": "create one immersive environment illustration candidate",
        "place": request.place_name,
        "medium": profile.medium,
        "palette": list(profile.palette),
        "lighting": profile.lighting,
        "camera_language": profile.camera_language,
        "context_candidates": list(context),
        "evidence_policy": (
            "context candidates are co-located source evidence candidates, "
            "not guaranteed present actors or canonical spatial facts"
        ),
        "negative_constraints": list(profile.negative_constraints),
    }
    semantic_prompt = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    brief_hash = hashlib.sha256(
        json.dumps(
            {
                "scene_key": request.stable_key,
                "style_key": profile.style_key,
                "source_refs": request.source_refs,
                "prompt": semantic_prompt,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:24]
    return _SceneGenerationBrief(
        brief_id=f"visual-brief:{brief_hash}",
        scene_key=request.stable_key,
        place_name=request.place_name,
        style_profile_id=profile.profile_id,
        style_key=profile.style_key,
        semantic_prompt=semantic_prompt,
        source_refs=request.source_refs,
        source_context_candidates=context,
        negative_constraints=profile.negative_constraints,
    )
