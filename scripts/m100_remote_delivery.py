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
from m100_remote_delivery_report import render_report
from m100_workflow_jobs import required_display_names, required_job_ids

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "artifacts" / "v55_stable" / "m100" / "remote_delivery.json"
REPORT = ROOT / "reports" / "M100_G103E_REMOTE_DELIVERY.md"
REPO = "huangdi97/wanxiang-world"
BRANCH = "release/v5.5-stable-certification"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
# The required set is derived from the workflow definition, never hard-coded:
# ci.yml overrides several job display names, so literals cannot match.
REQUIRED_JOB_IDS = required_job_ids(WORKFLOW)
REQUIRED_JOBS = required_display_names(WORKFLOW)


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


def _ls_remote_sha(result: dict[str, Any]) -> str:
    """Return the SHA column of a live `git ls-remote` probe, or an empty string."""
    for line in str(result.get("output_tail", "")).splitlines():
        token = line.split("\t")[0].strip()
        if len(token) == 40 and all(char in "0123456789abcdef" for char in token):
            return token
    return ""


def _write(payload: dict[str, Any]) -> None:
    write_json(OUTPUT, payload)
    REPORT.write_text(render_report(payload), encoding="utf-8")


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
    remote_branch_sha = _ls_remote_sha(queries[1])
    branch_runs = _run_list(_json_output(queries[4]))
    recent_runs = _run_list(_json_output(queries[5]))
    candidate_runs = [run for run in branch_runs if run.get("headSha") == local_head]
    candidate_jobs_verified: bool = False
    candidate_job_conclusions: list[dict[str, str]] = []
    candidate_run_conclusion: str | None = None
    candidate_run_sha: str | None = None
    candidate_run_url: str | None = None
    database_id: str | int | None = None
    if candidate_runs:
        database_id = candidate_runs[0].get("databaseId")
        if not isinstance(database_id, (str, int)):
            candidate_runs = []
            database_id = None
        else:
            entry = candidate_runs[0]
            conclusion = entry.get("conclusion")
            candidate_run_conclusion = conclusion if isinstance(conclusion, str) else None
            sha = entry.get("headSha")
            candidate_run_sha = sha if isinstance(sha, str) else None
            url = entry.get("url")
            candidate_run_url = url if isinstance(url, str) else None
    if candidate_runs and database_id is not None:
        # PERFORMANCE: project the job list to a name/conclusion TSV so the
        # captured output tail cannot be truncated mid-JSON, which previously
        # made this predicate silently unsatisfiable.
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
                "jobs",
                "--jq",
                ".jobs[] | [.name, .conclusion] | @tsv",
            ],
        )
        queries.append(job_probe)
        names: set[str] = set()
        for line in str(job_probe.get("output_tail", "")).splitlines():
            parts = [part.strip() for part in line.split("\t")]
            if len(parts) != 2 or not all(parts):
                continue
            names.add(parts[0])
            candidate_job_conclusions.append({"name": parts[0], "conclusion": parts[1]})
        candidate_jobs_verified = (
            job_probe.get("exit_code") == 0
            and candidate_run_sha == local_head
            and candidate_run_conclusion == "success"
            and all(name in names for name in REQUIRED_JOBS)
        )
    remote_branch_present = bool(remote_branch_sha) or bool(remote_ref.get("object"))

    # SAFETY: the probe never asserts delivery success it did not observe. A
    # candidate is only PASS when a live remote branch ref exists AND the exact
    # local SHA has a completed run whose required jobs are all present and green.
    conclusion = "PASS" if remote_branch_present and candidate_jobs_verified else "LOCKED"
    candidate_run: dict[str, Any] = {}
    if candidate_runs:
        candidate_run = {
            "database_id": database_id,
            "head_sha": candidate_run_sha,
            "conclusion": candidate_run_conclusion,
            "url": candidate_run_url,
            "jobs": candidate_job_conclusions,
        }
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m100.remote-delivery.v1",
        "conclusion": conclusion,
        "local_head": local_head,
        "branch": BRANCH,
        "repo": REPO,
        "gate_79": gate_79,
        "gate_80": gate_80,
        "required_jobs": list(REQUIRED_JOBS),
        "required_job_ids": list(REQUIRED_JOB_IDS),
        "queries": queries,
        "remote_branch_present": remote_branch_present,
        "remote_branch_sha": remote_branch_sha,
        "candidate_run_present": bool(candidate_runs),
        "candidate_jobs_verified": candidate_jobs_verified,
        "candidate_run": candidate_run,
        "recent_remote_runs": recent_runs or [],
        "push": "NOT_PERFORMED_BY_THIS_PROBE",
        "tag": "NOT_ATTEMPTED",
        "github_release": "NOT_ATTEMPTED",
        "boundaries": {
            "implemented": ["read-only remote and required-CI delivery probe"],
            "validated": (
                ["live remote branch ref and candidate required-CI job conclusions"]
                if candidate_jobs_verified
                else ["local candidate SHA and repository workflow job declaration"]
            ),
            "not_proven": (
                [] if candidate_jobs_verified else ["candidate Actions required-job conclusions"]
            ),
            "external_blocked": (
                []
                if candidate_jobs_verified
                else ["remote branch/helper or candidate Actions identity is unavailable"]
            ),
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
