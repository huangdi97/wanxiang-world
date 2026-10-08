"""Live R7 E2 container provider qualification without registry/network pulls."""

from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
from dataclasses import replace
from pathlib import Path

import pytest
from wanxiang_execution import (
    EXIT_STATUS_COMPLETED,
    DockerContainerProvider,
    ExecutionClass,
    ExecutionPolicy,
    ExecutionRequest,
    FilesystemAccess,
    NetworkAccess,
)

pytestmark = pytest.mark.integration


def _docker_ready() -> bool:
    docker = shutil.which("docker")
    if docker is None:
        return False
    return (
        subprocess.run(
            [docker, "info"],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        ).returncode
        == 0
    )


def _copy_with_parents(source: Path, root: Path) -> None:
    target = root / source.relative_to("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _local_shell_image(tmp_path: Path) -> str:
    """Import /bin/sh + its shared libraries as a local Docker image."""
    if not _docker_ready():
        if os.environ.get("CI"):
            pytest.fail("Docker daemon is required by R7 container qualification")
        pytest.skip("Docker daemon unavailable on this host")

    root = tmp_path / "rootfs"
    root.mkdir()
    shell = Path("/bin/sh")
    _copy_with_parents(shell, root)

    ldd = subprocess.run(
        ["ldd", str(shell)],
        capture_output=True,
        check=True,
        encoding="utf-8",
        errors="strict",
    )
    libraries: set[Path] = set()
    for line in ldd.stdout.splitlines():
        for token in line.replace("=>", " ").split():
            if token.startswith("/") and Path(token).exists():
                libraries.add(Path(token))
    if not libraries:
        pytest.fail("could not discover /bin/sh runtime libraries")
    for library in sorted(libraries):
        _copy_with_parents(library, root)

    archive = tmp_path / "rootfs.tar"
    with tarfile.open(archive, "w") as tar:
        for path in sorted(root.rglob("*")):
            tar.add(path, arcname=str(path.relative_to(root)), recursive=False)

    tag = "wanxiang/r7-container-probe:local"
    with archive.open("rb") as stream:
        imported = subprocess.run(
            ["docker", "import", "-", tag],
            stdin=stream,
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    if imported.returncode != 0:
        pytest.fail(f"docker import failed: {imported.stderr}")
    return tag


def test_container_provider_enforces_no_network_read_only_root_and_proposal_only(
    tmp_path: Path,
) -> None:
    image = _local_shell_image(tmp_path)
    try:
        policy = replace(
            ExecutionPolicy.default_untrusted(),
            execution_class=ExecutionClass.CONTAINER,
            filesystem=FilesystemAccess.SCRATCH_WRITE,
            network=NetworkAccess.NONE,
            memory_mb_limit=128,
        )
        request = ExecutionRequest(
            execution_id="r7_container_live",
            capability_id="cap.r7.container-probe",
            capability_version="1.0.0",
            command=(
                "/bin/sh",
                "-c",
                "if touch /forbidden 2>/dev/null; then exit 9; fi; "
                "touch /workspace/ok; printf 'container-ok'",
            ),
            input_refs=(),
            policy=policy,
            environment={"R7_CONTAINER_PROBE": "1"},
        )

        result = DockerContainerProvider(image).run(request, tmp_path / "runs")

        assert result.trace.exit_status == EXIT_STATUS_COMPLETED
        assert result.trace.exit_code == 0
        assert result.stdout_text == "container-ok"
        assert result.observation["proposal_only"] is True
        assert result.trace.execution_class is ExecutionClass.CONTAINER
        assert result.trace.isolation["network"] == "loopback_only"
        assert result.trace.isolation["root_filesystem"] == "read_only"
        assert result.trace.isolation["host_mounts"] == "none"
        assert result.trace.isolation["capabilities"] == "all_dropped"
        assert str(result.observation["container_image_id"]).startswith("sha256:")
    finally:
        subprocess.run(
            ["docker", "image", "rm", "-f", image],
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
