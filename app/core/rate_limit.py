from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from threading import Lock
from time import time

from fastapi import Header, HTTPException, Request, status

from app.core.config import get_settings


@dataclass
class InMemoryRateLimiter:
    window_seconds: int = 60
    _storage: dict[str, deque[float]] = field(default_factory=lambda: defaultdict(deque))
    _lock: Lock = field(default_factory=Lock)

    def allow(self, key: str, limit: int) -> bool:
        now = time()
        threshold = now - self.window_seconds

        with self._lock:
            bucket = self._storage[key]
            while bucket and bucket[0] < threshold:
                bucket.popleft()

            if len(bucket) >= limit:
                return False

            bucket.append(now)
            return True


_rate_limiter = InMemoryRateLimiter()


def enforce_rate_limit(
    request: Request,
    x_api_key: str | None = Header(default=None),
) -> None:
    settings = get_settings()
    limit = max(settings.rate_limit_per_minute, 1)
    client_host = request.client.host if request.client else "unknown"
    key = x_api_key or client_host

    if not _rate_limiter.allow(key=key, limit=limit):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
