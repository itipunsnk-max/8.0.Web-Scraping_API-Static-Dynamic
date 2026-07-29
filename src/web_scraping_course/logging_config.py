"""Consistent logging setup that avoids exposing request secrets."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(
    *,
    level: int = logging.INFO,
    log_file: Path | None = None,
    logger_name: str = "web_scraping_course",
) -> logging.Logger:
    """Configure console logging and optionally a UTF-8 file handler."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        if log_file is not None:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    return logger
