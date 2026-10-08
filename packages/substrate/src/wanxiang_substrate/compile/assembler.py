"""World package assembler + validation (G60B/G60C).

Assembles a WorldPackageDraft reusing the official PackageManifest schema
(world kind) with pinned draft revision, source versions, domains, evidence
coverage, rights, and unresolved-gap status. Validation separates preview
(ok with non-blocking gaps) from publish (requires no blocking gaps + rights).
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.compile.boundary import CompileOutcome
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.packages.model import (
    PackageKind,
    PackageManifest,
    SemanticVersion,
)


@dataclass(frozen=True, slots=True)
class WorldPackageDraft:
    """A compiled world package draft (reuses PackageManifest schema)."""

    package_id: str
    draft_id: str
    draft_revision: int
    manifest: PackageManifest
    source_versions: tuple[tuple[str, str], ...]
    domain_versions: tuple[tuple[str, str], ...]
    evidence_coverage: float
    unresolved_gaps: tuple[str, ...]
    rights_ok: bool
    for_preview: bool
    draft: WorldDraft

    def __post_init__(self) -> None:
        if not self.package_id or not self.draft_id:
            raise ContractError("package requires package and draft ids")
        if not (0.0 <= self.evidence_coverage <= 1.0):
            raise ContractError("evidence_coverage must be within [0,1]")
        if self.manifest.kind != "world":
            raise ContractError("world package draft must use the world manifest kind")
        if self.manifest.content_hash != self.manifest.compute_hash():
            raise ContractError("world package manifest hash is invalid")
        if len(dict(self.source_versions)) != len(self.source_versions):
            raise ContractError("world package source pins must not contain duplicates")
        if len(dict(self.domain_versions)) != len(self.domain_versions):
            raise ContractError("world package domain pins must not contain duplicates")


@dataclass(frozen=True, slots=True)
class PackageValidationResult:
    package_id: str
    preview_ok: bool
    publish_ok: bool
    reasons: tuple[str, ...]


class PackageAssembler:
    """Builds a WorldPackageDraft on the official PackageManifest schema."""

    def assemble(
        self,
        draft: WorldDraft,
        *,
        compile_outcome: CompileOutcome,
        domain_versions: tuple[tuple[str, str], ...],
        evidence_coverage: float,
        for_preview: bool,
    ) -> WorldPackageDraft:
        if not compile_outcome.ok:
            raise ContractError("cannot assemble a failed compiler outcome")
        if compile_outcome.draft_id != draft.draft_id:
            raise ContractError("compiler outcome targets a different draft")
        if compile_outcome.pinned_revision != draft.revision:
            raise ContractError("compiler outcome revision does not match the draft")
        if tuple(sorted(draft.source_refs)) != tuple(sorted(dict(draft.source_versions))):
            raise ContractError("draft source references and pins are inconsistent")
        if tuple(sorted(draft.source_versions)) != tuple(sorted(draft.source_versions)):
            raise ContractError("draft source pins must be deterministically ordered")
        if tuple(sorted(draft.selected_domains)) != tuple(
            sorted(domain_id for domain_id, _version in domain_versions)
        ):
            raise ContractError("domain pins do not match selected domains")
        manifest = PackageManifest(
            package_id=f"world:{draft.draft_id}",
            kind=cast_kind("world"),
            version=SemanticVersion(1, 0, 0),
            name=f"World {draft.draft_id}",
            dependencies=tuple(
                (domain_id, f"=={version}") for domain_id, version in domain_versions
            ),
            constitution_ref=draft.constitution_ref or None,
            genesis_ref=compile_outcome.draft_id,
        ).with_hash()
        return WorldPackageDraft(
            package_id=manifest.package_id,
            draft_id=draft.draft_id,
            draft_revision=compile_outcome.pinned_revision,
            manifest=manifest,
            source_versions=draft.source_versions,
            domain_versions=domain_versions,
            evidence_coverage=evidence_coverage,
            unresolved_gaps=draft.completion_items,
            rights_ok=not draft.unresolved_rights,
            for_preview=for_preview,
            draft=draft,
        )


def cast_kind(value: str) -> PackageKind:
    from typing import cast

    return cast(PackageKind, value)


class PackageValidator:
    """Preview vs publish gate over a WorldPackageDraft."""

    def validate(self, package: WorldPackageDraft) -> PackageValidationResult:
        reasons: list[str] = []
        if package.manifest.content_hash != package.manifest.compute_hash():
            reasons.append("manifest hash mismatch")
        if package.manifest.kind != "world":
            reasons.append("manifest kind is not world")
        if not package.rights_ok:
            reasons.append("rights not satisfied")
        if package.evidence_coverage < 0.5:
            reasons.append("evidence coverage below 0.5")
        preview_ok = not any("rights" in r or "evidence" in r or "manifest" in r for r in reasons)
        blocking_gaps = [gap for gap in package.unresolved_gaps if gap]
        publish_ok = preview_ok and not blocking_gaps and package.rights_ok
        if not preview_ok:
            reasons.append("preview gate failed")
        if not publish_ok and package.unresolved_gaps:
            reasons.append("unresolved gaps block publish")
        return PackageValidationResult(
            package_id=package.package_id,
            preview_ok=preview_ok,
            publish_ok=publish_ok,
            reasons=tuple(reasons),
        )
