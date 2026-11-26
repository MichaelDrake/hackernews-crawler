from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import ClassVar

from hn_crawler.domain.models import Entry


class EntryFilter(ABC):
    name: ClassVar[str]

    def apply(self, entries: Sequence[Entry]) -> list[Entry]:
        selected = [entry for entry in entries if self.matches(entry)]
        return sorted(selected, key=self.sort_key, reverse=True)

    @abstractmethod
    def matches(self, entrie: Entry) -> bool:
        """matches abstract method"""

    @abstractmethod
    def sort_key(self, entrie: Entry) -> int:
        """sortkey abstract method"""
