"""Structured package registry error taxonomy (G04A)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class PackageError(WanxiangError):
    """Base error for package registry failures."""

    code = "package_error"


class InvalidManifest(PackageError):
    code = "invalid_package_manifest"


class MissingDependency(PackageError):
    code = "missing_package_dependency"


class DependencyCycle(PackageError):
    code = "package_dependency_cycle"


class DependencyConflict(PackageError):
    code = "package_dependency_conflict"


class IncompatiblePackage(PackageError):
    code = "incompatible_package"


class PackageNotFound(PackageError):
    code = "package_not_found"


class UntrustedExecutable(PackageError):
    code = "untrusted_executable"
