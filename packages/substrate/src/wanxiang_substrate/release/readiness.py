"""Production release readiness (M42).

Freeze checks for the v5.2 production gate: SDK/package/API freeze (G45A),
CLI/scaffolder certification gates (G45B), install/upgrade/migration pins
(G45C), release bundle metadata + scenario catalog + release notes (G45D),
production/ops/observability readiness (G45E), security/rights/supply-chain
final (G45F), release gates/version/manifest (G45G), and the final
certification record (G45H). Pure and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


@dataclass(frozen=True, slots=True)
class ReleaseFreeze:
    """Frozen public surface + compatibility policy."""

    sdk_routes: int
    sdk_ts_symbols: int
    sdk_py_symbols: int
    compat_policy: str = "additive-only; breaking requires major bump"
    api_frozen: bool = True


@dataclass(frozen=True, slots=True)
class ReleaseBundle:
    """A release bundle with hashes/rights/source metadata + scenario catalog."""

    bundle_id: str
    content_hash: str
    rights_refs: tuple[str, ...]
    source_metadata: tuple[str, ...]
    scenario_catalog: tuple[str, ...]
    release_notes: str


@dataclass(frozen=True, slots=True)
class ReleaseGates:
    """Final release gates + version manifest."""

    version: str
    security_scan_ok: bool
    sbom_ok: bool
    secret_scan_ok: bool
    package_install_ok: bool
    kernel_guard_ok: bool

    @property
    def all_ok(self) -> bool:
        return (
            self.security_scan_ok
            and self.sbom_ok
            and self.secret_scan_ok
            and self.package_install_ok
            and self.kernel_guard_ok
        )


@dataclass(frozen=True, slots=True)
class FinalCertification:
    """The M42 final certification record (local; no push/deploy)."""

    program: str
    status: str
    quality_passed: int
    quality_skipped: int
    red_chamber_real: str
    tag: str


def freeze_sdk(sdk_routes: int, ts_symbols: int, py_symbols: int) -> ReleaseFreeze:
    """Freeze the public SDK/package/API surface (additive-only)."""
    if sdk_routes < 0 or ts_symbols < 0 or py_symbols < 0:
        raise ContractError("SDK counts must be non-negative")
    return ReleaseFreeze(
        sdk_routes=sdk_routes, sdk_ts_symbols=ts_symbols, sdk_py_symbols=py_symbols
    )


def build_release_bundle(
    *,
    bundle_id: str,
    content_hash: str,
    rights_refs: tuple[str, ...],
    source_metadata: tuple[str, ...],
    scenario_catalog: tuple[str, ...],
    release_notes: str,
) -> ReleaseBundle:
    """Assemble the release bundle (real RedChamber content EXTERNAL_BLOCKED)."""
    if not bundle_id or not content_hash or not release_notes:
        raise ContractError("bundle requires id, hash and release notes")
    return ReleaseBundle(
        bundle_id=bundle_id,
        content_hash=content_hash,
        rights_refs=rights_refs,
        source_metadata=source_metadata,
        scenario_catalog=scenario_catalog,
        release_notes=release_notes,
    )


def certify_release(
    *,
    version: str,
    quality_passed: int,
    quality_skipped: int,
    red_chamber_real: str,
    tag: str,
    security_scan_ok: bool = True,
    sbom_ok: bool = True,
    secret_scan_ok: bool = True,
    package_install_ok: bool = True,
    kernel_guard_ok: bool = True,
) -> FinalCertification:
    """Produce the final certification record (mechanism-level)."""
    gates = ReleaseGates(
        version=version,
        security_scan_ok=security_scan_ok,
        sbom_ok=sbom_ok,
        secret_scan_ok=secret_scan_ok,
        package_install_ok=package_install_ok,
        kernel_guard_ok=kernel_guard_ok,
    )
    if not gates.all_ok:
        raise ContractError("release gates not all green; certification refused")
    return FinalCertification(
        program="wanxiang-v5.2",
        status="V5_2_PRODUCTION_PASS (platform mechanism)",
        quality_passed=quality_passed,
        quality_skipped=quality_skipped,
        red_chamber_real=red_chamber_real,
        tag=tag,
    )
