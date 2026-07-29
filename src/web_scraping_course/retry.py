"""Bounded retry and exponential backoff helpers."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

import requests

from .exceptions import (
    HTTPStatusError,
    RequestConnectionError,
    RequestTimeoutError,
    RetryExhaustedError,
)

T = TypeVar("T")
RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}


def exponential_backoff(attempt: int, factor: float, max_delay: float) -> float:
    """Return a bounded delay for a zero-based retry attempt."""
    if attempt < 0 or factor < 0 or max_delay < 0:
        raise ValueError("attempt and backoff values cannot be negative")
    return min(max_delay, factor * (2**attempt))


def is_retryable_error(error: Exception) -> bool:
    """Return whether an error is safe to retry under this course policy."""
    if isinstance(error, HTTPStatusError):
        return error.status_code in RETRYABLE_STATUS_CODES
    return isinstance(
        error,
        (
            requests.Timeout,
            requests.ConnectionError,
            RequestTimeoutError,
            RequestConnectionError,
        ),
    )


def retry_call(
    operation: Callable[[], T],
    *,
    max_retries: int,
    backoff_factor: float,
    max_backoff: float,
    sleeper: Callable[[float], None] = time.sleep,
    should_retry: Callable[[Exception], bool] = is_retryable_error,
    operation_name: str = "operation",
) -> T:
    """Run an operation with bounded retries and injectable sleeping for tests."""
    if max_retries < 0:
        raise ValueError("max_retries cannot be negative")
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except Exception as error:
            last_error = error
            if not should_retry(error):
                raise
            if attempt >= max_retries:
                raise RetryExhaustedError(operation_name, attempt + 1, error) from error
            sleeper(exponential_backoff(attempt, backoff_factor, max_backoff))
    raise RetryExhaustedError(operation_name, max_retries + 1, last_error) from last_error
