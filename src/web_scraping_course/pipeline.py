"""Schema-first raw/processed data pipeline and multi-format exporters."""

from __future__ import annotations

import csv
import json
import sqlite3
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd

from .exceptions import ExportError, ValidationError
from .utils import deduplicate_records

SCHEMA_COLUMNS = (
    "source_url",
    "scraped_at",
    "record_id",
    "name",
    "value",
    "status",
    "raw_value",
    "data_quality_flag",
)


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Paths and counts produced by one pipeline run."""

    raw_path: Path
    processed_paths: dict[str, Path]
    input_count: int
    processed_count: int
    duplicate_count: int


def _validate_source_url(source_url: str) -> None:
    parsed = urlparse(source_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("source_url must be an absolute http(s) URL")


def _serialize_raw_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _normalize_numeric(value: object) -> tuple[float | None, str]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None, "missing_value"
    try:
        return float(value), "ok"
    except (TypeError, ValueError):
        return None, "invalid_value"


def normalize_records(
    records: Iterable[Mapping[str, Any]],
    source_url: str,
    *,
    scraped_at: str | None = None,
) -> list[dict[str, Any]]:
    """Normalize raw mappings into the stable Phase 10 schema."""
    _validate_source_url(source_url)
    timestamp = scraped_at or datetime.now(UTC).isoformat()
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for position, record in enumerate(records, start=1):
        record_id = record.get("record_id", record.get("id"))
        if record_id in (None, ""):
            raise ValidationError(f"record {position} is missing record_id")
        record_key = str(record_id)
        name = record.get("name", record.get("title", ""))
        value, value_flag = _normalize_numeric(record.get("value"))
        flags = []
        if not str(name).strip():
            flags.append("missing_name")
        if value_flag != "ok":
            flags.append(value_flag)
        if record_key in seen_ids:
            flags.append("duplicate_record")
        seen_ids.add(record_key)
        normalized.append(
            {
                "source_url": source_url,
                "scraped_at": timestamp,
                "record_id": record_key,
                "name": str(name).strip(),
                "value": value,
                "status": str(record.get("status", "active")).strip() or "unknown",
                "raw_value": _serialize_raw_value(record.get("value")),
                "data_quality_flag": ";".join(flags) if flags else "ok",
            }
        )
    return normalized


def _write_json(records: list[Mapping[str, Any]], path: Path) -> None:
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(records: list[Mapping[str, Any]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(SCHEMA_COLUMNS))
        writer.writeheader()
        writer.writerows(records)


def _write_excel(records: list[Mapping[str, Any]], path: Path) -> None:
    pd.DataFrame(records, columns=SCHEMA_COLUMNS).to_excel(path, index=False)


def _write_sqlite(records: list[Mapping[str, Any]], path: Path) -> None:
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                source_url TEXT NOT NULL,
                scraped_at TEXT NOT NULL,
                record_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                value REAL,
                status TEXT NOT NULL,
                raw_value TEXT NOT NULL,
                data_quality_flag TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO records (
                source_url, scraped_at, record_id, name, value, status, raw_value, data_quality_flag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(record_id) DO UPDATE SET
                source_url = excluded.source_url,
                scraped_at = excluded.scraped_at,
                name = excluded.name,
                value = excluded.value,
                status = excluded.status,
                raw_value = excluded.raw_value,
                data_quality_flag = excluded.data_quality_flag
            """,
            [tuple(record[column] for column in SCHEMA_COLUMNS) for record in records],
        )


def export_processed(records: list[Mapping[str, Any]], output_dir: Path) -> dict[str, Path]:
    """Export processed records to JSON, UTF-8 CSV, Excel and SQLite."""
    if not records:
        raise ExportError("cannot export an empty processed dataset")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": output_dir / "records.json",
        "csv": output_dir / "records.csv",
        "excel": output_dir / "records.xlsx",
        "sqlite": output_dir / "records.sqlite3",
    }
    try:
        _write_json(records, paths["json"])
        _write_csv(records, paths["csv"])
        _write_excel(records, paths["excel"])
        _write_sqlite(records, paths["sqlite"])
    except (OSError, ValueError, sqlite3.Error) as error:
        raise ExportError(f"could not export processed dataset: {error}") from error
    return paths


def run_pipeline(
    records: Iterable[Mapping[str, Any]],
    output_dir: Path,
    source_url: str,
    *,
    scraped_at: str | None = None,
) -> PipelineResult:
    """Store raw input, normalize/deduplicate it, then export processed data."""
    raw_records = list(records)
    normalized = normalize_records(raw_records, source_url, scraped_at=scraped_at)
    processed, duplicate_count = deduplicate_records(normalized, "record_id")
    raw_dir = output_dir / "raw"
    processed_dir = output_dir / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / "records.json"
    _write_json(raw_records, raw_path)
    processed_paths = export_processed(processed, processed_dir)
    return PipelineResult(
        raw_path=raw_path,
        processed_paths=processed_paths,
        input_count=len(raw_records),
        processed_count=len(processed),
        duplicate_count=duplicate_count,
    )
