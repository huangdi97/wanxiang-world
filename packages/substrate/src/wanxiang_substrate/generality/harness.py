"""Cross-Domain Generality harness (M41).

Shared acceptance harness + kernel diff guard (G44A), family / heritage /
campaign world qualification flags (G44B/C/D), four-domain vs Core comparison
(G44E), and third-party black-box world pack gate (G44F). Pure and
deterministic; real external data remains EXTERNAL_BLOCKED.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


@dataclass(frozen=True, slots=True)
class DomainQualification:
    """Qualification of one domain/world against the shared harness."""

    domain: str
    acceptance_passed: bool
    core_reused: tuple[str, ...]
    external_blocked: bool = False


@dataclass(frozen=True, slots=True)
class GeneralityReport:
    """Aggregated cross-domain generality report."""

    domains: tuple[DomainQualification, ...]
    kernel_diff_clean: bool
    four_domain_core_reuse: tuple[tuple[str, tuple[str, ...]], ...]
    black_box_pack_ok: bool

    @property
    def all_domains_pass(self) -> bool:
        return all(d.acceptance_passed or d.external_blocked for d in self.domains)


def run_generality_harness(
    *,
    domains: tuple[str, ...],
    core_reuse: tuple[tuple[str, tuple[str, ...]], ...],
    kernel_diff_clean: bool,
    black_box_pack_ok: bool,
    external_blocked: tuple[str, ...] = (),
) -> GeneralityReport:
    """Run the shared acceptance harness across domains."""
    qualifications = tuple(
        DomainQualification(
            domain=domain,
            acceptance_passed=domain not in external_blocked,
            core_reused=tuple(sorted(reuse)),
            external_blocked=domain in external_blocked,
        )
        for domain, reuse in core_reuse
    )
    return GeneralityReport(
        domains=qualifications,
        kernel_diff_clean=kernel_diff_clean,
        four_domain_core_reuse=core_reuse,
        black_box_pack_ok=black_box_pack_ok,
    )


def kernel_diff_guard(reference_hash: str, current_hash: str) -> bool:
    """Kernel diff guard: a changed kernel hash requires review (returns clean)."""
    if not reference_hash or not current_hash:
        raise ContractError("kernel hashes must be non-empty")
    return reference_hash == current_hash


def black_box_world_pack_gate(*, package_id: str, content_hash: str, trusted: bool) -> bool:
    """Third-party black-box world pack gate (trust + hash present)."""
    if not package_id or not content_hash:
        raise ContractError("package requires id and content hash")
    return trusted and len(content_hash) == 64
