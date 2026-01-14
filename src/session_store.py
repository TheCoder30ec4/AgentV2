"""
In-memory session store for the Agent framework.

Provides a lightweight registry of SessionMemory objects keyed by session_id.
Sessions persist only within the current Python process.
"""

from typing import Dict, Optional

from schemas.SessionMemory import SessionMemory


class SessionStore:
    """
    In-memory registry of session memories.

    Thread-safe for basic operations (single-threaded Python context).
    Sessions are created on first access and persist until the process exits.
    """

    _instance: Optional["SessionStore"] = None

    def __init__(self):
        self._sessions: Dict[str, SessionMemory] = {}

    @classmethod
    def get_instance(cls) -> "SessionStore":
        """Get or create the singleton SessionStore instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, session_id: str) -> SessionMemory:
        """
        Get or create a SessionMemory for the given session_id.

        Args:
            session_id: Unique identifier for the session

        Returns:
            The SessionMemory for this session (created if not exists)
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionMemory(session_id=session_id)
        return self._sessions[session_id]

    def has(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions

    def clear(self, session_id: str) -> bool:
        """
        Clear/delete a specific session.

        Returns:
            True if session existed and was deleted, False otherwise
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def clear_all(self) -> int:
        """
        Clear all sessions.

        Returns:
            Number of sessions that were cleared
        """
        count = len(self._sessions)
        self._sessions.clear()
        return count

    @property
    def session_count(self) -> int:
        """Number of active sessions."""
        return len(self._sessions)


# Convenience function to get the global store
def get_session_store() -> SessionStore:
    """Get the global SessionStore instance."""
    return SessionStore.get_instance()
