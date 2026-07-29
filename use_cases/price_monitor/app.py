"""Compare product prices from two JSON snapshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_products(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise TypeError("product snapshot must be a JSON array")
    return [dict(item) for item in payload]


def compare_prices(
    previous: list[dict[str, Any]], current: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    old_by_id = {str(item["record_id"]): item for item in previous}
    changes = []
    for item in current:
        record_id = str(item["record_id"])
        old_price = old_by_id.get(record_id, {}).get("price")
        new_price = float(item["price"])
        if old_price is None or float(old_price) != new_price:
            change = None if old_price is None else round(new_price - float(old_price), 2)
            change_pct = None if old_price in (None, 0) else round(change / float(old_price) * 100, 2)
            changes.append(
                {
                    "record_id": record_id,
                    "name": item.get("name", ""),
                    "previous_price": old_price,
                    "current_price": new_price,
                    "change": change,
                    "change_pct": change_pct,
                }
            )
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two product price snapshots")
    parser.add_argument("--previous", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare_prices(load_products(args.previous), load_products(args.current))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
