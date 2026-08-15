"""Material read-and-remember (G36D).

Reading a sealed payload forms an observation memory for the reader: the
existing material read transition plus an epistemic memory entity, resolved
through the single Commit Authority. Reuses material/resolver_ops.resolve_read
for the read transition (no duplicate logic).
"""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.epistemic.components import memory_component
from wanxiang_substrate.material.resolver_ops import resolve_read

ACTION_READ_AND_REMEMBER = "material.read_and_remember"


def resolve_read_and_remember(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Read a payload and form an observation memory for the reader."""
    if state is None:
        from wanxiang_domain.errors import ValidationRejected

        raise ValidationRejected("read requires current state")
    read_delta = resolve_read(command, state)
    payload = dict(command.payload)
    item_id = str(payload.get("item_id") or "")
    reader_id = str(payload.get("reader_id") or "")
    memory_id = EntityId(f"mem_read_{item_id}_{reader_id}")
    at_ticks = payload.get("at_ticks", 0)
    at_ticks_value = at_ticks if isinstance(at_ticks, int) and not isinstance(at_ticks, bool) else 0
    # The payload_ref is resolved from the read transition inputs; the memory
    # content_ref is the reader-local observation of the read item.
    content_ref = f"item:{item_id}"
    memory_create = EntityCreate(
        entity_id=memory_id,
        entity_type="epistemic.memory",
        components=(
            memory_component(
                memory_id,
                EntityId(reader_id),
                "observation",
                content_ref,
                at_ticks_value,
            ),
        ),
    )
    return ProposedWorldDelta(operations=read_delta.operations + (memory_create,))


def register_reading_resolvers(registry: ResolverRegistry) -> None:
    """Register the read-and-remember action on a resolver registry."""
    registry.register(ACTION_READ_AND_REMEMBER, resolve_read_and_remember)
