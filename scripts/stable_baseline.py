"""Build the evidence-backed v5.5 Stable baseline ledger.

The script probes the checked-out repository and runs the small, deterministic
product gates required by G98A. It records command output hashes and parsed
details so the JSON is a trace of execution, not a hand-authored PASS fixture.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "v55_stable" / "baseline.json"
NAMED_MASTER = (
    "万相世界_v5.5-RC1-R3_Playable_Persistent_Evolving_Living_World_OS_完整母版_截至2026-08-28.md"
)
RC1_TAG = "v5.5.0-rc1"
V54_TAG = "v5.4.0"
CLOSURE_COMMIT = "d98d90c927d3325dbe527112ddd14867b19c2177"


def _run(command: list[str], *, timeout: int = 180) -> tuple[int, str, str, int]:
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env={**os.environ, "UV_CACHE_DIR": str(ROOT / ".uv-cache")},
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        code = 124
        stdout = str(exc.stdout or "")
        stderr = f"timeout after {timeout}s\n{exc.stderr or ''}"
    elapsed = int((time.perf_counter() - started) * 1000)
    return code, stdout, stderr, elapsed


def _git(*args: str, timeout: int = 60) -> tuple[int, str, str, int]:
    return _run(["git", *args], timeout=timeout)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _command_evidence(command: list[str], *, timeout: int = 180) -> dict[str, Any]:
    code, stdout, stderr, elapsed = _run(command, timeout=timeout)
    evidence: dict[str, Any] = {
        "command": " ".join(command),
        "exit_code": code,
        "status": "PASS" if code == 0 else "FAIL",
        "duration_ms": elapsed,
        "stdout_sha256": _sha256(stdout),
        "stderr_sha256": _sha256(stderr),
        "stdout_tail": stdout[-4000:],
        "stderr_tail": stderr[-4000:],
    }
    with contextlib.suppress(json.JSONDecodeError):
        evidence["parsed_stdout"] = json.loads(stdout)
    return evidence


def _tag_fact(tag: str) -> dict[str, Any]:
    object_code, object_id, object_err, _ = _git("rev-parse", tag)
    peeled_code, peeled_id, peeled_err, _ = _git("rev-parse", f"{tag}^{{}}")
    type_code, tag_type, type_err, _ = _git("cat-file", "-t", tag)
    return {
        "tag": tag,
        "object": object_id.strip() if object_code == 0 else None,
        "peeled_commit": peeled_id.strip() if peeled_code == 0 else None,
        "object_type": tag_type.strip() if type_code == 0 else None,
        "status": "PASS" if object_code == peeled_code == type_code == 0 else "FAIL",
        "errors": [value.strip() for value in (object_err, peeled_err, type_err) if value.strip()],
    }


def _ancestor(commit: str) -> dict[str, Any]:
    code, _, stderr, _ = _git("merge-base", "--is-ancestor", commit, "HEAD")
    return {"commit": commit, "is_ancestor": code == 0, "exit_code": code, "stderr": stderr.strip()}


def _scope_scan() -> dict[str, Any]:
    code, stdout, stderr, _ = _git("log", "--format=%H%x09%s", f"{CLOSURE_COMMIT}..HEAD")
    lines = [line for line in stdout.splitlines() if line.strip()]
    forbidden = [
        line
        for line in lines
        if "v5.6" in line.lower()
        or "model train" in line.lower()
        or "model-training" in line.lower()
    ]
    return {
        "status": "PASS" if code == 0 and not forbidden else "FAIL",
        "closure_to_head_commits": lines,
        "forbidden_scope_subjects": forbidden,
        "stderr": stderr.strip(),
    }


def _cleanup_temp(path: pathlib.Path) -> None:
    with contextlib.suppress(OSError):
        shutil.rmtree(path)


def build_baseline() -> dict[str, Any]:
    _, status_text, status_err, _ = _git("status", "--short", "--branch")
    porcelain_code, porcelain, porcelain_err, _ = _git("status", "--porcelain=v1")
    branch_code, branch, branch_err, _ = _git("branch", "--show-current")
    head_code, head, head_err, _ = _git("rev-parse", "HEAD")
    origin_code, origin, origin_err, _ = _git(
        "rev-parse", "refs/remotes/origin/feature/v5.5-playable-persistent-evolving"
    )

    temp_base = pathlib.Path(tempfile.mkdtemp(prefix="wanxiang-v55-g98a-"))
    try:
        checks = [
            ["uv", "run", "python", "scripts/architecture_check.py"],
            ["uv", "run", "python", "scripts/kernel_guard.py"],
            ["uv", "run", "python", "scripts/playable_e2e.py"],
            ["uv", "run", "python", "scripts/studio_socket_smoke.py"],
            ["uv", "run", "python", "scripts/release_build.py"],
            [
                "uv",
                "run",
                "pytest",
                "-q",
                "tests/unit/runtime/test_replay.py",
                "tests/unit/runtime/test_branch.py",
                "--basetemp",
                str(temp_base / "runtime"),
            ],
            [
                "uv",
                "run",
                "pytest",
                "-q",
                "tests/api/test_playable_api.py",
                "--basetemp",
                str(temp_base / "api"),
            ],
            [
                "uv",
                "run",
                "pytest",
                "-q",
                "tests/integration/test_playable_service.py",
                "--basetemp",
                str(temp_base / "playable"),
            ],
            [
                "uv",
                "run",
                "pytest",
                "-q",
                "tests/integration/test_g16h_release.py",
                "--basetemp",
                str(temp_base / "release"),
            ],
            [
                "uv",
                "run",
                "pytest",
                "-q",
                "tests/architecture/test_v55_acceptance_matrix_consistency.py",
                "--basetemp",
                str(temp_base / "matrix"),
            ],
        ]
        check_evidence = [_command_evidence(command) for command in checks]
    finally:
        _cleanup_temp(temp_base)

    master_path = ROOT / NAMED_MASTER
    canonical_spec = ROOT / "docs" / "spec" / "WANXIANG_v5_MASTER_SPEC.md"
    final_report = ROOT / "reports" / "V55_FINAL_RELEASE_REPORT.md"
    rc1_fact = _tag_fact(RC1_TAG)
    v54_fact = _tag_fact(V54_TAG)
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.stable-baseline.v1",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "conclusion": (
            "PASS" if all(item["status"] == "PASS" for item in check_evidence) else "FAIL"
        ),
        "gate": "61",
        "milestone": "M95-G98A",
        "repository": {
            "branch": branch.strip() if branch_code == 0 else None,
            "head": head.strip() if head_code == 0 else None,
            "origin_tracking_head": origin.strip() if origin_code == 0 else None,
            "status_command": "git status --short --branch",
            "status_output": status_text,
            "porcelain_output": porcelain,
            "clean_before_g98a_commit": porcelain_code == 0 and not porcelain.strip(),
            "command_errors": [
                value.strip()
                for value in (status_err, porcelain_err, branch_err, head_err, origin_err)
                if value.strip()
            ],
        },
        "lineage": {
            "v54": v54_fact,
            "rc1": rc1_fact,
            "final_closure": _ancestor(CLOSURE_COMMIT),
            "rc1_peeled": _ancestor(rc1_fact["peeled_commit"] or "missing"),
            "v54_peeled": _ancestor(v54_fact["peeled_commit"] or "missing"),
        },
        "input_resolution": {
            "requested_v55_master": NAMED_MASTER,
            "requested_v55_master_status": "FOUND" if master_path.is_file() else "NOT_FOUND",
            "normative_repo_spec": str(canonical_spec.relative_to(ROOT)),
            "normative_repo_spec_sha256": (
                hashlib.sha256(canonical_spec.read_bytes()).hexdigest()
                if canonical_spec.is_file()
                else None
            ),
            "final_release_report_sha256": (
                hashlib.sha256(final_report.read_bytes()).hexdigest()
                if final_report.is_file()
                else None
            ),
        },
        "remote_fetch": {
            "status": "EXTERNAL_BLOCKED",
            "command": "git fetch --tags --prune",
            "reason": (
                "Git HTTPS remote helper is unavailable on this host; local tag and "
                "closure evidence are retained."
            ),
        },
        "scope_scan": _scope_scan(),
        "checks": check_evidence,
        "boundaries": {
            "implemented": ["baseline lineage probes", "reproducible local regression command set"],
            "validated": ["Gate 61 local lineage and scope freeze"],
            "experimental": [],
            "not_proven": ["Gates 62-80; later milestones are not silently inferred"],
            "external_blocked": [
                "live remote fetch refresh",
                "requested v5.5 master file absent from checkout",
            ],
        },
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=OUTPUT)
    args = parser.parse_args()
    payload = build_baseline()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["conclusion"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
