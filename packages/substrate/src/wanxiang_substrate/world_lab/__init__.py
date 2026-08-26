"""World laboratory evidence contracts (M92).

The laboratory is a proposal/evidence surface over the existing runtime.  It
does not own canonical state, event history, branches, or commit authority.
"""

from wanxiang_substrate.world_lab.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    WorldRunArtifact,
    sanitize_metadata,
)

__all__ = ["ARTIFACT_SCHEMA_VERSION", "WorldRunArtifact", "sanitize_metadata"]
