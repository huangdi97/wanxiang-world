"""Structured epistemic error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class BeliefError(WanxiangError):
    """Base error for epistemic substrate failures."""

    code = "belief_error"


class EpistemicConflict(BeliefError):
    code = "epistemic_conflict"


class MemoryAccessDenied(BeliefError):
    code = "memory_access_denied"
