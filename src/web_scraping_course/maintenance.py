"""Maintenance helpers for detecting website and data contract changes."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

from .exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class SnapshotComparison:
    """Digest comparison result for an HTML/JSON snapshot."""

    previous_digest: str
    current_digest: str

    @property
    def changed(self) -> bool:
        return self.previous_digest != self.current_digest


def snapshot_digest(content: str | bytes) -> str:
    """Return a stable SHA-256 digest for a response or normalized snapshot."""
    payload = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(payload).hexdigest()


def compare_snapshots(previous: str | bytes, current: str | bytes) -> SnapshotComparison:
    """Compare two snapshots without storing their potentially sensitive contents."""
    return SnapshotComparison(snapshot_digest(previous), snapshot_digest(current))


def first_matching(soup: BeautifulSoup, selectors: Iterable[str]) -> Tag | None:
    """Return the first matching selector, allowing a controlled selector fallback."""
    for selector in selectors:
        match = soup.select_one(selector)
        if match is not None:
            return match
    return None


def validate_record_count(
    actual: int,
    *,
    expected: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
) -> None:
    """Fail fast when a record count is outside an explicitly defined contract."""
    if actual < 0:
        raise ValidationError("record count cannot be negative")
    if expected is not None and actual != expected:
        raise ValidationError(f"record count anomaly: expected {expected}, got {actual}")
    if minimum is not None and actual < minimum:
        raise ValidationError(f"record count anomaly: minimum {minimum}, got {actual}")
    if maximum is not None and actual > maximum:
        raise ValidationError(f"record count anomaly: maximum {maximum}, got {actual}")


def schema_issues(records: Iterable[Mapping[str, object]], required_fields: Iterable[str]) -> list[str]:
    """Return field issues for all records so callers can alert or fail fast."""
    fields = tuple(required_fields)
    issues: list[str] = []
    for position, record in enumerate(records, start=1):
        missing = [field for field in fields if field not in record]
        if missing:
            issues.append(f"record {position} missing: {', '.join(missing)}")
    return issues
