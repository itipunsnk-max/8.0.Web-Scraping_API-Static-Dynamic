"""Tests for Phase 10 schema and export pipeline."""

from __future__ import annotations

import json
import sqlite3

import pytest

from web_scraping_course.exceptions import ValidationError
from web_scraping_course.pipeline import SCHEMA_COLUMNS, run_pipeline


def test_pipeline_writes_all_formats_and_removes_duplicate(tmp_path) -> None:
    records = [
        {"record_id": "a", "name": "Alpha", "value": "10.5", "status": "active"},
        {"record_id": "a", "name": "Alpha duplicate", "value": "11", "status": "active"},
        {"record_id": "b", "name": "Beta", "value": "", "status": "pending"},
    ]
    result = run_pipeline(records, tmp_path, "https://example.test/catalog", scraped_at="2026-07-30T00:00:00+00:00")

    assert result.input_count == 3
    assert result.processed_count == 2
    assert result.duplicate_count == 1
    assert result.raw_path.exists()
    assert set(result.processed_paths) == {"json", "csv", "excel", "sqlite"}
    for path in result.processed_paths.values():
        assert path.exists()
    exported = json.loads(result.processed_paths["json"].read_text(encoding="utf-8"))
    assert list(exported[0]) == list(SCHEMA_COLUMNS)
    assert exported[1]["data_quality_flag"] == "missing_value"

    with sqlite3.connect(result.processed_paths["sqlite"]) as connection:
        rows = connection.execute("SELECT record_id, value FROM records ORDER BY record_id").fetchall()
    assert rows == [("a", 10.5), ("b", None)]


def test_pipeline_upserts_incrementally(tmp_path) -> None:
    run_pipeline(
        [{"record_id": "a", "name": "Alpha", "value": 1, "status": "active"}],
        tmp_path,
        "https://example.test/catalog",
    )
    run_pipeline(
        [{"record_id": "a", "name": "Alpha updated", "value": 2, "status": "inactive"}],
        tmp_path,
        "https://example.test/catalog",
    )
    with sqlite3.connect(tmp_path / "processed" / "records.sqlite3") as connection:
        row = connection.execute("SELECT name, value, status FROM records WHERE record_id = 'a'").fetchone()
    assert row == ("Alpha updated", 2.0, "inactive")


def test_pipeline_requires_absolute_source_url(tmp_path) -> None:
    with pytest.raises(ValidationError):
        run_pipeline([{"record_id": "a", "name": "Alpha", "value": 1}], tmp_path, "/relative")
