"""Advisory process lock for a shared local visual-cache JSON index.

The lock covers cache lookup, provider call, blob write, and index replace.
This is a single-filesystem deployment adapter, not a distributed lock.
"""

from __future__ import annotations

import os
import pathlib
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def _exclusive_index_lock(path: pathlib.Path) -> Generator[None, None, None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt

            # Windows byte-range locks need a persistent byte to lock.
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
