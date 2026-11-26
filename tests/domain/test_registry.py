import pytest

from hn_crawler.domain.filters import (
    FilterRegistry,
    LongTitleFilter,
    ShortTitleFilter,
    UnknownFilterError,
    default_registry,
)


def test_default_registry_contains_the_exercise_filters() -> None:
    assert default_registry().names == ["long_title_filter", "short_title_filter"]


def test_get_returns_the_filter_with_that_name() -> None:
    registry = default_registry()

    assert isinstance(registry.get("long_title_filter"), LongTitleFilter)
    assert isinstance(registry.get("short_title_filter"), ShortTitleFilter)


def test_unknown_name_raises_an_error_listing_available_filters() -> None:
    registry = FilterRegistry([LongTitleFilter(), ShortTitleFilter])

    with pytest.raises(
        UnknownFilterError, match="Available: long_title_filter, short_title_filter"
    ):
        registry.get("any")
