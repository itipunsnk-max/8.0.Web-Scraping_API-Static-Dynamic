"""Discover and optionally download documents from an allowed HTML page."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx"}


def safe_filename(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("document URL must be an absolute http(s) URL")
    name = Path(parsed.path).name or "downloaded-document"
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[:150]


def discover_documents(html: str, base_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    documents = []
    for link in soup.select("a[href]"):
        url = urljoin(base_url, link["href"])
        if Path(urlparse(url).path).suffix.casefold() not in ALLOWED_EXTENSIONS:
            continue
        documents.append({"name": safe_filename(url), "url": url, "label": link.get_text(" ", strip=True)})
    return documents


def download_documents(documents: list[dict[str, str]], output_dir: Path, *, timeout: float = 20) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    with requests.Session() as session:
        for document in documents:
            response = session.get(document["url"], timeout=timeout)
            response.raise_for_status()
            path = output_dir / document["name"]
            path.write_bytes(response.content)
            paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover downloadable documents")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--base-url", default="https://example.test/documents/")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    documents = discover_documents(args.input.read_text(encoding="utf-8"), args.base_url)
    rendered = json.dumps(documents, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
