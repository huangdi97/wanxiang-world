"""G18E: family portal completion.

- Conflicting claims remain visible as conflicts (never silently merged).
- Unauthorized users cannot see protected living-person fields/media.
- Export preserves supported source references.
"""

from __future__ import annotations

import pytest
from wanxiang_api.family_portal_service import FamilyPortalService, FamilyPrivacyDenied
from wanxiang_substrate.genealogy.family import FamilyClaim, FamilyWorld, Person
from wanxiang_substrate.genealogy.privacy import ConsentState, LivingArchive


def _fixture() -> tuple[FamilyWorld, LivingArchive]:
    world = FamilyWorld()
    world.add_person(Person("p1", "Pat", living=True))
    world.add_claim(
        FamilyClaim(
            claim_id="c1",
            person_id="p1",
            proposition="birth_year",
            value="1950",
            source_refs=("s1",),
        )
    )
    world.add_claim(
        FamilyClaim(
            claim_id="c2",
            person_id="p1",
            proposition="birth_year",
            value="1948",
            source_refs=("s2",),
        )
    )
    archive = LivingArchive()
    archive.record_consent(ConsentState(person_id="p1", consent_granted=True))
    archive.add_private_item("p1", "media:photo1")
    return world, archive


def test_conflicting_claims_remain_visible_as_conflicts() -> None:
    world, archive = _fixture()
    service = FamilyPortalService(world, archive)
    view = service.person_view("p1", "p1")
    assert view["conflicts"] == {"birth_year": ["1950", "1948"]}
    assert len(view["claims"]) == 2


def test_unauthorized_user_cannot_see_protected_view() -> None:
    world = FamilyWorld()
    world.add_person(Person("p1", "Pat", living=True))
    archive = LivingArchive()
    archive.record_consent(ConsentState(person_id="p1", consent_granted=False))
    service = FamilyPortalService(world, archive)
    with pytest.raises(FamilyPrivacyDenied):
        service.person_view("p1", "stranger")
    with pytest.raises(FamilyPrivacyDenied):
        service.export("p1", "stranger")


def test_export_preserves_source_references() -> None:
    world, archive = _fixture()
    service = FamilyPortalService(world, archive)
    exported = service.export("p1", "p1")
    assert "SOUR" in exported or "s1" in exported or "s2" in exported
