"""Record v5.5 remote/CI delivery readiness without performing a push (G103E)."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, cast

from m98_burn_in_support import write_json

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "v55_stable" / "m100" / "remote_delivery.json"
REPORT = ROOT / "reports" / "M100_G103E_REMOTE_DELIVERY.md"
REPO = "huangdi97/wanxiang-world"
BRANCH = "release/v5.5-stable-certification"
REQUIRED_JOBS = ("safety", "python", "postgres", "api-sdk", "ts", "release-smoke")


def _run(name: str, command: list[str], timeout: int = 120) -> dict[str, Any]:
    started = time.perf_counter()
    environment = {**os.environ, "GH_PAGER": "cat"}
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except FileNotFoundError as exc:
        code, stdout, stderr = 127, "", f"{type(exc).__name__}: {exc}"
    except subprocess.TimeoutExpired as exc:
        code = 124
        stdout = str(exc.stdout or "")
        stderr = f"timeout after {timeout}s\n{exc.stderr or ''}"
    combined = stdout + stderr
    return {
        "name": name,
        "command": " ".join(command),
        "exit_code": code,
        "status": "PASS" if code == 0 else "EXTERNAL_BLOCKED",
        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "output_tail": combined[-6000:],
    }


def _matrix_status(matrix: str, gate: int) -> str:
    prefix = f"| {gate} |"
    for line in matrix.splitlines():
        if line.startswith(prefix):
            return line.split("|")[3].strip()
    return "MISSING"


def _json_output(result: dict[str, Any]) -> Any:
    try:
        return json.loads(result["output_tail"])
    except (json.JSONDecodeError, TypeError):
        return None


def _run_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    items = cast(list[Any], value)
    return [cast(dict[str, Any], item) for item in items if isinstance(item, dict)]


def _mapping(value: Any) -> dict[str, Any]:
    return cast(dict[str, Any], value) if isinstance(value, dict) else {}


def _write(payload: dict[str, Any]) -> None:
    write_json(OUTPUT, payload)
    queries = payload["queries"]
    query_rows = "\n".join(
        f"| {item['name']} | {item['status']} | {item['exit_code']} |" for item in queries
    )
    REPORT.write_text(
        f"""# M100 G103E Remote Delivery / Required CI

Conclusion: `{payload["conclusion"]}`; Gate 80: `{payload["gate_80"]}`.
Local candidate: `{payload["local_head"]}`; branch: `{payload["branch"]}`.

| Read-only query | Status | Exit |
|---|---|---:|
{query_rows}

Required workflow jobs: `{", ".join(payload["required_jobs"])}`.
Candidate branch exists remotely: `{payload["remote_branch_present"]}`;
candidate Actions run exists: `{payload["candidate_run_present"]}`;
all required jobs verified for candidate: `{payload["candidate_jobs_verified"]}`.

No push, tag creation, or GitHub Release was attempted: Gate 80 is locked by the
M95 human-player Gates 62–66 and the stable predicate is not true. The Git remote
helper/remote branch and candidate Actions identity are not inferred from local
tracking refs. Existing successful Actions runs, if any, are retained only when
their SHA is shown in the artifact and are not substituted for this candidate.

Boundaries: IMPLEMENTED = read-only delivery/CI probe; VALIDATED = local SHA and
workflow definition; NOT_PROVEN = remote candidate push and candidate CI jobs;
EXTERNAL_BLOCKED = unavailable remote/helper or absent candidate delivery state.

Evidence: `artifacts/v55_stable/m100/remote_delivery.json`
Reproduce: `uv run python scripts/m100_remote_delivery.py`
""",
        encoding="utf-8",
    )


def run() -> dict[str, Any]:
    local_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    matrix = (ROOT / "reports" / "V55_STABLE_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")
    gate_79 = _matrix_status(matrix, 79)
    gate_80 = _matrix_status(matrix, 80)
    queries = [
        _run("git_remote", ["git", "remote", "-v"]),
        _run("git_ls_remote_branch", ["git", "ls-remote", "--heads", "origin", BRANCH]),
        _run("git_ls_remote_stable_tag", ["git", "ls-remote", "--tags", "origin", "v5.5.0"]),
        _run("gh_remote_branch", ["gh", "api", f"repos/{REPO}/git/ref/heads/{BRANCH}"]),
        _run(
            "gh_candidate_branch_runs",
            [
                "gh",
                "run",
                "list",
                "--repo",
                REPO,
                "--branch",
                BRANCH,
                "--limit",
                "20",
                "--json",
                "databaseId,headSha,status,conclusion,name,event,createdAt,url",
            ],
        ),
        _run(
            "gh_recent_runs",
            [
                "gh",
                "run",
                "list",
                "--repo",
                REPO,
                "--limit",
                "20",
                "--json",
                "databaseId,headSha,status,conclusion,name,event,createdAt,url",
            ],
        ),
    ]
    remote_ref = _mapping(_json_output(queries[3]))
    branch_runs = _run_list(_json_output(queries[4]))
    recent_runs = _run_list(_json_output(queries[5]))
    candidate_runs = [run for run in branch_runs if run.get("headSha") == local_head]
    candidate_jobs_verified: bool = False
    database_id: str | int | None = None
    job_probe: dict[str, Any] | None = None
    if candidate_runs:
        database_id = candidate_runs[0].get("databaseId")
        if not isinstance(database_id, (str, int)):
            candidate_runs = []
    if candidate_runs and database_id is not None:
        job_probe = _run(
            "gh_candidate_run_jobs",
            [
                "gh",
                "run",
                "view",
                str(database_id),
                "--repo",
                REPO,
                "--json",
                "jobs,headSha,status,conclusion,url",
            ],
        )
        queries.append(job_probe)
        job_data = _mapping(_json_output(job_probe))
        raw_jobs = job_data.get("jobs", [])
        jobs = _run_list(raw_jobs)
        names: set[str] = set()
        for job in jobs:
            name = job.get("name")
            if isinstance(name, str):
                names.add(name)
        candidate_jobs_verified = (
            job_data.get("headSha") == local_head
            and all(name in names for name in REQUIRED_JOBS)
            and job_data.get("conclusion") == "success"
        )
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m100.remote-delivery.v1",
        "conclusion": "LOCKED",
        "local_head": local_head,
        "branch": BRANCH,
        "repo": REPO,
        "gate_79": gate_79,
        "gate_80": gate_80,
        "required_jobs": list(REQUIRED_JOBS),
        "queries": queries,
        "remote_branch_present": bool(remote_ref.get("object")),
        "candidate_run_present": bool(candidate_runs),
        "candidate_jobs_verified": candidate_jobs_verified,
        "recent_remote_runs": recent_runs or [],
        "push": "NOT_ATTEMPTED",
        "tag": "NOT_ATTEMPTED",
        "github_release": "NOT_ATTEMPTED",
        "boundaries": {
            "implemented": ["read-only remote and required-CI delivery probe"],
            "validated": ["local candidate SHA and repository workflow job declaration"],
            "not_proven": ["remote candidate push and candidate Actions conclusions"],
            "external_blocked": [
                "remote branch/helper or candidate Actions identity is unavailable"
            ],
        },
    }
    _write(payload)
    return payload


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                "conclusion": result["conclusion"],
                "local_head": result["local_head"],
                "gate_79": result["gate_79"],
                "gate_80": result["gate_80"],
                "remote_branch_present": result["remote_branch_present"],
                "candidate_jobs_verified": result["candidate_jobs_verified"],
                "push": result["push"],
            },
            indent=2,
        )
    )
