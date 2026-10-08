"""Pure consistency checks between provider outputs and canonical read models."""

from __future__ import annotations

from wanxiang_domain.delta import EntityUpdate
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.consistency_models import (
    RealityConsistencyResult,
    RealityConsistencyStatus,
    RealityOutputKind,
    RealityReconciliationProposal,
    ReconciliationAction,
)
from wanxiang_substrate.world_lab.physical_models import PhysicalSnapshot
from wanxiang_substrate.world_lab.physical_outputs import PhysicalResolution
from wanxiang_substrate.world_lab.visual_models import VisualSceneState
from wanxiang_substrate.world_lab.visual_outputs import VisualProjectionFrame


class RealityConsistencyChecker:
    """Compare immutable reality snapshots without applying provider output."""

    def check(
        self,
        canonical: VisualSceneState | PhysicalSnapshot,
        observed: VisualProjectionFrame | PhysicalResolution,
    ) -> RealityConsistencyResult:
        if type(canonical) is VisualSceneState and type(observed) is VisualProjectionFrame:
            return self.check_visual(canonical, observed)
        if type(canonical) is PhysicalSnapshot and type(observed) is PhysicalResolution:
            return self.check_physical(canonical, observed)
        raise ContractError("canonical and provider output kinds do not match")

    def check_visual(
        self,
        scene: VisualSceneState,
        frame: VisualProjectionFrame,
    ) -> RealityConsistencyResult:
        mismatches: list[str] = []
        if frame.scene_ref != scene.scene_ref:
            mismatches.append("scene_ref_mismatch")
        if frame.snapshot_ref != scene.snapshot_ref:
            mismatches.append("snapshot_ref_mismatch")
        if frame.snapshot_revision != scene.revision:
            mismatches.append("stale_revision")
        if frame.state_hash != scene.state_hash:
            mismatches.append("state_hash_mismatch")
        if frame.status != "projected":
            mismatches.append("projection_not_projected")
        self._check_visual_objects(scene, frame, mismatches)
        if not set(frame.event_refs).issubset(scene.event_refs):
            mismatches.append("unknown_event_ref")
        if not {asset.asset_id for asset in frame.asset_refs}.issubset(
            {asset.asset_id for asset in scene.asset_refs}
        ):
            mismatches.append("unknown_asset_ref")
        stale_codes = {"scene_ref_mismatch", "snapshot_ref_mismatch", "stale_revision"}
        rejected_codes = {"projection_not_projected"}
        status = self._status(mismatches, stale_codes, rejected_codes)
        return self._result(
            output_kind="visual_projection",
            status=status,
            canonical_ref=scene.snapshot_ref,
            canonical_revision=scene.revision,
            canonical_state_hash=scene.state_hash,
            observed_ref=frame.frame_ref,
            observed_revision=frame.snapshot_revision,
            observed_state_hash=frame.state_hash,
            mismatch_codes=mismatches,
        )

    def check_physical(
        self,
        snapshot: PhysicalSnapshot,
        resolution: PhysicalResolution,
    ) -> RealityConsistencyResult:
        mismatches: list[str] = []
        if resolution.snapshot_ref != snapshot.snapshot_ref:
            mismatches.append("snapshot_ref_mismatch")
        if resolution.snapshot_revision != snapshot.revision:
            mismatches.append("stale_revision")
        if resolution.status != "resolved":
            mismatches.append("resolution_not_resolved")
        body_refs = {body.body_ref for body in snapshot.bodies}
        if any(
            isinstance(operation, EntityUpdate) and operation.entity_id.value not in body_refs
            for operation in resolution.proposed_delta.operations
        ):
            mismatches.append("unknown_physical_entity")
        stale_codes = {"snapshot_ref_mismatch", "stale_revision"}
        rejected_codes = {"resolution_not_resolved"}
        status = self._status(mismatches, stale_codes, rejected_codes)
        return self._result(
            output_kind="physical_resolution",
            status=status,
            canonical_ref=snapshot.snapshot_ref,
            canonical_revision=snapshot.revision,
            canonical_state_hash=snapshot.state_hash,
            observed_ref=resolution.resolution_id,
            observed_revision=resolution.snapshot_revision,
            observed_state_hash=None,
            mismatch_codes=mismatches,
        )

    @staticmethod
    def _check_visual_objects(
        scene: VisualSceneState,
        frame: VisualProjectionFrame,
        mismatches: list[str],
    ) -> None:
        objects = {item.object_ref: item for item in scene.objects}
        for projected in frame.objects:
            source = objects.get(projected.object_ref)
            if source is None:
                mismatches.append("unknown_object_ref")
                continue
            if (
                source.entity_ref != projected.entity_ref
                or source.position != projected.position
                or source.asset_ref != projected.asset_ref
            ):
                mismatches.append("object_state_mismatch")

    @staticmethod
    def _status(
        mismatches: list[str],
        stale_codes: set[str],
        rejected_codes: set[str],
    ) -> RealityConsistencyStatus:
        if any(code in stale_codes for code in mismatches):
            return "stale"
        if any(code in rejected_codes for code in mismatches):
            return "rejected"
        return "divergent" if mismatches else "consistent"

    @classmethod
    def _result(
        cls,
        *,
        output_kind: RealityOutputKind,
        status: RealityConsistencyStatus,
        canonical_ref: str,
        canonical_revision: int,
        canonical_state_hash: str,
        observed_ref: str,
        observed_revision: int,
        observed_state_hash: str | None,
        mismatch_codes: list[str],
    ) -> RealityConsistencyResult:
        codes = tuple(sorted(set(mismatch_codes)))
        identity = {
            "output_kind": output_kind,
            "status": status,
            "canonical_ref": canonical_ref,
            "canonical_revision": canonical_revision,
            "canonical_state_hash": canonical_state_hash,
            "observed_ref": observed_ref,
            "observed_revision": observed_revision,
            "observed_state_hash": observed_state_hash,
            "mismatch_codes": list(codes),
        }
        result_ref = "consistency:" + semantic_sha256(identity)
        action: ReconciliationAction
        if status == "consistent":
            action = "retain"
            reason = "provider output provenance matches the canonical read model"
        elif status == "stale":
            action = (
                "refresh_projection" if output_kind == "visual_projection" else "recompute_physical"
            )
            reason = "provider output must be recomputed from the current canonical snapshot"
        else:
            action = "review"
            reason = "provider output diverges from or does not represent canonical reality"
        evidence_refs = (
            f"canonical:{canonical_ref}",
            f"observed:{observed_ref}",
            f"consistency:{result_ref}",
        )
        proposal_digest = semantic_sha256(
            {"result_ref": result_ref, "status": status, "action": action}
        )
        proposal = RealityReconciliationProposal(
            proposal_ref="reconcile:" + proposal_digest,
            output_kind=output_kind,
            status=status,
            action=action,
            canonical_ref=canonical_ref,
            canonical_revision=canonical_revision,
            observed_ref=observed_ref,
            observed_revision=observed_revision,
            reason=reason,
            evidence_refs=evidence_refs,
        )
        return RealityConsistencyResult(
            result_ref=result_ref,
            output_kind=output_kind,
            status=status,
            canonical_ref=canonical_ref,
            canonical_revision=canonical_revision,
            canonical_state_hash=canonical_state_hash,
            observed_ref=observed_ref,
            observed_revision=observed_revision,
            observed_state_hash=observed_state_hash,
            mismatch_codes=codes,
            proposal=proposal,
            evidence_refs=evidence_refs,
        )


__all__ = ["RealityConsistencyChecker"]
