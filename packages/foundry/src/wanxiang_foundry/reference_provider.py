"""Deterministic, LLM-free reference Artifact2Capability provider.

RuleBasedFoundryProvider is a reference implementation of the provider seam. It
is honest about being a reference: it does not claim to be Paper2Agent and it
never fabricates. A declaration that lacks a required, well-typed field (for
example an input/output contract) or an artifact without a declared rights basis
is refused with CandidateError rather than guessed.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import cast

from wanxiang_execution import SideEffectClass

from wanxiang_foundry.candidate import ArtifactRef, CapabilityCandidate
from wanxiang_foundry.errors import CandidateError


class RuleBasedFoundryProvider:
    """A deterministic reference provider built only from declared fields.

    Attributes:
        provider_id: Honest reference id; never claims to be Paper2Agent.
        provider_version: Reference provider version.
        is_reference_provider: Always True for this provider.
    """

    provider_id = "foundry-rule-based-reference"
    provider_version = "1.0.0"
    is_reference_provider = True

    def propose(
        self, artifact: ArtifactRef, declaration: Mapping[str, object]
    ) -> CapabilityCandidate:
        """Build a candidate from declared fields, refusing anything missing.

        Args:
            artifact: The source artifact; it must declare a rights basis.
            declaration: Declared fields, including an input/output contract.

        Returns:
            A proposal-only capability candidate.

        Raises:
            CandidateError: If the artifact has no rights basis, or a required
                declaration field is missing or ill-typed.
        """
        if not artifact.rights_basis.strip():
            raise CandidateError(
                f"artifact has no declared rights basis; refusing to reuse {artifact.uri!r}"
            )
        capability_id = _require_str(declaration, "capability_id")
        proposed_version = _require_str(declaration, "proposed_version")
        inputs = _require_str_tuple(declaration, "inputs")
        outputs = _require_str_tuple(declaration, "outputs")
        candidate_id = _optional_str(declaration, "candidate_id") or (
            f"{capability_id}@{proposed_version}"
        )
        return CapabilityCandidate(
            candidate_id=candidate_id,
            capability_id=capability_id,
            proposed_version=proposed_version,
            artifact=artifact,
            proposed_interface={"inputs": inputs, "outputs": outputs},
            environment_declaration=_optional_mapping(declaration, "environment"),
            requested_side_effects=_optional_side_effects(declaration),
        )


def _require_str(declaration: Mapping[str, object], key: str) -> str:
    value = declaration.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CandidateError(f"declaration field {key!r} must be a non-empty string: got {value!r}")
    return value


def _optional_str(declaration: Mapping[str, object], key: str) -> str:
    value = declaration.get(key)
    if value is None:
        return ""
    if not isinstance(value, str) or not value.strip():
        raise CandidateError(f"declaration field {key!r} must be a non-empty string when set")
    return value


def _require_str_tuple(declaration: Mapping[str, object], key: str) -> tuple[str, ...]:
    entries = _require_sequence(declaration.get(key), key)
    return tuple(_require_str_entry(entry, key) for entry in entries)


def _require_sequence(value: object, key: str) -> list[object]:
    items = _as_object_list(value)
    if not items:
        raise CandidateError(
            f"declaration field {key!r} must be a non-empty sequence: got {value!r}"
        )
    return items


def _as_object_list(value: object) -> list[object] | None:
    # WHY: declaration values are untyped JSON-like data. `isinstance` narrows
    # `object` to `list[Unknown]`/`tuple[Unknown, ...]`; this cast is the single
    # honest boundary that recovers a concrete element type. Every element is
    # then validated individually, so no unverified value escapes.
    if isinstance(value, list):
        return list(cast("Iterable[object]", value))
    if isinstance(value, tuple):
        return list(cast("Iterable[object]", value))
    return None


def _require_str_entry(entry: object, key: str) -> str:
    if not isinstance(entry, str) or not entry.strip():
        raise CandidateError(f"declaration field {key!r} entries must be non-empty strings")
    return entry


def _optional_side_effects(declaration: Mapping[str, object]) -> tuple[SideEffectClass, ...]:
    value = declaration.get("requested_side_effects")
    if value is None:
        return ()
    entries = _as_object_list(value)
    if entries is None:
        raise CandidateError("declaration field 'requested_side_effects' must be a sequence")
    allowed = ", ".join(sorted(member.value for member in SideEffectClass))
    return tuple(_require_side_effect(entry, allowed) for entry in entries)


def _require_side_effect(entry: object, allowed: str) -> SideEffectClass:
    if not isinstance(entry, str) or entry not in {member.value for member in SideEffectClass}:
        raise CandidateError(
            f"unexpected requested side effect {entry!r}; expected one of {allowed}"
        )
    return SideEffectClass(entry)


def _optional_mapping(declaration: Mapping[str, object], key: str) -> Mapping[str, object]:
    value = declaration.get(key)
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise CandidateError(f"declaration field {key!r} must be a mapping")
    # WHY: same untyped-declaration boundary as _as_object_list; the mapping is
    # treated read-only and its entries are validated by the caller.
    return cast("Mapping[str, object]", value)
