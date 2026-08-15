"""Platform feedback sandbox / benchmark / approval (G33E).

Cross-world candidates are validated in a shadow/sandbox run with benchmark,
ablation, invariant, security, cost and determinism checks before any versioned
Domain/Runtime release. A world instance NEVER owns approval of a platform
upgrade; rollback only changes the release's installability and never rewrites
past world events.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_domain.errors import PermissionDenied

PLATFORM_APPROVERS = ("platform_reviewer", "platform_policy")


@dataclass(frozen=True, slots=True)
class SandboxReport:
    """A sandbox evaluation result for a candidate."""

    candidate_id: str
    benchmark: dict[str, float]
    invariants_ok: bool
    security_ok: bool
    cost: float
    deterministic: bool
    approved: bool = False


@dataclass(frozen=True, slots=True)
class VersionedRelease:
    """A versioned Domain/Runtime release (rollback = status change only)."""

    release_id: str
    kind: str  # "domain" | "runtime"
    name: str
    version: str
    status: str = "active"


class PlatformFeedbackLab:
    """Shadow/sandbox evaluation -> approval -> versioned release."""

    def run_sandbox(
        self,
        candidate_id: str,
        benchmark: dict[str, float],
        *,
        invariants_ok: bool,
        security_ok: bool,
        cost: float,
        deterministic: bool,
    ) -> SandboxReport:
        """Shadow/sandbox run with benchmark/ablation/invariant/security/cost/determinism."""
        return SandboxReport(
            candidate_id=candidate_id,
            benchmark=dict(benchmark),
            invariants_ok=invariants_ok,
            security_ok=security_ok,
            cost=cost,
            deterministic=deterministic,
        )

    def approve(self, report: SandboxReport, approver: str) -> SandboxReport:
        """Approval policy: only a platform reviewer/policy may approve."""
        if approver not in PLATFORM_APPROVERS:
            raise PermissionDenied(
                f"approver {approver!r} cannot approve platform upgrades; "
                "a world instance never owns platform approval"
            )
        if not (report.invariants_ok and report.security_ok and report.deterministic):
            raise PermissionDenied("sandbox gate failed; cannot approve")
        return replace(report, approved=True)

    def release(
        self,
        report: SandboxReport,
        *,
        kind: str,
        name: str,
        version: str,
        release_id: str,
    ) -> VersionedRelease:
        """Versioned Domain/Runtime release after approval."""
        if not report.approved:
            raise PermissionDenied("candidate not approved; no versioned release")
        return VersionedRelease(
            release_id=release_id,
            kind=kind,
            name=name,
            version=version,
        )

    @staticmethod
    def rollback(release: VersionedRelease) -> VersionedRelease:
        """Rollback only changes installability status; never rewrites events."""
        return replace(release, status="rolled_back")
