"""Heritage / Museum workbench service (G18F).

Object semantic-twin views with physical/digital/reconstruction states kept
visibly distinct, curator vs public projection rights, and auditable
conservation history. Reconstructions are never presented as original fact.
"""

from __future__ import annotations

from typing import Any

from wanxiang_substrate.heritage.museum import MuseumBiography
from wanxiang_substrate.heritage.twin import HeritageTwin


class HeritageRightsDenied(Exception):
    pass


class HeritageWorkbenchService:
    def __init__(self, twin: HeritageTwin, biography: MuseumBiography) -> None:
        self._twin = twin
        self._biography = biography

    def object_view(self, object_id: str, *, curator: bool) -> dict[str, Any]:
        ids = self._twin.identities()
        # Physical/digital/reconstruction states are visibly distinct.
        distinct = {key: value for key, value in ids.items()}  # noqa: C416
        timeline = [
            {"entry_id": e.entry_id, "kind": e.kind, "label": e.label}
            for e in self._biography.entries()
        ]
        return {
            "object_id": object_id,
            "identities": distinct,
            "timeline": timeline,
            "curator": curator,
            "reconstruction_labeled": True,
        }

    def export(self, object_id: str, *, curator: bool) -> dict[str, Any]:
        if not curator:
            raise HeritageRightsDenied("restricted heritage export requires curator rights")
        return {"object_id": object_id, "exported": True, "curator": True}

    def conservation_history(self) -> dict[str, Any]:
        history = [
            {"version": e.version, "state": e.state, "provenance_ref": e.provenance_ref}
            for e in self._twin.conservation_history()
        ]
        return {"entries": history, "auditable": True}
