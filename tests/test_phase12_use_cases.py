"""Contract tests for all seven Phase 12 use cases."""

from __future__ import annotations

import json
from pathlib import Path

from use_cases.document_downloader.app import discover_documents, safe_filename
from use_cases.location_directory.app import parse_locations, validate_coordinates
from use_cases.power_bi_pipeline.app import load_records
from use_cases.price_monitor.app import compare_prices, load_products
from use_cases.public_announcements.app import filter_announcements, parse_announcements
from use_cases.solar_datasheet_catalog.app import filter_by_power, parse_catalog
from use_cases.weather_api.app import normalize_forecast, summarize_forecast

USE_CASES = Path(__file__).parents[1] / "use_cases"


def test_price_monitor_detects_drop_and_new_product() -> None:
    previous = load_products(USE_CASES / "price_monitor" / "previous.json")
    current = load_products(USE_CASES / "price_monitor" / "current.json")
    changes = compare_prices(previous, current)
    assert [item["record_id"] for item in changes] == ["p-001", "p-003"]
    assert changes[0]["change_pct"] == -7.75
    assert changes[1]["previous_price"] is None


def test_public_announcement_tracker_filters_by_keyword_and_date() -> None:
    html = (USE_CASES / "public_announcements" / "announcements.html").read_text(encoding="utf-8")
    records = parse_announcements(html, "https://example.test/")
    filtered = filter_announcements(records, keyword="road", since=None)
    assert len(filtered) == 1
    assert filtered[0]["url"] == "https://example.test/announcements/road"


def test_document_downloader_allows_only_document_extensions() -> None:
    html = (USE_CASES / "document_downloader" / "documents.html").read_text(encoding="utf-8")
    documents = discover_documents(html, "https://example.test/documents/")
    assert [item["name"] for item in documents] == ["annual-report.pdf", "data-sheet.xlsx"]
    assert safe_filename("https://example.test/files/a report.pdf") == "a_report.pdf"


def test_location_directory_parses_and_validates_coordinates() -> None:
    html = (USE_CASES / "location_directory" / "locations.html").read_text(encoding="utf-8")
    records = parse_locations(html)
    validate_coordinates(records)
    assert len(records) == 2
    assert records[0]["name"] == "Bangkok Service Center"


def test_weather_api_normalizes_records_and_summary() -> None:
    payload = json.loads((USE_CASES / "weather_api" / "forecast.json").read_text(encoding="utf-8"))
    records = normalize_forecast(payload)
    assert len(records) == 2
    assert summarize_forecast(records) == {"average_temperature_c": 31.5, "total_precipitation_mm": 10.5}


def test_solar_catalog_filters_by_power() -> None:
    html = (USE_CASES / "solar_datasheet_catalog" / "catalog.html").read_text(encoding="utf-8")
    catalog = parse_catalog(html, "https://example.test/solar/")
    result = filter_by_power(catalog, 400)
    assert len(result) == 1
    assert result[0]["datasheet_url"] == "https://example.test/files/sun-450.pdf"


def test_power_bi_pipeline_input_is_json_array() -> None:
    records = load_records(USE_CASES / "power_bi_pipeline" / "input.json")
    assert len(records) == 3
    assert records[2]["record_id"] == "asset-002"
