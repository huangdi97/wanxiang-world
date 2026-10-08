"""Read-only lookup helpers for durable world-instance metadata."""

from __future__ import annotations

from wanxiang_domain.errors import PersistenceError, WanxiangError
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_application.ports import PersistenceBundle


def find_root_branch(
    persistence: PersistenceBundle, instance_id: WorldInstanceId
) -> BranchId | None:
    """Find the one durable root branch for an existing instance."""
    try:
        persistence.instances.get(instance_id)
    except (WanxiangError, KeyError):
        return None
    roots = tuple(
        branch
        for branch in persistence.branches.list(instance_id)
        if branch.ancestry.parent_branch_id is None
    )
    if len(roots) != 1:
        raise PersistenceError(
            f"world instance {instance_id.value} does not have exactly one root branch"
        )
    return roots[0].branch_id
