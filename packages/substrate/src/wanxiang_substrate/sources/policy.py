"""Versioned source intake policy (G04B)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.sources.model import MAX_PAYLOAD_BYTES

# Instruction-like markers that make a payload unsafe as data: the gate flags
# sources that try to inject system/prompt instructions.
MALICIOUS_MARKERS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "system:",
    "you are now",
    "as an ai",
    "override your instructions",
)


@dataclass(frozen=True, slots=True)
class SourcePolicy:
    """Policy that controls what may become canonical-eligible."""

    policy_version: int = 1
    require_rights_approval: bool = True
    max_payload_bytes: int = MAX_PAYLOAD_BYTES
    malicious_markers: tuple[str, ...] = MALICIOUS_MARKERS

    def __post_init__(self) -> None:
        if self.policy_version <= 0:
            raise ValueError("policy_version must be positive")
        if self.max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes must be positive")
