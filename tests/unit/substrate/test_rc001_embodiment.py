"""G36F: embodiment + ShadowPolicy handoff with control modes (mechanism; synthetic).

Embodiment of an actor key (e.g. lin_daiyu role target) with
intent/co-drive/full-control modes; ShadowPolicy never makes major decisions.
No fabricated canon content.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.session.control import ShadowPolicy
from wanxiang_substrate.session.embodiment import (
    EmbodimentController,
    major_decision,
)
from wanxiang_substrate.session.errors import LeaseConflict, ShadowCannotCommit
from wanxiang_substrate.session.model import Session
from wanxiang_substrate.session.service import LeaseService

INSTANCE = WorldInstanceId("wld_rc001")


def _session(session_id: str = "ses_human") -> Session:
    return Session(
        session_id=session_id,
        controller="human",
        instance_id=INSTANCE,
        mode="embody",
        created_seq=0,
    )


@pytest.mark.unit
def test_acquire_lease_under_full_control() -> None:
    controller = EmbodimentController()
    state = controller.acquire(
        _session(),
        "lin_daiyu",
        lease_id="lease_1",
        mode="full_control",
        acquired_seq=10,
        expires_seq=100,
    )
    assert state.control_mode == "full_control"
    assert state.lease_active is True
    events = controller.events("lin_daiyu")
    assert len(events) == 1
    assert events[0].event_type == "acquire"
    assert events[0].control_mode == "full_control"


@pytest.mark.unit
def test_mode_change_intent_co_drive() -> None:
    controller = EmbodimentController()
    controller.acquire(
        _session(),
        "lin_daiyu",
        lease_id="lease_1",
        mode="intent",
        acquired_seq=10,
        expires_seq=100,
    )
    co = controller.set_mode("lin_daiyu", "co_drive", at_seq=11)
    assert co.control_mode == "co_drive"
    kinds = [e.event_type for e in controller.events("lin_daiyu")]
    assert kinds == ["acquire", "mode_change"]


@pytest.mark.unit
def test_release_hands_back_to_autonomous() -> None:
    controller = EmbodimentController()
    controller.acquire(
        _session(),
        "lin_daiyu",
        lease_id="lease_1",
        mode="full_control",
        acquired_seq=10,
        expires_seq=100,
    )
    released = controller.release("lin_daiyu", "lease_1", released_seq=20)
    assert released.lease_active is False
    assert released.controller_session is None
    assert controller.events("lin_daiyu")[-1].event_type == "release"
    # Lease released: no active primary controller.
    leases = LeaseService()
    assert leases.primary_controller("lin_daiyu") is None


@pytest.mark.unit
def test_shadow_never_makes_major_decisions() -> None:
    shadow = ShadowPolicy()
    with pytest.raises(ShadowCannotCommit):
        major_decision("lin_daiyu", "嫁娶", advice_seq=1)
    # Advice is recorded in the advice channel but never committed.
    advice = shadow.advise("lin_daiyu", "suggestion", advice_seq=2)
    assert advice
    with pytest.raises(ShadowCannotCommit):
        shadow.commit("anything")


@pytest.mark.unit
def test_embodiment_requires_embody_session() -> None:
    controller = EmbodimentController()
    observer = Session(
        session_id="ses_observer",
        controller="human",
        instance_id=INSTANCE,
        mode="observe",
        created_seq=0,
    )
    with pytest.raises(LeaseConflict):
        controller.acquire(
            observer,
            "lin_daiyu",
            lease_id="lease_1",
            mode="full_control",
            acquired_seq=10,
            expires_seq=100,
        )
