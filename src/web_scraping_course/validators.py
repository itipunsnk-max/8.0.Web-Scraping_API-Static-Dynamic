"""Validation helpers for scraped records and HTTP metadata."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from .exceptions import DuplicateRecordError, ValidationError


def require_fields(record: Mapping[str, object], fields: Iterable[str]) -> None:
    """Require non-empty values for each named field."""
    missing = [field for field in fields if field not in record or record[field] in (None, "")]
    if missing:
        raise ValidationError(f"missing required fields: {', '.join(missing)}")


def validate_unique_records(
    records: Iterable[Mapping[str, object]], key: str
) -> list[Mapping[str, object]]:
    """Validate a unique record key and return records as a list."""
    validated = list(records)
    seen: set[object] = set()
    for record in validated:
        require_fields(record, [key])
        value = record[key]
        if value in seen:
            raise DuplicateRecordError(f"duplicate record key: {value}")
        seen.add(value)
    return validated


def validate_content_type(content_type: str, allowed: Iterable[str]) -> str:
    """Validate and normalize an HTTP Content-Type header value."""
    normalized = content_type.split(";", 1)[0].strip().lower()
    accepted = {value.lower() for value in allowed}
    if normalized not in accepted:
        raise ValidationError(f"unexpected Content-Type: {normalized or '<missing>'}")
    return normalized


def validate_size(size: int, maximum: int) -> None:
    """Ensure a byte count is within a positive configured limit."""
    if size < 0 or maximum < 1:
        raise ValidationError("size and maximum must be valid positive values")
    if size > maximum:
        raise ValidationError(f"response size {size} exceeds maximum {maximum}")
