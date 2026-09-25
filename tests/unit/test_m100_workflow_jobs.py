"""Guards the Gate 79 required-job derivation.

The Stable preflight predicate previously compared hard-coded job-id literals
against GitHub's *display* names, which can never match for the jobs whose
`name:` is overridden in `ci.yml`. That made Gate 79 unsatisfiable; these tests
pin the workflow-derived mapping instead.
"""

from __future__ import annotations

from pathlib import Path

from scripts.m100_workflow_jobs import (
    expected_job_names,
    required_display_names,
    required_job_ids,
)

CI_WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "ci.yml"


def test_ci_workflow_job_ids_are_derived() -> None:
    assert required_job_ids(CI_WORKFLOW) == (
        "api-sdk",
        "postgres",
        "python",
        "release-smoke",
        "safety",
        "ts",
    )


def test_ci_workflow_display_names_match_github_job_names() -> None:
    # These are the names GitHub reports for the required run; they are what the
    # candidate-run probe must match, so they are pinned explicitly here.
    assert required_display_names(CI_WORKFLOW) == (
        "API / package / SDK generation + drift",
        "PostgreSQL migration + integration",
        "Release build + clean-room certification smoke",
        "Repository safety / secret scan / forbidden tracked files",
        "python",
        "ts",
    )


def test_job_without_name_override_falls_back_to_its_id(tmp_path: Path) -> None:
    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        "name: ci\n"
        "jobs:\n"
        "  plain:\n"
        "    runs-on: ubuntu-latest\n"
        "  renamed:\n"
        "    name: Human readable job\n"
        "    runs-on: ubuntu-latest\n"
        "on:\n"
        "  push:\n",
        encoding="utf-8",
    )

    assert expected_job_names(workflow) == {
        "plain": "plain",
        "renamed": "Human readable job",
    }


def test_trailing_workflow_keys_are_not_treated_as_jobs(tmp_path: Path) -> None:
    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        "jobs:\n  only:\n    runs-on: ubuntu-latest\npermissions:\n  contents: read\n",
        encoding="utf-8",
    )

    assert expected_job_names(workflow) == {"only": "only"}
