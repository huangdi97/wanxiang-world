"""Asset storage errors (G16D)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class AssetStoreError(WanxiangError):
    code = "asset_store_error"


class AssetNotFound(AssetStoreError):
    code = "asset_not_found"


class AssetCorrupt(AssetStoreError):
    code = "asset_corrupt"


class AssetRightsDenied(AssetStoreError):
    code = "asset_rights_denied"
