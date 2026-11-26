from datetime import datetime

import pytest

from hn_crawler.application.ports import EntrySource, SourceError, UsageRepository
from hn_crawler.domain.models import CrawlResultStatus, Entry, UsageRecord, UsageSummary


class FakeSource(EntrySource):
    def __init__(self, entries: list[Entry] | None = None) -> None:
        self._entries = entries

    def get_entries(self) -> list[Entry]:
        if self._entries is None:
            raise SourceError("unavailable")
        return self._entries


class InMemoryRepository(UsageRepository):
    def __init__(self) -> None:
        self.records: list[UsageRecord] = []

    def save(self, record: UsageRecord) -> None:
        self.records.append(record)

    def summary(self) -> UsageSummary:
        return UsageSummary(
            total_requests=len(self.records),
            requests_by_filter={},
            error_count=0,
            average_duration_ms=0.0,
        )


@pytest.mark.parametrize("port", [EntrySource, UsageRepository])
def test_ports_cannot_be_instantiated(port: type) -> None:
    with pytest.raises(TypeError):
        port()


def test_entry_source_returns_entries() -> None:
    entries = [Entry(number=1, title="A", points=1, comments=0)]
    assert FakeSource(entries).get_entries() == entries


def test_entry_source_can_raise_source_error() -> None:
    with pytest.raises(SourceError):
        FakeSource().get_entries()


def test_usage_repository_saves_records() -> None:
    repo = InMemoryRepository()
    repo.save(UsageRecord(datetime(2026, 1, 1), "all", CrawlResultStatus.SUCCESS, 30, 12.5))
    assert repo.summary().total_requests == 1
