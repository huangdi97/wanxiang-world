"""Real-subprocess behavior of the local process provider."""

from __future__ import annotations

import hashlib
import sys
from collections.abc import Callable, Mapping
from dataclasses import replace
from pathlib import Path

import pytest
from wanxiang_execution import (
    EXIT_STATUS_COMPLETED,
    EXIT_STATUS_FAILED,
    EXIT_STATUS_TIMEOUT,
    MAX_CAPTURE_BYTES,
    TIMEOUT_EXIT_CODE,
    ExecutionClass,
    ExecutionError,
    ExecutionPolicy,
    ExecutionRequest,
    LocalProcessProvider,
    NetworkAccess,
    PolicyViolation,
    SideEffectClass,
    trace_digest,
)


def _request(
    command: tuple[str, ...],
    policy: ExecutionPolicy,
    *,
    execution_id: str = "exec_test",
    environment: Mapping[str, str] | None = None,
    stdin_text: str | None = None,
) -> ExecutionRequest:
    return ExecutionRequest(
        execution_id=execution_id,
        capability_id="cap_test",
        capability_version="1.0.0",
        command=command,
        input_refs=(),
        policy=policy,
        environment={} if environment is None else dict(environment),
        stdin_text=stdin_text,
    )


def _python(script: Path) -> tuple[str, ...]:
    return (sys.executable, str(script))


@pytest.mark.unit
def test_process_execution_captures_stdout_and_completes(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("probe.py", "import sys\nsys.stdout.write('hello-fabric')\n")
    result = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path)

    assert result.trace.exit_status == EXIT_STATUS_COMPLETED
    assert result.trace.exit_code == 0
    assert result.stdout_text == "hello-fabric"
    assert result.trace.stdout_digest == hashlib.sha256(b"hello-fabric").hexdigest()
    assert result.trace.stdout_bytes == len(b"hello-fabric")
    assert result.trace.commands == (_python(script),)
    assert result.trace.provider_id == "execution-local-process"
    assert result.trace.wall_ms >= 0


@pytest.mark.unit
def test_nonzero_exit_code_is_recorded_as_failed(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("failer.py", "import sys\nsys.exit(3)\n")
    result = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path)

    assert result.trace.exit_status == EXIT_STATUS_FAILED
    assert result.trace.exit_code == 3


@pytest.mark.unit
def test_wall_limit_exceeded_is_recorded_as_timeout(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("sleeper.py", "import time\ntime.sleep(2)\n")
    policy = replace(untrusted_policy, wall_seconds_limit=1)
    result = LocalProcessProvider().run(_request(_python(script), policy), tmp_path)

    assert result.trace.exit_status == EXIT_STATUS_TIMEOUT
    assert result.trace.exit_code == TIMEOUT_EXIT_CODE


@pytest.mark.unit
def test_child_environment_is_scrubbed(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WANXIANG_EXECUTION_LEAK_CANARY", "parent-only-value")
    script = write_script(
        "env_probe.py",
        "import os\n"
        "print(os.environ.get('WANXIANG_EXECUTION_LEAK_CANARY', 'absent'))\n"
        "print(os.environ.get('PYTHONHASHSEED', 'absent'))\n"
        "print(os.environ.get('TEMP', 'absent'))\n",
    )
    result = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path)

    lines = result.stdout_text.splitlines()
    assert "parent-only-value" not in result.stdout_text
    assert lines[0] == "absent"
    assert lines[1] == "0"
    assert lines[2] == str(tmp_path / "exec_test")


@pytest.mark.unit
def test_stdout_is_capped_while_full_byte_count_is_recorded(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("noisy.py", "import sys\nsys.stdout.write('x' * 70000)\n")
    result = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path)

    assert len(result.stdout_text) == MAX_CAPTURE_BYTES
    assert result.trace.stdout_bytes == 70000
    assert result.trace.stdout_digest == hashlib.sha256(b"x" * 70000).hexdigest()


@pytest.mark.unit
@pytest.mark.parametrize("execution_id", ["../escape", "a/b", "", ".."])
def test_invalid_execution_id_is_rejected(
    execution_id: str, untrusted_policy: ExecutionPolicy
) -> None:
    with pytest.raises(ExecutionError):
        _request((sys.executable, "-c", "pass"), untrusted_policy, execution_id=execution_id)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("execution_class", ExecutionClass.CONTAINER),
        ("network", NetworkAccess.EGRESS),
        ("side_effects", SideEffectClass.IRREVERSIBLE_EXTERNAL),
    ],
)
def test_denied_policy_never_starts_a_process(
    field_name: str,
    bad_value: object,
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    policy = replace(untrusted_policy, **{field_name: bad_value})
    request = _request((sys.executable, "-c", "print('must not run')"), policy)

    with pytest.raises(PolicyViolation):
        LocalProcessProvider().run(request, tmp_path)
    assert not (tmp_path / request.execution_id).exists()


@pytest.mark.unit
def test_stdin_text_is_forwarded_to_child(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("echo.py", "import sys\nsys.stdout.write(sys.stdin.read().upper())\n")
    result = LocalProcessProvider().run(
        _request(_python(script), untrusted_policy, stdin_text="ping"), tmp_path
    )

    assert result.stdout_text == "PING"


@pytest.mark.unit
def test_observation_is_proposal_only(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("probe.py", "import sys\nsys.stdout.write('observed')\n")
    result = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path)

    observation = result.observation
    assert observation["kind"] == "execution-observation"
    assert observation["execution_id"] == "exec_test"
    assert observation["proposal_only"] is True
    assert observation["trace_digest"] == trace_digest(result.trace)
    assert observation["stdout_digest"] == result.trace.stdout_digest


@pytest.mark.unit
def test_isolation_reports_network_and_memory_as_not_enforced(
    write_script: Callable[[str, str], Path],
    tmp_path: Path,
    untrusted_policy: ExecutionPolicy,
) -> None:
    script = write_script("probe.py", "import sys\nsys.stdout.write('ok')\n")
    trace = LocalProcessProvider().run(_request(_python(script), untrusted_policy), tmp_path).trace

    assert trace.isolation["network"] == "not_enforced"
    assert trace.isolation["memory"] == "not_enforced"
    assert trace.isolation["process"] == "enforced"
    assert trace.isolation["environment"] == "scrubbed"
