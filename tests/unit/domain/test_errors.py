"""GOAL_01A: structured error taxonomy."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import (
    Conflict,
    CorruptEventStream,
    DuplicateCommandConflict,
    IncompatibleVersion,
    StaleRevision,
    WanxiangError,
)


@pytest.mark.unit
def test_error_codes_are_distinct() -> None:
    assert StaleRevision.code == "stale_revision"
    assert DuplicateCommandConflict.code == "duplicate_command_conflict"
    assert CorruptEventStream.code == "corrupt_event_stream"
    assert IncompatibleVersion.code == "incompatible_version"


@pytest.mark.unit
def test_conflict_hierarchy() -> None:
    assert issubclass(StaleRevision, Conflict)
    assert issubclass(DuplicateCommandConflict, Conflict)
    assert issubclass(Conflict, WanxiangError)


@pytest.mark.unit
def test_error_to_primitive_is_structured() -> None:
    error = StaleRevision("stale", details={"expected": 1, "actual": 2})
    primitive = error.to_primitive()
    assert primitive["code"] == "stale_revision"
    assert primitive["details"] == {"expected": 1, "actual": 2}
