"""Provider-neutral ExecutionRouter behavior."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from wanxiang_execution import (
    DockerContainerProvider,
    ExecutionClass,
    ExecutionPolicy,
    ExecutionRequest,
    ExecutionRouter,
    LocalProcessProvider,
    PolicyViolation,
)


def test_router_selects_registered_provider_by_execution_class(tmp_path: Path) -> None:
    router = ExecutionRouter((LocalProcessProvider(),))
    policy = ExecutionPolicy.default_untrusted()
    request = ExecutionRequest(
        execution_id="router-process",
        capability_id="cap.router",
        capability_version="1.0.0",
        command=("python", "-c", "print('router-ok')"),
        input_refs=(),
        policy=policy,
    )

    result = router.run(request, tmp_path)

    assert result.trace.provider_id == "execution-local-process"
    assert result.stdout_text == "router-ok\n"


def test_router_fails_closed_when_execution_class_has_no_provider() -> None:
    router = ExecutionRouter((LocalProcessProvider(),))
    policy = replace(
        ExecutionPolicy.default_untrusted(),
        execution_class=ExecutionClass.CONTAINER,
    )

    with pytest.raises(PolicyViolation, match="no execution provider"):
        router.resolve(policy)


def test_router_rejects_two_providers_for_same_execution_class() -> None:
    router = ExecutionRouter((LocalProcessProvider(),))
    with pytest.raises(PolicyViolation, match="already registered"):
        router.register(LocalProcessProvider())


def test_provider_classes_declare_their_execution_class() -> None:
    assert LocalProcessProvider.execution_class is ExecutionClass.PROCESS
    assert DockerContainerProvider.execution_class is ExecutionClass.CONTAINER
