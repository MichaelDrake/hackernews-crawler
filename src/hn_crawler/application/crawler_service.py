"""Use case: apply a filter to the front-page entries and record the usage."""

import time
from datetime import UTC, datetime

from hn_crawler.application.ports import EntrySource, UsageRepository
from hn_crawler.domain.filters import FilterRegistry
from hn_crawler.domain.models import CrawlResultStatus, Entry, UsageRecord, UsageSummary


class CrawlerService:
    """Coordinates the entry source, the filters and the usage repository."""

    def __init__(
        self, source: EntrySource, repository: UsageRepository, registry: FilterRegistry
    ) -> None:
        self._source = source
        self._repository = repository
        self._registry = registry

    def run(self, filter_name: str) -> list[Entry]:
        """Return the filtered entries. Every call is recorded, failures included."""
        timestamp = datetime.now(UTC)
        started = time.perf_counter()
        try:
            entry_filter = self._registry.get(filter_name)
            entries = self._source.get_entries()
            result = entry_filter.apply(entries)
        except Exception as error:
            self._save(timestamp, filter_name, started, CrawlResultStatus.ERROR, 0, str(error))
            raise
        self._save(timestamp, filter_name, started, CrawlResultStatus.SUCCESS, len(result))
        return result

    def usage_summary(self) -> UsageSummary:
        return self._repository.summary()

    def _save(
        self,
        timestamp: datetime,
        filter_name: str,
        started: float,
        status: CrawlResultStatus,
        entries_returned: int,
        error: str | None = None,
    ) -> None:
        duration_ms = (time.perf_counter() - started) * 1000
        record = UsageRecord(timestamp, filter_name, status, entries_returned, duration_ms, error)
        self._repository.save(record)
