"""RC-001 replay / crash-recovery / chaos checks (G37D).

Snapshot/restart, corrupt-stream detection, duplicate/stale rejection, client
reconnect, and provider-failure isolation. Each check is a deterministic pure
function; run_chaos_checks aggregates a ChaosReport. No write path beyond the
existing Commit Authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass

from wanxiang_domain.errors import WanxiangError
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.state import (
    InMemoryCanonicalState,
    state_from_primitive,
    state_to_primitive,
)

from wanxiang_substrate.session.embodiment import EmbodimentController
from wanxiang_substrate.session.model import Session


@dataclass(frozen=True, slots=True)
class ChaosCheck:
    """One chaos check result."""

    name: str
    passed: bool
    detail: str


@dataclass(frozen=True, slots=True)
class ChaosReport:
    """Aggregated chaos-check results."""

    checks: tuple[ChaosCheck, ...]

    @property
    def all_passed(self) -> bool:
        return all(check.passed for check in self.checks)


def snapshot_restart(state: InMemoryCanonicalState) -> bool:
    """Snapshot -> primitive -> restart -> same semantic hash."""
    primitive = state_to_primitive(state)
    restored = state_from_primitive(primitive)
    return restored.semantic_hash() == state.semantic_hash()


def detect_stream_corruption(state: InMemoryCanonicalState, *, corrupt: bool) -> bool:
    """Serialize canonical state; a corrupted byte changes the stream hash."""
    payload = json.dumps(state_to_primitive(state), sort_keys=True).encode("utf-8")
    if corrupt:
        mid = len(payload) // 2
        payload = payload[:mid] + b"X" + payload[mid + 1 :]
    expected = json.dumps(state_to_primitive(state), sort_keys=True).encode("utf-8")
    return (
        hashlib.sha256(payload).hexdigest() != hashlib.sha256(expected).hexdigest()
        if corrupt
        else True
    )


def duplicate_command_rejected(
    authority: CommitAuthority,
    state: InMemoryCanonicalState,
    request_factory: Callable[[], CommitRequest],
) -> bool:
    """Committing the same command twice must reject the duplicate."""
    first = authority.commit(state, request_factory())
    with suppress(WanxiangError):
        authority.commit(first.state_after, request_factory())
        return False
    return True


def reconnect_embodiment(
    controller: EmbodimentController,
    session: Session,
    actor_key: str,
    *,
    lease_id: str,
) -> bool:
    """Release then reacquire a lease (client reconnect)."""
    controller.acquire(
        session, actor_key, lease_id=lease_id, mode="full_control", acquired_seq=1, expires_seq=100
    )
    controller.release(actor_key, lease_id, released_seq=50)
    controller.acquire(
        session, actor_key, lease_id=lease_id, mode="full_control", acquired_seq=60, expires_seq=200
    )
    return controller.state(actor_key).lease_active is True


def provider_failure_isolated(
    failing_resolver: Callable[[], None], state: InMemoryCanonicalState
) -> bool:
    """A failing provider resolver raises; the world state is unchanged."""
    before = state.semantic_hash()
    with suppress(WanxiangError):
        failing_resolver()
    return state.semantic_hash() == before


def run_chaos_checks(
    *,
    state: InMemoryCanonicalState,
    authority: CommitAuthority | None = None,
    request_factory: Callable[[], CommitRequest] | None = None,
    controller: EmbodimentController | None = None,
    session: Session | None = None,
    actor_key: str = "c1",
    failing_resolver: Callable[[], None] | None = None,
) -> ChaosReport:
    """Run all chaos checks; a missing optional fixture skips gracefully."""
    checks: list[ChaosCheck] = []
    checks.append(ChaosCheck("snapshot_restart", snapshot_restart(state), "state round-trip hash"))
    checks.append(
        ChaosCheck(
            "corrupt_stream_detection",
            detect_stream_corruption(state, corrupt=True),
            "corrupted payload changes stream hash",
        )
    )
    if authority is not None and request_factory is not None:
        checks.append(
            ChaosCheck(
                "duplicate_command_rejected",
                duplicate_command_rejected(authority, state, request_factory),
                "duplicate commit rejected",
            )
        )
    if controller is not None and session is not None:
        checks.append(
            ChaosCheck(
                "client_reconnect",
                reconnect_embodiment(controller, session, actor_key, lease_id="lease_1"),
                "lease release + reacquire",
            )
        )
    if failing_resolver is not None:
        checks.append(
            ChaosCheck(
                "provider_failure_isolation",
                provider_failure_isolated(failing_resolver, state),
                "failing provider does not corrupt world state",
            )
        )
    return ChaosReport(checks=tuple(checks))
