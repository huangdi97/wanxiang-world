"""Family privacy, living archive & digital persona modes (G09C).

Evidence / Reconstructed Persona / Creative Legacy modes are strictly labeled;
outputs are never conflated. Consent, revocation and posthumous policy gate
private memories/media.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.genealogy.errors import PrivacyDenied

PersonaMode = Literal["evidence", "reconstructed_persona", "creative_legacy"]


@dataclass(frozen=True, slots=True)
class ConsentState:
    """Living-archive consent with revocation and posthumous policy."""

    person_id: str
    consent_granted: bool
    posthumous_policy: str = "private"
    revoked: bool = False

    @property
    def can_surface(self) -> bool:
        return self.consent_granted and not self.revoked


class LivingArchive:
    """Gates private memories/media by consent and mode."""

    def __init__(self) -> None:
        self._consent: dict[str, ConsentState] = {}
        self._private_items: dict[str, str] = {}

    def record_consent(self, state: ConsentState) -> ConsentState:
        self._consent[state.person_id] = state
        return state

    def revoke(self, person_id: str) -> ConsentState:
        current = self._consent.get(person_id)
        if current is None:
            raise PrivacyDenied(f"no consent record for {person_id!r}")
        updated = ConsentState(
            person_id=current.person_id,
            consent_granted=current.consent_granted,
            posthumous_policy=current.posthumous_policy,
            revoked=True,
        )
        self._consent[person_id] = updated
        return updated

    def add_private_item(self, person_id: str, item_ref: str) -> None:
        self._private_items[item_ref] = person_id

    def require_surface(self, person_id: str, item_ref: str, mode: PersonaMode) -> None:
        state = self._consent.get(person_id)
        if state is None or not state.can_surface:
            raise PrivacyDenied(f"no consent to surface {item_ref!r}")
        owner = self._private_items.get(item_ref)
        if owner is not None and owner != person_id:
            raise PrivacyDenied(f"item {item_ref!r} is private to {owner!r}")
        if mode == "creative_legacy" and state.posthumous_policy != "public":
            raise PrivacyDenied("creative legacy mode requires public posthumous policy")


def mode_label(mode: PersonaMode) -> str:
    """Strict output labeling per persona mode."""
    return {
        "evidence": "evidence",
        "reconstructed_persona": "reconstructed",
        "creative_legacy": "creative",
    }[mode]
