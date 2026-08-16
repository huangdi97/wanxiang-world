"""Coverage / missingness metrics for a WorldDraft (G59E).

Assesses how completely a draft covers selected domains' provided
capabilities, and reports unknown/blocking/rights/conflict items honestly.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.draft.model import WorldDraft


@dataclass(frozen=True, slots=True)
class CoverageReport:
    draft_id: str
    coverage: float
    unknown: tuple[str, ...]
    blocking: tuple[str, ...]
    rights_issues: int
    conflicts: int

    @property
    def has_blocking_gap(self) -> bool:
        return bool(self.blocking)


class CoverageAssessor:
    """Measures required-capability coverage of a draft (deterministic)."""

    REQUIRED_SECTIONS = (
        ("entities", "actor entities"),
        ("relations", "relations"),
        ("places", "places"),
        ("events", "events"),
        ("rules", "rules"),
    )

    def assess(self, draft: WorldDraft, registry: DomainRegistry) -> CoverageReport:
        unknown: list[str] = []
        for field, label in self.REQUIRED_SECTIONS:
            if not getattr(draft, field):
                unknown.append(label)
        blocking = tuple(
            label for label in unknown if label in ("actor entities", "places", "events")
        )
        # Capability coverage across selected domains.
        required_capabilities: set[str] = set()
        for domain_id in draft.selected_domains:
            domain = registry.get(domain_id)
            if domain:
                required_capabilities.update(domain.provides)
        covered = 0
        for capability in required_capabilities:
            if self._covers(draft, capability):
                covered += 1
        total = len(required_capabilities)
        coverage = (covered / total) if total else 0.0
        return CoverageReport(
            draft_id=draft.draft_id,
            coverage=coverage,
            unknown=tuple(unknown),
            blocking=blocking,
            rights_issues=len(draft.unresolved_rights),
            conflicts=len(draft.unresolved_conflicts),
        )

    def _covers(self, draft: WorldDraft, capability: str) -> bool:
        key = capability.lower()
        if key in ("family", "genealogy"):
            return bool(draft.entities and draft.relations)
        if key in ("social", "relation"):
            return bool(draft.relations)
        if key in ("temporal", "timeline"):
            return bool(draft.events)
        if key in ("spatial", "place", "topology"):
            return bool(draft.places)
        if key in ("institution", "organization"):
            return bool(draft.organizations)
        if key in ("norm", "rule", "ritual"):
            return bool(draft.rules)
        if key in ("epistemic", "knowledge"):
            return bool(draft.knowledge_boundaries)
        if key in ("narrative", "character"):
            return bool(draft.character_profiles or draft.entities)
        return False
