"""EntrySource backed by the live Hacker News website."""

from hn_crawler.adapters.hacker_news.client import HackerNewsClient
from hn_crawler.adapters.hacker_news.parser import HackerNewsParser
from hn_crawler.application.ports import EntrySource
from hn_crawler.domain.models import Entry


class HackerNewsSource(EntrySource):
    """Downloads the front page and parses its first `limit` stories."""

    def __init__(self, client: HackerNewsClient, parser: HackerNewsParser, limit: int = 30) -> None:
        self._client = client
        self._parser = parser
        self._limit = limit

    def get_entries(self) -> list[Entry]:
        return self._parser.parse(self._client.fetch_front_page(), self._limit)
