"""Tracked science capability used by the R7 reference-world qualification.

This is intentionally tiny: the point is not the arithmetic, but proving that a
real tracked artifact can be proposed, verified (golden/negative/boundary/security),
admitted, executed in the Execution Fabric and returned as Observation/Proposal
without acquiring canonical write authority.
"""

from __future__ import annotations

import os
import sys


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--security"]:
        # The reference case proves the wrapper does not depend on an injected
        # WANXIANG_SECRET. It is not a claim that PROCESS is a hostile-code sandbox.
        if os.environ.get("WANXIANG_SECRET"):
            print("unsafe")
            return 3
        print("safe")
        return 0
    if len(args) != 1:
        return 2
    try:
        value = int(args[0])
    except ValueError:
        return 2
    if value < 0:
        return 2
    print(value * 2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
