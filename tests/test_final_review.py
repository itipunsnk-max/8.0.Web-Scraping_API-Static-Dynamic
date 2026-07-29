"""Tests for the deterministic Phase 15 release review."""

from __future__ import annotations

from pathlib import Path

from scripts.final_review import run_review


def test_repository_final_review_passes() -> None:
    root = Path(__file__).parents[1]
    result = run_review(root)
    assert result["passed"] is True
    assert result["missing_files"] == []
    assert result["broken_links"] == []
    assert result["secret_matches"] == []
