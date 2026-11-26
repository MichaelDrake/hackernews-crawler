"""Registry all filters by name"""

from collections.abc import Iterable

from hn_crawler.domain.filters.base import EntryFilter
from hn_crawler.domain.filters.text_filter import LongTitleFilter, ShortTitleFilter


class UnknownFilterError(ValueError):
    """Raised when a filter name is not registered."""


class FilterRegistry:
    """Holds the available filters and finds them by name."""

    def __init__(self, filters: Iterable[EntryFilter]) -> None:
        self._filters = {entry_filter.name: entry_filter for entry_filter in filters}

    @property
    def names(self) -> list[str]:
        return sorted(self._filters)

    def get(self, name: str) -> EntryFilter:
        try:
            return self._filters[name]
        except KeyError:
            available = ", ".join(self.names)
            raise UnknownFilterError(f"Unknown filter '{name}'. Available: {available}") from None


def default_registry() -> FilterRegistry:
    return FilterRegistry([LongTitleFilter(), ShortTitleFilter()])
