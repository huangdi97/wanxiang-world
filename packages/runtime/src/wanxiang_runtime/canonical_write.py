"""Canonical-write lease: the sole credential for canonical writes (R7 Gate C).

A canonical write (an event append, or a write to a canonical row such as a
world instance, branch, snapshot, lineage node/edge or audit trace) is accepted
only while it presents a `CanonicalWriteLease`.

The lease is minted by the Commit Authority through `mint_canonical_write_lease`
and is branded and registered in `wanxiang_runtime.internal.lease_core`. Because
acceptance is decided by the brand registry rather than by field equality, an
object that merely reproduces the four public fields is rejected: holding the
credential means having received it from the authority, never having rebuilt its
shape.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from wanxiang_domain.ids import BranchId, WorldInstanceId

# WHY: these are the module-private brand core; importing them here is the single
# sanctioned boundary, so the private-usage rule is scoped to these two names.
from wanxiang_runtime.internal.lease_core import (
    _is_issued,  # pyright: ignore[reportPrivateUsage]
    _mint,  # pyright: ignore[reportPrivateUsage]
)

_MS_PER_SECOND = 1_000_000


class WanxiangRuntimeError(Exception):
    """Base class for runtime-layer errors that are not domain errors.

    The runtime package owns this base deliberately: a canonical-write denial is
    a runtime-authority failure, not a domain validation failure, so it must not
    be caught by handlers that map `wanxiang_domain.errors.WanxiangError`.
    """


class CanonicalWriteRejected(WanxiangRuntimeError):
    """A canonical write was attempted without a valid, correctly-scoped lease."""


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CanonicalWriteLease:
    """An un-forgeable credential authorizing a write to one worldline.

    `_brand` is `init=False`: it has no constructor parameter, and only
    `internal.lease_core._mint` can set it. A hand-built instance with identical
    `instance_id`/`branch_id`/`issued_at_ms`/`audit_ref` keeps `_brand is None`
    and is therefore never accepted.
    """

    instance_id: WorldInstanceId
    branch_id: BranchId
    issued_at_ms: int
    audit_ref: str
    _brand: object | None = field(default=None, init=False, repr=False, compare=False)


def mint_canonical_write_lease(
    *,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    audit_ref: str,
) -> CanonicalWriteLease:
    """Mint and register a lease for one `(instance_id, branch_id)` worldline.

    This is the only production minter. It is called by the Commit Authority
    (`wanxiang_runtime.authority`) and by tests; no other production module may
    reference it.

    Args:
        instance_id: The world instance the lease authorizes writes to.
        branch_id: The branch/worldline the lease authorizes writes to.
        audit_ref: Deterministic provenance string recorded with the credential.

    Returns:
        A registered `CanonicalWriteLease`.
    """
    return _mint(
        CanonicalWriteLease(
            instance_id=instance_id,
            branch_id=branch_id,
            issued_at_ms=time.time_ns() // _MS_PER_SECOND,
            audit_ref=audit_ref,
        )
    )


def require_canonical_write_lease(
    value: object,
    *,
    instance_id: WorldInstanceId | None = None,
    branch_id: BranchId | None = None,
) -> CanonicalWriteLease:
    """Return `value` when it authorizes the requested target, else reject it.

    A value is accepted only when it is a lease minted by the authority (brand
    check) and, for every scope dimension supplied by the caller, it was minted
    for that exact `instance_id`/`branch_id`. A lease minted for one worldline
    therefore never authorizes a write to another (the cross-worldline denial).

    Args:
        value: The candidate credential; `None` is always rejected.
        instance_id: Expected instance scope, or `None` to skip that dimension
            (used by rows that carry no instance, e.g. the lineage graph).
        branch_id: Expected branch scope, or `None` to skip that dimension.

    Raises:
        CanonicalWriteRejected: `value` is not an issued lease, or it was minted
            for a different instance and/or branch.
    """
    if not isinstance(value, CanonicalWriteLease) or not _is_issued(value):
        raise CanonicalWriteRejected(
            "canonical write requires an issued lease; refusing an un-minted or "
            "look-alike credential"
        )
    if instance_id is not None and value.instance_id != instance_id:
        raise CanonicalWriteRejected(
            f"lease issued for instance {value.instance_id.value!r} cannot write instance "
            f"{instance_id.value!r}"
        )
    if branch_id is not None and value.branch_id != branch_id:
        raise CanonicalWriteRejected(
            f"lease issued for branch {value.branch_id.value!r} cannot write branch "
            f"{branch_id.value!r}"
        )
    return value
