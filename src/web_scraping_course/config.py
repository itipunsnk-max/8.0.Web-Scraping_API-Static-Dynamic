"""Validated, secret-free configuration for scraping clients."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from .exceptions import ConfigurationError


@dataclass(frozen=True, slots=True)
class ScraperConfig:
    """Runtime settings shared by HTTP scraping utilities."""

    base_url: str | None = None
    timeout: float = 10.0
    max_retries: int = 3
    backoff_factor: float = 0.5
    max_backoff: float = 30.0
    min_request_interval: float = 0.0
    max_response_bytes: int = 10 * 1024 * 1024
    user_agent: str = "web-scraping-zero-to-practical/1.0"

    def __post_init__(self) -> None:
        if self.base_url is not None:
            parsed = urlparse(self.base_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ConfigurationError("base_url must be an absolute http(s) URL")
        if self.timeout <= 0:
            raise ConfigurationError("timeout must be greater than zero")
        if self.max_retries < 0:
            raise ConfigurationError("max_retries cannot be negative")
        if self.backoff_factor < 0 or self.max_backoff < 0:
            raise ConfigurationError("backoff values cannot be negative")
        if self.min_request_interval < 0:
            raise ConfigurationError("min_request_interval cannot be negative")
        if self.max_response_bytes < 1:
            raise ConfigurationError("max_response_bytes must be greater than zero")
        if not self.user_agent.strip():
            raise ConfigurationError("user_agent cannot be empty")

    @classmethod
    def from_env(cls, prefix: str = "SCRAPER_") -> ScraperConfig:
        """Build configuration from non-secret environment variables."""

        def read_int(name: str, default: int) -> int:
            value = os.getenv(prefix + name)
            if value is None:
                return default
            try:
                return int(value)
            except ValueError as error:
                raise ConfigurationError(f"{prefix}{name} must be an integer") from error

        def read_float(name: str, default: float) -> float:
            value = os.getenv(prefix + name)
            if value is None:
                return default
            try:
                return float(value)
            except ValueError as error:
                raise ConfigurationError(f"{prefix}{name} must be a number") from error

        return cls(
            base_url=os.getenv(prefix + "BASE_URL") or None,
            timeout=read_float("TIMEOUT", cls.timeout),
            max_retries=read_int("MAX_RETRIES", cls.max_retries),
            backoff_factor=read_float("BACKOFF_FACTOR", cls.backoff_factor),
            max_backoff=read_float("MAX_BACKOFF", cls.max_backoff),
            min_request_interval=read_float(
                "MIN_REQUEST_INTERVAL", cls.min_request_interval
            ),
            max_response_bytes=read_int("MAX_RESPONSE_BYTES", cls.max_response_bytes),
            user_agent=os.getenv(prefix + "USER_AGENT", cls.user_agent),
        )
