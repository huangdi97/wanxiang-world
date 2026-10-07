"""Runtime Control Ledger: auditable runtime/provider configuration history.

Runtime-control records are never World Commits. They explain which provider,
profile, permission, parameter or migration was active for a worldline/revision
without entering or rewriting canonical World history.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Literal

RuntimeControlStatus = Literal["applied", "failed", "rolled_back"]
RuntimeControlOperation = Literal[
    "activate",
    "deactivate",
    "install",
    "uninstall",
    "reload",
    "rollback",
    "migrate",
    "profile_patch",
    "permission_update",
    "model_switch",
    "rule_update",
    "simulation_update",
]

_REMOVING_OPERATIONS = {"deactivate", "uninstall"}


@dataclass(frozen=True, slots=True)
class RuntimeControlTransaction:
    """One typed, append-only runtime-control record."""

    transaction_id: str
    operation: RuntimeControlOperation
    provider_id: str
    capability_name: str
    version: str
    rationale: str
    created_at: str
    status: RuntimeControlStatus = "applied"
    runtime_revision: int = 0
    worldline_id: str = ""
    effective_world_revision: int | None = None
    world_event_ref: str = ""
    profile_ref: str = ""
    patch_ref: str = ""
    permissions: tuple[str, ...] = ()
    parameters: tuple[tuple[str, str], ...] = ()
    migration_ref: str = ""
    artifact_hash: str = ""
    execution_trace_ref: str = ""
    input_artifact_refs: tuple[str, ...] = ()
    output_artifact_refs: tuple[str, ...] = ()
    usage: tuple[tuple[str, str], ...] = ()
    resulting_proposal_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.transaction_id or not self.provider_id or not self.capability_name:
            raise ValueError("runtime control transaction requires ids and capability name")
        if not self.version or not self.created_at:
            raise ValueError("runtime control transaction requires version and created_at")
        if self.runtime_revision < 0:
            raise ValueError("runtime_revision must not be negative")
        if self.effective_world_revision is not None and self.effective_world_revision < 0:
            raise ValueError("effective_world_revision must not be negative")
        if len(set(self.permissions)) != len(self.permissions):
            raise ValueError("permissions must not contain duplicates")
        keys = [key for key, _value in self.parameters]
        if len(set(keys)) != len(keys) or any(not key for key in keys):
            raise ValueError("parameters must have unique non-empty keys")
        sensitive_terms = ("secret", "token", "password", "api_key", "private_key")
        if any(any(term in key.lower() for term in sensitive_terms) for key in keys):
            raise ValueError("runtime control parameters must not contain secret-bearing keys")
        usage_keys = [key for key, _value in self.usage]
        if len(set(usage_keys)) != len(usage_keys) or any(not key for key in usage_keys):
            raise ValueError("usage must have unique non-empty keys")


class RuntimeControlLedger:
    """Append-only runtime configuration history with optional JSONL persistence."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path
        self._entries: list[RuntimeControlTransaction] = []
        if path is not None and path.exists():
            self._load(path)

    def record(self, transaction: RuntimeControlTransaction) -> RuntimeControlTransaction:
        if any(item.transaction_id == transaction.transaction_id for item in self._entries):
            raise ValueError(f"duplicate runtime transaction id {transaction.transaction_id!r}")
        expected_revision = len(self._entries) + 1
        if transaction.runtime_revision not in (0, expected_revision):
            raise ValueError(
                f"runtime revision must be 0 or next revision {expected_revision}, "
                f"got {transaction.runtime_revision}"
            )
        recorded = replace(transaction, runtime_revision=expected_revision)
        self._entries.append(recorded)
        self._append(recorded)
        return recorded

    def entries(self) -> tuple[RuntimeControlTransaction, ...]:
        return tuple(self._entries)

    def active_at(
        self,
        *,
        worldline_id: str,
        world_revision: int,
    ) -> dict[str, RuntimeControlTransaction]:
        """Return active capability configuration at one World revision."""
        if world_revision < 0:
            raise ValueError("world_revision must not be negative")
        active: dict[str, RuntimeControlTransaction] = {}
        for item in self._entries:
            if item.status != "applied":
                continue
            if item.worldline_id and item.worldline_id != worldline_id:
                continue
            effective = item.effective_world_revision
            if effective is not None and effective > world_revision:
                continue
            if item.operation in _REMOVING_OPERATIONS:
                active.pop(item.capability_name, None)
            else:
                active[item.capability_name] = item
        return active

    def configuration_for_event(
        self,
        world_event_ref: str,
    ) -> tuple[RuntimeControlTransaction, ...]:
        """Return applied records explicitly linked to a World event."""
        return tuple(
            item
            for item in self._entries
            if item.status == "applied" and item.world_event_ref == world_event_ref
        )

    def _append(self, item: RuntimeControlTransaction) -> None:
        if self._path is None:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(item), sort_keys=True, separators=(",", ":")))
            handle.write("\n")

    def _load(self, path: Path) -> None:
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            value = json.loads(raw)
            for name in (
                "permissions",
                "input_artifact_refs",
                "output_artifact_refs",
                "resulting_proposal_refs",
            ):
                value[name] = tuple(value.get(name, ()))
            value["parameters"] = tuple(tuple(pair) for pair in value.get("parameters", ()))
            value["usage"] = tuple(tuple(pair) for pair in value.get("usage", ()))
            item = RuntimeControlTransaction(**value)
            expected = len(self._entries) + 1
            if item.runtime_revision != expected:
                raise ValueError(
                    f"runtime control ledger revision gap at line {line_number}: "
                    f"expected {expected}, got {item.runtime_revision}"
                )
            self._entries.append(item)


__all__ = [
    "RuntimeControlLedger",
    "RuntimeControlOperation",
    "RuntimeControlStatus",
    "RuntimeControlTransaction",
]
