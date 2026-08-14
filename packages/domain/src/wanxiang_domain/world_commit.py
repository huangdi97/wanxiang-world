"""World Commit kinds (G30F).

One CommitAuthority supports exactly three World Commit payload kinds ?
State, Ontology, Law. Runtime control changes are NOT a fourth World Commit:
they use RuntimeControlTransaction and the Runtime Control Ledger.
"""

from __future__ import annotations

from typing import Literal

from wanxiang_domain.errors import ContractError

WorldCommitKind = Literal["state", "ontology", "law"]

WORLD_COMMIT_KINDS: tuple[WorldCommitKind, ...] = ("state", "ontology", "law")

DELTA_SCHEMA_VERSION = 1


def validate_world_commit_kind(kind: object) -> WorldCommitKind:
    if kind not in WORLD_COMMIT_KINDS:
        raise ContractError(
            f"invalid World Commit kind {kind!r}; expected one of {WORLD_COMMIT_KINDS}"
        )
    return kind
