"""Typed playable refusals (the product state is client-visible).

These are refusals of a *session* request, never canonical world failures: the
client is told what to do next instead of receiving a generic contract error.
"""

from __future__ import annotations

from wanxiang_domain.errors import ContractError


class ReplayReadOnly(ContractError):
    """The session is viewing a past world time, so it cannot commit an action.

    Replay is a read mode: while a viewer is looking at the past the server
    refuses to append an event, and the viewer must return to now first. This is
    enforced on the server because a client-side read mode cannot protect canon.
    """

    code = "replay_read_only"
    product_state = "REPLAY_READ_ONLY"
