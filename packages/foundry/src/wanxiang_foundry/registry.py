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
    revoked: bool
    revocation_reason: str | None


class VerifiedCapabilityRegistry:
    """An append-only, versioned registry of admitted capability packages."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], _AdmittedEntry] = {}
        self._order: list[tuple[str, str]] = []

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
            revoked=False,
            revocation_reason=None,
        )
        self._order.append(key)

    def get(self, capability_id: str, version: str) -> CapabilityPackage | None:
        """Return the admitted package for id+version, or None when absent."""
        entry = self._entries.get((capability_id, version))
        return None if entry is None else entry.package

    def versions(self, capability_id: str) -> tuple[str, ...]:
        """Return admitted versions for capability_id in admission order."""
        return tuple(version for (cid, version) in self._order if cid == capability_id)

    def active(self, capability_id: str) -> CapabilityPackage | None:
        """Return the latest admitted, non-revoked package for capability_id."""
        for key in reversed(self._order):
            if key[0] != capability_id:
                continue
            entry = self._entries[key]
            if not entry.revoked:
                return entry.package
        return None

    def revoke(self, capability_id: str, version: str, reason: str) -> None:
        """Record a revocation without deleting the admitted package.

        Args:
            capability_id: Capability id.
            version: Version to revoke.
            reason: Non-empty revocation reason.

        Raises:
            RegistryError: If the capability is not admitted, or reason is empty.
        """
        key = (capability_id, version)
        entry = self._entries.get(key)
        if entry is None:
            raise RegistryError(f"cannot revoke unregistered capability {capability_id}@{version}")
        if not reason.strip():
            raise RegistryError("revocation reason must be a non-empty string")
        self._entries[key] = _AdmittedEntry(
            package=entry.package,
            promotion=entry.promotion,
            revoked=True,
            revocation_reason=reason,
        )

    def promotions(self, capability_id: str, version: str) -> PromotionGrant | None:
        """Return the recorded promotion grant for id+version, or None."""
        entry = self._entries.get((capability_id, version))
        return None if entry is None else entry.promotion

    def is_invocable(self, capability_id: str, version: str) -> bool:
        """Return True only when the capability is admitted and not revoked."""
        entry = self._entries.get((capability_id, version))
        return entry is not None and not entry.revoked
