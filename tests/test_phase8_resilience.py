"""Unit tests for Phase 8 resilience utilities."""

from __future__ import annotations

import pytest
import requests
import responses

from web_scraping_course.config import ScraperConfig
from web_scraping_course.exceptions import (
    ConfigurationError,
    DuplicateRecordError,
    RetryExhaustedError,
)
from web_scraping_course.http_client import HttpClient
from web_scraping_course.rate_limiter import RateLimiter
from web_scraping_course.retry import exponential_backoff, retry_call
from web_scraping_course.utils import deduplicate_records, safe_filename
from web_scraping_course.validators import validate_unique_records


def test_config_rejects_invalid_timeout() -> None:
    with pytest.raises(ConfigurationError):
        ScraperConfig(timeout=0)


def test_backoff_is_bounded() -> None:
    assert [exponential_backoff(index, 0.5, 3) for index in range(5)] == [0.5, 1, 2, 3, 3]


def test_retry_call_retries_transient_error_without_sleeping_in_test() -> None:
    calls = 0
    sleeps: list[float] = []

    def operation() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise requests.Timeout("temporary")
        return "ok"

    assert retry_call(
        operation,
        max_retries=3,
        backoff_factor=0.5,
        max_backoff=5,
        sleeper=sleeps.append,
    ) == "ok"
    assert calls == 3
    assert sleeps == [0.5, 1.0]


def test_retry_call_stops_after_bound() -> None:
    with pytest.raises(RetryExhaustedError) as error:
        retry_call(
            lambda: (_ for _ in ()).throw(requests.Timeout("down")),
            max_retries=2,
            backoff_factor=0,
            max_backoff=0,
            sleeper=lambda _: None,
        )
    assert error.value.attempts == 3


def test_rate_limiter_records_wait_without_real_sleep() -> None:
    now = [0.0]
    sleeps: list[float] = []

    def sleeper(delay: float) -> None:
        sleeps.append(delay)
        now[0] += delay

    limiter = RateLimiter(1.0, clock=lambda: now[0], sleeper=sleeper)
    limiter.wait()
    limiter.wait()
    assert sleeps == [1.0]


def test_safe_filename_and_deduplication() -> None:
    assert safe_filename(r"..\CON.pdf") == "_CON.pdf"
    records, duplicates = deduplicate_records(
        [{"id": "a"}, {"id": "a"}, {"id": "b"}], "id"
    )
    assert [record["id"] for record in records] == ["a", "b"]
    assert duplicates == 1


def test_validation_rejects_duplicate_key() -> None:
    with pytest.raises(DuplicateRecordError):
        validate_unique_records([{"id": "a"}, {"id": "a"}], "id")


@responses.activate
def test_http_client_retries_503_and_returns_text() -> None:
    url = "https://example.test/catalog"
    responses.add(responses.GET, url, status=503)
    responses.add(responses.GET, url, status=200, body="<html>ok</html>")
    sleeps: list[float] = []
    with HttpClient(ScraperConfig(max_retries=1, backoff_factor=0.1), sleeper=sleeps.append) as client:
        assert client.get_text(url) == "<html>ok</html>"
    assert len(responses.calls) == 2
    assert sleeps == [0.1]
