"""Executable extension trust policy (G04A): default deny for untrusted."""

from __future__ import annotations

from wanxiang_substrate.packages.errors import UntrustedExecutable
from wanxiang_substrate.packages.model import TRUSTED, TrustClass

# Known executable-capable extensions.
_EXECUTABLE_EXTENSIONS = frozenset({".py", ".pyc", ".js", ".wasm", ".dll", ".so", ".exe"})


class ExecutableExtensionPolicy:
    """Decides whether an executable extension may run for a trust class.

    Trusted packages may execute declared known extensions; untrusted packages
    are denied by default and may never register an executable resolver.
    """

    @staticmethod
    def allows(trust: TrustClass, extension: str) -> bool:
        if trust == TRUSTED:
            return extension.lower() in _EXECUTABLE_EXTENSIONS
        return False

    @staticmethod
    def require_executable(trust: TrustClass, extension: str) -> None:
        if not ExecutableExtensionPolicy.allows(trust, extension):
            raise UntrustedExecutable(
                f"executable extension {extension!r} is not allowed for {trust!r}"
            )
