"""Normalize a weather API response into daily records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def normalize_forecast(payload: dict[str, Any]) -> list[dict[str, Any]]:
    location = payload.get("location", "unknown")
    records = []
    for item in payload.get("forecast", []):
        records.append(
            {
                "location": location,
                "date": item["date"],
                "temperature_c": float(item["temperature_c"]),
                "condition": str(item["condition"]).strip(),
                "precipitation_mm": float(item.get("precipitation_mm", 0)),
            }
        )
    return records


def summarize_forecast(records: list[dict[str, Any]]) -> dict[str, float]:
    if not records:
        return {"average_temperature_c": 0.0, "total_precipitation_mm": 0.0}
    return {
        "average_temperature_c": round(sum(item["temperature_c"] for item in records) / len(records), 2),
        "total_precipitation_mm": round(sum(item["precipitation_mm"] for item in records), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a weather API fixture")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    records = normalize_forecast(json.loads(args.input.read_text(encoding="utf-8")))
    print(json.dumps({"records": records, "summary": summarize_forecast(records)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
