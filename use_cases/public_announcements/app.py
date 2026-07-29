"""Track public announcements from a small, stable HTML contract."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_announcements(html: str, base_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    records = []
    for card in soup.select("[data-announcement]"):
        title_node = card.select_one("[data-title]")
        date_node = card.select_one("time")
        link = card.select_one("a[href]")
        if not title_node or not date_node or not link:
            continue
        records.append(
            {
                "title": title_node.get_text(" ", strip=True),
                "published": date_node.get("datetime", date_node.get_text(strip=True)),
                "url": urljoin(base_url, link["href"]),
            }
        )
    return records


def filter_announcements(
    records: list[dict[str, str]], *, keyword: str = "", since: date | None = None
) -> list[dict[str, str]]:
    keyword = keyword.casefold()
    result = []
    for record in records:
        if keyword and keyword not in record["title"].casefold():
            continue
        if since and date.fromisoformat(record["published"]) < since:
            continue
        result.append(record)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter announcements from a local HTML fixture")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--keyword", default="")
    parser.add_argument("--since", type=date.fromisoformat)
    args = parser.parse_args()
    records = parse_announcements(args.input.read_text(encoding="utf-8"), "https://example.test/")
    print(json.dumps(filter_announcements(records, keyword=args.keyword, since=args.since), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
