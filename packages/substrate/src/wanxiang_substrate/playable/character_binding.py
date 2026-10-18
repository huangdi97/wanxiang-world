"""Bind created characters to source-grounded actor entities.

Character creation must not invent a runtime entity: a world actor only exists
because the source package declared it and the preview host created it. This
helper derives the same canonical ids the preview host uses so a user-created
character can actually act through Commit Authority.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.preview.runtime import _safe_id

_ACTOR_TYPES = frozenset({"actor", "person", "character"})


def source_actor_ids(package: WorldPackageDraft) -> tuple[str, ...]:
    """Return canonical ids for actor entities, in preview creation order."""

    entity_types = dict(package.draft.entity_types)
    used: set[str] = set()
    actor_ids: list[str] = []
    for index, (key, display_name) in enumerate(package.draft.entities, start=1):
        readable = display_name if key.startswith("gedcom:") else key
        canonical_id = _safe_id(readable, index, used)
        used.add(canonical_id)
        entity_type = entity_types.get(key, "actor").strip() or "actor"
        if entity_type in _ACTOR_TYPES:
            actor_ids.append(canonical_id)
    return tuple(actor_ids)
