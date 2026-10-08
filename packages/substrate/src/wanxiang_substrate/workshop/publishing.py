"""Publishing visibility, rights, metadata and safety extension contracts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.models import Visibility
from wanxiang_substrate.sources.model import SourceRecord


@dataclass(frozen=True, slots=True)
class RightsSummary:
    """Aggregated rights evidence; absence of approval is a blocking result."""

    source_refs: tuple[str, ...] = ()
    package_allowed_refs: tuple[str, ...] = ()
    public_export_allowed_refs: tuple[str, ...] = ()
    blocked_refs: tuple[str, ...] = ()
    review_refs: tuple[str, ...] = ()
    creator_intent_only: bool = False

    @property
    def package_allowed(self) -> bool:
        return self.creator_intent_only or (
            bool(self.source_refs) and set(self.source_refs) == set(self.package_allowed_refs)
        )

    @property
    def public_export_allowed(self) -> bool:
        return self.creator_intent_only or (
            bool(self.source_refs) and set(self.source_refs) == set(self.public_export_allowed_refs)
        )

    @classmethod
    def from_sources(cls, sources: tuple[SourceRecord, ...]) -> RightsSummary:
        source_refs = tuple(sorted(source.source_id for source in sources))
        package = tuple(
            sorted(
                source.source_id
                for source in sources
                if source.rights is not None and source.rights.allows("package")
            )
        )
        public = tuple(
            sorted(
                source.source_id
                for source in sources
                if source.rights is not None and source.rights.allows("public_export")
            )
        )
        blocked = tuple(sorted(set(source_refs) - set(package)))
        review = tuple(
            sorted(source.source_id for source in sources if not source.canonical_eligible())
        )
        return cls(source_refs, package, public, blocked, review)

    @classmethod
    def creator_intent(cls, intent_ref: str) -> RightsSummary:
        if not intent_ref:
            raise ContractError("creator intent rights summary requires an intent ref")
        return cls(review_refs=(intent_ref,), creator_intent_only=True)

    def to_dict(self) -> dict[str, object]:
        return {
            "source_refs": list(self.source_refs),
            "package_allowed_refs": list(self.package_allowed_refs),
            "public_export_allowed_refs": list(self.public_export_allowed_refs),
            "blocked_refs": list(self.blocked_refs),
            "review_refs": list(self.review_refs),
            "creator_intent_only": self.creator_intent_only,
            "package_allowed": self.package_allowed,
            "public_export_allowed": self.public_export_allowed,
        }


@dataclass(frozen=True, slots=True)
class PackageMetadata:
    package_id: str
    version: str
    display_name: str
    categories: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    compatibility: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.package_id or not self.version or not self.display_name.strip():
            raise ContractError("package metadata requires id, version and display name")
        if self.schema_version != 1:
            raise ContractError("unsupported package metadata schema")
        for name, values in (
            ("categories", self.categories),
            ("tags", self.tags),
            ("compatibility", self.compatibility),
            ("provenance_refs", self.provenance_refs),
        ):
            if any(not value.strip() for value in values) or len(set(values)) != len(values):
                raise ContractError(f"{name} must contain unique non-empty values")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "package_id": self.package_id,
            "version": self.version,
            "display_name": self.display_name,
            "categories": list(self.categories),
            "tags": list(self.tags),
            "compatibility": list(self.compatibility),
            "provenance_refs": list(self.provenance_refs),
        }


@dataclass(frozen=True, slots=True)
class SafetyExtensionPoints:
    moderation_policy_ref: str = ""
    safety_review_ref: str = ""
    extension_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if len(set(self.extension_refs)) != len(self.extension_refs):
            raise ContractError("safety extension refs must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "moderation_policy_ref": self.moderation_policy_ref,
            "safety_review_ref": self.safety_review_ref,
            "extension_refs": list(self.extension_refs),
        }


@dataclass(frozen=True, slots=True)
class PublishingProfile:
    profile_id: str
    visibility: Visibility
    owner_id: str
    metadata: PackageMetadata
    rights: RightsSummary
    safety: SafetyExtensionPoints = SafetyExtensionPoints()
    audience_ref: str = ""
    schema_version: int = 1
    review_complete: bool = True

    def __post_init__(self) -> None:
        if not self.profile_id or not self.owner_id:
            raise ContractError("publishing profile requires id and owner")
        if self.visibility not in {"public", "private", "unlisted", "family-private"}:
            raise ContractError(f"unsupported publishing visibility {self.visibility!r}")
        if self.visibility == "family-private" and not self.audience_ref:
            raise ContractError("family-private publishing requires an audience ref")
        if self.schema_version != 1:
            raise ContractError("unsupported publishing profile schema")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "visibility": self.visibility,
            "owner_id": self.owner_id,
            "audience_ref": self.audience_ref,
            "metadata": self.metadata.to_dict(),
            "rights": self.rights.to_dict(),
            "safety": self.safety.to_dict(),
            "review_complete": self.review_complete,
        }


@dataclass(frozen=True, slots=True)
class PublishingDecision:
    profile_id: str
    publishable: bool
    visible_in_plaza: bool
    reasons: tuple[str, ...]
    decision_hash: str


class PublishingPolicy:
    """Evaluate publication without registering or mutating a package."""

    def assess(self, profile: PublishingProfile) -> PublishingDecision:
        reasons: list[str] = []
        if not profile.rights.package_allowed:
            reasons.append("package rights are not approved")
        if profile.visibility == "public" and not profile.rights.public_export_allowed:
            reasons.append("public export rights are not approved")
        if profile.rights.blocked_refs:
            reasons.append("blocked rights refs: " + ",".join(profile.rights.blocked_refs))
        if not profile.review_complete:
            reasons.append("content review is incomplete")
        publishable = not reasons
        visible = publishable and profile.visibility == "public"
        payload = {
            "profile": profile.to_dict(),
            "publishable": publishable,
            "visible_in_plaza": visible,
            "reasons": reasons,
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return PublishingDecision(profile.profile_id, publishable, visible, tuple(reasons), digest)


__all__ = [
    "PackageMetadata",
    "PublishingDecision",
    "PublishingPolicy",
    "PublishingProfile",
    "RightsSummary",
    "SafetyExtensionPoints",
]
