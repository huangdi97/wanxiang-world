"""Package, schema & dependency registry substrate (G04A)."""

from wanxiang_substrate.packages.errors import (
    DependencyConflict,
    DependencyCycle,
    IncompatiblePackage,
    InvalidManifest,
    MissingDependency,
    PackageError,
    PackageNotFound,
    UntrustedExecutable,
)
from wanxiang_substrate.packages.fixture import build_town_packages
from wanxiang_substrate.packages.install import (
    InstallRecord,
    PackageInstaller,
    export_install,
    install_export_hash,
)
from wanxiang_substrate.packages.migration import (
    CURRENT_MANIFEST_SCHEMA,
    compatible,
    migrate_manifest,
)
from wanxiang_substrate.packages.model import (
    MANIFEST_SCHEMA_VERSION,
    PackageKind,
    PackageLock,
    PackageManifest,
    SemanticVersion,
    TrustClass,
    VersionConstraint,
)
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry
from wanxiang_substrate.packages.resolver import DependencyResolver
from wanxiang_substrate.packages.sdk import (
    PUBLIC_API_POLICY,
    validate_manifest_for_authoring,
)
from wanxiang_substrate.packages.trust import ExecutableExtensionPolicy

__all__ = [
    "CURRENT_MANIFEST_SCHEMA",
    "DependencyConflict",
    "DependencyCycle",
    "DependencyResolver",
    "ExecutableExtensionPolicy",
    "IncompatiblePackage",
    "InMemoryPackageRegistry",
    "InstallRecord",
    "InvalidManifest",
    "MANIFEST_SCHEMA_VERSION",
    "MissingDependency",
    "PUBLIC_API_POLICY",
    "PackageError",
    "PackageInstaller",
    "PackageKind",
    "PackageLock",
    "PackageManifest",
    "PackageNotFound",
    "SemanticVersion",
    "TrustClass",
    "UntrustedExecutable",
    "VersionConstraint",
    "build_town_packages",
    "compatible",
    "export_install",
    "install_export_hash",
    "migrate_manifest",
    "validate_manifest_for_authoring",
]
