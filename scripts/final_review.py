"""Run deterministic release-readiness checks for the learning repository."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_FILES = (
    "README.md",
    "ROADMAP.md",
    "pyproject.toml",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "RELEASE_CHECKLIST.md",
    "vercel.json",
    "site/index.html",
)
TEXT_EXTENSIONS = {".md", ".py", ".ps1", ".psm1", ".toml", ".yml", ".yaml", ".json", ".html", ".css"}
SECRET_PATTERN = re.compile(r"(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/]{12,}", re.IGNORECASE)


def iter_review_files(root: Path) -> list[Path]:
    excluded = {".git", ".venv", ".pytest_cache", ".ruff_cache", "output", "data"}
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.casefold() in TEXT_EXTENSIONS and not excluded.intersection(path.parts)
    ]


def check_required_files(root: Path) -> list[str]:
    return [relative for relative in REQUIRED_FILES if not (root / relative).is_file()]


def check_utf8(files: list[Path]) -> list[str]:
    errors = []
    for path in files:
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(str(path))
    return errors


def check_markdown_links(root: Path, files: list[Path]) -> list[str]:
    errors = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.casefold() != ".md":
            continue
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_file() or root.resolve() not in resolved.parents:
                errors.append(f"{path.relative_to(root)} -> {target}")
    return errors


def check_secrets(files: list[Path]) -> list[str]:
    return [str(path) for path in files if SECRET_PATTERN.search(path.read_text(encoding="utf-8"))]


def run_review(root: Path) -> dict[str, object]:
    files = iter_review_files(root)
    result = {
        "missing_files": check_required_files(root),
        "invalid_utf8": check_utf8(files),
        "broken_links": check_markdown_links(root, files),
        "secret_matches": check_secrets(files),
        "reviewed_files": len(files),
    }
    result["passed"] = not any(result[key] for key in ("missing_files", "invalid_utf8", "broken_links", "secret_matches"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check release readiness")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = run_review(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
