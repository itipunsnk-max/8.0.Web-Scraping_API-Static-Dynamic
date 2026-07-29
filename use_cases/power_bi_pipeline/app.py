"""Create Power BI-friendly exports using the shared Phase 10 pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from web_scraping_course.pipeline import run_pipeline


def load_records(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise TypeError("pipeline input must be a JSON array")
    return [dict(item) for item in payload]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export records for Power BI ingestion")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-url", default="https://example.test/power-bi-source")
    args = parser.parse_args()
    result = run_pipeline(load_records(args.input), args.output_dir, args.source_url)
    print(
        json.dumps(
            {
                "raw": str(result.raw_path),
                "processed": {key: str(value) for key, value in result.processed_paths.items()},
                "processed_count": result.processed_count,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
