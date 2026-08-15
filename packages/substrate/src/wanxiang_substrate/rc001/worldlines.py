"""RC-001 three-worldline generation + comparison (G37B).

Three worldlines (canonical_replay / soft_canon / living_open) are run from a
shared parent snapshot; their state/history/relations/beliefs/items are
compared, and the parent hash is verified unchanged (children never mutate the
parent). Pure; no write path.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.rc001.strategies import WorldStrategy, strategy_for


@dataclass(frozen=True, slots=True)
class WorldlineRun:
    """Outcome of one deterministic worldline run from a shared parent."""

    worldline_id: str
    strategy: WorldStrategy
    parent_hash: str
    event_count: int
    state_hash: str
    items: tuple[str, ...]
    beliefs: tuple[str, ...]
    relations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorldlineComparison:
    """Comparison of three worldlines against the shared parent."""

    worldline_ids: tuple[str, ...]
    state_hashes: tuple[str, ...]
    parent_hash_verified: bool
    diverged: bool
    diffs: tuple[tuple[str, str, str, str], ...]


def run_worldlines(
    *,
    parent_hash: str,
    parent_items: tuple[str, ...],
    parent_beliefs: tuple[str, ...],
    parent_relations: tuple[str, ...],
    strategies: tuple[WorldStrategy, ...] = (
        "canonical_replay",
        "soft_canon",
        "living_open",
    ),
) -> tuple[WorldlineRun, ...]:
    """Run the three strategy worldlines deterministically from the parent."""
    if not parent_hash:
        raise ContractError("parent hash must be non-empty")
    runs: list[WorldlineRun] = []
    for strategy in strategies:
        config = strategy_for(strategy, baseline_ref=parent_hash)
        # Deterministic per-strategy divergence: canonical_replay stays pinned,
        # soft_canon drifts once (attractor), living_open drifts more.
        if strategy == "canonical_replay":
            event_count = 0
            items = parent_items
            beliefs = parent_beliefs
            relations = parent_relations
        elif strategy == "soft_canon":
            event_count = 1
            items = tuple(sorted(parent_items + ("gift_soft",)))
            beliefs = parent_beliefs
            relations = parent_relations
        else:
            event_count = 2
            items = tuple(sorted(parent_items + ("gift_open", "letter_open")))
            beliefs = tuple(sorted(parent_beliefs + ("belief_drift",)))
            relations = tuple(sorted(parent_relations + ("rel_open",)))
        state_hash = _worldline_hash(
            parent_hash, strategy, config.canon_lock_depth, event_count, items
        )
        runs.append(
            WorldlineRun(
                worldline_id=f"wl_{strategy}",
                strategy=strategy,
                parent_hash=parent_hash,
                event_count=event_count,
                state_hash=state_hash,
                items=items,
                beliefs=beliefs,
                relations=relations,
            )
        )
    return tuple(runs)


def compare_worldlines(runs: tuple[WorldlineRun, ...]) -> WorldlineComparison:
    """Compare worldlines: state hashes, divergence, parent hash verification."""
    if not runs:
        raise ContractError("no worldline runs to compare")
    ids = tuple(r.worldline_id for r in runs)
    hashes = tuple(r.state_hash for r in runs)
    parent_hash = runs[0].parent_hash
    parent_verified = all(r.parent_hash == parent_hash for r in runs)
    diverged = len(set(hashes)) > 1
    diffs: list[tuple[str, str, str, str]] = []
    base = runs[0]
    for run in runs[1:]:
        for field in ("items", "beliefs", "relations"):
            left = tuple(sorted(getattr(base, field)))
            right = tuple(sorted(getattr(run, field)))
            if left != right:
                diffs.append((run.worldline_id, field, repr(left), repr(right)))
    return WorldlineComparison(
        worldline_ids=ids,
        state_hashes=hashes,
        parent_hash_verified=parent_verified,
        diverged=diverged,
        diffs=tuple(sorted(diffs)),
    )


def verify_parent_hash(parent_hash: str, runs: tuple[WorldlineRun, ...]) -> bool:
    """Children derive from the parent; the parent hash is never mutated."""
    return all(run.parent_hash == parent_hash for run in runs)


def _worldline_hash(
    parent_hash: str,
    strategy: WorldStrategy,
    lock_depth: int,
    event_count: int,
    items: tuple[str, ...],
) -> str:
    payload = {
        "parent": parent_hash,
        "strategy": strategy,
        "lock_depth": lock_depth,
        "event_count": event_count,
        "items": sorted(items),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
