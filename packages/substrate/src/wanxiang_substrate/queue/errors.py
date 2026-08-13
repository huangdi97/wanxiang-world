"""Command queue error taxonomy (G06B)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class QueueError(WanxiangError):
    """Base error for command queue failures."""

    code = "command_queue_error"


class QueueFull(QueueError):
    code = "command_queue_full"


class DuplicateQueuedCommand(QueueError):
    code = "duplicate_queued_command"
