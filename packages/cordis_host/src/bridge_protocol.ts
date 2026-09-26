/**
 * Frozen JSON-RPC 2.0 protocol for the history-authority bridge: the wire
 * vocabulary, the response-envelope parser and the serialized stdio transport.
 *
 * The authority is a separate Python process (`python -m wanxiang_reality.rpc
 * --stdio`). One `RpcStdioClient` owns one authority child, keeps a single
 * request in flight (the protocol pairs each request line with exactly one
 * response line, matched by id) and parses result payloads in `./bridge`.
 */
import {
  spawn,
  type ChildProcessByStdio,
  type SpawnOptionsWithStdioTuple,
  type StdioPipe,
} from "node:child_process";
import { createInterface } from "node:readline";
import type { Readable, Writable } from "node:stream";

/** The only JSON-RPC version the authority speaks. */
export const JSONRPC_VERSION = "2.0";

/** Error codes the authority returns (frozen). */
export const RPC_PARSE_ERROR = -32700;
export const RPC_INVALID_REQUEST = -32600;
export const RPC_UNKNOWN_METHOD = -32601;
export const RPC_INVALID_PARAMS = -32602;
export const RPC_REVISION_CONFLICT = -32001;
export const RPC_COMMIT_DENIED = -32002;

/**
 * Client-side failure: no server answer was produced (spawn failure, timeout,
 * closed pipe, malformed line or result). JSON-RPC reserves -32000..-32099 for
 * implementation-defined errors, so this never collides with an authority code.
 */
export const RPC_TRANSPORT_FAILURE = -32000;

/** Frozen method names. */
export const RpcMethods = {
  runtimeInfo: "runtime.info",
  seamDigest: "seam.digest",
  registerHolder: "authority.register_holder",
  grant: "authority.grant",
  historyHead: "history.head",
  historyRead: "history.read",
  historyCheckpoint: "history.checkpoint",
  historyWorldlines: "history.worldlines",
  historyAppend: "history.append",
} as const;

export type RpcMethod = (typeof RpcMethods)[keyof typeof RpcMethods];

/** A JSON object decoded from the wire. */
export type JsonFields = Readonly<Record<string, unknown>>;

/** The frozen JSON-RPC error object. */
export type RpcError = { readonly code: number; readonly message: string; readonly data: JsonFields };

/** One parsed response line: exactly one of `result` or `error` is present. */
export type RpcResponse =
  | { readonly kind: "result"; readonly id: number; readonly result: unknown }
  | { readonly kind: "error"; readonly id: number; readonly error: RpcError };

/** Typed protocol failure: a frozen authority code or `RPC_TRANSPORT_FAILURE`. */
export class RpcProtocolError extends Error {
  override readonly name = "RpcProtocolError";

  constructor(readonly code: number, message: string, readonly data: JsonFields = {}) {
    super(message);
  }
}

/**
 * Narrow decoded wire data to a JSON object.
 *
 * SAFETY: only values decoded from the wire reach this function, and the guard
 * rejects null and arrays, so every property read yields `unknown` and no `any`
 * leaks out of the parse boundary.
 */
export function asJsonObject(value: unknown, what: string): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `${what} must be a JSON object`);
  }
  return value as Record<string, unknown>;
}

/** Parse one stdout line; anything malformed raises `RpcProtocolError`. */
export function parseResponseLine(line: string): RpcResponse {
  let parsed: unknown;
  try {
    parsed = JSON.parse(line);
  } catch {
    const preview = line.trim().slice(0, 120);
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, `response line is not valid JSON: ${preview}`);
  }
  const envelope = asJsonObject(parsed, "response");
  if (envelope["jsonrpc"] !== JSONRPC_VERSION) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "response must declare jsonrpc '2.0'");
  }
  const id = envelope["id"];
  if (typeof id !== "number" || !Number.isInteger(id)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "response 'id' must be an integer");
  }
  const hasResult = "result" in envelope;
  const hasError = "error" in envelope;
  if (hasResult === hasError) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "response must carry exactly one of 'result' or 'error'");
  }
  if (!hasError) return { kind: "result", id, result: envelope["result"] };
  return { kind: "error", id, error: parseErrorPayload(envelope["error"]) };
}

function parseErrorPayload(raw: unknown): RpcError {
  const fields = asJsonObject(raw, "response error");
  const code = fields["code"];
  const message = fields["message"];
  const data = fields["data"];
  if (typeof code !== "number" || !Number.isInteger(code)) {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "response error 'code' must be an integer");
  }
  if (typeof message !== "string") {
    throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "response error 'message' must be a string");
  }
  return { code, message, data: data === undefined ? {} : asJsonObject(data, "response error data") };
}

/** Encode one request as the single compact line the authority expects. */
export function encodeRequest(id: number, method: RpcMethod, params: JsonFields): string {
  return `${JSON.stringify({ jsonrpc: JSONRPC_VERSION, id, method, params })}\n`;
}

/** How to start the authority process. */
export interface RpcTransportOptions {
  readonly command: readonly string[];
  readonly cwd: string;
  readonly requestTimeoutMs?: number;
}

/** Called when the authority process ends without a `dispose()` request. */
export type RpcExitHook = (exitCode: number | null) => void;

const DEFAULT_REQUEST_TIMEOUT_MS = 30_000;

type AuthorityChild = ChildProcessByStdio<Writable, Readable, Readable>;

interface PendingCall {
  readonly id: number;
  readonly method: RpcMethod;
  readonly resolve: (result: unknown) => void;
  readonly reject: (error: Error) => void;
  readonly timer: NodeJS.Timeout;
}

/**
 * Serialized JSON-RPC client for one authority child process.
 *
 * The child is spawned on first use, one request is in flight at a time, and
 * every request carries a timeout, so a wedged authority rejects instead of
 * hanging the host. A malformed line, an unknown response id or an unexpected
 * exit fails the client instead of being dropped silently: the authority keeps
 * capability grants in memory only, so a restart cannot be trusted.
 */
export class RpcStdioClient {
  private readonly command: readonly string[];
  private readonly cwd: string;
  private readonly timeoutMs: number;
  private readonly onExit: RpcExitHook | undefined;
  private child: AuthorityChild | null = null;
  private pending: PendingCall | null = null;
  private tail: Promise<unknown> = Promise.resolve();
  private nextId = 1;
  private disposed = false;
  private fatal: RpcProtocolError | null = null;

  constructor(options: RpcTransportOptions, onExit?: RpcExitHook) {
    this.command = options.command;
    this.cwd = options.cwd;
    this.timeoutMs = options.requestTimeoutMs ?? DEFAULT_REQUEST_TIMEOUT_MS;
    this.onExit = onExit;
  }

  /** Queue one request; calls run strictly one at a time. */
  call(method: RpcMethod, params: JsonFields): Promise<unknown> {
    const run = this.tail.then(() => this.exchange(method, params));
    this.tail = run.then(() => undefined, () => undefined);
    return run;
  }

  /** Kill the child and reject pending work; safe to call more than once. */
  async dispose(): Promise<void> {
    if (this.disposed) return;
    this.disposed = true;
    this.settle(new RpcProtocolError(RPC_TRANSPORT_FAILURE, "authority client was disposed"));
    const child = this.child;
    this.child = null;
    if (!child) return;
    await new Promise<void>((resolve) => {
      child.once("close", () => resolve());
      child.kill();
    });
  }

  private async exchange(method: RpcMethod, params: JsonFields): Promise<unknown> {
    if (this.disposed) throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "authority client is disposed");
    if (this.fatal) throw this.fatal;
    const child = this.ensureChild();
    const id = this.nextId;
    this.nextId += 1;
    return await new Promise<unknown>((resolve, reject) => {
      const timer = setTimeout(() => this.onTimeout(id), this.timeoutMs);
      this.pending = { id, method, resolve, reject, timer };
      child.stdin.write(encodeRequest(id, method, params), (error?: Error | null) => {
        if (error) this.fail(`failed to write ${method}: ${error.message}`);
      });
    });
  }

  private ensureChild(): AuthorityChild {
    if (this.child) return this.child;
    const [command, ...args] = this.command;
    if (!command) throw new RpcProtocolError(RPC_TRANSPORT_FAILURE, "rpc command must name an executable");
    const spawnOptions: SpawnOptionsWithStdioTuple<StdioPipe, StdioPipe, StdioPipe> = {
      cwd: this.cwd,
      stdio: ["pipe", "pipe", "pipe"],
    };
    const child = spawn(command, args, spawnOptions);
    createInterface({ input: child.stdout, crlfDelay: Infinity }).on("line", (line: string) => {
      this.onResponseLine(line);
    });
    child.stderr.resume();
    child.on("error", (error: Error) => this.onSpawnError(error));
    child.on("close", (code: number | null) => this.onChildClose(code));
    this.child = child;
    return child;
  }

  private onResponseLine(line: string): void {
    let response: RpcResponse;
    try {
      response = parseResponseLine(line);
    } catch (error: unknown) {
      const failure = error instanceof RpcProtocolError ? error : new RpcProtocolError(RPC_TRANSPORT_FAILURE, String(error));
      this.settle(failure);
      return;
    }
    const pending = this.pending;
    if (!pending || pending.id !== response.id) {
      this.fail(`response id ${response.id} has no pending request`);
      return;
    }
    this.pending = null;
    clearTimeout(pending.timer);
    if (response.kind === "result") pending.resolve(response.result);
    else pending.reject(new RpcProtocolError(response.error.code, response.error.message, response.error.data));
  }

  private onTimeout(id: number): void {
    const pending = this.pending;
    if (!pending || pending.id !== id) return;
    this.pending = null;
    // A late answer then carries an unmatched id and fails the client.
    const message = `request ${pending.method} (id ${id}) timed out after ${this.timeoutMs} ms`;
    pending.reject(new RpcProtocolError(RPC_TRANSPORT_FAILURE, message));
  }

  /** Fail the client permanently and reject whatever is pending. */
  private fail(message: string): void {
    this.settle(new RpcProtocolError(RPC_TRANSPORT_FAILURE, message));
  }

  private settle(error: RpcProtocolError): void {
    this.fatal = error;
    const pending = this.pending;
    if (!pending) return;
    this.pending = null;
    clearTimeout(pending.timer);
    pending.reject(error);
  }

  private onChildClose(code: number | null): void {
    this.child = null;
    if (this.disposed) return;
    this.fail(`authority process exited (code ${code})`);
    this.onExit?.(code);
  }

  private onSpawnError(error: Error): void {
    if (this.disposed) return;
    this.fail(`authority process failed to start: ${error.message}`);
  }
}
