"""Verified capability registry: admission, versioning and revocation.

INVARIANT: only a package with a full-pass C3 verification report AND a matching
verification digest is admitted. Admission never overwrites: a new version
coexists with the previous one, and revocation records intent without deleting
history. The registry is proposal-side bookkeeping and holds no path to canonical
world state.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_foundry.errors import RegistryError
from wanxiang_foundry.levels import PromotionLevel
from wanxiang_foundry.package import CapabilityPackage
from wanxiang_foundry.verification import VerificationReport


@dataclass(frozen=True, slots=True)
class PromotionGrant:
    """The recorded promotion level and the evidence digest that granted it.

    Attributes:
        level: The promotion level recorded at admission.
        evidence_digest: The verification evidence digest that granted it.
    """

    level: PromotionLevel
    evidence_digest: str


@dataclass(frozen=True, slots=True)
class _AdmittedEntry:
    """Internal per-(capability, version) record; never exposed directly."""

    package: CapabilityPackage
    promotion: PromotionGrant
    status: str
    status_reason: str | None


class VerifiedCapabilityRegistry:
    """An append-only, versioned registry of admitted capability packages."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], _AdmittedEntry] = {}
        self._order: list[tuple[str, str]] = []
        self._preferred: dict[str, str] = {}
        self._lifecycle: list[tuple[str, str, str, str]] = []

    def admit(self, package: CapabilityPackage, report: VerificationReport) -> None:
        """Admit a package only with a matching full-pass C3 report.

        Args:
            package: The verified package to admit.
            report: The verification report that must grant C3.

        Raises:
            RegistryError: If the report does not grant C3, the package's
                verification_digest does not match the report, or this exact
                id+version is already admitted. On refusal nothing changes.
        """
        if not report.grants_c3:
            raise RegistryError(
                f"package {package.capability_id}@{package.version} not admitted: "
                "report does not grant C3 with every case kind passed"
            )
        if package.verification_digest != report.evidence_digest:
            raise RegistryError(
                f"package {package.capability_id}@{package.version} not admitted: "
                "verification_digest does not match the report evidence digest"
            )
        if set(package.verification_case_ids) != set(report.passed_case_ids):
            raise RegistryError(
                f"package {package.capability_id}@{package.version} not admitted: "
                "verification_case_ids do not match the report's passed cases"
            )
        key = (package.capability_id, package.version)
        if key in self._entries:
            raise RegistryError(
                f"capability {package.capability_id}@{package.version} already admitted"
            )
        self._entries[key] = _AdmittedEntry(
            package=package,
            promotion=PromotionGrant(
                level=PromotionLevel.C3_VERIFIED, evidence_digest=report.evidence_digest
            ),
            status="ACTIVE",
            status_reason=None,
        )
        self._order.append(key)
        self._preferred[package.capability_id] = package.version
        self._lifecycle.append(
            (package.capability_id, package.version, "ADMIT", report.evidence_digest)
        )

    def get(self, capability_id: str, version: str) -> CapabilityPackage | None:
        """Return the admitted package for id+version, or None when absent."""
        entry = self._entries.get((capability_id, version))
        return None if entry is None else entry.package

    def versions(self, capability_id: str) -> tuple[str, ...]:
        """Return admitted versions for capability_id in admission order."""
        return tuple(version for (cid, version) in self._order if cid == capability_id)

    def active(self, capability_id: str) -> CapabilityPackage | None:
        """Return the explicitly selected, invocable package for capability_id."""
        preferred = self._preferred.get(capability_id)
        if preferred is not None and self.is_invocable(capability_id, preferred):
            return self._entries[(capability_id, preferred)].package
        for key in reversed(self._order):
            if key[0] != capability_id:
                continue
            entry = self._entries[key]
            if entry.status == "ACTIVE":
                return entry.package
        return None

    def _transition(self, capability_id: str, version: str, status: str, reason: str) -> None:
        key = (capability_id, version)
        entry = self._entries.get(key)
        if entry is None:
            raise RegistryError(f"cannot change unregistered capability {capability_id}@{version}")
        if not reason.strip():
            raise RegistryError("lifecycle reason must be a non-empty string")
        if status not in {"ACTIVE", "SUSPENDED", "DEPRECATED", "REVOKED"}:
            raise RegistryError(f"unknown capability lifecycle status {status!r}")
        if entry.status == "REVOKED" and status != "REVOKED":
            raise RegistryError(
                f"revoked capability {capability_id}@{version} cannot be reactivated"
            )
        self._entries[key] = _AdmittedEntry(
            package=entry.package,
            promotion=entry.promotion,
            status=status,
            status_reason=reason,
        )
        self._lifecycle.append((capability_id, version, status, reason))
        if status in {"SUSPENDED", "DEPRECATED", "REVOKED"} and self._preferred.get(capability_id) == version:
            self._preferred.pop(capability_id, None)

    def suspend(self, capability_id: str, version: str, reason: str) -> None:
        """Temporarily make one version non-invocable without deleting evidence."""
        self._transition(capability_id, version, "SUSPENDED", reason)

    def deprecate(self, capability_id: str, version: str, reason: str) -> None:
        """Mark a version deprecated; direct pinned invocation remains possible."""
        self._transition(capability_id, version, "DEPRECATED", reason)

    def restore(self, capability_id: str, version: str, reason: str) -> None:
        """Restore a suspended/deprecated version; a revoked version stays terminal."""
        self._transition(capability_id, version, "ACTIVE", reason)

    def revoke(self, capability_id: str, version: str, reason: str) -> None:
        """Permanently revoke a version while retaining package and evidence."""
        self._transition(capability_id, version, "REVOKED", reason)

    def rollback(self, capability_id: str, to_version: str, reason: str) -> None:
        """Select an older invocable version for future calls without rewriting history."""
        if not reason.strip():
            raise RegistryError("rollback reason must be a non-empty string")
        if not self.is_invocable(capability_id, to_version):
            raise RegistryError(
                f"cannot rollback to non-invocable capability {capability_id}@{to_version}"
            )
        self._preferred[capability_id] = to_version
        self._lifecycle.append((capability_id, to_version, "ROLLBACK", reason))

    def status(self, capability_id: str, version: str) -> str | None:
        """Return ACTIVE/SUSPENDED/DEPRECATED/REVOKED, or None when absent."""
        entry = self._entries.get((capability_id, version))
        return None if entry is None else entry.status

    def lifecycle(self, capability_id: str) -> tuple[tuple[str, str, str, str], ...]:
        """Return append-only lifecycle records for one capability."""
        return tuple(item for item in self._lifecycle if item[0] == capability_id)

    def promotions(self, capability_id: str, version: str) -> PromotionGrant | None:
        """Return the recorded promotion grant for id+version, or None."""
        entry = self._entries.get((capability_id, version))
        return None if entry is None else entry.promotion

    def is_invocable(self, capability_id: str, version: str) -> bool:
        """Return True for admitted ACTIVE/DEPRECATED versions only."""
        entry = self._entries.get((capability_id, version))
        return entry is not None and entry.status in {"ACTIVE", "DEPRECATED"}
