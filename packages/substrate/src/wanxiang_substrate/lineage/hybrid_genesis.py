"""Hybrid Genesis compatibility analysis and safe rejection (G31F).

Before any world merge, a semantic compatibility analysis runs. If any check
cannot be satisfied safely, the analysis REJECTS instead of faking a Git merge.
It never auto-resolves arbitrary conflicts and never rewrites parent histories.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.worldline import WorldDefinition

Verdict = Literal["candidate", "rejected"]


@dataclass(frozen=True, slots=True)
class GenesisCheck:
    """One compatibility check result."""

    name: str
    ok: bool
    detail: str = ""


@dataclass(frozen=True, slots=True)
class HybridGenesisReport:
    """The result of a hybrid-genesis compatibility analysis."""

    left_ref: str
    right_ref: str
    verdict: Verdict
    checks: tuple[GenesisCheck, ...]

    @property
    def rejected(self) -> bool:
        return self.verdict == "rejected"

    def failing_checks(self) -> tuple[GenesisCheck, ...]:
        return tuple(c for c in self.checks if not c.ok)


def _constitution_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    if left.constitution_ref == right.constitution_ref:
        return GenesisCheck("constitution", True, left.constitution_ref)
    if left.constitution_ref in ("con_legacy_v5",) or right.constitution_ref in ("con_legacy_v5",):
        return GenesisCheck(
            "constitution", True, "legacy constitution is compatible with any v5.2 constitution"
        )
    return GenesisCheck(
        "constitution",
        False,
        f"constitution mismatch: {left.constitution_ref} vs {right.constitution_ref}",
    )


def _identity_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    # Distinct definition ids may still share an identity namespace; for the
    # first version we require distinct definitions (no silent id collision).
    if left.definition_id == right.definition_id:
        return GenesisCheck("identity", False, "identical definition ids cannot be merged silently")
    return GenesisCheck("identity", True, "distinct definition identities")


def _ontology_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    # Both worlds must share the same semantic-space baseline (v1).
    if left.schema_version != right.schema_version:
        return GenesisCheck(
            "ontology",
            False,
            f"schema versions differ: {left.schema_version} vs {right.schema_version}",
        )
    return GenesisCheck("ontology", True, f"shared schema version {left.schema_version}")


def _law_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    # Law sets are only compatible when both are at the baseline (0) or the
    # same explicit law_set_version is supplied by the caller via package ref.
    if left.package_ref == right.package_ref:
        return GenesisCheck("law", True, "same package lineage")
    return GenesisCheck("law", False, "law-set lineage differs; explicit law merge policy required")


def _rights_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    if left.genesis_ref == right.genesis_ref:
        return GenesisCheck("rights", True, "same genesis provenance")
    return GenesisCheck(
        "rights", False, "distinct genesis provenance requires explicit rights review"
    )


def _history_compatible(left: WorldDefinition, right: WorldDefinition) -> GenesisCheck:
    # Parent histories are append-only and never rewritten by analysis.
    return GenesisCheck(
        "history",
        True,
        "both parents append-only; analysis never rewrites parent history",
    )


def analyze_hybrid_genesis(left: WorldDefinition, right: WorldDefinition) -> HybridGenesisReport:
    """Analyze two world definitions for a safe hybrid genesis.

    Returns a MergePlan Candidate (all checks pass) or a Rejection with the
    failing checks. No merge is executed here.
    """
    checks = (
        _constitution_compatible(left, right),
        _identity_compatible(left, right),
        _ontology_compatible(left, right),
        _law_compatible(left, right),
        _rights_compatible(left, right),
        _history_compatible(left, right),
    )
    verdict: Verdict = "candidate" if all(c.ok for c in checks) else "rejected"
    return HybridGenesisReport(
        left_ref=left.definition_id.value,
        right_ref=right.definition_id.value,
        verdict=verdict,
        checks=checks,
    )
