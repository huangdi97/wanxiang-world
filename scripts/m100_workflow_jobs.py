"""Derive the required CI job names from the repository workflow definition.

The Stable Gate 79 predicate must verify the candidate Actions run against the
jobs the workflow actually declares. Matching on hard-coded strings is wrong:
`ci.yml` overrides the display name of several jobs (for example the `safety`
job renders as "Repository safety / secret scan / forbidden tracked files"), so
a display-name literal would never match and the predicate could not succeed.
"""

from __future__ import annotations

import re
from pathlib import Path

_JOB_KEY = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$")
_JOB_NAME = re.compile(r"^    name:\s*(.+?)\s*$")


def expected_job_names(workflow_path: Path) -> dict[str, str]:
    """Map each workflow job id to the display name GitHub reports for it."""
    jobs: dict[str, str] = {}
    inside_jobs = False
    current: str | None = None
    for line in workflow_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("jobs:"):
            inside_jobs = True
            continue
        if not inside_jobs:
            continue
        if line and not line.startswith(" "):
            break
        key = _JOB_KEY.match(line)
        job_id = key.group(1) if key else None
        if job_id is not None:
            jobs[job_id] = job_id
            current = job_id
            continue
        label = _JOB_NAME.match(line)
        label_name = label.group(1) if label else None
        if label_name is not None and current is not None and jobs[current] == current:
            jobs[current] = label_name
    return jobs


def required_job_ids(workflow_path: Path) -> tuple[str, ...]:
    """Return the sorted workflow job ids that a candidate run must satisfy."""
    return tuple(sorted(expected_job_names(workflow_path)))


def required_display_names(workflow_path: Path) -> tuple[str, ...]:
    """Return the sorted display names of every job the workflow declares."""
    return tuple(sorted(expected_job_names(workflow_path).values()))
