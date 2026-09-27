"""Typed error taxonomy for the Capability Foundry.

The foundry turns an external artifact into a *candidate* capability package,
verifies it and admits it into a registry. Errors are split by stage so a caller
can tell an artifact-ingestion problem from a candidate-construction,
verification, registry or invocation problem.
"""

from __future__ import annotations


class FoundryError(Exception):
    """Base class for every Capability Foundry error."""


class ArtifactError(FoundryError):
    """A package, provenance record or declared value is malformed or inadmissible."""


class CandidateError(FoundryError):
    """A provider could not honestly build the requested candidate."""


class VerificationError(FoundryError):
    """A verification contract is inconsistent.

    This is distinct from a case that ran and failed: failed cases are data on a
    CaseResult, not an exception.
    """


class RegistryError(FoundryError):
    """A package was refused admission or a registry operation is invalid."""


class InvocationError(FoundryError):
    """An invocation was requested for a capability that is not invocable."""
