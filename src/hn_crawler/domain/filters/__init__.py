"""Base class, concrete filters and their registry."""

from hn_crawler.domain.filters.base import EntryFilter
from hn_crawler.domain.filters.registry import FilterRegistry, UnknownFilterError, default_registry
from hn_crawler.domain.filters.text_filter import LongTitleFilter, ShortTitleFilter

__all__ = [
    "EntryFilter",
    "FilterRegistry",
    "LongTitleFilter",
    "ShortTitleFilter",
    "UnknownFilterError",
    "default_registry",
]
