from hn_crawler.domain.filters.text_filter import LongTitleFilter, ShortTitleFilter
from hn_crawler.domain.models import Entry


def test_long_text_case_filter() -> None:
    entries = [
        Entry(number=10, title="THIS IS A LONG TEXT TEST", points=20, comments=4),
        Entry(number=20, title="THI IS NOT", points=3, comments=50),
        Entry(number=30, title="THIS IS EITHER A LONG TEXT TEST", points=10, comments=5),
    ]
    result = LongTitleFilter().apply(entries)
    assert [entry.number for entry in result] == [30, 10]


def test_short_text_case_filter() -> None:
    entries = [
        Entry(number=10, title="THIS IS A LONG TEXT TEST", points=20, comments=4),
        Entry(number=20, title="THI IS NOT", points=3, comments=50),
        Entry(number=21, title="THI IS NOT EITHER-EITHER TEST", points=32, comments=5),
        Entry(number=30, title="THIS IS EITHER A LONG TEXT TEST", points=10, comments=5),
    ]
    result = ShortTitleFilter().apply(entries)
    assert [entry.number for entry in result] == [20, 21]
