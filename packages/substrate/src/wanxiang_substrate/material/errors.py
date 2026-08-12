"""Structured material error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class MaterialError(WanxiangError):
    """Base error for material substrate failures."""

    code = "material_error"


class NotCustodian(MaterialError):
    code = "not_custodian"


class ContainerFull(MaterialError):
    code = "container_full"


class ContainmentCycle(MaterialError):
    code = "containment_cycle"


class InvalidMaterialState(MaterialError):
    code = "invalid_material_state"


class PayloadAlreadyRead(MaterialError):
    code = "payload_already_read"
