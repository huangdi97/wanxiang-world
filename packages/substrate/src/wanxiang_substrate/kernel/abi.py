"""Kernel v1 ABI manifest (G38B).

Enumerates the stable kernel v1 surface (types/schemas/versions) and produces
deterministic ABI golden hashes. Kernel v1 is frozen after M35: any change to
these entries requires a kernel-change guard review (G38C). No domain names,
no LLM/provider coupling.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

KERNEL_V1_VERSION = 1

# Stable kernel v1 ABI entries: (kind, name, version_or_ref).
KERNEL_V1_ABI: tuple[tuple[str, str, str], ...] = (
    ("id", "WorldInstanceId", "1"),
    ("id", "WorldDefinitionId", "1"),
    ("id", "WorldlineId", "1"),
    ("id", "BranchId", "1"),
    ("id", "EventId", "1"),
    ("id", "CommandId", "1"),
    ("id", "EntityId", "1"),
    ("version", "SchemaVersion", "1"),
    ("version", "RuntimeVersion", "1"),
    ("commit", "WorldCommitKind", "state|ontology|law"),
    ("event", "CommittedEvent", "1"),
    ("snapshot", "InMemoryCanonicalState", "1"),
    ("branch", "BranchMetadata", "1"),
    ("lineage", "LineageGraph", "1"),
    ("worldline", "WorldDefinition", "1"),
    ("constitution", "ConstitutionManifest", "1"),
    ("replay", "ReplayEngine", "1"),
    ("authority", "CommitAuthority", "1"),
    ("ledger", "CompletionLedger", "1"),
    ("promotion", "validate_promotion", "L0-L8"),
)


@dataclass(frozen=True, slots=True)
class KernelAbiManifest:
    """Frozen kernel v1 ABI manifest with a deterministic golden hash."""

    version: int
    entries: tuple[tuple[str, str, str], ...]
    golden_hash: str

    def entry(self, name: str) -> tuple[str, str, str] | None:
        for entry in self.entries:
            if entry[1] == name:
                return entry
        return None


def abi_manifest() -> KernelAbiManifest:
    """Build the kernel v1 ABI manifest (deterministic)."""
    payload = {"version": KERNEL_V1_VERSION, "entries": list(KERNEL_V1_ABI)}
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return KernelAbiManifest(version=KERNEL_V1_VERSION, entries=KERNEL_V1_ABI, golden_hash=digest)


def abi_golden() -> dict[str, Any]:
    """JSON-serializable golden snapshot for the ABI baseline."""
    manifest = abi_manifest()
    return {
        "kernel_v1_version": manifest.version,
        "entries": [list(e) for e in manifest.entries],
        "golden_hash": manifest.golden_hash,
    }


def verify_abi_golden(reference: dict[str, Any]) -> bool:
    """Golden hash is stable and matches the current manifest."""
    current = abi_golden()
    return current["golden_hash"] == reference.get("golden_hash") and current == reference
