"""Family Portal service (G18E).

Privacy-first family views over the family domain contracts: claims with
conflicts, rights-filtered person views, and GEDCOM export preserving source
references. Living-person private data is never exposed by default.
"""

from __future__ import annotations

from typing import Any

from wanxiang_substrate.genealogy.family import FamilyClaim, FamilyWorld
from wanxiang_substrate.genealogy.gedcom import serialize_gedcom
from wanxiang_substrate.genealogy.model import GedcomDocument, GedcomIndividual
from wanxiang_substrate.genealogy.privacy import LivingArchive


class FamilyPrivacyDenied(Exception):
    pass


class FamilyPortalService:
    def __init__(self, world: FamilyWorld, archive: LivingArchive) -> None:
        self._world = world
        self._archive = archive

    def _surface_allowed(self, person_id: str, item_ref: str) -> bool:
        try:
            self._archive.require_surface(person_id, item_ref, "evidence")
            return True
        except Exception:
            return False

    def person_view(self, person_id: str, viewer: str) -> dict[str, Any]:
        allowed = self._surface_allowed(person_id, f"view:{person_id}")
        if not allowed and viewer != person_id:
            raise FamilyPrivacyDenied("protected living-person view")
        claims = self._world.claims_for(person_id)
        by_prop: dict[str, list[FamilyClaim]] = {}
        for claim in claims:
            by_prop.setdefault(claim.proposition, []).append(claim)
        conflicts = {
            prop: [c.value for c in group]
            for prop, group in by_prop.items()
            if len({c.value for c in group}) > 1
        }
        return {
            "person_id": person_id,
            "claims": [
                {"proposition": c.proposition, "value": c.value, "source_refs": c.source_refs}
                for c in claims
            ],
            "conflicts": conflicts,
            "privacy": {"surface": allowed, "viewer_allowed": allowed or viewer == person_id},
        }

    def export(self, person_id: str, viewer: str) -> str:
        if not self._surface_allowed(person_id, f"export:{person_id}") and viewer != person_id:
            raise FamilyPrivacyDenied("living-person private data is not exported")
        claims = self._world.claims_for(person_id)
        source_refs: tuple[str, ...] = ()
        for claim in claims:
            source_refs = tuple(dict.fromkeys(source_refs + claim.source_refs))
        doc = GedcomDocument(
            individuals=(
                GedcomIndividual(xref=person_id, name=person_id, source_refs=source_refs),
            ),
            families=(),
            sources=(),
        )
        return serialize_gedcom(doc)
