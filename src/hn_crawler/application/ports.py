"""Storing and Entry Ports that adapters will use"""

from abc import ABC, abstractmethod

from hn_crawler.domain.models import Entry, UsageRecord, UsageSummary


class SourceError(Exception):
    """Raised by an EntrySource when entries cannot be obtained."""


class EntrySource(ABC):
    """Provides the current front-page entries, in rank order."""

    @abstractmethod
    def get_entries(self) -> list[Entry]:
        """Return the entries or raise SourceError."""


class UsageRepository(ABC):
    """Stores usage records and summarises them."""

    @abstractmethod
    def save(self, record: UsageRecord) -> None:
        """Store a record."""

    @abstractmethod
    def summary(self) -> UsageSummary:
        """Summary of every stored record."""
