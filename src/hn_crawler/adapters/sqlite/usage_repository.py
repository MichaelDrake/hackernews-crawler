"""Adapter that stores usage records in a SQLite database."""

import sqlite3
from pathlib import Path

from hn_crawler.application.ports import UsageRepository
from hn_crawler.domain.models import UsageRecord, UsageSummary


class SqliteUsageRepository(UsageRepository):
    """Saves one row per crawler request in the `usage` table."""

    def __init__(self, database: Path | str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usage (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp        TEXT    NOT NULL,
                filter_name      TEXT    NOT NULL,
                status           TEXT    NOT NULL,
                entries_returned INTEGER NOT NULL,
                duration_ms      REAL    NOT NULL,
                error            TEXT
            )
            """
        )
        self._connection.commit()

    def save(self, record: UsageRecord) -> None:
        self._connection.execute(
            """
            INSERT INTO usage (timestamp, filter_name, status, entries_returned, duration_ms, error)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                record.timestamp.isoformat(),
                record.filter_name,
                record.status.value,
                record.entries_returned,
                record.duration_ms,
                record.error,
            ),
        )
        self._connection.commit()

    def summary(self) -> UsageSummary:
        total, errors, average = self._connection.execute(
            "SELECT COUNT(*), SUM(status = 'error'), AVG(duration_ms) FROM usage"
        ).fetchone()
        by_filter = self._connection.execute(
            "SELECT filter_name, COUNT(*) FROM usage GROUP BY filter_name ORDER BY filter_name"
        ).fetchall()
        return UsageSummary(
            total_requests=total,
            requests_by_filter=dict(by_filter),
            error_count=errors or 0,
            average_duration_ms=average or 0.0,
        )
