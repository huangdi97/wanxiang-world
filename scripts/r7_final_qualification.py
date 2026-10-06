"""R7 final qualification chain: run the whole release gate for one exact SHA.

This is the qualification the R7 closure requires: one command that runs the real
repository gate (Python and TypeScript) on one frozen commit and writes machine
readable evidence. It is also what the clean-clone certification uses, so an
exact-SHA claim is reproducible from a fresh clone.

Steps that need something this host does not have (a browser binary, a tool on
PATH, a test file that does not exist yet) are reported as SKIPPED with an
explicit reason. Optional steps may skip; a skipped *required* step makes the
qualification NOT_PROVEN and returns non-zero. A failed step makes the run FAIL.

Usage::

    uv run python scripts/r7_final_qualification.py --expect-sha <sha>
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "artifacts" / "r7" / "qualification"
SCHEMA = "wanxiang.r7.qualification.v1"
OUTPUT_TAIL_LINES = 40

R7_PYTEST_SUITES = (
    "tests/unit/reality",
    "tests/unit/execution",
    "tests/unit/foundry",
    "tests/unit/runtime",
)
RUNTIME_LOCK_TESTS = (
    "tests/unit/reality/test_lock_store.py",
    "tests/unit/reality/test_worldline_open.py",
)
MIGRATION_TESTS = ("tests/unit/reality/test_migration.py",)
BROWSER_TESTS = (
    "tests/integration/test_m95_player_experience_browser.py",
    "tests/integration/test_g97e_browser_experience_product_chain.py",
)
REFERENCE_WORLD_TESTS = ("tests/integration/test_r7_reference_worlds.py",)
BROWSER_PROBE = (
    "uv",
    "run",
    "python",
    "-c",
    "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); "
    "b=p.chromium.launch(); b.close(); p.stop()",
)


@dataclasses.dataclass(frozen=True, slots=True)
class Step:
    """One qualification step: a command, its preconditions and its weight."""

    name: str
    command: tuple[str, ...]
    required: bool = True
    requires_paths: tuple[str, ...] = ()
    requires_command: str | None = None
    probe: tuple[str, ...] | None = None


def _uv(*args: str) -> tuple[str, ...]:
    return ("uv", "run", *args)


def steps() -> tuple[Step, ...]:
    """The qualification chain, in execution order."""
    return (
        Step("python-sync", ("uv", "sync", "--all-groups", "--all-packages")),
        Step("architecture-check", _uv("python", "scripts/architecture_check.py")),
        Step(
            "write-surface-inventory",
            _uv("python", "scripts/r7_write_surface_inventory.py"),
            requires_paths=("scripts/r7_write_surface_inventory.py",),
        ),
        Step("ruff-check", _uv("ruff", "check", ".")),
        Step("ruff-format", _uv("ruff", "format", "--check", ".")),
        Step("pyright", _uv("pyright")),
        Step("pytest-full", _uv("pytest", "-q")),
        Step("r7-unit", _uv("pytest", "-q", *R7_PYTEST_SUITES)),
        Step(
            "runtime-lock",
            _uv("pytest", "-q", *RUNTIME_LOCK_TESTS),
            requires_paths=RUNTIME_LOCK_TESTS,
        ),
        Step(
            "reality-migration",
            _uv("pytest", "-q", *MIGRATION_TESTS),
            requires_paths=MIGRATION_TESTS,
        ),
        Step(
            "security-denials",
            _uv("pytest", "-q", "tests/security"),
            requires_paths=("tests/security",),
        ),
        Step(
            "reference-worlds",
            _uv("pytest", "-q", *REFERENCE_WORLD_TESTS),
            requires_paths=REFERENCE_WORLD_TESTS,
        ),
        Step("pnpm-install", ("pnpm", "install", "--frozen-lockfile"), requires_command="pnpm"),
        Step("ts-typecheck", ("pnpm", "-r", "typecheck"), requires_command="pnpm"),
        Step("ts-lint", ("pnpm", "-r", "lint"), requires_command="pnpm"),
        Step("ts-test", ("pnpm", "-r", "test"), requires_command="pnpm"),
        Step("ts-build", ("pnpm", "-r", "build"), requires_command="pnpm"),
        Step(
            "playwright-install",
            _uv("playwright", "install", "--with-deps", "chromium"),
            required=False,
            requires_command="pnpm",
        ),
        Step(
            "browser-e2e",
            _uv("pytest", "-q", *BROWSER_TESTS),
            requires_paths=BROWSER_TESTS,
            probe=BROWSER_PROBE,
        ),
    )


def _which(name: str) -> bool:
    from shutil import which

    return which(name) is not None


def _skip_reason(step: Step) -> str | None:
    """Return the reason this step cannot run here, or None when it can."""
    missing = [path for path in step.requires_paths if not (ROOT / path).exists()]
    if missing:
        return f"missing path(s): {', '.join(missing)}"
    if step.requires_command is not None and not _which(step.requires_command):
        return f"{step.requires_command} is not on PATH"
    return None


def _probe(step: Step) -> str | None:
    """Run the step's probe: None when it passed, else the skip reason."""
    if step.probe is None:
        return None
    result = subprocess.run(
        step.probe,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 0:
        return None
    detail = (result.stderr or result.stdout).strip().splitlines()
    tail = detail[-1] if detail else "no output"
    return f"probe failed: {tail}"


def _tail(text: str) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return "\n".join(lines[-OUTPUT_TAIL_LINES:])


def run_step(step: Step) -> dict[str, object]:
    """Run one step and return its evidence record."""
    record: dict[str, object] = {
        "name": step.name,
        "command": " ".join(step.command),
        "required": step.required,
    }
    reason = _skip_reason(step) or _probe(step)
    if reason is not None:
        record.update({"status": "SKIPPED", "reason": reason, "durationSeconds": 0.0})
        return record
    started = time.monotonic()
    result = subprocess.run(
        step.command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    duration = round(time.monotonic() - started, 3)
    output = f"{result.stdout}\n{result.stderr}"
    record.update(
        {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "exitCode": result.returncode,
            "durationSeconds": duration,
            "outputTail": _tail(output),
        }
    )
    return record


def git_head() -> str:
    """The exact commit this qualification applies to."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def git_dirty() -> bool:
    """True when the working tree has uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return bool(result.stdout.strip())


def summarise(records: list[dict[str, object]]) -> str:
    """Render a short human-readable summary of the run."""
    lines = ["| step | status | detail |", "|---|---|---|"]
    for record in records:
        detail = record.get("reason") or record.get("outputTail") or ""
        first = str(detail).splitlines()[-1] if detail else ""
        lines.append(f"| {record['name']} | {record['status']} | {first[:160]} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Run the qualification chain and write the evidence artifacts."""
    parser = argparse.ArgumentParser(description="R7 final qualification chain")
    parser.add_argument("--expect-sha", default=None, help="fail unless HEAD equals this SHA")
    parser.add_argument("--label", default=None, help="label for the artifact file name")
    args = parser.parse_args(argv)

    head = git_head()
    if args.expect_sha is not None and head != args.expect_sha:
        print(f"HEAD {head} does not match expected {args.expect_sha}", file=sys.stderr)
        return 2

    records = [run_step(step) for step in steps()]
    failed = [record for record in records if record["status"] == "FAIL"]
    skipped = [record for record in records if record["status"] == "SKIPPED"]
    required_skipped = [
        record for record in skipped if bool(record.get("required", True))
    ]
    if failed:
        verdict = "FAIL"
    elif required_skipped:
        verdict = "NOT_PROVEN"
    else:
        verdict = "PASS"
    payload = {
        "schema": SCHEMA,
        "headSha": head,
        "workingTreeDirty": git_dirty(),
        "startedAt": dt.datetime.now(dt.UTC).isoformat(),
        "verdict": verdict,
        "steps": records,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    label = args.label or head[:12]
    json_path = OUT_DIR / f"qualification_{label}.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    markdown_path = OUT_DIR / f"qualification_{label}.md"
    markdown_path.write_text(
        "\n".join(
            [
                f"# R7 qualification — {label}",
                "",
                f"- HEAD: `{head}`",
                f"- working tree dirty: `{payload['workingTreeDirty']}`",
                f"- verdict: `{verdict}`",
                f"- steps: {len(records)} ({len(failed)} failed, {len(skipped)} skipped)",
                "",
                summarise(records),
                "",
                f"Machine readable: `{json_path.relative_to(ROOT).as_posix()}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        f"qualification: {verdict} ({len(records)} steps, "
        f"{len(failed)} failed, {len(skipped)} skipped, "
        f"{len(required_skipped)} required-skipped)"
    )
    print(f"artifact: {json_path.relative_to(ROOT).as_posix()}")
    for record in failed:
        print(f"FAILED {record['name']}: {str(record.get('outputTail', '')).splitlines()[-1:]}")
    for record in skipped:
        required = "required" if bool(record.get("required", True)) else "optional"
        print(f"SKIPPED ({required}) {record['name']}: {record.get('reason')}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":  # pragma: no cover - process entry point
    raise SystemExit(main())
