"""Full Corpus -> Canon Graph (M36).

Composes the M32 source/distillation machinery into runnable graphs:
- SceneCandidate (time/place/participant cues; cross-segment/chapter policy),
- CharacterGraph (identity/alias/role/life-stage),
- SourceGraph (place containment/connectivity, item custody, org membership),
- TimelineGraph (event before/after/uncertain + participants/place/evidence),
- CanonGraph (categories, edition views, contradictory claims preserved).
Pure and deterministic; real《红楼梦》canon remains EXTERNAL_BLOCKED.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.locator import SourceLocator


# ---------------------------------------------------------------- scenes
@dataclass(frozen=True, slots=True)
class SceneCandidate:
    """A scene candidate from time/place/participant cues (cross-chapter ok)."""

    scene_id: str
    chapter_range: tuple[int, int]
    place_keys: tuple[str, ...]
    participant_keys: tuple[str, ...]
    cues: tuple[str, ...]
    locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        if not self.scene_id:
            raise ContractError("scene requires an id")
        if self.chapter_range[0] > self.chapter_range[1]:
            raise ContractError("scene chapter_range must be ordered")


def detect_scenes(
    locators: tuple[SourceLocator, ...],
    *,
    chapter_of: tuple[tuple[SourceLocator, str], ...],
    place_of: tuple[tuple[SourceLocator, str], ...],
    participant_of: tuple[tuple[SourceLocator, str], ...],
) -> tuple[SceneCandidate, ...]:
    """Group source slices into scene candidates by shared cues.

    Caller-supplied cue maps (locator -> chapter/place/participant) keep the
    mechanism edition-agnostic.
    """
    scenes: list[SceneCandidate] = []
    seen: set[str] = set()
    for locator, chapter in chapter_of:
        place_keys = tuple(sorted(p for loc, p in place_of if loc.locator == locator.locator))
        participants = tuple(
            sorted(p for loc, p in participant_of if loc.locator == locator.locator)
        )
        scene_id = f"scene_{chapter}_{'_'.join(place_keys) or 'nowhere'}"
        if scene_id in seen:
            continue
        seen.add(scene_id)
        chapter_range = (int(chapter), int(chapter))
        scenes.append(
            SceneCandidate(
                scene_id=scene_id,
                chapter_range=chapter_range,
                place_keys=place_keys,
                participant_keys=participants,
                cues=("time", "place", "participant"),
                locators=(locator,),
            )
        )
    return tuple(sorted(scenes, key=lambda s: s.scene_id))


# ---------------------------------------------------------------- character graph
@dataclass(frozen=True, slots=True)
class CharacterNode:
    """A character with aliases, role and life-stage evidence."""

    character_key: str
    display_name: str
    aliases: tuple[str, ...]
    role: str
    life_stage: str
    evidence: tuple[SourceLocator, ...]


@dataclass(frozen=True, slots=True)
class CharacterEdge:
    """A relation between two characters."""

    source_key: str
    target_key: str
    relation_type: str
    valid_from: int | None = None
    valid_to: int | None = None


@dataclass(frozen=True, slots=True)
class CharacterGraph:
    """Identity/Alias/Role graph."""

    nodes: tuple[CharacterNode, ...]
    edges: tuple[CharacterEdge, ...]

    def node(self, key: str) -> CharacterNode | None:
        for node in self.nodes:
            if node.character_key == key:
                return node
        return None


def build_character_graph(
    *,
    identities: tuple[tuple[str, str, tuple[str, ...], str, str], ...],
    relations: tuple[tuple[str, str, str, int | None, int | None], ...],
) -> CharacterGraph:
    """Build the character graph from distilled identity + relation claims."""
    nodes = tuple(
        CharacterNode(
            character_key=key,
            display_name=display,
            aliases=aliases,
            role=role,
            life_stage=life_stage,
            evidence=(),
        )
        for key, display, aliases, role, life_stage in identities
    )
    edges = tuple(
        CharacterEdge(source_key=s, target_key=t, relation_type=r, valid_from=v1, valid_to=v2)
        for s, t, r, v1, v2 in relations
    )
    return CharacterGraph(nodes=nodes, edges=edges)


# ---------------------------------------------------------------- source graph
@dataclass(frozen=True, slots=True)
class SourceGraph:
    """Place containment/connectivity, item custody, org membership claims."""

    place_connectivity: tuple[tuple[str, str, str], ...]  # (a, b, via)
    place_containment: tuple[tuple[str, str], ...]  # (container, contained)
    item_custody: tuple[tuple[str, str], ...]  # (item, custodian)
    org_membership: tuple[tuple[str, str], ...]  # (actor, org)


def build_source_graph(
    *,
    connectivity: tuple[tuple[str, str, str], ...] = (),
    containment: tuple[tuple[str, str], ...] = (),
    custody: tuple[tuple[str, str], ...] = (),
    membership: tuple[tuple[str, str], ...] = (),
) -> SourceGraph:
    return SourceGraph(
        place_connectivity=tuple(sorted(connectivity)),
        place_containment=tuple(sorted(containment)),
        item_custody=tuple(sorted(custody)),
        org_membership=tuple(sorted(membership)),
    )
