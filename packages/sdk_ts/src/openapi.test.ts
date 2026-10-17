import { describe, expect, it } from "vitest";

import contract from "./openapi-contract.json";
import { API_VERSION_POLICY, parseOpenApi, type OpenApiDocument } from "./openapi.js";

describe("G13D openapi contract", () => {
  it("parses the exported server contract deterministically", () => {
    const ops = parseOpenApi(contract as unknown as OpenApiDocument);
    expect(ops.length).toBe(86);
    const again = parseOpenApi(contract as unknown as OpenApiDocument);
    expect(JSON.stringify(ops)).toBe(JSON.stringify(again));
  });

  it("documents the real server vocabulary", () => {
    const ops = parseOpenApi(contract as unknown as OpenApiDocument);
    const ids = ops.map((o) => o.operationId);
    for (const expected of [
      "create_world_worlds_post",
      "get_world_worlds__instance_id__get",
      "get_state_worlds__instance_id__state_get",
      "get_events_worlds__instance_id__events_get",
      "submit_action_worlds__instance_id__actions_post",
      "create_branch_worlds__instance_id__branches_post",
      "compare_worlds__instance_id__branches_compare_post",
      "checkpoint_worlds__instance_id__checkpoint_post",
      "replay_worlds__instance_id__replay_post",
      "healthz_healthz_get",
      "player_plaza_experience_player_plaza_get",
      "player_world_detail_experience_player_worlds__profile_id__get",
      "player_panorama_generation_status_experience_player_worlds__profile_id__panoramas_get",
      "player_upgrade_visual_place_to_panorama_experience_player_worlds__profile_id__panoramas_post",
      "player_enter_world_experience_player_worlds__profile_id__enter_post",
      "player_submit_spatial_place_experience_player_worlds__profile_id__spatial_post",
      "player_poll_spatial_place_experience_player_worlds__profile_id__spatial__submission_id__get",
      "player_action_instance_experience_player_instances__instance_id__action_post",
      "player_replay_instance_experience_player_instances__instance_id__replay_get",
      "player_instance_history_experience_player_instances__instance_id__history_get",
      "player_fork_worldline_experience_player_instances__instance_id__fork_post",
      "player_list_worldlines_experience_player_instances__instance_id__worldlines_get",
      "player_compare_worldlines_experience_player_instances__instance_id__compare_get",
    ]) {
      expect(ids).toContain(expected);
    }
  });

  it("documents the version policy", () => {
    expect(API_VERSION_POLICY.current).toBe("v1");
    expect(API_VERSION_POLICY.generated).toContain("deterministic");
  });
});
