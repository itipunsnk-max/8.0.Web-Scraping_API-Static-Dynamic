"""Custom exceptions used by resilient scraping utilities."""

from __future__ import annotations


class ScrapingError(Exception):
    """Base class for expected scraping failures."""


class ConfigurationError(ScrapingError):
    """Raised when scraper configuration is invalid."""


class NetworkError(ScrapingError):
    """Base class for request and response failures."""


class RequestTimeoutError(NetworkError):
    """Raised when a request times out."""


class RequestConnectionError(NetworkError):
    """Raised when a connection cannot be established."""


class HTTPStatusError(NetworkError):
    """Raised when a response has an unsuccessful HTTP status."""

    def __init__(self, status_code: int, url: str, body_preview: str = "") -> None:
        self.status_code = status_code
        self.url = url
        self.body_preview = body_preview
        message = f"HTTP {status_code} for {url}"
        if body_preview:
            message += f": {body_preview[:200]}"
        super().__init__(message)


class ResponseTooLargeError(NetworkError):
    """Raised when a response exceeds the configured byte limit."""


class RetryExhaustedError(NetworkError):
    """Raised after all permitted retries fail."""

    def __init__(self, operation_name: str, attempts: int, last_error: Exception) -> None:
        self.operation_name = operation_name
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"{operation_name} failed after {attempts} attempts: {last_error}")


class ParseError(ScrapingError):
    """Raised when a response cannot be parsed into the expected format."""


class ValidationError(ScrapingError):
    """Raised when scraped data fails schema or value validation."""


class DuplicateRecordError(ValidationError):
    """Raised when a record key is duplicated where uniqueness is required."""


class ExportError(ScrapingError):
    """Raised when normalized data cannot be exported."""
