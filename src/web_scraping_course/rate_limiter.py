"""Small, testable minimum-interval rate limiter."""

from __future__ import annotations

import time
from collections.abc import Callable
from threading import Lock
from typing import Self


class RateLimiter:
    """Ensure calls are separated by at least ``min_interval`` seconds."""

    def __init__(
        self,
        min_interval: float = 0.0,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if min_interval < 0:
            raise ValueError("min_interval cannot be negative")
        self.min_interval = min_interval
        self._clock = clock
        self._sleeper = sleeper
        self._next_allowed_at = 0.0
        self._lock = Lock()

    def wait(self) -> None:
        """Wait before the next request, if the configured interval requires it."""
        with self._lock:
            now = self._clock()
            delay = self._next_allowed_at - now
            if delay > 0:
                self._sleeper(delay)
            self._next_allowed_at = max(self._clock(), self._next_allowed_at) + self.min_interval

    def __enter__(self) -> Self:
        self.wait()
        return self

    def __exit__(self, *_: object) -> None:
        return None
