"""Invoke an admitted capability and return a proposal-only outcome.

SECURITY INVARIANT: a CapabilityOutcome can NEVER be appended to canonical world
history. It carries only proposal/observation data plus an execution digest; this
module imports no state writer, and only a commit authority (outside this
package) could turn such a payload into canonical state.

An invocation is refused with InvocationError unless the capability is admitted
and not revoked in the registry.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from wanxiang_execution import (
    ExecutionError,
    ExecutionPolicy,
    ExecutionRequest,
    ExecutionResult,
    LocalProcessProvider,
    trace_digest,
)

from wanxiang_foundry.errors import InvocationError
from wanxiang_foundry.package import CapabilityPackage
from wanxiang_foundry.registry import VerifiedCapabilityRegistry


@dataclass(frozen=True, slots=True)
class CapabilityRequest:
    """A caller request to run an admitted capability.

    Attributes:
        execution_id: Unique id; also the per-invocation scratch directory name.
        command: Non-empty argv tuple to run.
        input_refs: Content digests of the declared inputs.
        environment: Extra child environment variables.
        stdin_text: Optional text written to the child's stdin.
    """

    execution_id: str
    command: tuple[str, ...]
    input_refs: tuple[str, ...] = ()
    environment: Mapping[str, str] = field(default_factory=dict[str, str])
    stdin_text: str | None = None


@dataclass(frozen=True, slots=True)
class CapabilityOutcome:
    """The proposal-only result of one capability invocation.

    SECURITY INVARIANT: this object is not world history and can never be
    appended to canonical history. A downstream authority decides on its own
    what (if anything) becomes canonical state; this package cannot.

    Attributes:
        capability_id: Capability that ran.
        capability_version: Capability version.
        observation: Proposal-only observation from the execution fabric.
        proposal: Proposal-only payload describing the invocation output.
        execution_digest: sha256 digest of the execution trace.
    """

    capability_id: str
    capability_version: str
    observation: Mapping[str, object]
    proposal: Mapping[str, object]
    execution_digest: str


def invoke(
    registry: VerifiedCapabilityRegistry,
    package: CapabilityPackage,
    request: CapabilityRequest,
    policy: ExecutionPolicy,
    workspace_dir: Path,
) -> CapabilityOutcome:
    """Run an admitted capability and return a proposal-only outcome.

    Args:
        registry: Registry used to confirm the capability is invocable.
        package: The admitted capability package to run.
        request: The caller's execution request.
        policy: Execution policy for this invocation.
        workspace_dir: Parent directory for the per-invocation scratch dir.

    Returns:
        A proposal-only CapabilityOutcome.

    Raises:
        InvocationError: If the capability is not admitted or is revoked, or the
            execution could not be started under the policy.
    """
    if not registry.is_invocable(package.capability_id, package.version):
        raise InvocationError(
            f"capability {package.capability_id}@{package.version} is not invocable "
            "(unregistered or revoked)"
        )
    execution_request = ExecutionRequest(
        execution_id=request.execution_id,
        capability_id=package.capability_id,
        capability_version=package.version,
        command=request.command,
        input_refs=request.input_refs,
        policy=policy,
        environment=request.environment,
        stdin_text=request.stdin_text,
    )
    try:
        result = LocalProcessProvider().run(execution_request, workspace_dir)
    except ExecutionError as exc:
        raise InvocationError(
            f"capability {package.capability_id}@{package.version} could not run: {exc}"
        ) from exc
    return _outcome(package, request.execution_id, result)


def _outcome(
    package: CapabilityPackage, execution_id: str, result: ExecutionResult
) -> CapabilityOutcome:
    """Assemble the proposal-only outcome; holds no path to canonical state."""
    proposal: dict[str, object] = {
        "kind": "capability-proposal",
        "capability_id": package.capability_id,
        "capability_version": package.version,
        "output_class": package.world_effect.allowed_output_class.value,
        "execution_id": execution_id,
        "stdout_digest": result.trace.stdout_digest,
        "proposal_only": True,
    }
    return CapabilityOutcome(
        capability_id=package.capability_id,
        capability_version=package.version,
        observation=result.observation,
        proposal=proposal,
        execution_digest=trace_digest(result.trace),
    )
