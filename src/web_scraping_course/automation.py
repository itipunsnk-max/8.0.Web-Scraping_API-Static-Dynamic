"""Small, dependency-free helpers for scheduled scraping jobs."""

from __future__ import annotations

import json
import os
import socket
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Self

from .logging_config import configure_logging


class LockAcquisitionError(RuntimeError):
    """Raised when another scheduled job already owns the lock file."""


class FileLock:
    """Create an exclusive, inspectable lock file for one scheduled run."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._handle = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._handle = self.path.open("x", encoding="utf-8")
        except FileExistsError as error:
            raise LockAcquisitionError(f"lock already exists: {self.path}") from error
        metadata = {
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "started_at": datetime.now(UTC).isoformat(),
        }
        self._handle.write(json.dumps(metadata, ensure_ascii=False) + "\n")
        self._handle.flush()

    def release(self) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None
        self.path.unlink(missing_ok=True)

    def __enter__(self) -> Self:
        self.acquire()
        return self

    def __exit__(self, *_: object) -> None:
        self.release()


def run_job(
    job_name: str,
    job: Callable[[], None],
    *,
    lock_path: Path,
    log_path: Path,
) -> int:
    """Run a job with stable exit codes, logging and single-run protection.

    Exit codes: 0 success, 1 unexpected job failure, 2 lock contention.
    """
    logger = configure_logging(log_file=log_path, logger_name=f"web_scraping_course.{job_name}")
    try:
        with FileLock(lock_path):
            logger.info("job_started name=%s", job_name)
            job()
            logger.info("job_finished name=%s", job_name)
    except LockAcquisitionError:
        logger.warning("job_skipped reason=lock_exists path=%s", lock_path)
        return 2
    except Exception:
        logger.exception("job_failed name=%s", job_name)
        return 1
    return 0
