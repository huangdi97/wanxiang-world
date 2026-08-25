"""Static configuration helpers for the source-to-draft pipeline."""

from __future__ import annotations

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill import (
    CharacterKnowledgePass,
    DistillerDAG,
    EventTimeSpacePass,
    IdentityPass,
    ObjectRuleSkillPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry


def default_domain_registry() -> DomainRegistry:
    registry = DomainRegistry()
    for domain in (
        DomainCapability("family", "Family", "1.0.0", ("family", "genealogy")),
        DomainCapability(
            "narrative",
            "Narrative",
            "1.0.0",
            ("narrative", "character", "temporal"),
            requires=("family",),
        ),
        DomainCapability("household", "Household", "1.0.0", ("social", "norm", "institution")),
        DomainCapability("spatial", "Spatial", "1.0.0", ("spatial", "place", "topology")),
    ):
        registry.register(domain)
    return registry


def distiller_dag() -> DistillerDAG:
    return DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )


def field(candidate: CandidateEnvelope, *names: str, default: str = "") -> str:
    values = candidate.fields
    return next((values[name] for name in names if values.get(name)), default)


def expand_domains(registry: DomainRegistry, selected: tuple[str, ...]) -> tuple[str, ...]:
    found = set(selected)
    changed = True
    while changed:
        changed = False
        for domain_id in tuple(found):
            domain = registry.get(domain_id)
            if domain is None:
                continue
            for required in domain.requires:
                if required not in found:
                    found.add(required)
                    changed = True
    return tuple(sorted(found))


__all__ = [
    "default_domain_registry",
    "distiller_dag",
    "expand_domains",
    "field",
]
