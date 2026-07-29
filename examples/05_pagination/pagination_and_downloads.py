"""Paginate a local catalog and download permitted PDF/image assets safely."""

from __future__ import annotations

import argparse
import csv
import hashlib
import logging
import re
from itertools import count
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

DEFAULT_START_URL = "http://127.0.0.1:8000/pagination/page-1.html"
DEFAULT_DOWNLOADS_URL = "http://127.0.0.1:8000/downloads.html"
DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_PAGES = 10
DEFAULT_MAX_FILE_BYTES = 5 * 1024 * 1024
DEFAULT_USER_AGENT = "web-scraping-zero-to-practical/1.0"
DEFAULT_OUTPUT_DIR = Path("output/pagination_downloads")

LOGGER = logging.getLogger(__name__)
EXPECTED_CONTENT_TYPES = {
    ".pdf": {"application/pdf"},
    ".svg": {"image/svg+xml", "image/svg"},
}


class PaginationError(RuntimeError):
    """Raised when pagination cannot be completed safely."""


class DownloadError(RuntimeError):
    """Raised when an asset fails validation or cannot be saved safely."""


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-url", default=DEFAULT_START_URL)
    parser.add_argument("--downloads-url", default=DEFAULT_DOWNLOADS_URL)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def fetch_html(session: requests.Session, url: str, timeout: float, user_agent: str) -> str:
    """Fetch an HTML page with explicit timeout and permission handling."""
    if timeout <= 0:
        raise PaginationError("timeout must be greater than zero")
    try:
        response = session.get(
            url,
            headers={"Accept": "text/html", "User-Agent": user_agent},
            timeout=timeout,
        )
        if response.status_code in (401, 403):
            raise PaginationError(f"HTTP {response.status_code}: stop and check permission")
        response.raise_for_status()
        if not response.encoding:
            response.encoding = response.apparent_encoding or "utf-8"
        return response.text
    except requests.Timeout as error:
        raise PaginationError(f"request timed out: {url}") from error
    except requests.HTTPError as error:
        raise PaginationError(f"HTTP {response.status_code} for {url}") from error
    except requests.RequestException as error:
        raise PaginationError(f"request failed: {url}") from error


def parse_item(item: Tag, page_url: str) -> dict[str, Any]:
    """Convert one catalog item into a normalized record."""
    record_id = item.get("data-record-id")
    name_element = item.select_one(".item-name")
    value_element = item.select_one(".item-value")
    if not record_id or name_element is None or value_element is None:
        raise PaginationError(f"catalog item is missing required fields on {page_url}")
    return {
        "record_id": record_id,
        "name": name_element.get_text(" ", strip=True),
        "value": value_element.get_text(" ", strip=True),
        "source_url": page_url,
    }


def paginate_items(
    session: requests.Session,
    start_url: str,
    timeout: float,
    max_pages: int,
    user_agent: str,
) -> list[dict[str, Any]]:
    """Follow Next links with page and record de-duplication."""
    if max_pages < 1:
        raise PaginationError("max-pages must be at least 1")
    records: list[dict[str, Any]] = []
    seen_pages: set[str] = set()
    seen_record_ids: set[str] = set()
    page_url: str | None = start_url
    pages_read = 0

    while page_url:
        if page_url in seen_pages:
            raise PaginationError(f"pagination loop detected at {page_url}")
        if pages_read >= max_pages:
            raise PaginationError("max-pages reached while a next page still exists")
        seen_pages.add(page_url)
        pages_read += 1
        html = fetch_html(session, page_url, timeout, user_agent)
        soup = BeautifulSoup(html, "lxml")
        items = soup.select(".catalog-item")
        if not items:
            raise PaginationError(f"no catalog items found on {page_url}")
        for item in items:
            record = parse_item(item, page_url)
            if record["record_id"] in seen_record_ids:
                LOGGER.warning("Skipping duplicate record %s", record["record_id"])
                continue
            seen_record_ids.add(record["record_id"])
            records.append(record)

        next_element = soup.select_one("a.next-page[href]")
        page_url = urljoin(page_url, next_element["href"]) if next_element else None

    return records


def safe_filename(url: str, fallback: str = "downloaded-file") -> str:
    """Create a safe filename from a URL without allowing path traversal."""
    path_name = Path(unquote(urlparse(url).path)).name or fallback
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", path_name).strip(" .")
    if not cleaned:
        cleaned = fallback
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    if cleaned.split(".")[0].upper() in reserved:
        cleaned = f"_{cleaned}"
    return cleaned


def unique_destination(directory: Path, filename: str) -> Path:
    """Return a non-existing path, adding a numeric suffix when needed."""
    candidate = directory / filename
    if not candidate.exists():
        return candidate
    for index in count(1):
        candidate = directory / f"{Path(filename).stem}_{index}{Path(filename).suffix}"
        if not candidate.exists():
            return candidate
    raise DownloadError("could not find an available destination filename")


def download_file(
    session: requests.Session,
    url: str,
    output_dir: Path,
    timeout: float,
    max_file_bytes: int,
    user_agent: str,
) -> dict[str, Any]:
    """Stream one permitted file, validate it, and return manifest metadata."""
    if max_file_bytes < 1:
        raise DownloadError("max-file-bytes must be greater than zero")
    filename = safe_filename(url)
    suffix = Path(filename).suffix.lower()
    allowed_types = EXPECTED_CONTENT_TYPES.get(suffix)
    if allowed_types is None:
        raise DownloadError(f"unsupported download extension: {suffix or '<none>'}")

    output_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(output_dir, filename)
    partial = destination.with_name(destination.name + ".part")
    total_bytes = 0
    digest = hashlib.sha256()

    try:
        with session.get(
            url,
            headers={"Accept": ", ".join(sorted(allowed_types)), "User-Agent": user_agent},
            timeout=timeout,
            stream=True,
        ) as response:
            if response.status_code in (401, 403):
                raise DownloadError(f"HTTP {response.status_code}: stop and check permission")
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type not in allowed_types:
                raise DownloadError(f"unexpected Content-Type {content_type or '<missing>'} for {filename}")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_file_bytes:
                raise DownloadError(f"file exceeds max-file-bytes: {filename}")

            with partial.open("wb") as output_file:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue
                    total_bytes += len(chunk)
                    if total_bytes > max_file_bytes:
                        raise DownloadError(f"file exceeds max-file-bytes while streaming: {filename}")
                    output_file.write(chunk)
                    digest.update(chunk)
        if total_bytes == 0:
            raise DownloadError(f"downloaded file is empty: {filename}")
        partial.replace(destination)
    except (OSError, requests.RequestException, ValueError) as error:
        if partial.exists():
            partial.unlink()
        raise DownloadError(f"download failed for {url}") from error
    except DownloadError:
        if partial.exists():
            partial.unlink()
        raise

    return {
        "source_url": url,
        "filename": destination.name,
        "path": str(destination),
        "content_type": content_type,
        "bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def download_assets(
    session: requests.Session,
    downloads_url: str,
    output_dir: Path,
    timeout: float,
    max_file_bytes: int,
    user_agent: str,
) -> list[dict[str, Any]]:
    """Read permitted links from a page and download each supported asset."""
    html = fetch_html(session, downloads_url, timeout, user_agent)
    soup = BeautifulSoup(html, "lxml")
    links = soup.select("a.download-link[href]")
    if not links:
        raise DownloadError("no download links found")
    results: list[dict[str, Any]] = []
    for link in links:
        asset_url = urljoin(downloads_url, link["href"])
        results.append(download_file(session, asset_url, output_dir, timeout, max_file_bytes, user_agent))
    return results


def write_manifest(records: list[dict[str, Any]], path: Path) -> None:
    """Write download metadata to a CSV manifest."""
    if not records:
        raise DownloadError("cannot write an empty download manifest")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as manifest_file:
        writer = csv.DictWriter(manifest_file, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    """Run pagination and download workflows."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    try:
        with requests.Session() as session:
            items = paginate_items(
                session, args.start_url, args.timeout, args.max_pages, DEFAULT_USER_AGENT
            )
            download_dir = args.output_dir / "files"
            downloads = download_assets(
                session,
                args.downloads_url,
                download_dir,
                args.timeout,
                args.max_file_bytes,
                DEFAULT_USER_AGENT,
            )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with (args.output_dir / "items.csv").open("w", newline="", encoding="utf-8-sig") as item_file:
            writer = csv.DictWriter(item_file, fieldnames=list(items[0]))
            writer.writeheader()
            writer.writerows(items)
        write_manifest(downloads, args.output_dir / "download_manifest.csv")
    except (DownloadError, OSError, PaginationError, ValueError) as error:
        LOGGER.error("%s", error)
        return 1

    print(f"Fetched {len(items)} unique items from pagination")
    for download in downloads:
        print(
            f"Downloaded {download['filename']} ({download['bytes']} bytes, "
            f"{download['content_type']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
