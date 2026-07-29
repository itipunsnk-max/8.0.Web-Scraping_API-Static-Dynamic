"""Build a searchable catalog of solar products and datasheet links."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_catalog(html: str, base_url: str) -> list[dict[str, object]]:
    soup = BeautifulSoup(html, "lxml")
    catalog = []
    for card in soup.select("[data-solar-product]"):
        title = card.select_one("[data-title]")
        manufacturer = card.select_one("[data-manufacturer]")
        power = card.select_one("[data-power-w]")
        datasheet = card.select_one("a[data-datasheet][href]")
        if not all((title, manufacturer, power, datasheet)):
            continue
        catalog.append(
            {
                "name": title.get_text(" ", strip=True),
                "manufacturer": manufacturer.get_text(" ", strip=True),
                "power_w": float(power.get_text(strip=True)),
                "datasheet_url": urljoin(base_url, datasheet["href"]),
            }
        )
    return catalog


def filter_by_power(catalog: list[dict[str, object]], minimum_w: float) -> list[dict[str, object]]:
    return [item for item in catalog if float(item["power_w"]) >= minimum_w]


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a solar datasheet catalog fixture")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--minimum-w", type=float, default=0)
    args = parser.parse_args()
    catalog = parse_catalog(args.input.read_text(encoding="utf-8"), "https://example.test/solar/")
    print(json.dumps(filter_by_power(catalog, args.minimum_w), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
