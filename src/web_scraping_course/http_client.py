"""HTTP client with timeout, bounded retry, rate limiting and size checks."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from typing import Any, Self
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests

from .config import ScraperConfig
from .exceptions import (
    HTTPStatusError,
    ParseError,
    RequestConnectionError,
    RequestTimeoutError,
    ResponseTooLargeError,
)
from .rate_limiter import RateLimiter
from .retry import retry_call
from .validators import validate_size


def _safe_url(url: str) -> str:
    """Remove query and fragment values from URLs written to logs."""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


class HttpClient:
    """Small requests-based client with explicit resilience policies."""

    def __init__(
        self,
        config: ScraperConfig | None = None,
        *,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
        sleeper: Any = None,
    ) -> None:
        self.config = config or ScraperConfig()
        self.session = session or requests.Session()
        self.logger = logger or logging.getLogger("web_scraping_course.http")
        limiter_sleeper = sleeper if sleeper is not None else None
        limiter_kwargs = {"min_interval": self.config.min_request_interval}
        if limiter_sleeper is not None:
            limiter_kwargs["sleeper"] = limiter_sleeper
        self.rate_limiter = RateLimiter(**limiter_kwargs)
        self._sleeper = sleeper

    def _request_once(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None,
        headers: Mapping[str, str] | None,
        stream: bool,
    ) -> requests.Response:
        self.rate_limiter.wait()
        request_headers = {"User-Agent": self.config.user_agent}
        if headers:
            request_headers.update(headers)
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                headers=request_headers,
                timeout=self.config.timeout,
                stream=stream,
            )
        except requests.Timeout as error:
            raise RequestTimeoutError(f"request timed out: {_safe_url(url)}") from error
        except requests.ConnectionError as error:
            raise RequestConnectionError(f"connection failed: {_safe_url(url)}") from error

        if response.status_code >= 400:
            preview = ""
            if not stream:
                preview = response.text[:200]
            response.close()
            raise HTTPStatusError(response.status_code, _safe_url(url), preview)
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > self.config.max_response_bytes:
            response.close()
            raise ResponseTooLargeError(f"response exceeds limit: {_safe_url(url)}")
        self.logger.info("HTTP %s %s -> %s", method.upper(), _safe_url(url), response.status_code)
        return response

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        """Make a resilient request; only safe transient failures are retried."""
        target = urljoin(self.config.base_url or "", url)
        sleeper = self._sleeper if self._sleeper is not None else None
        retry_kwargs = {
            "operation": lambda: self._request_once(
                method, target, params=params, headers=headers, stream=stream
            ),
            "max_retries": self.config.max_retries,
            "backoff_factor": self.config.backoff_factor,
            "max_backoff": self.config.max_backoff,
            "operation_name": f"{method.upper()} {_safe_url(target)}",
        }
        if sleeper is not None:
            retry_kwargs["sleeper"] = sleeper
        return retry_call(**retry_kwargs)

    def get_bytes(self, url: str, **kwargs: Any) -> bytes:
        """Read a response as bytes while enforcing the configured size limit."""
        response = self.request("GET", url, stream=True, **kwargs)
        chunks: list[bytes] = []
        total = 0
        try:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                try:
                    validate_size(total, self.config.max_response_bytes)
                except Exception as error:
                    raise ResponseTooLargeError(str(error)) from error
                chunks.append(chunk)
        finally:
            response.close()
        return b"".join(chunks)

    def get_text(self, url: str, **kwargs: Any) -> str:
        """Read a response as text with the same byte limit as downloads."""
        return self.get_bytes(url, **kwargs).decode("utf-8", errors="replace")

    def get_json(self, url: str, **kwargs: Any) -> Any:
        """Read and parse JSON, translating malformed payloads to ParseError."""
        try:
            return json.loads(self.get_text(url, **kwargs))
        except json.JSONDecodeError as error:
            raise ParseError(f"invalid JSON from {_safe_url(url)}") from error

    def close(self) -> None:
        """Close the underlying requests session."""
        self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
