/**
 * History bridge: the composition host writes canonical history through a
 * separate Python authority process over the frozen JSON-RPC stdio protocol.
 *
 * `RpcHistoryProvider` is the async view of the history seam: the in-process
 * `HistoryProvider` (./history) is synchronous, while a stdio client cannot be,
 * because the event loop must stay free to read the authority's stdout. The
 * seam contract (`wanxiang.history@1`) is unchanged, only the transport is.
 * `RpcAuthorityBootstrap` performs the calls a host needs before it can commit
 * (info, seam digest, holder registration, grant) and shares one authority
 * process with the provider when given the same `RpcStdioClient`.
 */
import {
  RPC_COMMIT_DENIED,
  RPC_REVISION_CONFLICT,
  RPC_TRANSPORT_FAILURE,
  RpcMethods,
  RpcProtocolError,
  RpcStdioClient,
  asJsonObject,
  type JsonFields,
  type RpcExitHook,
  type RpcTransportOptions,
} from "./bridge_protocol";
import {
  CommitDeniedError,
  RevisionConflictError,
  type AppendRequest,
  type AppendResult,
  type Revision,
  type WorldEvent,
} from "./history";

/** Looks up the capability token the authority granted to a holder. */
export type RpcTokenLookup = (holderId: string) => string | undefined;

/**
 * Promise-returning view of the history port: the same five operations and
 * provider identity as `HistoryProvider` (./history), only the return types
 * differ, because the transport is a child process.
 */
export interface AsyncHistoryProvider {
  readonly providerId: string;
  readonly providerVersion: string;
  head(worldlineId: string): Promise<Revision>;
  read(worldlineId: string, fromRevision: number): Promise<readonly WorldEvent[]>;
  append(request: AppendRequest): Promise<AppendResult>;
  checkpoint(worldlineId: string): Promise<Revision>;
  worldlines(): Promise<readonly string[]>;
}

/** `runtime.info` result. */
export interface RuntimeInfo {
  readonly server: string;
  readonly version: string;
  readonly schema: string;
}

/** `authority.register_holder` result. */
export interface HolderRegistration {
  readonly holderId: string;
  readonly registered: boolean;
}

function readField(fields: JsonFields, key: string, what: string): unknown {
  const value = fields[key];
  if (value === undefined) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what} is missing '${key}'`);
  }
  return value;
}

function readString(fields: JsonFields, key: string, what: string): string {
  const value = readField(fields, key, what);
  if (typeof value !== "string") {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'${key}' must be a string`);
  }
  return value;
}

function readInteger(fields: JsonFields, key: string, what: string): number {
  const value = readField(fields, key, what);
  if (typeof value !== "number" || !Number.isInteger(value)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'${key}' must be an integer`);
  }
  return value;
}

function readStringArray(fields: JsonFields, key: string, what: string): readonly string[] {
  const value = readField(fields, key, what);
  if (!Array.isArray(value)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'${key}' must be an array`);
  }
  return value.map((item: unknown): string => {
    if (typeof item !== "string") {
      throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'${key}' must contain strings`);
    }
    return item;
  });
}

/** Parse a `history.head` or `history.checkpoint` result. */
function readRevision(result: unknown, what: string): Revision {
  const fields = asJsonObject(result, what);
  return {
    revision: readInteger(fields, "revision", what),
    stateHash: readString(fields, "stateHash", what),
  };
}

/** Parse a `history.read` result. */
function readEvents(result: unknown): readonly WorldEvent[] {
  const what = "history.read result";
  const events = readField(asJsonObject(result, what), "events", what);
  if (!Array.isArray(events)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'events' must be an array`);
  }
  return events.map((raw: unknown): WorldEvent => {
    const event = asJsonObject(raw, `${what} event`);
    return {
      eventId: readString(event, "eventId", `${what} event`),
      kind: readString(event, "kind", `${what} event`),
      payloadDigest: readString(event, "payloadDigest", `${what} event`),
    };
  });
}

/**
 * The history seam over the authority's JSON-RPC protocol.
 *
 * `append` never sends a request without a capability token: the history seam
 * stamps `authorityHolderId` after its own capability check, and a missing
 * holder or a holder without a granted token fails here instead.
 */
export class RpcHistoryProvider implements AsyncHistoryProvider {
  readonly providerId = "history-authority-rpc";
  readonly providerVersion = "1.0.0";
  private readonly client: RpcStdioClient;
  private readonly ownsClient: boolean;

  constructor(
    options: RpcTransportOptions,
    private readonly tokenFor: RpcTokenLookup,
    onExit?: RpcExitHook,
    client?: RpcStdioClient,
  ) {
    this.ownsClient = client === undefined;
    this.client = client ?? new RpcStdioClient(options, onExit);
  }

  async head(worldlineId: string): Promise<Revision> {
    const result = await this.client.call(RpcMethods.historyHead, { worldlineId });
    return readRevision(result, "history.head result");
  }

  async read(worldlineId: string, fromRevision: number): Promise<readonly WorldEvent[]> {
    return readEvents(await this.client.call(RpcMethods.historyRead, { worldlineId, fromRevision }));
  }

  async checkpoint(worldlineId: string): Promise<Revision> {
    const result = await this.client.call(RpcMethods.historyCheckpoint, { worldlineId });
    return readRevision(result, "history.checkpoint result");
  }

  async worldlines(): Promise<readonly string[]> {
    const what = "history.worldlines result";
    const result = await this.client.call(RpcMethods.historyWorldlines, {});
    return readStringArray(asJsonObject(result, what), "worldlines", what);
  }

  async append(request: AppendRequest): Promise<AppendResult> {
    const capabilityToken = this.capabilityTokenFor(request);
    try {
      const result = await this.client.call(RpcMethods.historyAppend, {
        worldlineId: request.worldlineId,
        expectedRevision: request.expectedRevision,
        events: request.events,
        capabilityToken,
      });
      const what = "history.append result";
      const fields = asJsonObject(result, what);
      return {
        revision: readInteger(fields, "revision", what),
        stateHash: readString(fields, "stateHash", what),
        eventIds: readStringArray(fields, "eventIds", what),
      };
    } catch (error: unknown) {
      throw toHistoryError(error, request);
    }
  }

  /** Close the authority process when this provider created it. */
  async dispose(): Promise<void> {
    if (this.ownsClient) await this.client.dispose();
  }

  private capabilityTokenFor(request: AppendRequest): string {
    const holderId = request.authorityHolderId;
    if (!holderId) {
      // SAFETY: the history seam performs the capability check before it stamps
      // the holder, so a request without one never passed that check.
      throw new RpcProtocolError(RPC_COMMIT_DENIED, "append requires authorityHolderId stamped by the history seam");
    }
    const token = this.tokenFor(holderId);
    if (!token) {
      throw new RpcProtocolError(RPC_COMMIT_DENIED, `no capability token was granted for holder ${holderId}`);
    }
    return token;
  }
}

/** The calls a host needs to bootstrap a capability token before committing. */
export class RpcAuthorityBootstrap {
  readonly client: RpcStdioClient;
  private readonly ownsClient: boolean;

  constructor(options: RpcTransportOptions, onExit?: RpcExitHook, client?: RpcStdioClient) {
    this.ownsClient = client === undefined;
    this.client = client ?? new RpcStdioClient(options, onExit);
  }

  async info(): Promise<RuntimeInfo> {
    const what = "runtime.info result";
    const fields = asJsonObject(await this.client.call(RpcMethods.runtimeInfo, {}), what);
    return {
      server: readString(fields, "server", what),
      version: readString(fields, "version", what),
      schema: readString(fields, "schema", what),
    };
  }

  async seamDigest(): Promise<string> {
    const what = "seam.digest result";
    const result = await this.client.call(RpcMethods.seamDigest, {});
    return readString(asJsonObject(result, what), "digest", what);
  }

  async registerHolder(holderId: string, auditRef: string): Promise<HolderRegistration> {
    const what = "authority.register_holder result";
    const result = await this.client.call(RpcMethods.registerHolder, { holderId, auditRef });
    const fields = asJsonObject(result, what);
    const registered = readField(fields, "registered", what);
    if (typeof registered !== "boolean") {
      throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what}.'registered' must be a boolean`);
    }
    return { holderId: readString(fields, "holderId", what), registered };
  }

  async grant(holderId: string): Promise<string> {
    const what = "authority.grant result";
    try {
      const result = await this.client.call(RpcMethods.grant, { holderId });
      return readString(asJsonObject(result, what), "capabilityToken", what);
    } catch (error: unknown) {
      throw asDomainError(error);
    }
  }

  /** Close the authority process when this bootstrap created it. */
  async dispose(): Promise<void> {
    if (this.ownsClient) await this.client.dispose();
  }
}

/** Map a protocol failure onto the typed error the history seam exposes. */
function toHistoryError(error: unknown, request: AppendRequest): Error {
  if (!(error instanceof RpcProtocolError)) return asError(error);
  if (error.code === RPC_REVISION_CONFLICT) {
    const expected = integerField(error.data, "expectedRevision");
    const actual = integerField(error.data, "actualRevision");
    // A conflict payload without both revisions stays a protocol error: never
    // fabricate a revision the authority did not report.
    if (expected === undefined || actual === undefined) return error;
    const reported = error.data["worldlineId"];
    const worldlineId = typeof reported === "string" ? reported : request.worldlineId;
    return new RevisionConflictError(worldlineId, expected, actual);
  }
  if (error.code === RPC_COMMIT_DENIED) return new CommitDeniedError(error.message);
  return error;
}

/** Map `authority.grant` failures onto the seam's typed denial. */
function asDomainError(error: unknown): Error {
  if (error instanceof RpcProtocolError && error.code === RPC_COMMIT_DENIED) {
    return new CommitDeniedError(error.message);
  }
  return asError(error);
}

function asError(error: unknown): Error {
  return error instanceof Error ? error : new RpcProtocolError(RPC_TRANSPORT_FAILURE, String(error));
}

function integerField(fields: JsonFields, key: string): number | undefined {
  const value = fields[key];
  return typeof value === "number" && Number.isInteger(value) ? value : undefined;
}
