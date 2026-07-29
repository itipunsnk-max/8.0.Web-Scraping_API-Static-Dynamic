"""Fetch a permitted page with the Phase 8 resilient HTTP client."""

from __future__ import annotations

import argparse
from pathlib import Path

from web_scraping_course.config import ScraperConfig
from web_scraping_course.exceptions import ScrapingError
from web_scraping_course.http_client import HttpClient
from web_scraping_course.logging_config import configure_logging

DEFAULT_URL = "http://127.0.0.1:8000/index.html"


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--min-interval", type=float, default=0.2)
    parser.add_argument("--log-file", type=Path, default=Path("output/resilient_http.log"))
    return parser.parse_args()


def main() -> int:
    """Fetch and report a page without logging query values or secrets."""
    args = parse_args()
    logger = configure_logging(log_file=args.log_file)
    config = ScraperConfig(
        timeout=args.timeout,
        max_retries=args.max_retries,
        min_request_interval=args.min_interval,
    )
    try:
        with HttpClient(config, logger=logger) as client:
            text = client.get_text(args.url)
    except ScrapingError as error:
        logger.error("fetch failed: %s", error)
        return 1
    print(f"Fetched {len(text)} characters from {args.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
