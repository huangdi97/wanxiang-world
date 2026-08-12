"""Reference adjudicators: deterministic and seeded probabilistic."""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.resolution.model import Adjudication
from wanxiang_substrate.resolution.rng import SeededRng

ADJUDICATION_SCHEMA = SchemaVersion(1)


class DeterministicTransferAdjudicator:
    """Deterministic: transfer `amount` from source to target (delta only)."""

    def __init__(self, version: int = 1) -> None:
        self.version = version

    def __call__(
        self, command: CommandEnvelope, state: InMemoryCanonicalState, seed: int
    ) -> Adjudication:
        payload = dict(command.payload)
        source_raw = payload.get("source_id")
        target_raw = payload.get("target_id")
        amount_raw = payload.get("amount")
        if (
            not isinstance(source_raw, str)
            or not isinstance(target_raw, str)
            or not isinstance(amount_raw, int)
        ):
            from wanxiang_domain.errors import ValidationRejected

            raise ValidationRejected(
                "transfer adjudication requires source_id, target_id and amount"
            )
        source = EntityId(source_raw)
        target = EntityId(target_raw)
        amount = amount_raw
        source_component = resource_component(source, resource_count(state, source) - amount)
        target_component = resource_component(target, resource_count(state, target) + amount)
        delta = ProposedWorldDelta(
            operations=(
                EntityUpdate(entity_id=source, components=(source_component,)),
                EntityUpdate(entity_id=target, components=(target_component,)),
            )
        )
        return Adjudication(
            action_type=command.action_type,
            version=self.version,
            seed=seed,
            outcome="transferred",
            delta=delta,
            explanation=f"transferred {amount} from {source.value} to {target.value}",
            provenance=(f"rule:deterministic_transfer:v{self.version}",),
            uncertainty=0.0,
        )


class GambleAdjudicator:
    """Seeded probabilistic: success with probability `success_probability`."""

    def __init__(self, version: int = 1) -> None:
        self.version = version

    def __call__(
        self, command: CommandEnvelope, state: InMemoryCanonicalState, seed: int
    ) -> Adjudication:
        payload = dict(command.payload)
        actor_raw = payload.get("actor_id")
        probability_raw = payload.get("success_probability", 0.5)
        if not isinstance(actor_raw, str) or not isinstance(probability_raw, (int, float)):
            from wanxiang_domain.errors import ValidationRejected

            raise ValidationRejected(
                "gamble adjudication requires actor_id and success_probability"
            )
        actor = EntityId(actor_raw)
        probability = float(probability_raw)
        rng = SeededRng(seed, stream=f"gamble:{command.command_id.value}")
        success = rng.chance(probability)
        delta = ProposedWorldDelta(
            operations=(
                EntityUpdate(
                    entity_id=actor,
                    components=(
                        ComponentData(
                            component_id=ComponentId(f"gamble_{actor.value}"),
                            component_type="resolution.outcome",
                            schema_version=ADJUDICATION_SCHEMA,
                            fields={"outcome": "success" if success else "failure"},
                        ),
                    ),
                ),
            )
        )
        return Adjudication(
            action_type=command.action_type,
            version=self.version,
            seed=seed,
            outcome="success" if success else "failure",
            delta=delta,
            explanation=f"gamble with p={probability} drew {'success' if success else 'failure'}",
            observability=(actor,),
            provenance=(f"rule:seeded_gamble:v{self.version}:seed{seed}",),
            uncertainty=probability if not success else 1 - probability,
        )


def resource_component(entity: EntityId, count: int) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"res_{entity.value}"),
        component_type="material.resource",
        schema_version=ADJUDICATION_SCHEMA,
        fields={"count": count},
    )


def resource_count(state: InMemoryCanonicalState, entity: EntityId) -> int:
    current = state.entity(entity)
    if current is None:
        return 0
    for component in current.components.values():
        if component.component_type == "material.resource":
            count = component.fields.get("count", 0)
            return int(count) if isinstance(count, (int, float)) else 0
    return 0
