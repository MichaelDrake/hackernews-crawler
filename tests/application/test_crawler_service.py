import pytest

from hn_crawler.application.crawler_service import CrawlerService
from hn_crawler.application.ports import EntrySource, SourceError, UsageRepository
from hn_crawler.domain.filters import UnknownFilterError, default_registry
from hn_crawler.domain.models import CrawlResultStatus, Entry, UsageRecord, UsageSummary

LONG_ENTRY = Entry(number=1, title="This title has six words total", points=10, comments=5)
SHORT_ENTRIES = [
    Entry(number=2, title="Short title", points=20, comments=1),
    Entry(number=3, title="Show HN: Tiny", points=5, comments=8),
]
SUMMARY = UsageSummary(
    total_requests=3,
    requests_by_filter={"long_title_filter": 3},
    error_count=0,
    average_duration_ms=1.5,
)


class FakeSource(EntrySource):
    def __init__(self, entries: list[Entry] | None = None) -> None:
        self._entries = entries
        self.calls = 0

    def get_entries(self) -> list[Entry]:
        self.calls += 1
        if self._entries is None:
            raise SourceError("unavailable")
        return self._entries


class RecordingRepository(UsageRepository):
    def __init__(self) -> None:
        self.records: list[UsageRecord] = []

    def save(self, record: UsageRecord) -> None:
        self.records.append(record)

    def summary(self) -> UsageSummary:
        return SUMMARY


def make_service(
    source: FakeSource, repository: RecordingRepository | None = None
) -> CrawlerService:
    return CrawlerService(source, repository or RecordingRepository(), default_registry())


def test_run_returns_filtered_entries_and_records_success() -> None:
    repository = RecordingRepository()
    service = make_service(FakeSource([LONG_ENTRY, *SHORT_ENTRIES]), repository)

    assert service.run("long_title_filter") == [LONG_ENTRY]

    [record] = repository.records
    assert record.filter_name == "long_title_filter"
    assert record.status is CrawlResultStatus.SUCCESS
    assert record.entries_returned == 1
    assert record.error is None
    assert record.duration_ms >= 0


def test_run_records_error_and_reraises_when_source_fails() -> None:
    repository = RecordingRepository()
    service = make_service(FakeSource(), repository)

    with pytest.raises(SourceError):
        service.run("short_title_filter")

    [record] = repository.records
    assert record.status is CrawlResultStatus.ERROR
    assert record.entries_returned == 0
    assert record.error == "unavailable"


def test_run_with_unknown_filter_records_error_without_calling_source() -> None:
    repository = RecordingRepository()
    source = FakeSource(SHORT_ENTRIES)
    service = make_service(source, repository)

    with pytest.raises(UnknownFilterError):
        service.run("missing")

    [record] = repository.records
    assert record.status is CrawlResultStatus.ERROR
    assert source.calls == 0


def test_usage_summary_comes_from_repository() -> None:
    assert make_service(FakeSource([])).usage_summary() == SUMMARY
