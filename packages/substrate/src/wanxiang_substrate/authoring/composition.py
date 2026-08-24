"""Domain composition and sandbox gap packs (M63)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.domains.resolver import DomainDependencyResolver


@dataclass(frozen=True, slots=True)
class DomainComposition:
    composition_id: str
    domain_versions: tuple[tuple[str, str], ...]
    dependency_order: tuple[str, ...]
    dependency_lock: tuple[str, ...]
    gaps: tuple[str, ...]
    fingerprint: str
    candidate_only: bool = True


@dataclass(frozen=True, slots=True)
class DomainGapPack:
    gap_id: str
    domain_id: str
    missing_capabilities: tuple[str, ...]
    sandbox_only: bool = True


def compose_domains(
    registry: DomainRegistry,
    selected: tuple[str, ...],
    *,
    composition_id: str = "composition_1",
) -> DomainComposition:
    resolution = DomainDependencyResolver().resolve(registry, selected)
    versions = tuple(
        sorted(
            (domain_id, registry.require(domain_id).version)
            for domain_id in resolution.selected
            if registry.get(domain_id)
        )
    )
    payload = {"versions": versions, "order": resolution.order, "conflicts": resolution.conflicts}
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DomainComposition(
        composition_id=composition_id,
        domain_versions=versions,
        dependency_order=resolution.order,
        dependency_lock=resolution.order,
        gaps=resolution.conflicts,
        fingerprint=fingerprint,
    )


def make_gap_pack(
    composition: DomainComposition, registry: DomainRegistry
) -> tuple[DomainGapPack, ...]:
    packs: list[DomainGapPack] = []
    for domain_id, _version in composition.domain_versions:
        domain = registry.require(domain_id)
        if not domain.actions or not domain.rules:
            missing = tuple(
                item
                for item, present in (
                    ("actions", bool(domain.actions)),
                    ("rules", bool(domain.rules)),
                )
                if not present
            )
            packs.append(DomainGapPack(f"gap_{domain_id}", domain_id, missing))
    return tuple(packs)
