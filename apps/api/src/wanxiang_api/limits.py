"""API abuse controls (G16F): rate limiting + payload size guard.

Rate limiting uses a simple fixed-window token bucket keyed by caller identity.
Payload size is enforced for the sensitive write endpoints. These are
server-side controls; frontend hiding is never accepted as authorization.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

MAX_PAYLOAD_BYTES = 64 * 1024


class RateLimited(Exception):
    def __init__(self, retry_after_seconds: int = 1) -> None:
        self.retry_after_seconds = retry_after_seconds
        super().__init__("rate limit exceeded")


class PayloadTooLarge(Exception):
    def __init__(self, size: int, limit: int = MAX_PAYLOAD_BYTES) -> None:
        self.size = size
        self.limit = limit
        super().__init__(f"payload {size} bytes exceeds limit {limit}")


@dataclass
class RateLimiter:
    """Fixed-window token bucket keyed by caller identity."""

    limit: int
    window_seconds: float = 60.0
    _buckets: dict[str, list[float]] = field(default_factory=dict[str, list[float]])

    def allow(self, key: str, now: float | None = None) -> bool:
        now = now if now is not None else time.monotonic()
        bucket = [t for t in self._buckets.get(key, []) if now - t < self.window_seconds]
        if len(bucket) >= self.limit:
            self._buckets[key] = bucket
            return False
        bucket.append(now)
        self._buckets[key] = bucket
        return True

    def check(self, key: str) -> None:
        if not self.allow(key):
            raise RateLimited(retry_after_seconds=int(self.window_seconds))

    def reset(self) -> None:
        """Clear the fixed-window buckets (test isolation; production state reset)."""
        self._buckets.clear()


def check_payload_size(payload: object) -> None:
    size = len(repr(payload).encode("utf-8"))
    if size > MAX_PAYLOAD_BYTES:
        raise PayloadTooLarge(size)
