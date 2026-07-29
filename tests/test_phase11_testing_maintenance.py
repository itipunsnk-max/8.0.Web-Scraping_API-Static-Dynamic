"""Fixture-based parser, mock HTTP and maintenance regression tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import requests
import responses
from bs4 import BeautifulSoup
from static_scraper import StaticScrapingError, fetch_html, parse_inventory_table, parse_products

from web_scraping_course.exceptions import ValidationError
from web_scraping_course.maintenance import (
    compare_snapshots,
    first_matching,
    schema_issues,
    snapshot_digest,
    validate_record_count,
)
from web_scraping_course.pipeline import normalize_records

FIXTURES = Path(__file__).parent / "fixtures"


def test_static_parser_fixture_and_exports_contract() -> None:
    html = (FIXTURES / "static_products.html").read_text(encoding="utf-8")
    products = parse_products(html, "https://example.test/products")
    inventory = parse_inventory_table(html, "https://example.test/products")
    assert len(products) == 2
    assert products[0]["record_id"] == "fixture-001"
    assert products[0]["price"] == 1299.0
    assert products[0]["data_quality_flag"] == "ok"
    assert len(inventory) == 2


def test_static_parser_fails_fast_when_selector_disappears() -> None:
    with pytest.raises(StaticScrapingError, match="no product cards"):
        parse_products("<html><body><div class='changed-card'>No match</div></body></html>", "https://example.test")


@responses.activate
def test_mock_http_response_handles_timeout_without_real_network() -> None:
    url = "https://example.test/products"
    responses.add(responses.GET, url, body=requests.Timeout("fixture timeout"))
    with pytest.raises(StaticScrapingError, match="timed out"):
        fetch_html(url, timeout=1, user_agent="phase11-test")


@responses.activate
def test_mock_http_response_returns_fixture_html() -> None:
    url = "https://example.test/products"
    html = (FIXTURES / "static_products.html").read_text(encoding="utf-8")
    responses.add(responses.GET, url, body=html, status=200)
    assert "fixture-001" in fetch_html(url, timeout=1, user_agent="phase11-test")


def test_selector_fallback_and_snapshot_change_detection() -> None:
    soup = BeautifulSoup("<main><h2 class='new-title'>Stable title</h2></main>", "lxml")
    match = first_matching(soup, [".old-title", ".new-title"])
    assert match is not None and match.get_text(strip=True) == "Stable title"
    comparison = compare_snapshots("before", "after")
    assert comparison.changed
    assert snapshot_digest("same") == snapshot_digest("same")


def test_record_count_and_schema_anomaly_checks() -> None:
    validate_record_count(2, minimum=1, maximum=3)
    with pytest.raises(ValidationError, match="record count anomaly"):
        validate_record_count(0, minimum=1)
    assert schema_issues([{"id": 1}, {"name": "missing id"}], ["id", "name"]) == [
        "record 1 missing: name",
        "record 2 missing: id",
    ]


def test_api_json_fixture_and_pipeline_schema() -> None:
    payload = json.loads((FIXTURES / "api_todos.json").read_text(encoding="utf-8"))
    normalized = normalize_records(
        [
            {"record_id": item["id"], "name": item["title"], "value": item["userId"]}
            for item in payload
        ],
        "https://example.test/todos",
        scraped_at="2026-07-30T00:00:00+00:00",
    )
    assert [record["record_id"] for record in normalized] == ["101", "102"]
