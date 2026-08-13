"""Command queue value objects (G06B)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.command import CommandEnvelope

SubmissionStatus = Literal["accepted", "conflict", "rejected", "duplicate"]


@dataclass(frozen=True, slots=True)
class QueuedCommand:
    """A command enqueued for serialized submission."""

    envelope: CommandEnvelope
    enqueue_seq: int


@dataclass(frozen=True, slots=True)
class SubmissionResult:
    command_id: str
    status: SubmissionStatus
    message: str = ""
    revision: int = 0
