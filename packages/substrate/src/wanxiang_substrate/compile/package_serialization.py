"""Validated JSON serialization for compiled world package drafts.

The durable Player catalog stores the compiled package so a restarted service
can rebuild its derived package/experience/install maps. This module only
serializes; it never writes canonical state or History.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.packages.model import (
    PackageManifest,
    SemanticVersion,
)

PACKAGE_SERIALIZATION_VERSION = 1
_KINDS = ("domain", "world", "scenario")
_TRUST = ("trusted", "untrusted")


def package_to_dict(package: WorldPackageDraft) -> dict[str, object]:
    """Lossless JSON-friendly representation of one compiled package."""

    return {
        "serialization_version": PACKAGE_SERIALIZATION_VERSION,
        "package_id": package.package_id,
        "draft_id": package.draft_id,
        "draft_revision": package.draft_revision,
        "manifest": _manifest_to_dict(package.manifest),
        "source_versions": [list(item) for item in package.source_versions],
        "domain_versions": [list(item) for item in package.domain_versions],
        "evidence_coverage": package.evidence_coverage,
        "unresolved_gaps": list(package.unresolved_gaps),
        "rights_ok": package.rights_ok,
        "for_preview": package.for_preview,
        "draft": package.draft.to_dict(),
    }


def package_from_dict(data: Mapping[str, object]) -> WorldPackageDraft:
    """Rebuild a package and re-validate its manifest hash and draft schema."""

    version = data.get("serialization_version")
    if version != PACKAGE_SERIALIZATION_VERSION:
        raise ContractError(f"unsupported package serialization version {version!r}")
    draft_data = data.get("draft")
    manifest_data = data.get("manifest")
    if not isinstance(draft_data, dict) or not isinstance(manifest_data, dict):
        raise ContractError("package payload requires manifest and draft objects")
    return WorldPackageDraft(
        package_id=_text(data.get("package_id"), "package_id"),
        draft_id=_text(data.get("draft_id"), "draft_id"),
        draft_revision=_positive_int(data.get("draft_revision"), "draft_revision"),
        manifest=_manifest_from_dict(cast(dict[str, object], manifest_data)),
        source_versions=_pairs(data.get("source_versions", []), "source_versions"),
        domain_versions=_pairs(data.get("domain_versions", []), "domain_versions"),
        evidence_coverage=_unit_float(data.get("evidence_coverage"), "evidence_coverage"),
        unresolved_gaps=_strings(data.get("unresolved_gaps", []), "unresolved_gaps"),
        rights_ok=_boolean(data.get("rights_ok"), "rights_ok"),
        for_preview=_boolean(data.get("for_preview"), "for_preview"),
        draft=WorldDraft.from_dict(cast(dict[str, object], draft_data)),
    )


def _manifest_to_dict(manifest: PackageManifest) -> dict[str, object]:
    return {
        "package_id": manifest.package_id,
        "kind": manifest.kind,
        "version": str(manifest.version),
        "name": manifest.name,
        "dependencies": [list(item) for item in manifest.dependencies],
        "schema_version": manifest.schema_version,
        "content_hash": manifest.content_hash,
        "executable_trust": manifest.executable_trust,
        "compat": list(manifest.compat),
        "constitution_ref": manifest.constitution_ref,
        "genesis_ref": manifest.genesis_ref,
        "evolution_policy_ref": manifest.evolution_policy_ref,
        "lineage_ref": manifest.lineage_ref,
    }


def _manifest_from_dict(data: Mapping[str, object]) -> PackageManifest:
    kind = data.get("kind")
    if kind not in _KINDS:
        raise ContractError(f"unsupported package kind {kind!r}")
    trust = data.get("executable_trust", "untrusted")
    if trust not in _TRUST:
        raise ContractError(f"unsupported executable trust {trust!r}")
    return PackageManifest(
        package_id=_text(data.get("package_id"), "manifest package_id"),
        kind=kind,
        version=_version(data.get("version")),
        name=_text(data.get("name"), "manifest name"),
        dependencies=_pairs(data.get("dependencies", []), "manifest dependencies"),
        schema_version=_positive_int(data.get("schema_version", 1), "manifest schema_version"),
        content_hash=_optional_text(data.get("content_hash", ""), "manifest content_hash"),
        executable_trust=trust,
        compat=_strings(data.get("compat", []), "manifest compat"),
        constitution_ref=_optional_ref(data.get("constitution_ref")),
        genesis_ref=_optional_ref(data.get("genesis_ref")),
        evolution_policy_ref=_optional_ref(data.get("evolution_policy_ref")),
        lineage_ref=_optional_ref(data.get("lineage_ref")),
    )


def _version(value: object) -> SemanticVersion:
    text = _text(value, "manifest version")
    parts = text.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ContractError(f"invalid semantic version {text!r}")
    return SemanticVersion(int(parts[0]), int(parts[1]), int(parts[2]))


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{name} must be a non-empty string")
    return value


def _optional_text(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{name} must be text")
    return value


def _optional_ref(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ContractError("manifest refs must be text or null")
    return value


def _positive_int(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ContractError(f"{name} must be a positive integer")
    return value


def _unit_float(value: object, name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ContractError(f"{name} must be numeric")
    number = float(value)
    if not (0.0 <= number <= 1.0):
        raise ContractError(f"{name} must be within [0,1]")
    return number


def _boolean(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise ContractError(f"{name} must be boolean")
    return value


def _strings(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ContractError(f"{name} must be a list of strings")
    raw = cast(list[object], value)
    if any(not isinstance(item, str) for item in raw):
        raise ContractError(f"{name} must be a list of strings")
    return tuple(cast(list[str], raw))


def _pairs(value: object, name: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise ContractError(f"{name} must be a list")
    pairs: list[tuple[str, str]] = []
    for item in cast(list[object], value):
        if not isinstance(item, list):
            raise ContractError(f"{name} items must be [text, text]")
        parts = cast(list[object], item)
        if len(parts) != 2:
            raise ContractError(f"{name} items must be [text, text]")
        first, second = parts
        if not isinstance(first, str) or not isinstance(second, str):
            raise ContractError(f"{name} items must be [text, text]")
        pairs.append((first, second))
    return tuple(pairs)
