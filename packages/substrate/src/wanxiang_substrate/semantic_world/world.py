"""Full Semantic World (M37).

Composes the canon graph + narrative domain + spatial/material/schedule
mechanisms into a runnable SemanticWorld: full World Definition (G40A),
household/society rules incl. reputation (G40B), historical-China narrative
rules with propose-only secrets/scenes/arcs (G40C), per-character packages with
persona-vs-state separation (G40D), full spatial (G40E), material bindings
(G40F), schedules/body/completion (G40G), and multi-scenario dry-run + Core
proper-noun scan (G40H). Pure and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.canon_graph import CanonGraph, CoverageReport
from wanxiang_substrate.worldpack.assembler import AssembledWorldPack


@dataclass(frozen=True, slots=True)
class CharacterPackage:
    """Per-character runnable package: persona vs state separated."""

    character_key: str
    identity: tuple[str, ...]  # identity/alias evidence
    life_arc: tuple[str, ...]  # life-stage beats
    goals: tuple[str, ...]
    relations: tuple[str, ...]
    knowledge: tuple[str, ...]
    capabilities: tuple[str, ...]
    evidence: tuple[str, ...]  # source refs
    persona: tuple[str, ...] = ()  # interpretive (never state)
    state: tuple[tuple[str, str], ...] = ()  # current state fields


@dataclass(frozen=True, slots=True)
class HouseholdSociety:
    """Generic household/society rules: duty/norm/permission/reputation."""

    duties: tuple[tuple[str, str, int], ...]  # (actor, duty_type, due_ticks)
    norms: tuple[str, ...]
    permissions: tuple[tuple[str, str, str], ...]  # (actor, permission, target)
    reputation: tuple[tuple[str, str, float], ...]  # (actor, dimension, score)


@dataclass(frozen=True, slots=True)
class HistoricalChinaRules:
    """Historical-China narrative rules; secret/scene/arc are propose-only."""

    time_rules: tuple[str, ...]
    identity_rules: tuple[str, ...]
    transport_rules: tuple[str, ...]
    life_rules: tuple[str, ...]
    secrets: tuple[str, ...] = ()  # propose-only, never auto-revealed
    scenes: tuple[str, ...] = ()
    arcs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SpatialWorld:
    """Full spatial world: rooms/portals/routes + visibility/acoustic/access."""

    rooms: tuple[str, ...]
    portals: tuple[tuple[str, str, str], ...]  # (a, b, state)
    routes: tuple[tuple[str, str, tuple[str, ...]], ...]
    visibility: tuple[tuple[str, str], ...]  # (from, to)
    acoustic: tuple[tuple[str, str], ...]
    access: tuple[tuple[str, str, str], ...]  # (actor, place, permission)


@dataclass(frozen=True, slots=True)
class SemanticWorld:
    """The full semantic world: definition + characters + domains + graphs."""

    definition: AssembledWorldPack
    characters: tuple[CharacterPackage, ...]
    household: HouseholdSociety
    history_rules: HistoricalChinaRules
    spatial: SpatialWorld
    material_bindings: tuple[tuple[str, str, str], ...]  # (item, kind, custodian)
    schedules: tuple[tuple[str, tuple[tuple[int, str], ...]], ...]
    canon: CanonGraph
    coverage: CoverageReport


def build_full_semantic_world(
    *,
    definition: AssembledWorldPack,
    characters: tuple[CharacterPackage, ...],
    household: HouseholdSociety,
    history_rules: HistoricalChinaRules,
    spatial: SpatialWorld,
    material_bindings: tuple[tuple[str, str, str], ...],
    schedules: tuple[tuple[str, tuple[tuple[int, str], ...]], ...],
    canon: CanonGraph,
    coverage: CoverageReport,
) -> SemanticWorld:
    """Assemble the full semantic world (pure)."""
    if not characters:
        raise ContractError("semantic world requires at least one character")
    return SemanticWorld(
        definition=definition,
        characters=characters,
        household=household,
        history_rules=history_rules,
        spatial=spatial,
        material_bindings=material_bindings,
        schedules=schedules,
        canon=canon,
        coverage=coverage,
    )


def multi_scenario_dry_run(
    world: SemanticWorld, scenarios: tuple[str, ...]
) -> tuple[tuple[str, bool], ...]:
    """Dry-run multiple scenarios: each scenario resolves without committing."""
    results: list[tuple[str, bool]] = []
    for scenario in scenarios:
        # A dry run only checks the world can be addressed for the scenario;
        # no Commit Authority write is performed here.
        known = any(
            scenario in c.character_key or scenario in r
            for c in world.characters
            for r in c.life_arc
        )
        results.append((scenario, known or scenario in world.definition.scenario.time_ref))
    return tuple(results)


def scan_core_proper_nouns(core_roots: tuple[str, ...]) -> tuple[str, ...]:
    """Scan Core packages for forbidden domain proper nouns (Kernel purity)."""
    from pathlib import Path

    forbidden = ("林黛玉", "贾宝玉", "潇湘馆", "怡红院", "红楼梦", "贾府", "太虚幻境")
    found: list[str] = []
    for root in core_roots:
        for py in Path(root).rglob("*.py"):
            text = py.read_text(encoding="utf-8")
            for name in forbidden:
                if name in text:
                    found.append(name)
    return tuple(sorted(set(found)))
