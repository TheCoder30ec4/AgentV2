from typing import Dict, Optional

from pydantic import BaseModel, Field


class SessionMemory(BaseModel):
    """
    Lightweight per-session memory for the Agent framework.

    Stores:
    - session_id: unique identifier for this session
    - cache: exact-match task -> reply cache (avoids repeat LLM calls)
    - last_reply: snippet of the most recent reply (for minimal prompt continuity)
    """

    session_id: str = Field(description="Unique session identifier")

    cache: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of normalized_task -> final_reply for exact-match caching",
    )

    last_reply: Optional[str] = Field(
        default=None,
        description="Truncated snippet of the last reply (for minimal prompt context)",
    )

    # Configuration
    max_last_reply_length: int = Field(
        default=200, exclude=True, description="Max characters to store in last_reply"
    )

    def set_last_reply(self, reply: str) -> None:
        """Store a truncated version of the reply."""
        if reply:
            self.last_reply = reply[: self.max_last_reply_length]
            if len(reply) > self.max_last_reply_length:
                self.last_reply += "..."
        else:
            self.last_reply = None

    def cache_reply(self, normalized_task: str, reply: str) -> None:
        """Cache a reply for a normalized task."""
        self.cache[normalized_task] = reply
        self.set_last_reply(reply)

    def get_cached_reply(self, normalized_task: str) -> Optional[str]:
        """Get cached reply if exists."""
        return self.cache.get(normalized_task)

    def has_cache(self, normalized_task: str) -> bool:
        """Check if a task is cached."""
        return normalized_task in self.cache
