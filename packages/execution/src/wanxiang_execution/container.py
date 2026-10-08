"""Docker-backed container execution provider for the R7 Execution Fabric.

The provider never pulls images: the requested image must already exist locally.
This makes image acquisition an explicit supply-chain step outside execution.
The container receives no host filesystem mount, no host environment, no secrets
and no canonical world writer. Its result is an ExecutionObservation only.

This is stronger isolation than LocalProcessProvider but is still not claimed to
be a hostile multi-tenant security boundary equivalent to a microVM.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path

from wanxiang_execution.errors import ExecutionError, PolicyViolation
from wanxiang_execution.fabric import ExecutionRequest, ExecutionResult
from wanxiang_execution.local_process import (
    MAX_CAPTURE_BYTES,
    ProcessOutcome,
    decode_partial,
    output_refs,
    sha256_text,
    truncate_to_bytes,
)
from wanxiang_execution.policy import (
    ExecutionClass,
    FilesystemAccess,
    NetworkAccess,
    authorize_for,
)
from wanxiang_execution.trace import (
    EXIT_STATUS_COMPLETED,
    EXIT_STATUS_FAILED,
    EXIT_STATUS_TIMEOUT,
    TIMEOUT_EXIT_CODE,
    ExecutionTrace,
    environment_hash,
    trace_digest,
)


class DockerContainerProvider:
    """Run a proposal-only capability in a pre-existing local Docker image."""

    provider_id = "execution-docker-container"
    provider_version = "1.0.0"
    execution_class = ExecutionClass.CONTAINER

    def __init__(self, image_ref: str, *, docker_binary: str = "docker") -> None:
        if not image_ref.strip():
            raise ExecutionError("container image_ref must be non-empty")
        binary = shutil.which(docker_binary)
        if binary is None:
            raise ExecutionError(f"docker binary is unavailable: {docker_binary!r}")
        self._docker = binary
        self._image_ref = image_ref
        self._image_id = self._inspect_image(image_ref)

    @property
    def image_ref(self) -> str:
        return self._image_ref

    @property
    def image_id(self) -> str:
        return self._image_id

    def run(self, request: ExecutionRequest, workspace_dir: Path) -> ExecutionResult:
        """Execute one request in a rootless-style, no-network container envelope."""
        authorize_for(request.policy, ExecutionClass.CONTAINER)
        if request.policy.network is NetworkAccess.EGRESS:
            raise PolicyViolation("DockerContainerProvider does not grant network egress")
        workspace_dir.mkdir(parents=True, exist_ok=True)
        container_name = f"wanxiang-{request.execution_id}".lower()
        args = self._docker_args(request, container_name)
        started = time.monotonic()
        outcome = self._run_docker(
            args,
            request.stdin_text,
            request.policy.wall_seconds_limit,
            container_name,
        )
        wall_ms = int((time.monotonic() - started) * 1000)
        return self._build_result(request, outcome, wall_ms)

    def _inspect_image(self, image_ref: str) -> str:
        completed = subprocess.run(
            [self._docker, "image", "inspect", "--format", "{{.Id}}", image_ref],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        image_id = completed.stdout.strip()
        if completed.returncode != 0 or not image_id.startswith("sha256:"):
            detail = completed.stderr.strip() or "image is not present locally"
            raise ExecutionError(
                f"container image must already exist locally: {image_ref!r}: {detail}"
            )
        return image_id

    def _docker_args(self, request: ExecutionRequest, container_name: str) -> list[str]:
        args = [
            self._docker,
            "run",
            "--rm",
            "--name",
            container_name,
            "--network",
            "none",
            "--read-only",
            "--pids-limit",
            "64",
            "--memory",
            f"{request.policy.memory_mb_limit}m",
            "--cpus",
            "1.0",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--user",
            "65534:65534",
        ]
        if request.policy.filesystem is FilesystemAccess.SCRATCH_WRITE:
            args.extend(
                [
                    "--tmpfs",
                    "/workspace:rw,nosuid,nodev,size=64m",
                    "--workdir",
                    "/workspace",
                ]
            )
        else:
            args.extend(["--workdir", "/"])
        for key, value in sorted(request.environment.items()):
            if not key or "=" in key or "\x00" in key or "\x00" in value:
                raise ExecutionError(f"invalid container environment variable: {key!r}")
            args.extend(["--env", f"{key}={value}"])
        args.append(self._image_ref)
        args.extend(request.command)
        return args

    def _run_docker(
        self,
        args: list[str],
        stdin_text: str | None,
        timeout_seconds: int,
        container_name: str,
    ) -> ProcessOutcome:
        try:
            completed = subprocess.run(
                args,
                input=stdin_text,
                stdin=subprocess.DEVNULL if stdin_text is None else None,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
                encoding="utf-8",
                errors="replace",
                env={"PATH": os.environ.get("PATH", "")},
            )
        except subprocess.TimeoutExpired as exc:
            subprocess.run(
                [self._docker, "rm", "-f", container_name],
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
                env={"PATH": os.environ.get("PATH", "")},
            )
            return ProcessOutcome(
                exit_status=EXIT_STATUS_TIMEOUT,
                exit_code=TIMEOUT_EXIT_CODE,
                stdout_text=decode_partial(exc.stdout),
                stderr_text=decode_partial(exc.stderr),
            )
        return ProcessOutcome(
            exit_status=(
                EXIT_STATUS_COMPLETED if completed.returncode == 0 else EXIT_STATUS_FAILED
            ),
            exit_code=completed.returncode,
            stdout_text=completed.stdout,
            stderr_text=completed.stderr,
        )

    def _build_result(
        self,
        request: ExecutionRequest,
        outcome: ProcessOutcome,
        wall_ms: int,
    ) -> ExecutionResult:
        stdout_digest = sha256_text(outcome.stdout_text)
        stderr_digest = sha256_text(outcome.stderr_text)
        traced_environment: dict[str, str] = dict(request.environment)
        traced_environment["WANXIANG_CONTAINER_IMAGE_ID"] = self._image_id
        trace = ExecutionTrace(
            execution_id=request.execution_id,
            capability_id=request.capability_id,
            capability_version=request.capability_version,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            execution_class=request.policy.execution_class,
            trust=request.policy.trust,
            environment_hash=environment_hash(traced_environment),
            input_refs=request.input_refs,
            commands=(request.command,),
            output_refs=output_refs(stdout_digest, stderr_digest, outcome),
            exit_status=outcome.exit_status,
            exit_code=outcome.exit_code,
            wall_ms=wall_ms,
            stdout_bytes=len(outcome.stdout_text.encode("utf-8")),
            stderr_bytes=len(outcome.stderr_text.encode("utf-8")),
            stdout_digest=stdout_digest,
            stderr_digest=stderr_digest,
            snapshot_ref=None,
            resume_ref=None,
            isolation={
                "process": "docker-container",
                "root_filesystem": "read_only",
                "filesystem_scratch": (
                    "tmpfs_64m"
                    if request.policy.filesystem is FilesystemAccess.SCRATCH_WRITE
                    else "none"
                ),
                "environment": "explicit_only",
                "network": "loopback_only",
                "memory": f"docker_limit_{request.policy.memory_mb_limit}m",
                "cpu": "docker_rate_limit_1_cpu; total_cpu_seconds_not_enforced",
                "pids": "docker_limit_64",
                "capabilities": "all_dropped",
                "privilege": "no_new_privileges",
                "host_mounts": "none",
                "image_id": self._image_id,
            },
        )
        observation: dict[str, object] = {
            "kind": "execution-observation",
            "execution_id": request.execution_id,
            "trace_digest": trace_digest(trace),
            "stdout_digest": stdout_digest,
            "proposal_only": True,
            "container_image_id": self._image_id,
        }
        return ExecutionResult(
            trace=trace,
            stdout_text=truncate_to_bytes(outcome.stdout_text, MAX_CAPTURE_BYTES),
            stderr_text=truncate_to_bytes(outcome.stderr_text, MAX_CAPTURE_BYTES),
            observation=observation,
        )


__all__ = ["DockerContainerProvider"]
