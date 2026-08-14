"""Generative asset / scene pipeline & semantic binding research (G19F, experimental).

Generated assets are PROJECTIONS/ARTIFACTS, never authority: they are bound to
canonical entities, packages, revisions, rights and provenance, and they can be
discarded/regenerated without touching world truth. A deterministic local
foundry provides the generic contract when external generation providers are
unavailable (EXTERNAL_BLOCKED slice).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AssetSpec:
    """Request for a generated asset bound to canonical truth."""

    asset_id: str
    kind: str  # "visual" | "audio" | "three_d"
    entity_ref: str
    package_ref: str
    revision: int
    rights: str


@dataclass(frozen=True, slots=True)
class AssetManifest:
    """Metadata for one generated asset; rights/provenance travel with it."""

    asset_id: str
    kind: str
    entity_ref: str
    package_ref: str
    revision: int
    rights: str
    provenance: str
    version: int
    generated: bool = True
    fallback: bool = False

    def bind_key(self) -> tuple[str, str, int]:
        # Canonical binding: entity + package + revision.
        return (self.entity_ref, self.package_ref, self.revision)


@dataclass(frozen=True, slots=True)
class SceneAnchor:
    """Semantic anchor: a slot in a scene bound to a canonical entity + asset."""

    slot: str
    entity_ref: str
    asset_id: str


@dataclass(frozen=True, slots=True)
class SceneLayout:
    """Projection of a scene rebuilt from semantic state (never canonical)."""

    scene_id: str
    anchors: tuple[SceneAnchor, ...]
    assets: tuple[AssetManifest, ...]

    def rebuild_hash(self) -> str:
        canonical = "|".join(
            [
                self.scene_id,
                "|".join(f"{a.slot}:{a.entity_ref}:{a.asset_id}" for a in self.anchors),
                "|".join(
                    f"{m.asset_id}:{m.kind}:{m.entity_ref}:{m.package_ref}:"
                    f"{m.revision}:{m.version}:{m.rights}:{m.provenance}:{m.fallback}"
                    for m in self.assets
                ),
            ]
        )
        return hashlib.sha256(canonical.encode()).hexdigest()


class AssetGenerator(Protocol):
    def generate(self, spec: AssetSpec) -> AssetManifest: ...


class DeterministicFoundry:
    """Deterministic local generator for the generic contract (no paid API)."""

    def __init__(self, generator_id: str = "local-foundry-1") -> None:
        self._generator_id = generator_id

    def generate(self, spec: AssetSpec) -> AssetManifest:
        return AssetManifest(
            asset_id=spec.asset_id,
            kind=spec.kind,
            entity_ref=spec.entity_ref,
            package_ref=spec.package_ref,
            revision=spec.revision,
            rights=spec.rights,
            provenance=f"{self._generator_id}:v1",
            version=1,
        )


class AssetFoundryPipeline:
    """Binds generation to canonical truth; regeneration versions, never overwrites."""

    def __init__(self, generator: AssetGenerator) -> None:
        self._generator = generator
        self._active: dict[str, AssetManifest] = {}
        self._history: dict[str, list[AssetManifest]] = {}

    def generate(self, spec: AssetSpec) -> AssetManifest:
        previous = self._active.get(spec.asset_id)
        if previous is None:
            manifest = self._generator.generate(spec)
        else:
            manifest = AssetManifest(
                asset_id=spec.asset_id,
                kind=spec.kind,
                entity_ref=spec.entity_ref,
                package_ref=spec.package_ref,
                revision=spec.revision,
                rights=spec.rights,
                provenance=previous.provenance,
                version=previous.version + 1,
            )
        self._active[spec.asset_id] = manifest
        self._history.setdefault(spec.asset_id, []).append(manifest)
        return manifest

    def discard(self, asset_id: str) -> bool:
        # Discard removes only the active projection binding; history is retained.
        return self._active.pop(asset_id, None) is not None

    def active(self, asset_id: str) -> AssetManifest | None:
        return self._active.get(asset_id)

    def history(self, asset_id: str) -> tuple[AssetManifest, ...]:
        return tuple(self._history.get(asset_id, []))


class SceneProjector:
    """Rebuilds a scene from semantic anchors; missing assets become fallback markers."""

    def __init__(self, foundry: AssetFoundryPipeline) -> None:
        self._foundry = foundry

    def project(self, scene_id: str, anchors: tuple[SceneAnchor, ...]) -> SceneLayout:
        assets: list[AssetManifest] = []
        for anchor in anchors:
            manifest = self._foundry.active(anchor.asset_id)
            if manifest is None:
                manifest = AssetManifest(
                    asset_id=anchor.asset_id,
                    kind="unknown",
                    entity_ref=anchor.entity_ref,
                    package_ref="",
                    revision=0,
                    rights="",
                    provenance="missing:fallback",
                    version=0,
                    generated=False,
                    fallback=True,
                )
            assets.append(manifest)
        return SceneLayout(scene_id=scene_id, anchors=anchors, assets=tuple(assets))
