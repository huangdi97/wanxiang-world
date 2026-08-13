# ADR-0036: Command Queue & Idempotent Multi-client Semantics Design (G06B)
- Status: accepted
- Date: 2026-08-13

## Context
G06B needs per-instance command intake with M1 idempotency under concurrent
multi-client submissions, bounded backpressure and structured statuses.

## Decision
1. CommandQueue is bounded with command-id dedup and serialized drain (total
   order per branch).
2. Statuses are structured (accepted/conflict/rejected/duplicate); retries
   produce one effect; conflicting revisions cannot both commit.

## Consequences
- Multi-client retries are revision-safe and idempotent; no last-write-wins
  mutation.