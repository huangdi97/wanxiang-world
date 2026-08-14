# Production Topology (G16A)

## Topology (minimal for current evidence)
```text
[ HTTP API (FastAPI, single process) ]  ->  [ Wanxiang Runtime (modular monolith) ]  ->  [ Persistence ]
                                                                                           SQLite (dev/test)
                                                                                           PostgreSQL (production target)
```

## Decisions
- **Modular monolith, not microservices**: no service split without performance/isolation/
  failure-domain evidence; the current evidence (bounded event streams, single authority) does not
  justify microservices, Kafka/NATS/Redis/K8s.
- **Worker separation**: background work (autonomous scheduler, co-sim) runs in-process on demand;
  a separate worker process is only justified if long-horizon runs need isolation (tracked, not split now).
- **Profiles**: `development` / `test` (deterministic, offline, no secrets) and `production`
  (requires explicit `WANXIANG_DATABASE_URL` + `WANXIANG_SECRET_KEY`; dev defaults rejected).
- **Secrets**: injected via environment; never committed; the public settings surface redacts them.
- **Health**: `/healthz` answers; production startup fails fast on missing required config.

## Ownership
- Runtime/authority: `wanxiang_runtime`, `wanxiang_application`; API transport: `apps/api`;
  persistence adapters: `wanxiang_persistence`; observability/config: `wanxiang_observability`.

## Reproducibility
- Same env + lockfiles (uv.lock / pnpm-lock.yaml) + migrations produce the same deployable state;
  config changes are versioned in Git and documented in this file.
