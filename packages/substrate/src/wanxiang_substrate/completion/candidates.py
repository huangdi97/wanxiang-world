"""Completion candidates E0-E5 (G58E).

Completion classes follow 07_COMPLETION_CONSISTENCY_SPEC:
E0 direct evidence, E1 multi-source reconstruction, E2 domain/era rule,
E3 runtime-required default, E4 experiential, E5 user fiction.
can_enter_canon defaults FALSE and always requires review; E1-E5 can never
silently upgrade to E0 (class is immutable).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

CompletionClass = Literal["E0", "E1", "E2", "E3", "E4", "E5"]
VALID_CLASSES = ("E0", "E1", "E2", "E3", "E4", "E5")
CompletionOrigin = Literal[
    "direct_evidence",
    "multi_source",
    "domain_rule",
    "runtime_default",
    "experiential",
    "user_fabricated",
]
CLASS_ORIGIN: dict[CompletionClass, CompletionOrigin] = {
    "E0": "direct_evidence",
    "E1": "multi_source",
    "E2": "domain_rule",
    "E3": "runtime_default",
    "E4": "experiential",
    "E5": "user_fabricated",
}


@dataclass(frozen=True, slots=True)
class CompletionCandidate:
    """A completion record; never silently becomes E0 Canon."""

    completion_id: str
    description: str
    completion_class: CompletionClass
    support_refs: tuple[str, ...]
    confidence: float
    can_enter_canon: bool = False
    origin: CompletionOrigin | None = None

    def __post_init__(self) -> None:
        if not self.completion_id or not self.description:
            raise ContractError("completion requires id and description")
        if self.completion_class not in VALID_CLASSES:
            raise ContractError(f"invalid completion class {self.completion_class!r}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")
        if self.can_enter_canon is not False:
            # Even E0 requires explicit review; never auto-eligible.
            raise ContractError("can_enter_canon must be False until explicitly reviewed")

    @property
    def origin_label(self) -> CompletionOrigin:
        return self.origin or CLASS_ORIGIN[self.completion_class]


def class_never_upgrades(current: CompletionClass, target: CompletionClass) -> bool:
    """E1-E5 can never silently upgrade to E0; equal/lower classes are allowed."""
    return not (target == "E0" and current != "E0")
