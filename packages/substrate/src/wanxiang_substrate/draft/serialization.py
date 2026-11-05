"""Lossless JSON-facing serialization for `WorldDraft`.

Kept separate from the model so the draft model stays a small, declarative
schema and durable Player catalogs can round-trip a compiled draft without
giving projections any canonical authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.draft.model import VALID_STATUSES, WorldDraft


def draft_to_dict(draft: WorldDraft) -> dict[str, object]:
    """JSON-friendly, lossless representation of one immutable draft."""

    return {
        "draft_id": draft.draft_id,
        "revision": draft.revision,
        "status": draft.status,
        "source_refs": list(draft.source_refs),
        "source_versions": [list(item) for item in draft.source_versions],
        "constitution_ref": draft.constitution_ref,
        "selected_domains": list(draft.selected_domains),
        "dependency_lock": list(draft.dependency_lock),
        "entities": [list(item) for item in draft.entities],
        "entity_types": [list(item) for item in draft.entity_types],
        "aliases": [list(item) for item in draft.aliases],
        "character_profiles": list(draft.character_profiles),
        "organizations": list(draft.organizations),
        "relations": [list(item) for item in draft.relations],
        "places": list(draft.places),
        "objects": list(draft.objects),
        "events": [list(item) for item in draft.events],
        "knowledge_boundaries": list(draft.knowledge_boundaries),
        "rules": list(draft.rules),
        "skills": list(draft.skills),
        "completion_items": list(draft.completion_items),
        "unresolved_conflicts": list(draft.unresolved_conflicts),
        "unresolved_rights": list(draft.unresolved_rights),
        "scenario_candidates": list(draft.scenario_candidates),
        "genesis_candidates": list(draft.genesis_candidates),
        "coverage": draft.coverage,
        "uncertainty": draft.uncertainty,
        "quality": draft.quality,
        "compiler_metadata": dict(draft.compiler_metadata),
    }


def draft_from_dict(data: Mapping[str, object]) -> WorldDraft:
    """Rebuild a validated draft; unknown/mistyped fields fail closed."""

    status = data.get("status")
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ContractError(f"invalid draft status {status!r}")
    return WorldDraft(
        draft_id=_required_text(data.get("draft_id"), "draft_id"),
        revision=_positive_int(data.get("revision"), "revision"),
        status=status,
        source_refs=_text_tuple(data.get("source_refs", []), "source_refs"),
        source_versions=_pair_tuple(data.get("source_versions", []), "source_versions"),
        constitution_ref=_optional_text(data.get("constitution_ref", ""), "constitution_ref"),
        selected_domains=_text_tuple(data.get("selected_domains", []), "selected_domains"),
        dependency_lock=_text_tuple(data.get("dependency_lock", []), "dependency_lock"),
        entities=_pair_tuple(data.get("entities", []), "entities"),
        entity_types=_pair_tuple(data.get("entity_types", []), "entity_types"),
        aliases=_pair_tuple(data.get("aliases", []), "aliases"),
        character_profiles=_text_tuple(data.get("character_profiles", []), "character_profiles"),
        organizations=_text_tuple(data.get("organizations", []), "organizations"),
        relations=_triple_tuple(data.get("relations", []), "relations"),
        places=_text_tuple(data.get("places", []), "places"),
        objects=_text_tuple(data.get("objects", []), "objects"),
        events=_pair_tuple(data.get("events", []), "events"),
        knowledge_boundaries=_text_tuple(
            data.get("knowledge_boundaries", []), "knowledge_boundaries"
        ),
        rules=_text_tuple(data.get("rules", []), "rules"),
        skills=_text_tuple(data.get("skills", []), "skills"),
        completion_items=_text_tuple(data.get("completion_items", []), "completion_items"),
        unresolved_conflicts=_text_tuple(
            data.get("unresolved_conflicts", []), "unresolved_conflicts"
        ),
        unresolved_rights=_text_tuple(data.get("unresolved_rights", []), "unresolved_rights"),
        scenario_candidates=_text_tuple(data.get("scenario_candidates", []), "scenario_candidates"),
        genesis_candidates=_text_tuple(data.get("genesis_candidates", []), "genesis_candidates"),
        coverage=_unit_float(data.get("coverage", 0.0), "coverage"),
        uncertainty=_unit_float(data.get("uncertainty", 0.0), "uncertainty"),
        quality=_unit_float(data.get("quality", 0.0), "quality"),
        compiler_metadata=_string_map(data.get("compiler_metadata", {}), "compiler_metadata"),
    )


def _required_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"draft {name} must be a non-empty string")
    return value


def _optional_text(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"draft {name} must be text")
    return value


def _positive_int(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ContractError(f"draft {name} must be a positive integer")
    return value


def _unit_float(value: object, name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ContractError(f"draft {name} must be numeric")
    number = float(value)
    if not (0.0 <= number <= 1.0):
        raise ContractError(f"draft {name} must be within [0,1]")
    return number


def _text_tuple(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ContractError(f"draft {name} must be a list of strings")
    raw = cast(list[object], value)
    if any(not isinstance(item, str) for item in raw):
        raise ContractError(f"draft {name} must be a list of strings")
    return tuple(cast(list[str], raw))


def _pair_tuple(value: object, name: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise ContractError(f"draft {name} must be a list")
    pairs: list[tuple[str, str]] = []
    for item in cast(list[object], value):
        if not isinstance(item, list):
            raise ContractError(f"draft {name} items must be [text, text]")
        parts = cast(list[object], item)
        if len(parts) != 2:
            raise ContractError(f"draft {name} items must be [text, text]")
        first, second = parts
        if not isinstance(first, str) or not isinstance(second, str):
            raise ContractError(f"draft {name} items must be [text, text]")
        pairs.append((first, second))
    return tuple(pairs)


def _triple_tuple(value: object, name: str) -> tuple[tuple[str, str, str], ...]:
    if not isinstance(value, list):
        raise ContractError(f"draft {name} must be a list")
    triples: list[tuple[str, str, str]] = []
    for item in cast(list[object], value):
        if not isinstance(item, list):
            raise ContractError(f"draft {name} items must be [text, text, text]")
        parts = cast(list[object], item)
        if len(parts) != 3:
            raise ContractError(f"draft {name} items must be [text, text, text]")
        if any(not isinstance(part, str) for part in parts):
            raise ContractError(f"draft {name} items must be [text, text, text]")
        triples.append((cast(str, parts[0]), cast(str, parts[1]), cast(str, parts[2])))
    return tuple(triples)


def _string_map(value: object, name: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ContractError(f"draft {name} must be an object")
    mapping: dict[str, str] = {}
    for key, item in cast(dict[object, object], value).items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ContractError(f"draft {name} must map text to text")
        mapping[key] = item
    return mapping
