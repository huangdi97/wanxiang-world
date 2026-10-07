import {
  HarnessMethods,
  RPC_TRANSPORT_FAILURE,
  RpcProtocolError,
  RpcStdioClient,
  asJsonObject,
  type JsonFields,
  type RpcTransportOptions,
} from "./bridge_protocol";

/**
 * The frozen agent-harness protocol.
 *
 * A harness is an independent provider: it observes a read-only world view,
 * proposes, and is told what the world did with its proposal. It never receives a
 * commit capability and this module holds no canonical write path at all — the
 * decision always belongs to the caller's Commit Authority.
 */
export const HARNESS_PROTOCOL = "wanxiang.r7.agent-harness-rpc.v1";

export interface HarnessInfo {
  readonly harnessId: string;
  readonly harnessVersion: string;
  readonly kind: string;
  readonly protocol: string;
  /** True only for the official DeepSeek Harness; a reference harness reports false. */
  readonly officialDsh: boolean;
}

export type ProposalFieldValue = string | number | boolean | null;

export interface AgentProposal {
  readonly proposalId: string;
  readonly action: string;
  readonly rationaleRef: string;
  readonly payloadDigest: string;
  readonly payload: Readonly<Record<string, ProposalFieldValue>>;
}

export type HarnessDecision =
  | { readonly status: "proposed"; readonly proposal: AgentProposal; readonly reason: string }
  | { readonly status: "abstained"; readonly reason: string };

export interface HarnessObservationInput {
  readonly worldlineId: string;
  readonly revision: number;
  readonly allowedContext?: Readonly<Record<string, string>>;
}

export interface HarnessConsequence {
  readonly proposalId: string;
  readonly status: "committed" | "rejected";
  /** Optional non-sensitive detail, e.g. the rejection reason or the new revision. */
  readonly detail?: string;
}

export interface HarnessAcknowledgement {
  readonly acknowledged: true;
  readonly status: "committed" | "rejected";
}

function requireText(fields: JsonFields, key: string, what: string): string {
  const value = fields[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.${key} must be a non-empty string`);
  }
  return value;
}

function parseInfo(result: unknown): HarnessInfo {
  const fields = asJsonObject(result, "harness.info result");
  const official = fields["officialDsh"];
  if (typeof official !== "boolean") {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "harness.info officialDsh must be a boolean");
  }
  const protocol = requireText(fields, "protocol", "harness.info result");
  if (protocol !== HARNESS_PROTOCOL) {
    // COMPATIBILITY: a different protocol means the harness is not this seam.
    throw new RpcProtocolError(
      RPC_TRANSPORT_FAILURE,
      `harness speaks ${protocol}, this bridge speaks ${HARNESS_PROTOCOL}`,
    );
  }
  return {
    harnessId: requireText(fields, "harnessId", "harness.info result"),
    harnessVersion: requireText(fields, "harnessVersion", "harness.info result"),
    kind: requireText(fields, "kind", "harness.info result"),
    protocol,
    officialDsh: official,
  };
}

function parseProposalPayload(raw: unknown): Readonly<Record<string, ProposalFieldValue>> {
  if (raw === undefined) return {};
  const fields = asJsonObject(raw, "harness.decide proposal.payload");
  const payload: Record<string, ProposalFieldValue> = {};
  for (const [key, value] of Object.entries(fields)) {
    if (key.length === 0) {
      throw new RpcProtocolError(
        RPC_TRANSPORT_FAILURE,
        "harness.decide proposal.payload keys must be non-empty",
      );
    }
    if (
      value !== null
      && typeof value !== "string"
      && typeof value !== "number"
      && typeof value !== "boolean"
    ) {
      throw new RpcProtocolError(
        RPC_TRANSPORT_FAILURE,
        `harness.decide proposal.payload.${key} must be a JSON primitive`,
      );
    }
    payload[key] = value;
  }
  return payload;
}

function parseProposal(raw: unknown): AgentProposal {
  const fields = asJsonObject(raw, "harness.decide proposal");
  return {
    proposalId: requireText(fields, "proposalId", "harness.decide proposal"),
    action: requireText(fields, "action", "harness.decide proposal"),
    rationaleRef: requireText(fields, "rationaleRef", "harness.decide proposal"),
    payloadDigest: requireText(fields, "payloadDigest", "harness.decide proposal"),
    payload: parseProposalPayload(fields["payload"]),
  };
}

/**
 * Parse one decision.
 *
 * INVARIANT:
 * An ill-formed answer is a typed protocol error, never a default. A harness that
 * omits its proposal cannot be read as "abstained", because abstaining is a real
 * decision the world records.
 */
export function parseDecision(result: unknown): HarnessDecision {
  const fields = asJsonObject(result, "harness.decide result");
  const status = fields["status"];
  const reason = typeof fields["reason"] === "string" ? fields["reason"] : "";
  if (status === "abstained") {
    return { status: "abstained", reason };
  }
  if (status === "proposed") {
    return { status: "proposed", proposal: parseProposal(fields["proposal"]), reason };
  }
  throw new RpcProtocolError(
    RPC_TRANSPORT_FAILURE,
    `harness.decide status must be 'proposed' or 'abstained', got ${JSON.stringify(status)}`,
  );
}

function parseAcknowledgement(result: unknown): HarnessAcknowledgement {
  const fields = asJsonObject(result, "harness.consequence result");
  if (fields["acknowledged"] !== true) {
    throw new RpcProtocolError(
      RPC_TRANSPORT_FAILURE,
      "harness.consequence must acknowledge the announcement",
    );
  }
  const status = fields["status"];
  if (status !== "committed" && status !== "rejected") {
    throw new RpcProtocolError(
      RPC_TRANSPORT_FAILURE,
      "harness.consequence status must be 'committed' or 'rejected'",
    );
  }
  return { acknowledged: true, status };
}

/**
 * Client for one agent-harness process.
 *
 * It reuses the serialized stdio transport of the history seam, so a wedged
 * harness rejects on timeout instead of stalling the host, and a malformed answer
 * fails the call rather than being dropped. Lifecycle is owned by whoever created
 * the client: `dispose()` is a no-op for an injected client.
 */
export class AgentHarnessClient {
  private readonly client: RpcStdioClient;
  private readonly ownsClient: boolean;

  constructor(options: RpcTransportOptions, client?: RpcStdioClient) {
    this.client = client ?? new RpcStdioClient(options);
    this.ownsClient = client === undefined;
  }

  async info(): Promise<HarnessInfo> {
    return parseInfo(await this.client.call(HarnessMethods.info, {}));
  }

  /** Ask the harness what it proposes for a read-only world view. */
  async decide(observation: HarnessObservationInput): Promise<HarnessDecision> {
    if (!Number.isInteger(observation.revision) || observation.revision < 0) {
      throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "observation.revision must be >= 0");
    }
    const allowedContext: Record<string, string> = { ...observation.allowedContext };
    const params: JsonFields = {
      observation: {
        worldlineId: observation.worldlineId,
        revision: observation.revision,
        allowedContext,
      },
    };
    return parseDecision(await this.client.call(HarnessMethods.decide, params));
  }

  /** Tell the harness what the world decided. Sends no capability and no world state. */
  async announce(consequence: HarnessConsequence): Promise<HarnessAcknowledgement> {
    const params: JsonFields =
      consequence.detail === undefined
        ? { proposalId: consequence.proposalId, status: consequence.status }
        : {
            proposalId: consequence.proposalId,
            status: consequence.status,
            detail: consequence.detail,
          };
    return parseAcknowledgement(await this.client.call(HarnessMethods.consequence, params));
  }

  async dispose(): Promise<void> {
    if (this.ownsClient) {
      await this.client.dispose();
    }
  }
}

/**
 * A harness proposal as the host sees it: proposal-only data.
 *
 * SAFETY:
 * This type deliberately carries no capability and no event payload — it is input
 * to the host's single commit path, which still requires a Commit Authority
 * capability of its own. Nothing here can append to canonical history.
 */
export interface HarnessProposalRecord {
  readonly worldlineId: string;
  readonly proposalId: string;
  readonly action: string;
  readonly rationaleRef: string;
  readonly payloadDigest: string;
  readonly payload: Readonly<Record<string, ProposalFieldValue>>;
}

export interface HarnessDecisionReport {
  readonly decision: HarnessDecision;
  readonly proposal: HarnessProposalRecord | null;
  readonly reason: string;
}

/**
 * The consequence path: decide, then announce the world's decision.
 *
 * The host stays the only decider. `decide` returns a proposal record (or an
 * abstention) and the caller decides whether to commit it; `announce` reports what
 * actually happened, including a rejection, so the harness cannot conclude success
 * from silence.
 */
/**
 * Materialise a harness answer into host-facing proposal data.
 *
 * The record carries the worldline the proposal was made for and nothing else the
 * host would have to trust: the harness cannot name a different worldline or a
 * capability through this type.
 */
function materialise(worldlineId: string, decision: HarnessDecision): HarnessDecisionReport {
  if (decision.status === "abstained") {
    return { decision, proposal: null, reason: decision.reason };
  }
  return {
    decision,
    proposal: {
      worldlineId,
      proposalId: decision.proposal.proposalId,
      action: decision.proposal.action,
      rationaleRef: decision.proposal.rationaleRef,
      payloadDigest: decision.proposal.payloadDigest,
      payload: decision.proposal.payload,
    },
    reason: decision.reason,
  };
}

/**
 * The consequence path: decide, then announce the world's decision.
 *
 * The host stays the only decider. `decide` returns a proposal record (or an
 * abstention) and the caller decides whether to commit it; `announce` reports what
 * actually happened, including a rejection, so the harness cannot conclude success
 * from silence. Exactly one harness call happens per method.
 */
export class HarnessConsequencePath {
  constructor(readonly harness: AgentHarnessClient) {}

  async decide(
    worldlineId: string,
    revision: number,
    allowedContext?: Readonly<Record<string, string>>,
  ): Promise<HarnessDecisionReport> {
    const observation: HarnessObservationInput =
      allowedContext === undefined
        ? { worldlineId, revision }
        : { worldlineId, revision, allowedContext };
    return materialise(worldlineId, await this.harness.decide(observation));
  }

  /** Announce a committed or rejected consequence of a proposal this path produced. */
  async announce(
    proposal: HarnessProposalRecord,
    outcome: "committed" | "rejected",
    detail?: string,
  ): Promise<HarnessAcknowledgement> {
    const consequence: HarnessConsequence = { proposalId: proposal.proposalId, status: outcome };
    if (detail !== undefined) {
      return this.harness.announce({ ...consequence, detail });
    }
    return this.harness.announce(consequence);
  }
}
