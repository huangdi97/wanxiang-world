"""Wanxiang transport layer (FastAPI routes are thin; no canonical rules)."""

from wanxiang_api.app import API_TITLE, API_VERSION, build_runtime, create_app

__version__ = "0.1.0"

__all__ = ["API_TITLE", "API_VERSION", "build_runtime", "create_app"]
