"""Repository-wide quality gate runner.

Stable command from repository root:

    uv run python scripts/quality.py

Runs Ruff lint, Ruff format check, Pyright, pytest, and (when present) the
architecture conformance check. Exit code 0 means every gate passed.
"""

from __future__ import annotations

import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

CHECKS: list[list[str]] = [
    ["uv", "run", "ruff", "check", "."],
    ["uv", "run", "ruff", "format", "--check", "."],
    ["uv", "run", "pyright"],
    ["uv", "run", "pytest", "-q"],
]


def _architecture_check() -> list[str] | None:
    script = ROOT / "scripts" / "architecture_check.py"
    if script.exists():
        return ["uv", "run", "python", str(script)]
    return None


def main() -> int:
    checks = list(CHECKS)
    arch = _architecture_check()
    if arch is not None:
        checks.append(arch)

    failed: list[list[str]] = []
    for cmd in checks:
        print(f"\n===== {' '.join(cmd)} =====", flush=True)
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failed.append(cmd)

    if failed:
        print("\nFAILED CHECKS:")
        for cmd in failed:
            print(" -", " ".join(cmd))
        return 1
    print("\nAll quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
