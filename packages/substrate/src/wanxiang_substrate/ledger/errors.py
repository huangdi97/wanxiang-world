"""Structured completion ledger error taxonomy (G04D)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class LedgerError(WanxiangError):
    """Base error for the completion ledger."""

    code = "ledger_error"


class InvalidPromotion(LedgerError):
    code = "invalid_label_promotion"


class ReviewRequired(LedgerError):
    code = "review_required_for_canon"


class CanonLocked(LedgerError):
    code = "canon_locked"


class RightsBlocked(LedgerError):
    code = "review_rights_blocked"


class ItemNotFound(LedgerError):
    code = "ledger_item_not_found"
