from pathlib import Path

import httpx

from hn_crawler.adapters.hacker_news.client import HackerNewsClient
from hn_crawler.adapters.hacker_news.parser import HackerNewsParser
from hn_crawler.adapters.hacker_news.source import HackerNewsSource

SAMPLE = (Path(__file__).parent.parent / "fixtures" / "front_page_sample.html").read_text()


def test_downloads_and_parses_the_front_page() -> None:
    http = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, text=SAMPLE))
    )
    source = HackerNewsSource(HackerNewsClient(http), HackerNewsParser(), limit=3)

    entries = source.get_entries()

    assert [entry.number for entry in entries] == [1, 2, 3]
