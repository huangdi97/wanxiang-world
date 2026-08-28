"""Run the applicable v5.5 Stable local regression matrix with evidence."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from m98_burn_in_support import write_json

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "v55_stable" / "m100" / "full_regression.json"
REPORT = ROOT / "reports" / "M100_G103B_FULL_REGRESSION.md"

COMMANDS: tuple[tuple[str, list[str], int], ...] = (
    ("python_quality", ["uv", "run", "python", "scripts/quality.py"], 1800),
    ("kernel_guard", ["uv", "run", "python", "scripts/kernel_guard.py"], 300),
    ("release_build", ["uv", "run", "python", "scripts/release_build.py"], 300),
    ("playable_e2e", ["uv", "run", "python", "scripts/playable_e2e.py"], 300),
    ("studio_socket_smoke", ["uv", "run", "python", "scripts/studio_socket_smoke.py"], 300),
    (
        "structured_mixed_smoke",
        ["uv", "run", "python", "scripts/structured_mixed_smoke.py"],
        300,
    ),
    ("sdk_baseline", ["uv", "run", "python", "scripts/sdk_baseline.py"], 300),
    ("openapi_export", ["uv", "run", "python", "scripts/export_openapi.py"], 300),
    (
        "clean_room",
        ["uv", "run", "python", "scripts/clean_room_certify.py"],
        900,
    ),
    (
        "security_reliability",
        ["uv", "run", "python", "scripts/security_reliability_certify.py"],
        900,
    ),
    (
        "security_forensics",
        ["uv", "run", "python", "scripts/security_forensics.py"],
        300,
    ),
    (
        "blackbox_acceptance",
        ["uv", "run", "python", "scripts/blackbox_final_acceptance.py"],
        900,
    ),
    (
        "postgres_profile",
        ["uv", "run", "pytest", "-q", "tests/integration/test_g16b_postgres.py"],
        300,
    ),
    ("pnpm_install", ["pnpm", "install", "--frozen-lockfile"], 900),
    ("ts_lint", ["pnpm", "-r", "lint"], 300),
    ("ts_typecheck", ["pnpm", "-r", "typecheck"], 300),
    ("ts_test", ["pnpm", "-r", "test"], 600),
    ("ts_build", ["pnpm", "-r", "build"], 600),
)


def _classify(name: str, code: int, output: str) -> str:
    if name == "postgres_profile":
        lowered = output.lower()
        if "skipped" in lowered and "failed" not in lowered:
            return "EXTERNAL_BLOCKED"
        if code != 0 and any(
            marker in lowered
            for marker in ("connection refused", "could not connect", "no postgres")
        ):
            return "EXTERNAL_BLOCKED"
    return "PASS" if code == 0 else "FAIL"


def _run(name: str, command: list[str], timeout: int) -> dict[str, Any]:
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
        code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except FileNotFoundError as exc:
        code = 127
        stdout = ""
        stderr = f"{type(exc).__name__}: {exc}"
    except subprocess.TimeoutExpired as exc:
        code = 124
        stdout = str(exc.stdout or "")
        stderr = f"timeout after {timeout}s\n{exc.stderr or ''}"
    combined = stdout + stderr
    return {
        "name": name,
        "command": " ".join(command),
        "exit_code": code,
        "status": _classify(name, code, combined),
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "output_tail": combined[-4000:],
    }


def run() -> dict[str, Any]:
    results = [_run(name, command, timeout) for name, command, timeout in COMMANDS]
    failures = [item["name"] for item in results if item["status"] == "FAIL"]
    external = [item["name"] for item in results if item["status"] == "EXTERNAL_BLOCKED"]
    conclusion = "FAIL" if failures else "PASS"
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m100.full-regression.v1",
        "conclusion": conclusion,
        "generated_build_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip(),
        "commands": results,
        "command_count": len(results),
        "failed_commands": failures,
        "external_blocked_commands": external,
        "boundaries": {
            "implemented": [
                "Python quality/kernel/release/product/safety command matrix",
                "TypeScript install/lint/typecheck/test/build matrix",
            ],
            "validated": [
                "all commands with PASS status",
                "full applicable local regression scope",
            ],
            "experimental": [],
            "not_proven": [
                "live PostgreSQL when the service is absent",
                "production hosting and external infrastructure",
            ],
            "external_blocked": [
                "live PostgreSQL profile when skipped or unreachable",
            ],
        },
    }
    write_json(OUTPUT, payload)
    rows = "\n".join(
        f"| {item['name']} | {item['status']} | {item['exit_code']} | {item['duration_ms']} ms |"
        for item in results
    )
    REPORT.write_text(
        f"""# M100 G103B Full Regression

Conclusion: {conclusion}. {len(results)} commands were executed from the
candidate checkout; failures are never converted to PASS. Python quality
includes the full pytest suite, Ruff, Pyright, and architecture check.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
{rows}

PostgreSQL is reported as EXTERNAL_BLOCKED when the real service is skipped or
unreachable. It is not represented as a passing live-PostgreSQL test. All
other command failures remain FAIL in the machine-readable artifact.

Machine-readable evidence: artifacts/v55_stable/m100/full_regression.json
Reproduce with: uv run python scripts/m100_regression.py
""",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "conclusion": result["conclusion"],
                "command_count": result["command_count"],
                "failed_commands": result["failed_commands"],
                "external_blocked_commands": result["external_blocked_commands"],
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
