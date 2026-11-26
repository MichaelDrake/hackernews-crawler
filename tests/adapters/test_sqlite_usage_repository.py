import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hn_crawler.adapters.sqlite.usage_repository import SqliteUsageRepository
from hn_crawler.domain.models import CrawlResultStatus, UsageRecord


def make_record(filter_name: str, status: CrawlResultStatus, duration_ms: float) -> UsageRecord:
    return UsageRecord(
        timestamp=datetime(2026, 11, 26, 10, 30, tzinfo=UTC),
        filter_name=filter_name,
        status=status,
        entries_returned=3,
        duration_ms=duration_ms,
    )


def test_save_writes_a_row_to_the_usage_table(tmp_path: Path) -> None:
    database = tmp_path / "usage.db"

    SqliteUsageRepository(database).save(
        make_record("long_titles", CrawlResultStatus.SUCCESS, 250.5)
    )

    rows = (
        sqlite3.connect(database)
        .execute(
            "SELECT timestamp, filter_name, status, entries_returned, duration_ms, error FROM usage"
        )
        .fetchall()
    )
    assert rows == [("2026-11-26T10:30:00+00:00", "long_titles", "success", 3, 250.5, None)]


def test_summary_of_an_empty_database(tmp_path: Path) -> None:
    summary = SqliteUsageRepository(tmp_path / "usage.db").summary()

    assert summary.total_requests == 0
    assert summary.requests_by_filter == {}
    assert summary.error_count == 0
    assert summary.average_duration_ms == 0.0


def test_summary_counts_requests_errors_and_average_duration(tmp_path: Path) -> None:
    repository = SqliteUsageRepository(tmp_path / "usage.db")
    repository.save(make_record("long_titles", CrawlResultStatus.SUCCESS, 10.0))
    repository.save(make_record("long_titles", CrawlResultStatus.ERROR, 20.0))
    repository.save(make_record("short_titles", CrawlResultStatus.SUCCESS, 30.0))

    summary = repository.summary()

    assert summary.total_requests == 3
    assert summary.requests_by_filter == {"long_titles": 2, "short_titles": 1}
    assert summary.error_count == 1
    assert summary.average_duration_ms == pytest.approx(20.0)


def test_data_is_kept_when_the_database_is_opened_again(tmp_path: Path) -> None:
    database = tmp_path / "usage.db"
    SqliteUsageRepository(database).save(
        make_record("short_titles", CrawlResultStatus.SUCCESS, 5.0)
    )

    assert SqliteUsageRepository(database).summary().total_requests == 1
