"""Scheduled entry point for the Phase 12 price monitor example."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from use_cases.price_monitor.app import compare_prices, load_products
from web_scraping_course.automation import run_job


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a scraping job with lock, log and exit codes")
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    def job() -> None:
        changes = compare_prices(load_products(args.previous), load_products(args.current))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return run_job(
        "price-monitor",
        job,
        lock_path=args.lock,
        log_path=args.log,
    )


if __name__ == "__main__":
    sys.exit(main())
