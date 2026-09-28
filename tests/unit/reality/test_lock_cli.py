"""Behaviour of the runtime-lock operator CLI (create / verify)."""

from __future__ import annotations

import json
import pathlib

import pytest
from wanxiang_reality import lock_cli

pytestmark = pytest.mark.unit

WORLDLINE = "wl_cli"


def _create_args(root: pathlib.Path) -> list[str]:
    return [
        "create-worldline",
        "--root",
        str(root),
        "--world-id",
        "world-1",
        "--world-instance-id",
        "instance-1",
        "--worldline-id",
        WORLDLINE,
    ]


def _verify_args(root: pathlib.Path) -> list[str]:
    return ["verify-worldline", "--root", str(root), "--worldline-id", WORLDLINE]


def test_create_then_verify_reports_opened_with_the_same_digest(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert lock_cli.main(_create_args(tmp_path)) == 0
    created = json.loads(capsys.readouterr().out.strip())

    assert created["status"] == "CREATED"
    assert created["worldlineId"] == WORLDLINE
    assert created["revision"] == 1
    assert created["path"].endswith(f"{WORLDLINE}.json")
    digest = created["lockDigest"]

    assert lock_cli.main(_verify_args(tmp_path)) == 0
    verified = json.loads(capsys.readouterr().out.strip())

    assert verified["status"] == "OPENED"
    assert verified["lockDigest"] == digest
    assert verified["drift"] == []


def test_tampering_the_file_is_reported_as_tampered(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lock_cli.main(_create_args(tmp_path))
    capsys.readouterr()
    path = tmp_path / f"{WORLDLINE}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["lock"]["provider_versions"]["provider.model.reference"] = "9.9.9"
    path.write_text(json.dumps(payload), encoding="utf-8")

    code = lock_cli.main(_verify_args(tmp_path))
    result = json.loads(capsys.readouterr().out.strip())

    assert code != 0
    assert result["status"] == "TAMPERED"


def test_verifying_a_missing_worldline_reports_missing(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = lock_cli.main(_verify_args(tmp_path))
    result = json.loads(capsys.readouterr().out.strip())

    assert code != 0
    assert result["status"] == "MISSING"
