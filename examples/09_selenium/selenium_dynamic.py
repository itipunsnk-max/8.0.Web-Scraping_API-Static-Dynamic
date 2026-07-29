"""Read the same JavaScript-rendered catalog with Selenium for comparison."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

DEFAULT_URL = "http://127.0.0.1:8000/dynamic/index.html"
DEFAULT_OUTPUT_DIR = Path("output/selenium_dynamic")
DEFAULT_TIMEOUT_SECONDS = 10
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--headed", action="store_true", help="show the browser window")
    return parser.parse_args()


def build_driver(download_dir: Path, headed: bool, timeout_seconds: int) -> webdriver.Chrome:
    """Create a Chrome WebDriver with a controlled download directory."""
    options = Options()
    if not headed:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1000")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(download_dir.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(timeout_seconds)
    return driver


def wait_for_rows(driver: webdriver.Chrome, timeout_seconds: int, minimum: int = 1) -> None:
    """Wait until JavaScript has rendered at least the requested rows."""
    WebDriverWait(driver, timeout_seconds).until(
        lambda browser: len(browser.find_elements(By.CSS_SELECTOR, "#catalog-table tbody tr"))
        >= minimum
    )


def read_rows(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Read visible table rows into normalized dictionaries."""
    rows: list[dict[str, str]] = []
    for row in driver.find_elements(By.CSS_SELECTOR, "#catalog-table tbody tr"):
        cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if len(cells) != 4:
            raise ValueError(f"unexpected table row: {cells}")
        rows.append({"id": cells[0], "name": cells[1], "category": cells[2], "price": cells[3]})
    return rows


def load_all_pages(driver: webdriver.Chrome, timeout_seconds: int) -> int:
    """Click Load more until the button is disabled and return row count."""
    while driver.find_element(By.ID, "load-more").is_enabled():
        previous_count = len(driver.find_elements(By.CSS_SELECTOR, "#catalog-table tbody tr"))
        minimum_count = previous_count + 1
        driver.find_element(By.ID, "load-more").click()
        WebDriverWait(driver, timeout_seconds).until(
            lambda browser, minimum=minimum_count: len(
                browser.find_elements(By.CSS_SELECTOR, "#catalog-table tbody tr")
            )
            >= minimum
        )
    return len(driver.find_elements(By.CSS_SELECTOR, "#catalog-table tbody tr"))


def save_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    """Save extracted rows as UTF-8 CSV."""
    with output_path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["id", "name", "category", "price"])
        writer.writeheader()
        writer.writerows(rows)


def run(url: str, output_dir: Path, timeout_seconds: int, headed: bool) -> int:
    """Run the Selenium workflow and return a process exit code."""
    if timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be greater than zero")
    output_dir.mkdir(parents=True, exist_ok=True)
    download_path = output_dir / "dynamic-catalog.csv"
    download_path.unlink(missing_ok=True)
    Path(f"{download_path}.crdownload").unlink(missing_ok=True)

    driver = build_driver(output_dir, headed, timeout_seconds)
    try:
        wait = WebDriverWait(driver, timeout_seconds)
        driver.get(url)
        wait.until(EC.visibility_of_element_located((By.ID, "dynamic-status")))
        wait_for_rows(driver, timeout_seconds)
        if not driver.save_screenshot(str(output_dir / "dynamic-catalog-initial.png")):
            raise OSError("could not save initial screenshot")

        Select(driver.find_element(By.ID, "category-filter")).select_by_value("books")
        driver.find_element(By.CSS_SELECTOR, "#filter-form button[type='submit']").click()
        filtered_rows = read_rows(driver)
        if not filtered_rows or any(row["category"] != "books" for row in filtered_rows):
            raise ValueError("category filter did not return only books")

        Select(driver.find_element(By.ID, "category-filter")).select_by_value("all")
        driver.find_element(By.CSS_SELECTOR, "#filter-form button[type='submit']").click()
        total_rows = load_all_pages(driver, timeout_seconds)
        rows = read_rows(driver)
        if total_rows != 6 or len(rows) != 6:
            raise ValueError(f"expected 6 dynamic rows, got {total_rows}")
        save_rows(rows, output_dir / "dynamic_items.csv")
        (output_dir / "dynamic_items.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if not driver.save_screenshot(str(output_dir / "dynamic-catalog-final.png")):
            raise OSError("could not save final screenshot")

        driver.find_element(By.ID, "download-csv").click()
        WebDriverWait(driver, timeout_seconds).until(lambda _: download_path.exists())
        WebDriverWait(driver, timeout_seconds).until(
            lambda _: not Path(f"{download_path}.crdownload").exists()
        )
    finally:
        driver.quit()

    print(f"Read {len(rows)} dynamic rows")
    print(f"Saved Selenium download: {download_path.name}")
    return 0


def main() -> int:
    """Run the Selenium example with clear setup and timeout errors."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    try:
        return run(args.url, args.output_dir, args.timeout_seconds, args.headed)
    except TimeoutException as error:
        LOGGER.error("Selenium timeout: %s", error)
        return 1
    except (OSError, ValueError, WebDriverException) as error:
        LOGGER.error("Selenium example failed: %s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
