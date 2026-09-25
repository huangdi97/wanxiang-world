"""Markdown rendering for the G103E remote-delivery / required-CI artifact."""

from __future__ import annotations

from typing import Any


def _query_rows(payload: dict[str, Any]) -> str:
    return "\n".join(
        f"| {item['name']} | {item['status']} | {item['exit_code']} |"
        for item in payload["queries"]
    )


def _job_rows(payload: dict[str, Any]) -> str:
    jobs: list[dict[str, str]] = payload["candidate_run"].get("jobs", [])
    return "\n".join(f"| {job['name']} | {job['conclusion']} |" for job in jobs)


def _run_identity(payload: dict[str, Any]) -> str:
    candidate_run = payload["candidate_run"]
    if not candidate_run:
        return "none"
    return f"`{candidate_run['database_id']}` at `{candidate_run['head_sha']}`"


def render_report(payload: dict[str, Any]) -> str:
    """Render the human-readable G103E report from the machine artifact."""
    return f"""# M100 G103E Remote Delivery / Required CI

Conclusion: `{payload["conclusion"]}`; Gate 79 ledger: `{payload["gate_79"]}`;
Gate 80: `{payload["gate_80"]}`.
Local candidate: `{payload["local_head"]}`; branch: `{payload["branch"]}`.

| Read-only query | Status | Exit |
|---|---|---:|
{_query_rows(payload)}

Required workflow jobs: `{", ".join(payload["required_jobs"])}`.
Remote branch ref: `{payload["remote_branch_sha"] or "absent"}`;
candidate branch exists remotely: `{payload["remote_branch_present"]}`;
candidate Actions run exists: `{payload["candidate_run_present"]}`;
all required jobs verified for candidate: `{payload["candidate_jobs_verified"]}`.
Candidate run identity: {_run_identity(payload)}.

| Candidate run job | Conclusion |
|---|---|
{_job_rows(payload)}

This probe is read-only and performs no push, tag creation, or GitHub Release.
The remote branch identity and candidate Actions job conclusions above are read
only from live `git ls-remote` / `gh` output; they are never inferred from local
tracking refs. Existing successful runs are retained only when their SHA is
shown in the artifact and are not substituted for this candidate.

Gate 80 stays `LOCKED` while the M95 human-player Gates 62-66 are
`USER_INPUT_REQUIRED`; this probe authorizes no Stable tag or release action.

Boundaries: IMPLEMENTED = read-only delivery/CI probe; VALIDATED = live remote
branch ref and candidate run job conclusions when present; NOT_PROVEN = anything
not returned by the live queries above; EXTERNAL_BLOCKED = unavailable remote
helper or absent candidate delivery state.

Evidence: `artifacts/v55_stable/m100/remote_delivery.json`
Reproduce: `uv run python scripts/m100_remote_delivery.py`
"""
