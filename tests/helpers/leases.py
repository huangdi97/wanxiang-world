"""Test helper: mint canonical-write leases for canonical-row test doubles.

Tests are allowed to be an explicit minter (the production golden set keeps
`mint_canonical_write_lease` out of every module except the authority); this helper
keeps that adaptation to a single call site per test instead of duplicating the
keyword arguments everywhere.
"""

from __future__ import annotations

from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.canonical_write import CanonicalWriteLease, mint_canonical_write_lease


def lease_for(
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    audit_ref: str = "tests:canonical-write-lease",
) -> CanonicalWriteLease:
    """Mint a lease scoped to `(instance_id, branch_id)` for a test write."""
    return mint_canonical_write_lease(
        instance_id=instance_id, branch_id=branch_id, audit_ref=audit_ref
    )
