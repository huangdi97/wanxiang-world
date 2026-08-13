"""Research adapter error taxonomy (G12D)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class ResearchError(WanxiangError):
    """Base error for research adapters."""

    code = "research_error"


class InvalidActionSpace(ResearchError):
    code = "invalid_action_space"


class NotReset(ResearchError):
    code = "environment_not_reset"
