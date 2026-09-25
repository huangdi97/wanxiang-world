"""Requalify v5.5 semantic invariants, rights, and safety boundaries."""

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
OUTPUT = ROOT / "artifacts" / "v55_stable" / "m100" / "semantic_safety.json"
REPORT = ROOT / "reports" / "M100_G103C_SEMANTIC_SAFETY.md"

COMMANDS: tuple[tuple[str, list[str], int], ...] = (
    (
        "security_reliability",
        ["uv", "run", "python", "scripts/security_reliability_certify.py"],
        900,
    ),
    ("security_forensics", ["uv", "run", "python", "scripts/security_forensics.py"], 300),
    ("architecture_guard", ["uv", "run", "python", "scripts/architecture_check.py"], 300),
    ("kernel_guard", ["uv", "run", "python", "scripts/kernel_guard.py"], 300),
    (
        "source_canon_immutability",
        [
            "uv",
            "run",
            "pytest",
            "-q",
            "tests/integration/test_v55_source_canon_immutability_qualification.py",
        ],
        900,
    ),
    (
        "provider_integration_boundaries",
        [
            "uv",
            "run",
            "pytest",
            "-q",
            "tests/integration/test_g95e_multi_provider_product_chain.py",
            "tests/integration/test_g96a_physical_provider_product_chain.py",
            "tests/integration/test_g96b_visual_provider_product_chain.py",
            "tests/integration/test_g96c_multi_perspective_product_chain.py",
            "tests/integration/test_g96d_reference_physical_product_chain.py",
            "tests/integration/test_g96e_reference_visual_product_chain.py",
            "tests/integration/test_g96f_external_engine_product_chain.py",
            "tests/integration/test_g96g_reality_consistency_product_chain.py",
            "tests/integration/test_g96h_provider_bridge_qualification.py",
        ],
        1200,
    ),
    (
        "provider_unit_boundaries",
        [
            "uv",
            "run",
            "pytest",
            "-q",
            "tests/unit/substrate/test_g95e_multi_provider.py",
            "tests/unit/substrate/test_g96a_physical_provider_abi.py",
            "tests/unit/substrate/test_g96b_visual_provider_abi.py",
            "tests/unit/substrate/test_g96c_multi_perspective_projection.py",
            "tests/unit/substrate/test_g96d_reference_physical_provider.py",
            "tests/unit/substrate/test_g96e_reference_visual_provider.py",
            "tests/unit/substrate/test_g96f_external_engine_adapter.py",
            "tests/unit/substrate/test_g96g_projection_reality_consistency.py",
        ],
        900,
    ),
    (
        "replay_branch_recovery",
        [
            "uv",
            "run",
            "pytest",
            "-q",
            "tests/integration/test_recovery.py",
            "tests/unit/runtime/test_branch.py",
            "tests/integration/test_g14b_crash_atomicity.py",
            "tests/integration/test_g14d_corruption.py",
            "tests/integration/test_g16g_backup_restore.py",
        ],
        900,
    ),
    (
        "rights_privacy_resources",
        [
            "uv",
            "run",
            "pytest",
            "-q",
            "tests/integration/test_g13f_security.py",
            "tests/integration/test_g14g_auth_privacy.py",
            "tests/integration/test_g14i_resource_fuzz.py",
            "tests/integration/test_g16a_config_secrets.py",
            "tests/integration/test_g16f_security_hardening.py",
            "tests/integration/test_g97f_security_safety_cost_storage.py",
        ],
        1200,
    ),
)


def _run(name: str, command: list[str], timeout: int) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env={**os.environ, "UV_CACHE_DIR": str(ROOT / ".uv-cache")},
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
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
    status = "PASS" if code == 0 else "EXTERNAL_BLOCKED" if code == 127 else "FAIL"
    return {
        "name": name,
        "command": " ".join(command),
        "exit_code": code,
        "status": status,
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "output_tail": combined[-5000:],
    }


def _write_evidence(payload: dict[str, Any]) -> None:
    results = payload["commands"]
    failures = [item["name"] for item in results if item["status"] == "FAIL"]
    external = [item["name"] for item in results if item["status"] == "EXTERNAL_BLOCKED"]
    payload["failed_commands"] = failures
    payload["external_blocked_commands"] = external
    payload["conclusion"] = "PASS" if not failures and not external else "FAIL"
    write_json(OUTPUT, payload)
    rows = "\n".join(
        f"| {item['name']} | {item['status']} | {item['exit_code']} | {item['duration_ms']} ms |"
        for item in results
    )
    REPORT.write_text(
        f"""# M100 G103C Semantic Safety Requalification

Conclusion: {payload["conclusion"]}. {len(results)}/{len(COMMANDS)} commands completed on
candidate SHA `{payload["candidate_sha"]}`. Each command stores stdout/stderr hashes and a
bounded output tail in the machine-readable artifact; no result is inferred from prose.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
{rows}

The matrix explicitly exercises source/canon immutability, provider proposal-only boundaries,
replay/branch/recovery, rights/privacy/resource controls, secret scanning, and kernel/architecture
guards. A missing executable is EXTERNAL_BLOCKED; every other non-zero command remains FAIL.
No private source, copyrighted source text, model cache, secret, or token is exported by this
qualification.

Boundaries: IMPLEMENTED = enforcement paths and guards; VALIDATED = PASS commands above;
EXPERIMENTAL/BOUNDED = provider/reference and research-adjacent behavior; NOT_PROVEN = live
customer data, production hosting, and external provider/hardware behavior; EXTERNAL_BLOCKED =
only commands whose required host executable is absent.

Machine-readable evidence: artifacts/v55_stable/m100/semantic_safety.json
Reproduce with: uv run python scripts/m100_semantic_safety.py
""",
        encoding="utf-8",
    )


def run() -> dict[str, Any]:
    candidate_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout.strip()
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m100.semantic-safety.v1",
        "conclusion": "IN_PROGRESS",
        "candidate_sha": candidate_sha,
        "commands": [],
        "failed_commands": [],
        "external_blocked_commands": [],
        "boundaries": {
            "implemented": [
                "server-enforced source, rights, privacy and canonical-state guards",
                "provider proposal-only and replay/branch/recovery invariants",
            ],
            "validated": [],
            "experimental_bounded": [
                "reference provider and external-engine adapter semantics",
            ],
            "not_proven": [
                "live customer/source export safety outside the tested local paths",
                "production hosting and real external provider or hardware behavior",
            ],
            "external_blocked": [],
        },
    }
    _write_evidence(payload)
    for name, command, timeout in COMMANDS:
        payload["commands"].append(_run(name, command, timeout))
        _write_evidence(payload)
    payload["boundaries"]["validated"] = [
        item["name"] for item in payload["commands"] if item["status"] == "PASS"
    ]
    payload["boundaries"]["external_blocked"] = payload["external_blocked_commands"]
    _write_evidence(payload)
    return payload


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "conclusion": result["conclusion"],
                "command_count": len(result["commands"]),
                "failed_commands": result["failed_commands"],
                "external_blocked_commands": result["external_blocked_commands"],
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
