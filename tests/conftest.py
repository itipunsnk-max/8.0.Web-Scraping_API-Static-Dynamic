"""Shared test import paths for example modules."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_EXAMPLE = PROJECT_ROOT / "examples" / "04_static_page"
if str(STATIC_EXAMPLE) not in sys.path:
    sys.path.insert(0, str(STATIC_EXAMPLE))
