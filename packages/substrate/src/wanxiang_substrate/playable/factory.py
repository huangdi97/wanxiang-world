"""Adapters from existing v5.4 WorldPackage outputs to the experience shell."""

from __future__ import annotations

from typing import Any

from wanxiang_substrate.playable.models import PlayableWorldProfile


def profile_from_world_package(
    package: Any,
    *,
    profile_id: str | None = None,
    scenario_ref: str = "default",
    runtime_profile_ref: str = "reference-commit-authority",
    experience_package_ref: str | None = None,
    projection_profile_ref: str = "default-player",
    owner_id: str = "",
    visibility: str = "private",
    display_name: str | None = None,
) -> PlayableWorldProfile:
    """Build only immutable refs from a v5.4 package; no world state is copied."""

    package_id = getattr(package, "package_id", "")
    if not isinstance(package_id, str) or not package_id:
        raise ValueError("world package must expose a non-empty package_id")
    selected_id = profile_id or f"experience:{package_id}"
    return PlayableWorldProfile(
        profile_id=selected_id,
        world_package_ref=package_id,
        scenario_ref=scenario_ref,
        runtime_profile_ref=runtime_profile_ref,
        experience_package_ref=experience_package_ref or selected_id,
        projection_profile_ref=projection_profile_ref,
        visibility=visibility,  # type: ignore[arg-type]
        owner_id=owner_id,
        display_name=display_name or getattr(package.manifest, "name", package_id),
    )
