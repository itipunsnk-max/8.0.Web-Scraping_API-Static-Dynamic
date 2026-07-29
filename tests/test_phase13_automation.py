"""Tests for Phase 13 lock, log and exit-code behavior."""

from __future__ import annotations

from pathlib import Path

from web_scraping_course.automation import FileLock, LockAcquisitionError, run_job


def test_file_lock_is_exclusive_and_removes_metadata(tmp_path: Path) -> None:
    lock_path = tmp_path / "job.lock"
    first = FileLock(lock_path)
    first.acquire()
    try:
        assert lock_path.exists()
        try:
            FileLock(lock_path).acquire()
        except LockAcquisitionError:
            pass
        else:
            raise AssertionError("second lock acquisition should fail")
    finally:
        first.release()
    assert not lock_path.exists()


def test_run_job_returns_success_and_writes_log(tmp_path: Path) -> None:
    output = tmp_path / "output.txt"
    code = run_job(
        "test-success",
        lambda: output.write_text("done", encoding="utf-8"),
        lock_path=tmp_path / "success.lock",
        log_path=tmp_path / "job.log",
    )
    assert code == 0
    assert output.read_text(encoding="utf-8") == "done"
    assert "job_finished" in (tmp_path / "job.log").read_text(encoding="utf-8")


def test_run_job_maps_failure_to_exit_code_one(tmp_path: Path) -> None:
    def fail() -> None:
        raise RuntimeError("fixture failure")

    code = run_job(
        "test-failure",
        fail,
        lock_path=tmp_path / "failure.lock",
        log_path=tmp_path / "job.log",
    )
    assert code == 1
    assert "job_failed" in (tmp_path / "job.log").read_text(encoding="utf-8")


def test_run_job_maps_lock_contention_to_exit_code_two(tmp_path: Path) -> None:
    lock_path = tmp_path / "busy.lock"
    held = FileLock(lock_path)
    held.acquire()
    try:
        code = run_job(
            "test-busy",
            lambda: None,
            lock_path=lock_path,
            log_path=tmp_path / "job.log",
        )
    finally:
        held.release()
    assert code == 2
