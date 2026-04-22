from __future__ import annotations

from app.core.rate_limit import InMemoryRateLimiter


def test_rate_limiter_allows_within_limit() -> None:
    limiter = InMemoryRateLimiter(window_seconds=60)
    assert limiter.allow("key", limit=2) is True
    assert limiter.allow("key", limit=2) is True


def test_rate_limiter_blocks_after_limit() -> None:
    limiter = InMemoryRateLimiter(window_seconds=60)
    assert limiter.allow("key", limit=1) is True
    assert limiter.allow("key", limit=1) is False
