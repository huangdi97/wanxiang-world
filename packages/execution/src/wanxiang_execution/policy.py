"""Execution policy vocabulary and the fabric authorization decision.

A policy is a declarative contract: it states what a caller wants. It is
validated for internal consistency when constructed, and then `authorize`
refuses anything this fabric cannot honestly deliver. Refusals are explicit
and name both the reason and the offending policy field.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from wanxiang_execution.errors import PolicyViolation


class ExecutionClass(StrEnum):
    """Isolation class requested for one execution."""

    FUNCTION = "function"
    PROCESS = "process"
    CONTAINER = "container"
    WASM = "wasm"
    MICROVM = "microvm"
    VM = "vm"
    GPU = "gpu"
    REMOTE = "remote"


class TrustLevel(StrEnum):
    """How much the caller trusts the code that will be executed."""

    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    THIRD_PARTY = "third_party"
    GENERATED = "generated"


class FilesystemAccess(StrEnum):
    """Filesystem capability granted to one execution."""

    NONE = "none"
    READ_ONLY = "read_only"
    SCRATCH_WRITE = "scratch_write"


class NetworkAccess(StrEnum):
    """Network capability granted to one execution."""

    NONE = "none"
    LOOPBACK = "loopback"
    EGRESS = "egress"


class SecretAccess(StrEnum):
    """Secret capability granted to one execution."""

    NONE = "none"
    EXPLICIT_GRANT = "explicit_grant"


class SideEffectClass(StrEnum):
    """Whether an execution may produce irreversible external effects."""

    NONE = "none"
    IRREVERSIBLE_EXTERNAL = "irreversible_external"


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    """Declared capabilities and limits for one execution request.

    Attributes:
        trust: Trust level of the code to execute.
        execution_class: Requested isolation class.
        filesystem: Filesystem capability.
        network: Network capability.
        secrets: Secret capability.
        cpu_seconds_limit: Positive CPU budget in seconds. Declared and traced,
            but NOT enforced by the local process provider.
        memory_mb_limit: Positive memory budget in MiB. Declared and traced,
            but NOT enforced by the local process provider.
        wall_seconds_limit: Positive wall-clock budget in seconds; enforced by
            the provider as a subprocess timeout.
        reproducibility: Non-empty free-form label, e.g. ``"best_effort"``.
        cost_class: Non-empty free-form label, e.g. ``"local_low"``.
        side_effects: Side-effect class the execution may produce.
    """

    trust: TrustLevel
    execution_class: ExecutionClass
    filesystem: FilesystemAccess
    network: NetworkAccess
    secrets: SecretAccess
    cpu_seconds_limit: int
    memory_mb_limit: int
    wall_seconds_limit: int
    reproducibility: str
    cost_class: str
    side_effects: SideEffectClass

    def __post_init__(self) -> None:
        """Validate internal consistency of the declared policy.

        Raises:
            PolicyViolation: If a limit is not positive or a label is empty.
        """
        if self.cpu_seconds_limit <= 0:
            raise PolicyViolation(
                f"cpu_seconds_limit must be positive: got {self.cpu_seconds_limit}"
            )
        if self.memory_mb_limit <= 0:
            raise PolicyViolation(f"memory_mb_limit must be positive: got {self.memory_mb_limit}")
        if self.wall_seconds_limit <= 0:
            raise PolicyViolation(
                f"wall_seconds_limit must be positive: got {self.wall_seconds_limit}"
            )
        if not self.reproducibility.strip():
            raise PolicyViolation("reproducibility must be a non-empty string")
        if not self.cost_class.strip():
            raise PolicyViolation("cost_class must be a non-empty string")

    @classmethod
    def default_untrusted(cls) -> ExecutionPolicy:
        """Return the baseline policy for untrusted/generated code.

        No network, no secrets, scratch writes only.
        """
        return cls(
            trust=TrustLevel.UNTRUSTED,
            execution_class=ExecutionClass.PROCESS,
            filesystem=FilesystemAccess.SCRATCH_WRITE,
            network=NetworkAccess.NONE,
            secrets=SecretAccess.NONE,
            cpu_seconds_limit=10,
            memory_mb_limit=512,
            wall_seconds_limit=10,
            reproducibility="best_effort",
            cost_class="local_low",
            side_effects=SideEffectClass.NONE,
        )

    @classmethod
    def default_trusted(cls) -> ExecutionPolicy:
        """Return the baseline policy for trusted first-party code.

        Loopback network only, no secrets, read-only filesystem.
        """
        return cls(
            trust=TrustLevel.TRUSTED,
            execution_class=ExecutionClass.PROCESS,
            filesystem=FilesystemAccess.READ_ONLY,
            network=NetworkAccess.LOOPBACK,
            secrets=SecretAccess.NONE,
            cpu_seconds_limit=60,
            memory_mb_limit=2048,
            wall_seconds_limit=60,
            reproducibility="best_effort",
            cost_class="local_standard",
            side_effects=SideEffectClass.NONE,
        )


def authorize(policy: ExecutionPolicy) -> None:
    """Authorize a policy for the local fabric, or refuse it explicitly.

    Args:
        policy: Declared execution policy for one request.

    Raises:
        PolicyViolation: If the policy requests an execution class this fabric
            does not implement, untrusted network egress, secret access
            (no secret broker exists), or irreversible external side effects
            (those must go through the outbox, never through the fabric).
    """
    if policy.execution_class is not ExecutionClass.PROCESS:
        raise PolicyViolation(
            "execution_class is not implemented by this fabric: "
            f"requested execution_class={policy.execution_class.value!r}, "
            f"only {ExecutionClass.PROCESS.value!r} is available"
        )
    if policy.trust is not TrustLevel.TRUSTED and policy.network is NetworkAccess.EGRESS:
        raise PolicyViolation(
            "network egress requires trust=trusted: "
            f"requested network={policy.network.value!r} with trust={policy.trust.value!r}"
        )
    if policy.secrets is SecretAccess.EXPLICIT_GRANT:
        raise PolicyViolation(
            "secret access is not available because no secret broker exists: "
            f"requested secrets={policy.secrets.value!r}"
        )
    if policy.side_effects is SideEffectClass.IRREVERSIBLE_EXTERNAL:
        raise PolicyViolation(
            "irreversible external effects must go through the outbox, not the fabric: "
            f"requested side_effects={policy.side_effects.value!r}"
        )
