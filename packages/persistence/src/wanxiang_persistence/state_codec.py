"""Canonical state codec (re-exported from the runtime).

The authoritative canonical-state serialization lives with the state type in
`wanxiang_runtime.state`; persistence and API layers both use it.
"""

from __future__ import annotations

from wanxiang_runtime.state import state_from_primitive, state_to_primitive

__all__ = ["state_from_primitive", "state_to_primitive"]
