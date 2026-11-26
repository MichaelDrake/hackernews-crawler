import pytest

from hn_crawler.domain.filters import EntryFilter
from hn_crawler.domain.models import Entry


class EvenPointsFilter(EntryFilter):
    name = "even-points"

    def matches(self, entrie: Entry) -> bool:
        return entrie.points % 2 == 0

    def sort_key(self, entrie: Entry) -> int:
        return entrie.points


def test_entry_filter_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        EntryFilter()  # type: ignore[abstract]


def test_apply_keeps_matching_entries_sorted_descending() -> None:
    entries = [
        Entry(number=1, title="A", points=2, comments=0),
        Entry(number=2, title="B", points=3, comments=0),
        Entry(number=3, title="C", points=10, comments=0),
    ]
    result = EvenPointsFilter().apply(entries)
    assert [entry.number for entry in result] == [3, 1]
