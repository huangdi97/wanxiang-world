"""Production identity boundary must never trust client-chosen user headers."""

from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app


class _TrustedOuterASGI:
    def __init__(
        self,
        app: Any,
        principal: str = "",
        roles: tuple[str, ...] = (),
    ) -> None:
        self.app = app
        self.principal = principal
        self.roles = roles

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] == "http" and self.principal:
            scope["wanxiang_authenticated_user"] = self.principal
            scope["wanxiang_authenticated_roles"] = self.roles
        await self.app(scope, receive, send)


def test_trusted_mode_denies_unverified_identity_even_with_owner_header(
    monkeypatch: Any,
) -> None:
    monkeypatch.setenv("WANXIANG_IDENTITY_MODE", "trusted")
    with TestClient(create_app()) as client:
        response = client.get("/experience/player/plaza", headers={"x-wanxiang-user": "studio"})
    assert response.status_code == 401
    assert response.json()["code"] == "trusted_identity_required"


def test_trusted_mode_overrides_spoofed_http_user_header(monkeypatch: Any) -> None:
    monkeypatch.setenv("WANXIANG_IDENTITY_MODE", "trusted")
    app = create_app()

    def trusted_probe(request: Request) -> dict[str, str]:
        return {"principal": request.headers.get("x-wanxiang-user", "")}

    app.add_api_route("/__trusted_identity_test", trusted_probe)
    with TestClient(_TrustedOuterASGI(app, "real-user")) as client:
        response = client.get("/__trusted_identity_test", headers={"x-wanxiang-user": "studio"})
    assert response.status_code == 200
    assert response.json() == {"principal": "real-user"}


def test_studio_requires_trusted_creator_role(monkeypatch: Any) -> None:
    monkeypatch.setenv("WANXIANG_IDENTITY_MODE", "trusted")
    app = create_app()
    with TestClient(_TrustedOuterASGI(app, "reader")) as client:
        denied = client.get("/studio/ui")
    assert denied.status_code == 403
    assert denied.json()["code"] == "studio_creator_role_required"

    with TestClient(_TrustedOuterASGI(app, "creator", ("creator",))) as client:
        allowed = client.get("/studio/ui")
    assert allowed.status_code == 200


def test_unknown_identity_mode_refuses_to_start(monkeypatch: Any) -> None:
    monkeypatch.setenv("WANXIANG_IDENTITY_MODE", "pretend-secure")
    try:
        create_app()
    except ValueError as error:
        assert "WANXIANG_IDENTITY_MODE" in str(error)
    else:
        raise AssertionError("unknown identity mode must fail closed")
