"""Normalize a location directory into map-friendly records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from bs4 import BeautifulSoup


def parse_locations(html: str) -> list[dict[str, object]]:
    soup = BeautifulSoup(html, "lxml")
    locations = []
    for card in soup.select("[data-location]"):
        name = card.select_one("[data-name]")
        address = card.select_one("[data-address]")
        if not name or not address:
            continue
        locations.append(
            {
                "name": name.get_text(" ", strip=True),
                "address": address.get_text(" ", strip=True),
                "latitude": float(card["data-latitude"]),
                "longitude": float(card["data-longitude"]),
            }
        )
    return locations


def validate_coordinates(records: list[dict[str, object]]) -> None:
    for record in records:
        if not -90 <= float(record["latitude"]) <= 90:
            raise ValueError(f"invalid latitude for {record['name']}")
        if not -180 <= float(record["longitude"]) <= 180:
            raise ValueError(f"invalid longitude for {record['name']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a location directory fixture")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    records = parse_locations(args.input.read_text(encoding="utf-8"))
    validate_coordinates(records)
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
