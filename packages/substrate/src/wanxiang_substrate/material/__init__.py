"""Material substrate: items, containers, custody, information payloads (G02C)."""

from wanxiang_substrate.material.components import (
    CONTAINED_COMPONENT,
    CONTAINER_COMPONENT,
    CUSTODY_COMPONENT,
    INFO_PAYLOAD_COMPONENT,
    ITEM_COMPONENT,
    OWNERSHIP_COMPONENT,
)
from wanxiang_substrate.material.errors import (
    ContainerFull,
    ContainmentCycle,
    InvalidMaterialState,
    MaterialError,
    NotCustodian,
    PayloadAlreadyRead,
)
from wanxiang_substrate.material.fixture import build_package_fixture_commands
from wanxiang_substrate.material.model import (
    Containment,
    Custody,
    DamageState,
    InfoPayload,
    ItemState,
    MaterialItem,
    Ownership,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import register_material_resolvers

__all__ = [
    "CONTAINED_COMPONENT",
    "CONTAINER_COMPONENT",
    "ContainerFull",
    "Containment",
    "ContainmentCycle",
    "CUSTODY_COMPONENT",
    "Custody",
    "DamageState",
    "INFO_PAYLOAD_COMPONENT",
    "ITEM_COMPONENT",
    "InfoPayload",
    "InvalidMaterialState",
    "ItemState",
    "MaterialError",
    "MaterialItem",
    "MaterialQuery",
    "NotCustodian",
    "OWNERSHIP_COMPONENT",
    "Ownership",
    "PayloadAlreadyRead",
    "build_package_fixture_commands",
    "register_material_resolvers",
]
