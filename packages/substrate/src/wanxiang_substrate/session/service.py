"""Session + embodiment lease services (G05B)."""

from __future__ import annotations

from wanxiang_domain.ids import WorldInstanceId

from wanxiang_substrate.session.errors import (
    LeaseConflict,
    LeaseExpired,
    LeaseNotFound,
    SessionNotFound,
)
from wanxiang_substrate.session.model import EmbodimentLease, Session


class SessionService:
    """Creates and tracks client sessions per world instance."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(
        self,
        session_id: str,
        controller: str,
        instance_id: WorldInstanceId,
        mode: str,
        created_seq: int,
    ) -> Session:
        session = Session(
            session_id=session_id,
            controller=controller,
            instance_id=instance_id,
            mode=mode,  # type: ignore[arg-type]
            created_seq=created_seq,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def require(self, session_id: str) -> Session:
        session = self.get(session_id)
        if session is None:
            raise SessionNotFound(f"session {session_id!r} not found")
        return session


class LeaseService:
    """Acquire/renew/release/expire embodiment leases (one primary per actor)."""

    def __init__(self) -> None:
        self._leases: dict[str, EmbodimentLease] = {}
        self._by_actor: dict[str, str] = {}

    def acquire(
        self,
        session: Session,
        actor_id: str,
        lease_id: str,
        acquired_seq: int,
        expires_seq: int,
    ) -> EmbodimentLease:
        if not session.may_embody():
            raise LeaseConflict(f"session {session.session_id!r} cannot embody actors")
        existing = self._by_actor.get(actor_id)
        if existing is not None and self.require(existing).active:
            raise LeaseConflict(f"actor {actor_id!r} already has primary controller {existing!r}")
        lease = EmbodimentLease(
            lease_id=lease_id,
            session_id=session.session_id,
            actor_id=actor_id,
            state="acquired",
            acquired_seq=acquired_seq,
            expires_seq=expires_seq,
        )
        self._leases[lease_id] = lease
        self._by_actor[actor_id] = lease_id
        return lease

    def renew(self, lease_id: str, expires_seq: int) -> EmbodimentLease:
        lease = self.require(lease_id)
        if not lease.active:
            raise LeaseExpired(f"lease {lease_id!r} is not active")
        updated = EmbodimentLease(
            lease_id=lease.lease_id,
            session_id=lease.session_id,
            actor_id=lease.actor_id,
            state="renewed",
            acquired_seq=lease.acquired_seq,
            expires_seq=expires_seq,
            released_seq=lease.released_seq,
        )
        self._leases[lease_id] = updated
        return updated

    def release(self, lease_id: str, released_seq: int) -> EmbodimentLease:
        lease = self.require(lease_id)
        updated = EmbodimentLease(
            lease_id=lease.lease_id,
            session_id=lease.session_id,
            actor_id=lease.actor_id,
            state="released",
            acquired_seq=lease.acquired_seq,
            expires_seq=lease.expires_seq,
            released_seq=released_seq,
        )
        self._leases[lease_id] = updated
        if self._by_actor.get(lease.actor_id) == lease_id:
            self._by_actor.pop(lease.actor_id, None)
        return updated

    def expire(self, lease_id: str) -> EmbodimentLease:
        lease = self.require(lease_id)
        updated = EmbodimentLease(
            lease_id=lease.lease_id,
            session_id=lease.session_id,
            actor_id=lease.actor_id,
            state="expired",
            acquired_seq=lease.acquired_seq,
            expires_seq=lease.expires_seq,
            released_seq=lease.released_seq,
        )
        self._leases[lease_id] = updated
        if self._by_actor.get(lease.actor_id) == lease_id:
            self._by_actor.pop(lease.actor_id, None)
        return updated

    def primary_controller(self, actor_id: str) -> str | None:
        lease_id = self._by_actor.get(actor_id)
        if lease_id is None:
            return None
        lease = self.require(lease_id)
        return lease.session_id if lease.active else None

    def require(self, lease_id: str) -> EmbodimentLease:
        lease = self._leases.get(lease_id)
        if lease is None:
            raise LeaseNotFound(f"lease {lease_id!r} not found")
        return lease
