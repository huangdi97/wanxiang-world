import { Context } from "cordis";

import type { CommitAuthority } from "./authority";
import type { ActorRule } from "./commit";
import { proposalDigest } from "./commit";

/**
 * Reference actor rules shipped with the composition host.
 *
 * A rule only proposes; it never appends. Rules are registered through the
 * authority service inside a Cordis effect, so unloading the plugin removes both
 * the rule and every runtime effect it created.
 */
export interface ActorRuleConfig {
  readonly worldlineId: string;
  readonly actorId: string;
  readonly salt: string;
}

/** Deterministic rule: the same head always yields the same proposal. */
export function makeActorRule(config: ActorRuleConfig, ruleVersion = "1"): ActorRule {
  const ruleId = `actor-rule/${config.actorId}/v${ruleVersion}`;
  const kind = `actor-rule/v${ruleVersion}/status`;
  return {
    ruleId,
    ruleVersion,
    propose: (head) => ({
      kind,
      payloadDigest: proposalDigest(ruleId, head.revision, `${kind}|${config.salt}`),
    }),
  };
}

/**
 * Counters for the lifecycle leak test.
 *
 * They are incremented inside effects and decremented in the effect's disposer,
 * so a leaked registration is visible as a non-zero value after unload.
 */
export const leakCounters = {
  timers: 0,
  listeners: 0,
  rules: 0,
};

export function actorRulePlugin(config: ActorRuleConfig, ruleVersion = "1"): (ctx: Context) => void {
  return (ctx: Context): void => {
    const authority = ctx.get("authority") as CommitAuthority | undefined;
    if (!authority) {
      throw new Error("actor-rule requires the authority service");
    }
    const rule = makeActorRule(config, ruleVersion);
    const unregister = authority.registerRule(config.worldlineId, rule);
    leakCounters.rules += 1;
    ctx.effect(() => {
      return () => {
        unregister();
        leakCounters.rules -= 1;
      };
    }, "actor-rule.registration");
    ctx.effect(() => {
      // PERFORMANCE: a real rule schedules itself; the timer exists so the
      // lifecycle test can prove it is cleared when the plugin unloads.
      const timer = setInterval(() => undefined, 60_000);
      leakCounters.timers += 1;
      return () => {
        clearInterval(timer);
        leakCounters.timers -= 1;
      };
    }, "actor-rule.timer");
    ctx.effect(() => {
      leakCounters.listeners += 1;
      return () => {
        leakCounters.listeners -= 1;
      };
    }, "actor-rule.listener");
  };
}

export function actorRuleV2Plugin(config: ActorRuleConfig): (ctx: Context) => void {
  return actorRulePlugin(config, "2");
}
