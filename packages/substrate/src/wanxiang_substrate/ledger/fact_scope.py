"""Fact Scope and Authority Partition (G30G).

Facts share one schema but are partitioned by write authority:

- canonical    -> only Commit Authority may write
- public       -> system / commit authority
- org          -> the owning organization
- actor        -> the owning actor (private belief)
- hypothesis   -> researchers (never canonical by scope edit)
- reconstruction -> researchers

Rules:
- A scope-only edit (changing the scope field in place) can NEVER upgrade a
  belief/hypothesis/reconstruction to canonical; canonical promotion MUST go
  through Commit (and the review/evidence pipeline).
- Projection/Perception filter facts by scope and rights: actor facts never
  leak to other actors; org facts never leak outside the org; hypothesis /
  reconstruction facts never reach actors or the public.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from wanxiang_domain.errors import PermissionDenied

FactScope = Literal["canonical", "public", "org", "actor", "hypothesis", "reconstruction"]

FACT_SCOPES: tuple[FactScope, ...] = (
    "canonical",
    "public",
    "org",
    "actor",
    "hypothesis",
    "reconstruction",
)

# Writer kinds allowed per scope (canonical is exclusive to commit authority).
FACT_SCOPE_WRITERS: Mapping[FactScope, tuple[str, ...]] = {
    "canonical": ("commit_authority",),
    "public": ("system", "commit_authority"),
    "org": ("org", "commit_authority"),
    "actor": ("actor",),
    "hypothesis": ("researcher", "commit_authority"),
    "reconstruction": ("researcher", "commit_authority"),
}


class FactScopePolicy:
    """Pure policy: write authority, elevation, and projection visibility."""

    @staticmethod
    def assert_write_allowed(scope: FactScope, writer: str) -> None:
        allowed = FACT_SCOPE_WRITERS[scope]
        if writer not in allowed:
            raise PermissionDenied(
                f"writer {writer!r} may not write scope {scope!r}; allowed {allowed}"
            )

    @staticmethod
    def assert_canonical_promotion_requires_commit(
        current: FactScope, target: FactScope, *, via_commit: bool
    ) -> None:
        """Scope-only edits can never elevate; canonical promotion needs Commit."""
        if current == target:
            return
        if target == "canonical" and not via_commit:
            raise PermissionDenied(
                "canonical promotion requires Commit; a scope-only edit is rejected"
            )
        if not via_commit:
            raise PermissionDenied(
                f"fact scope change {current} -> {target} requires Commit; rejected"
            )

    @staticmethod
    def can_view(scope: FactScope, viewer: str) -> bool:
        """Projection/perception filter by scope and viewer role.

        viewer is a role string: "system" / "admin" / "researcher" /
        "org:<id>" / "actor:<id>".
        """
        if viewer in ("system", "admin"):
            return True
        if scope in ("canonical", "public"):
            return True
        if scope == "org":
            return viewer.startswith("org:")
        if scope == "actor":
            return viewer.startswith("actor:")
        # hypothesis / reconstruction: researchers only
        return viewer == "researcher"
