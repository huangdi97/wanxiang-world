"""Resolve host executables before an evidence runner invokes them.

On Windows the npm toolchain is exposed as `.cmd`/`.ps1` shims, and
`subprocess.run` with an argument list does not apply `PATHEXT`. A bare `pnpm`
therefore raised `WinError 2`, and the whole TypeScript gate block was silently
classified `EXTERNAL_BLOCKED` instead of being executed. Resolving argv[0] via
`shutil.which` keeps those gates real on both Windows and Linux without
changing the recorded command text.
"""

from __future__ import annotations

import shutil


def resolve(command: list[str]) -> list[str]:
    """Return `command` with argv[0] mapped to the real host executable."""
    if not command:
        return command
    executable = shutil.which(command[0])
    if executable is None:
        return command
    return [executable, *command[1:]]
