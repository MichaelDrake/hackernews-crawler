from hn_crawler.domain.filters.base import EntryFilter
from hn_crawler.domain.models import Entry
from hn_crawler.domain.text import count_words

TITLE_WORD_LIMIT = 5


class LongTitleFilter(EntryFilter):
    name = "long_title_filter"

    def matches(self, entrie: Entry) -> bool:
        return count_words(entrie.title) > TITLE_WORD_LIMIT

    def sort_key(self, entrie: Entry) -> int:
        return entrie.comments


class ShortTitleFilter(EntryFilter):
    name = "short_title_filter"

    def matches(self, entrie: Entry) -> bool:
        return count_words(entrie.title) <= TITLE_WORD_LIMIT

    def sort_key(self, entrie: Entry) -> int:
        return -entrie.points
