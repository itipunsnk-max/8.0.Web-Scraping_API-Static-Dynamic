"""Fetch records from a public JSON API and export them to three formats."""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

DEFAULT_API_URL = "https://jsonplaceholder.typicode.com/todos"
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_LIMIT = 5
DEFAULT_USER_AGENT = "web-scraping-zero-to-practical/1.0"
DEFAULT_OUTPUT_DIR = Path("output/api_first")
REQUIRED_FIELDS = ("userId", "id", "title", "completed")


class ApiDataError(RuntimeError):
    """Raised when an API request or response cannot be used safely."""


def parse_args() -> argparse.Namespace:
    """Read optional command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="Maximum records to request")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for exports")
    return parser.parse_args()


def load_settings(args: argparse.Namespace) -> tuple[str, float, int, str, Path]:
    """Load API settings from environment variables and command-line overrides."""
    load_dotenv()
    api_url = os.getenv("API_BASE_URL", DEFAULT_API_URL).strip()
    timeout = float(os.getenv("API_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))
    limit = args.limit if args.limit is not None else int(os.getenv("API_LIMIT", str(DEFAULT_LIMIT)))
    user_agent = os.getenv("USER_AGENT", DEFAULT_USER_AGENT).strip()
    output_dir = args.output_dir or Path(os.getenv("OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR)))

    if not api_url.startswith(("https://", "http://")):
        raise ApiDataError("API_BASE_URL must start with http:// or https://")
    if timeout <= 0:
        raise ApiDataError("API_TIMEOUT_SECONDS must be greater than zero")
    if not 1 <= limit <= 100:
        raise ApiDataError("limit must be between 1 and 100 for this example")
    if not user_agent:
        raise ApiDataError("USER_AGENT must not be empty")
    return api_url, timeout, limit, user_agent, output_dir


def fetch_todos(
    api_url: str,
    timeout: float,
    limit: int,
    user_agent: str,
    session: requests.Session | None = None,
) -> list[dict[str, Any]]:
    """Fetch and validate Todo records from the public API."""
    owns_session = session is None
    http = session or requests.Session()
    headers = {"Accept": "application/json", "User-Agent": user_agent}

    try:
        response = http.get(api_url, params={"_limit": limit}, headers=headers, timeout=timeout)
    except requests.Timeout as error:
        raise ApiDataError("API request timed out; check the endpoint or network.") from error
    except requests.RequestException as error:
        raise ApiDataError("API request failed; check the endpoint or network.") from error
    finally:
        if owns_session:
            http.close()

    if response.status_code in (401, 403):
        raise ApiDataError(f"API returned {response.status_code}; stop and check permission.")
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise ApiDataError(f"API returned HTTP {response.status_code}.") from error

    try:
        payload = response.json()
    except ValueError as error:
        raise ApiDataError("API response was not valid JSON.") from error

    if not isinstance(payload, list):
        raise ApiDataError("API response must be a JSON array.")
    records: list[dict[str, Any]] = []
    for position, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ApiDataError(f"Record {position} is not a JSON object.")
        missing = [field for field in REQUIRED_FIELDS if field not in item]
        if missing:
            raise ApiDataError(f"Record {position} is missing fields: {', '.join(missing)}")
        records.append({field: item[field] for field in REQUIRED_FIELDS})
    return records


def build_export_records(records: list[dict[str, Any]], source_url: str) -> list[dict[str, Any]]:
    """Add stable field names and retrieval metadata to API records."""
    scraped_at = datetime.now(UTC).isoformat()
    return [
        {
            "source_url": source_url,
            "scraped_at": scraped_at,
            "record_id": item["id"],
            "user_id": item["userId"],
            "title": item["title"],
            "completed": item["completed"],
        }
        for item in records
    ]


def export_records(records: list[dict[str, Any]], output_dir: Path) -> dict[str, Path]:
    """Write records as JSON, CSV and Excel, returning created paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(records)
    paths = {
        "json": output_dir / "todos.json",
        "csv": output_dir / "todos.csv",
        "excel": output_dir / "todos.xlsx",
    }
    paths["json"].write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    dataframe.to_csv(paths["csv"], index=False, encoding="utf-8-sig")
    dataframe.to_excel(paths["excel"], index=False)
    return paths


def main() -> int:
    """Run the API-first extraction and export workflow."""
    try:
        args = parse_args()
        api_url, timeout, limit, user_agent, output_dir = load_settings(args)
        raw_records = fetch_todos(api_url, timeout, limit, user_agent)
        records = build_export_records(raw_records, api_url)
        paths = export_records(records, output_dir)
    except (ApiDataError, ImportError, OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1

    print(f"Fetched {len(records)} records from {api_url}")
    print(f"JSON: {paths['json']}")
    print(f"CSV: {paths['csv']}")
    print(f"Excel: {paths['excel']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
