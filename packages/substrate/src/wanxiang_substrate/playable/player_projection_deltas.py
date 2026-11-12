"""Consumer-language consequence helpers for the Player surface.

The Player must be able to say what changed without exposing canonical
internals: no entity ids, digests, revisions or raw component paths reach the
browser, and every shown field comes from a small allowlist. Nothing here can
write to the world; it is a read-only projection helper.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.event import CommittedEvent

from wanxiang_substrate.playable.player_i18n import _PlayerCopy
from wanxiang_substrate.playable.player_projection_labels import (
    _CATEGORY_KEYS,
    _STATUS_KEYS,
)
from wanxiang_substrate.playable.state_diff import DiffChange

# Field leaves a player may read, mapped to existing catalog label keys.
_DELTA_FIELD_LABELS = {
    "status": "status_label",
    "condition": "status_label",
    "location": "location_label",
    "place": "location_label",
    "position": "position_label",
    "name": "name_label",
    "display_name": "name_label",
    "weather": "weather_label",
    "environment": "environment_label",
}
# A field whose path mentions any of these is never shown to a player.
_UNSAFE_KEY_TOKENS = (
    "id",
    "sha",
    "digest",
    "hash",
    "revision",
    "token",
    "secret",
    "key",
)
_MAX_DELTAS = 3


def _is_scalar(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _shown_value(value: object, copy: _PlayerCopy) -> str:
    if value is None or (isinstance(value, str) and not value.strip()):
        return copy.text("delta_absent")
    if isinstance(value, str):
        status_key = _STATUS_KEYS.get(value)
        return copy.text(status_key) if status_key else value
    if isinstance(value, bool):
        return copy.text("delta_yes") if value else copy.text("delta_no")
    return str(value)


def _field_leaf(key: str) -> str | None:
    parts = [part for part in key.casefold().split(".") if part]
    if len(parts) >= 2 and parts[-1] in {"value", "text", "label"}:
        parts = parts[:-1]
    for part in reversed(parts):
        if part in _DELTA_FIELD_LABELS:
            return part
    return None


def _consumer_deltas(change: DiffChange, copy: _PlayerCopy) -> list[dict[str, str]]:
    """Return a bounded, localized before -> after list for one diff change."""

    before = dict(change.before)
    after = dict(change.after)
    rows: list[dict[str, str]] = []
    for key in sorted(set(before) | set(after)):
        folded = key.casefold()
        if any(token in folded for token in _UNSAFE_KEY_TOKENS):
            continue
        leaf = _field_leaf(key)
        if leaf is None:
            continue
        old = before.get(key)
        new = after.get(key)
        if old == new or not (_is_scalar(old) and _is_scalar(new)):
            continue
        rows.append(
            {
                "label": copy.text(_DELTA_FIELD_LABELS[leaf]),
                "before": _shown_value(old, copy),
                "after": (
                    copy.text("delta_removed")
                    if change.kind == "removed"
                    else _shown_value(new, copy)
                ),
            }
        )
        if len(rows) >= _MAX_DELTAS:
            break
    return rows


def _status_change(change: DiffChange, copy: _PlayerCopy) -> tuple[str, str] | None:
    """Return (before, after) when a consumer-visible status actually changed."""

    before = dict(change.before)
    after = dict(change.after)
    field = next(
        (
            key
            for key in sorted(set(before) | set(after))
            if key.casefold().endswith("status.value") and before.get(key) != after.get(key)
        ),
        None,
    )
    if field is None:
        return None
    old = before.get(field)
    new = after.get(field)
    if not isinstance(new, str) or not new.strip():
        return None
    if old is None or (isinstance(old, str) and not old.strip()):
        return None
    if not _is_scalar(old):
        return None
    return _shown_value(old, copy), _shown_value(new, copy)


def _operation_fields(event: CommittedEvent) -> list[tuple[str, object]]:
    fields: list[tuple[str, object]] = []
    for operation in event.delta.operations:
        if not isinstance(operation, (EntityCreate, EntityUpdate)):
            continue
        for component in operation.components:
            for key, value in component.fields.items():
                fields.append((f"{component.component_type}.{key}", value))
    return fields


def _chronicle_place(event: CommittedEvent, names: dict[str, str]) -> str:
    """Source-grounded place of a record, resolved through known display names."""

    for key, value in _operation_fields(event):
        folded = key.casefold()
        if not any(token in folded for token in ("place", "location")):
            continue
        if any(token in folded for token in ("id", "sha", "digest", "hash", "revision")):
            continue
        if isinstance(value, str) and value.strip():
            return names.get(value.strip(), value.strip())
    return ""


def _chronicle_who(
    event: CommittedEvent,
    actor_id: str,
    names: dict[str, str],
    copy: _PlayerCopy,
) -> str:
    if event.actor_id is None:
        return ""
    actor = event.actor_id.value
    if actor_id and actor == actor_id:
        return copy.text("chronicle_who_you")
    return names.get(actor, "")


def _chronicle_detail(event: CommittedEvent, names: dict[str, str], copy: _PlayerCopy) -> str:
    """One concrete consequence sentence derived only from the committed event.

    The same event therefore produces the same sentence in the live projection
    and in a replay of that tick, and no before-value is invented.
    """

    for operation in event.delta.operations:
        if not isinstance(operation, (EntityCreate, EntityUpdate)):
            continue
        subject = names.get(operation.entity_id.value, "")
        if not subject:
            continue
        for component in operation.components:
            for key, value in component.fields.items():
                if not key.casefold().endswith("status.value") or not isinstance(value, str):
                    continue
                status_key = _STATUS_KEYS.get(value)
                return copy.render(
                    "change_status",
                    subject=subject,
                    status=copy.text(status_key) if status_key else value,
                )
    return ""


def _chronicle_card(
    event: CommittedEvent,
    actor_id: str,
    copy: _PlayerCopy,
    names: dict[str, str] | None = None,
    detail: str = "",
) -> dict[str, object]:
    operations = event.delta.operations
    summary = copy.text("chronicle_progress")
    if event.actor_id is not None and event.actor_id.value == actor_id:
        summary = copy.text("chronicle_action")
    elif any(isinstance(item, EntityCreate) for item in operations):
        summary = copy.text("chronicle_new_fact")
    elif any(isinstance(item, EntityUpdate) for item in operations):
        summary = copy.text("chronicle_status_change")
    elif any(isinstance(item, RelationCreate) for item in operations):
        summary = copy.text("chronicle_new_relation")
    elif any(isinstance(item, (EntityDelete, RelationDelete)) for item in operations):
        summary = copy.text("chronicle_ended_fact")
    known = names or {}
    return {
        "time": event.world_time.ticks,
        "summary": summary,
        "detail": detail or _chronicle_detail(event, known, copy),
        "who": _chronicle_who(event, actor_id, known, copy),
        "place": _chronicle_place(event, known),
    }


def _change_card(change: DiffChange, names: dict[str, str], copy: _PlayerCopy) -> dict[str, object]:
    fields = dict(change.after)
    subject = names.get(change.subject_id, copy.text("entity_world"))
    status = next(
        (value for key, value in fields.items() if key.casefold().endswith("status.value")),
        None,
    )
    category = copy.text(_CATEGORY_KEYS.get(change.category, "category_state"))
    transition = _status_change(change, copy)
    if transition is not None:
        summary = copy.render(
            "change_status_from",
            subject=subject,
            before=transition[0],
            after=transition[1],
        )
    elif isinstance(status, str):
        status_key = _STATUS_KEYS.get(status)
        shown_status = copy.text(status_key) if status_key else status
        summary = copy.render("change_status", subject=subject, status=shown_status)
    elif change.kind == "removed":
        summary = copy.render("change_removed", subject=subject, category=category)
    else:
        summary = copy.render("change_updated", subject=subject, category=category)
    return {
        "kind": change.kind,
        "category": category,
        "summary": summary,
        "deltas": _consumer_deltas(change, copy),
    }
