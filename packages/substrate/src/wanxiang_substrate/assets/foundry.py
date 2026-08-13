"""World Asset Foundry seam (G12F).

SemanticSceneSpec -> AssetCandidate via generator/scan/reconstruction ports,
with geometry validation and semantic binding. The foundry produces asset
candidates only; it never owns world truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class SemanticSceneSpec:
    """A semantic description of what an asset must represent."""

    spec_id: str
    semantic_id: str
    kind: str
    requirements: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AssetCandidate:
    """A candidate asset with provenance; not yet world truth."""

    candidate_id: str
    spec_id: str
    generator: str
    geometry_valid: bool
    bounds: tuple[float, float, float] = (0.0, 0.0, 0.0)
    polygon_count: int = 0
    semantic_binding: str = ""
    rights: str = "unreviewed"


class AssetGenerator(Protocol):
    """Port for deterministic generators / scanners / reconstructions."""

    def generate(self, spec: SemanticSceneSpec) -> AssetCandidate: ...


class SyntheticAssetGenerator:
    """Deterministic generator returning a valid candidate."""

    def generate(self, spec: SemanticSceneSpec) -> AssetCandidate:
        return AssetCandidate(
            candidate_id=f"asset_{spec.spec_id}",
            spec_id=spec.spec_id,
            generator="synthetic",
            geometry_valid=True,
            bounds=(1.0, 2.0, 3.0),
            polygon_count=1000,
            semantic_binding=spec.semantic_id,
        )


def validate_geometry(
    candidate: AssetCandidate, *, max_polygons: int = 500_000
) -> tuple[bool, str]:
    """Geometry validation: bounded dimensions and sane polygon count."""
    x, y, z = candidate.bounds
    if x <= 0 or y <= 0 or z <= 0:
        return False, "non-positive bounds"
    if candidate.polygon_count < 0 or candidate.polygon_count > max_polygons:
        return False, "polygon count out of range"
    return True, "ok"


class AssetFoundry:
    """Runs specs through a generator and validates candidates."""

    def __init__(self, generator: AssetGenerator | None = None) -> None:
        self._generator = generator or SyntheticAssetGenerator()
        self._candidates: dict[str, AssetCandidate] = {}

    def produce(self, spec: SemanticSceneSpec) -> AssetCandidate:
        candidate = self._generator.generate(spec)
        valid, reason = validate_geometry(candidate)
        if not valid:
            raise ValueError(f"geometry validation failed: {reason}")
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def get(self, candidate_id: str) -> AssetCandidate | None:
        return self._candidates.get(candidate_id)
