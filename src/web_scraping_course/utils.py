"""General safe helpers shared by scraping examples."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from itertools import count
from pathlib import Path

WINDOWS_INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def safe_filename(value: str, fallback: str = "downloaded-file", max_length: int = 120) -> str:
    """Return a Windows-safe filename without path traversal or reserved names."""
    name = re.split(r"[/\\]", str(value))[-1]
    cleaned = WINDOWS_INVALID_CHARS.sub("_", name).strip(" .") or fallback
    if cleaned.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
        cleaned = f"_{cleaned}"
    if max_length < 1:
        raise ValueError("max_length must be greater than zero")
    if len(cleaned) > max_length:
        suffix = Path(cleaned).suffix
        cleaned = f"{cleaned[: max_length - len(suffix)]}{suffix}"
    return cleaned


def unique_destination(directory: Path, filename: str) -> Path:
    """Return a non-existing path, adding a numeric suffix when necessary."""
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / filename
    if not candidate.exists():
        return candidate
    for index in count(1):
        candidate = directory / f"{Path(filename).stem}_{index}{Path(filename).suffix}"
        if not candidate.exists():
            return candidate
    raise OSError("could not find an available destination filename")


def deduplicate_records(
    records: Iterable[Mapping[str, object]], key: str
) -> tuple[list[Mapping[str, object]], int]:
    """Keep the first record for each key and return records plus duplicate count."""
    seen: set[object] = set()
    unique: list[Mapping[str, object]] = []
    duplicates = 0
    for record in records:
        if key not in record:
            raise KeyError(f"record is missing deduplication key: {key}")
        if record[key] in seen:
            duplicates += 1
            continue
        seen.add(record[key])
        unique.append(record)
    return unique, duplicates
