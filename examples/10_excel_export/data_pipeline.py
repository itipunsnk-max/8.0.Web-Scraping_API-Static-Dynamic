"""Run a local sample through the Phase 10 raw/processed data pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from web_scraping_course.pipeline import run_pipeline

DEFAULT_INPUT = Path("data/samples/phase10_records.json")
DEFAULT_OUTPUT = Path("output/data_pipeline")
DEFAULT_SOURCE_URL = "https://example.test/course-catalog"


def parse_args() -> argparse.Namespace:
    """Read command-line settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    return parser.parse_args()


def main() -> int:
    """Load sample records and export all Phase 10 formats."""
    args = parse_args()
    try:
        records: list[dict[str, Any]] = json.loads(args.input.read_text(encoding="utf-8"))
        result = run_pipeline(records, args.output_dir, args.source_url)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return 1
    print(f"Input records: {result.input_count}")
    print(f"Processed records: {result.processed_count}")
    print(f"Duplicates removed: {result.duplicate_count}")
    print(f"Raw: {result.raw_path}")
    for format_name, path in result.processed_paths.items():
        print(f"{format_name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
