"""Scrape a local static product page and export cleaned records."""

from __future__ import annotations

import argparse
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

DEFAULT_URL = "http://127.0.0.1:8000/products.html"
DEFAULT_TIMEOUT = 10.0
DEFAULT_USER_AGENT = "web-scraping-zero-to-practical/1.0"
DEFAULT_OUTPUT_DIR = Path("output/static_page")

SELECTORS = {
    "product_card": ".product-card",
    "product_name": ".product-name",
    "product_price": ".product-price",
    "availability": ".availability",
    "product_link": ".product-link",
    "inventory_table": "#inventory-table",
    "inventory_row": "#inventory-table tbody tr",
}

LOGGER = logging.getLogger(__name__)


class StaticScrapingError(RuntimeError):
    """Raised when a static page cannot be fetched or parsed safely."""


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Static HTML page URL")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Request timeout")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def fetch_html(
    url: str,
    timeout: float,
    user_agent: str,
    session: requests.Session | None = None,
) -> str:
    """Fetch HTML with timeout, headers, status validation and encoding handling."""
    if timeout <= 0:
        raise StaticScrapingError("timeout must be greater than zero")
    if not url.startswith(("http://", "https://")):
        raise StaticScrapingError("url must start with http:// or https://")

    owns_session = session is None
    http = session or requests.Session()
    try:
        response = http.get(
            url,
            headers={"Accept": "text/html", "User-Agent": user_agent},
            timeout=timeout,
        )
        if response.status_code in (401, 403):
            raise StaticScrapingError(
                f"HTTP {response.status_code}: stop and check permission; do not bypass access control"
            )
        response.raise_for_status()
        if not response.encoding:
            response.encoding = response.apparent_encoding or "utf-8"
        return response.text
    except requests.Timeout as error:
        raise StaticScrapingError("request timed out; check the URL or local server") from error
    except requests.HTTPError as error:
        raise StaticScrapingError(f"HTTP request failed with status {response.status_code}") from error
    except requests.RequestException as error:
        raise StaticScrapingError("request failed; check the URL or network") from error
    finally:
        if owns_session:
            http.close()


def clean_text(element: Tag | None) -> str | None:
    """Return normalized text from an Element, or None when it is missing."""
    if element is None:
        return None
    value = element.get_text(" ", strip=True)
    return value or None


def clean_price(raw_price: str | None) -> float | None:
    """Convert a currency string such as ``฿1,299.00`` to a number."""
    if not raw_price:
        return None
    normalized = re.sub(r"[^0-9.-]", "", raw_price.replace(",", ""))
    try:
        return float(normalized) if normalized else None
    except ValueError:
        return None


def absolute_url(source_url: str, href: str | None) -> str | None:
    """Resolve a relative link against the page URL."""
    if not href:
        return None
    return urljoin(source_url, href)


def parse_products(html: str, source_url: str) -> list[dict[str, Any]]:
    """Extract product cards and flag missing fields instead of crashing."""
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(SELECTORS["product_card"])
    if not cards:
        raise StaticScrapingError("no product cards matched the configured selector")

    scraped_at = datetime.now(UTC).isoformat()
    records: list[dict[str, Any]] = []
    for position, card in enumerate(cards, start=1):
        record_id = card.get("data-product-id") or f"product-{position:03d}"
        name_element = card.select_one(SELECTORS["product_name"])
        price_element = card.select_one(SELECTORS["product_price"])
        availability_element = card.select_one(SELECTORS["availability"])
        link_element = card.select_one(SELECTORS["product_link"])

        raw_price = clean_text(price_element)
        availability = clean_text(availability_element)
        name = clean_text(name_element)
        href = link_element.get("href") if link_element else None
        flags: list[str] = []
        if name is None:
            flags.append("missing_name")
            LOGGER.warning("Product %s is missing name selector", record_id)
        if raw_price is None:
            flags.append("missing_price")
            LOGGER.warning("Product %s is missing price selector", record_id)
        if availability is None:
            flags.append("missing_availability")
            LOGGER.warning("Product %s is missing availability selector", record_id)
        if href is None:
            flags.append("missing_url")
            LOGGER.warning("Product %s is missing URL selector", record_id)

        records.append(
            {
                "source_url": source_url,
                "scraped_at": scraped_at,
                "record_id": record_id,
                "name": name,
                "price": clean_price(raw_price),
                "raw_price": raw_price,
                "availability": availability,
                "url": absolute_url(source_url, href),
                "data_quality_flag": ";".join(flags) if flags else "ok",
            }
        )
    return records


def parse_inventory_table(html: str, source_url: str) -> list[dict[str, Any]]:
    """Extract rows from the inventory table on the same static page."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one(SELECTORS["inventory_table"])
    if table is None:
        raise StaticScrapingError("inventory table was not found")

    scraped_at = datetime.now(UTC).isoformat()
    records: list[dict[str, Any]] = []
    for row in soup.select(SELECTORS["inventory_row"]):
        cells = row.select("td")
        if len(cells) < 4:
            LOGGER.warning("Skipping inventory row with fewer than four cells")
            continue
        records.append(
            {
                "source_url": source_url,
                "scraped_at": scraped_at,
                "record_id": row.get("data-product-id"),
                "name": clean_text(cells[0]),
                "stock": clean_text(cells[1]),
                "last_checked": clean_text(cells[2]),
                "status": clean_text(cells[3]),
                "data_quality_flag": "ok",
            }
        )
    return records


def export_records(records: list[dict[str, Any]], output_dir: Path, file_stem: str) -> dict[str, Path]:
    """Export records to UTF-8 CSV and Excel."""
    output_dir.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(records)
    paths = {
        "csv": output_dir / f"{file_stem}.csv",
        "excel": output_dir / f"{file_stem}.xlsx",
    }
    dataframe.to_csv(paths["csv"], index=False, encoding="utf-8-sig")
    dataframe.to_excel(paths["excel"], index=False)
    return paths


def main() -> int:
    """Run the static page extraction workflow."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    try:
        html = fetch_html(args.url, args.timeout, args.user_agent)
        products = parse_products(html, args.url)
        inventory = parse_inventory_table(html, args.url)
        product_paths = export_records(products, args.output_dir, "products")
        inventory_paths = export_records(inventory, args.output_dir, "inventory")
    except (ImportError, OSError, StaticScrapingError, ValueError) as error:
        LOGGER.error("%s", error)
        return 1

    print(f"Parsed {len(products)} products and {len(inventory)} inventory rows")
    for path in (*product_paths.values(), *inventory_paths.values()):
        print(f"Output: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
