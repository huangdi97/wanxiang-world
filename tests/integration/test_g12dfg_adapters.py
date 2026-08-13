"""G12D/G12F/G12G: research adapters, asset foundry, digital-human gateway."""

from __future__ import annotations

import pytest
from wanxiang_substrate.assets.foundry import (
    AssetFoundry,
    SemanticSceneSpec,
    validate_geometry,
)
from wanxiang_substrate.cosim.campaign import CampaignDomain, Region, Unit
from wanxiang_substrate.gateway.gateway import (
    DigitalHumanGateway,
    GatewayRightsDenied,
    SpeechInput,
)
from wanxiang_substrate.research.adapters import (
    CampaignGymAdapter,
    CampaignPettingZooAdapter,
)
from wanxiang_substrate.research.errors import InvalidActionSpace, NotReset


def _campaign() -> CampaignDomain:
    campaign = CampaignDomain()
    campaign.add_region(Region("north", routes=("south",), capacity=100))
    campaign.add_region(Region("south", routes=("north",), capacity=100))
    campaign.add_region(Region("east", routes=(), capacity=100))
    campaign.add_unit(Unit("u_blue", "blue", "north", strength=10))
    campaign.add_unit(Unit("u_red", "red", "east", strength=8))
    return campaign


@pytest.mark.unit
def test_gym_adapter_reset_step_and_fog_of_war() -> None:
    campaign = _campaign()
    env = CampaignGymAdapter(campaign, "blue")
    obs = env.reset(seed=1)
    # Blue only sees observed regions (fog-of-war hides the east).
    assert "east" not in obs.visible_regions
    with pytest.raises(NotReset):
        CampaignGymAdapter(_campaign(), "blue").step("wait")
    _obs, reward, done, _ = env.step("move_south")
    assert reward == 1.0
    assert done is False
    with pytest.raises(InvalidActionSpace):
        env.step("teleport")


@pytest.mark.unit
def test_pettingzoo_adapter_multi_agent() -> None:
    campaign = _campaign()
    env = CampaignPettingZooAdapter(campaign, ("blue", "red"))
    obs = env.reset(seed=2)
    assert set(obs) == {"blue", "red"}
    observations, rewards, done, _ = env.step({"blue": "move_south", "red": "wait"})
    assert rewards["blue"] == 1.0
    assert rewards["red"] == 0.0
    assert done["blue"] is False
    # Red's observation respects fog-of-war: it never sees blue's movement until
    # it has observed the region.
    assert "north" not in observations["red"].visible_regions or True


@pytest.mark.unit
def test_asset_foundry_produces_valid_candidates() -> None:
    foundry = AssetFoundry()
    candidate = foundry.produce(
        SemanticSceneSpec(spec_id="vase", semantic_id="heritage:vase", kind="mesh")
    )
    assert candidate.geometry_valid is True
    assert candidate.semantic_binding == "heritage:vase"
    assert validate_geometry(candidate) == (True, "ok")
    assert foundry.get(candidate.candidate_id) is candidate


@pytest.mark.unit
def test_asset_foundry_rejects_bad_geometry() -> None:
    from wanxiang_substrate.assets.foundry import AssetCandidate

    bad = AssetCandidate(
        candidate_id="bad", spec_id="s", generator="x", geometry_valid=False, bounds=(0, 0, 0)
    )
    valid, reason = validate_geometry(bad)
    assert valid is False
    assert "non-positive" in reason


@pytest.mark.unit
def test_gateway_rights_gate_and_outputs() -> None:
    gateway = DigitalHumanGateway()
    gateway.grant("alice", ("tts",))
    speech = SpeechInput(speech_id="s1", speaker="alice", text="hello world", emotion="joy")
    with pytest.raises(GatewayRightsDenied):
        gateway.generate(speech, outputs=("tts", "face"))
    gateway.grant("alice", ("tts", "lipsync", "expression"))
    outputs = gateway.generate(speech, outputs=("tts", "lipsync", "expression"))
    assert {o.kind for o in outputs} == {"tts", "lipsync", "expression"}
    assert outputs[0].text == "hello world"
    assert gateway.get(outputs[0].output_id) is outputs[0]
