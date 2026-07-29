"""Read a JavaScript-rendered catalog with Playwright."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

DEFAULT_URL = "http://127.0.0.1:8000/dynamic/index.html"
DEFAULT_OUTPUT_DIR = Path("output/playwright_dynamic")
DEFAULT_TIMEOUT_MS = 10_000
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    parser.add_argument("--headed", action="store_true", help="show the browser window")
    return parser.parse_args()


def wait_for_dynamic_table(page: Page, timeout_ms: int) -> None:
    """Wait for the first JavaScript-rendered row without using time.sleep()."""
    page.locator("#dynamic-status").wait_for(state="visible", timeout=timeout_ms)
    page.locator("#catalog-table tbody tr").first.wait_for(state="visible", timeout=timeout_ms)


def load_all_pages(page: Page, timeout_ms: int) -> int:
    """Click Load more until the browser disables it and return row count."""
    while page.locator("#load-more").is_enabled():
        previous_count = page.locator("#catalog-table tbody tr").count()
        page.get_by_role("button", name="Load more").click()
        page.wait_for_function(
            "(previous) => document.querySelectorAll('#catalog-table tbody tr').length > previous",
            arg=previous_count,
            timeout=timeout_ms,
        )
    return page.locator("#catalog-table tbody tr").count()


def read_rows(page: Page) -> list[dict[str, str]]:
    """Read visible table rows into normalized dictionaries."""
    rows: list[dict[str, str]] = []
    for row in page.locator("#catalog-table tbody tr").all():
        cells = row.locator("td").all_text_contents()
        if len(cells) != 4:
            raise ValueError(f"unexpected table row: {cells}")
        rows.append({"id": cells[0], "name": cells[1], "category": cells[2], "price": cells[3]})
    return rows


def save_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    """Save extracted rows as UTF-8 CSV."""
    with output_path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["id", "name", "category", "price"])
        writer.writeheader()
        writer.writerows(rows)


def run(url: str, output_dir: Path, timeout_ms: int, headed: bool) -> int:
    """Run the browser workflow and return a process exit code."""
    if timeout_ms <= 0:
        raise ValueError("timeout-ms must be greater than zero")
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(timeout_ms)
        try:
            page.goto(url, wait_until="domcontentloaded")
            wait_for_dynamic_table(page, timeout_ms)
            page.screenshot(path=str(output_dir / "dynamic-catalog-initial.png"), full_page=True)

            page.locator("#category-filter").select_option("books")
            page.get_by_role("button", name="Apply filter").click()
            filtered_rows = read_rows(page)
            if not filtered_rows or any(row["category"] != "books" for row in filtered_rows):
                raise ValueError("category filter did not return only books")

            page.locator("#category-filter").select_option("all")
            page.get_by_role("button", name="Apply filter").click()
            total_rows = load_all_pages(page, timeout_ms)
            rows = read_rows(page)
            if total_rows != 6 or len(rows) != 6:
                raise ValueError(f"expected 6 dynamic rows, got {total_rows}")
            save_rows(rows, output_dir / "dynamic_items.csv")
            (output_dir / "dynamic_items.json").write_text(
                json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            page.screenshot(path=str(output_dir / "dynamic-catalog-final.png"), full_page=True)

            with page.expect_download(timeout=timeout_ms) as download_info:
                page.get_by_role("button", name="Download CSV").click()
            download = download_info.value
            download.save_as(output_dir / download.suggested_filename)
        finally:
            context.close()
            browser.close()

    print(f"Read {len(rows)} dynamic rows")
    print(f"Saved browser download: {download.suggested_filename}")
    return 0


def main() -> int:
    """Run the Playwright example with a clear error for missing browser setup."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    try:
        return run(args.url, args.output_dir, args.timeout_ms, args.headed)
    except PlaywrightTimeoutError as error:
        LOGGER.error("Playwright timeout: %s", error)
        return 1
    except (OSError, RuntimeError, ValueError) as error:
        LOGGER.error("Playwright example failed: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
