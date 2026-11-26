from pathlib import Path

import pytest

from hn_crawler.adapters.hacker_news.parser import HackerNewsParser
from hn_crawler.application.ports import SourceError

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def parser() -> HackerNewsParser:
    return HackerNewsParser()


def test_respects_the_limit(parser: HackerNewsParser) -> None:
    html = (FIXTURES / "front_page_sample.html").read_text()

    assert [entry.number for entry in parser.parse(html, limit=2)] == [1, 2]


def test_real_front_page_snapshot_has_thirty_entries(parser: HackerNewsParser) -> None:
    html = (FIXTURES / "front_page_sample.html").read_text()

    entries = parser.parse(html)

    assert [entry.number for entry in entries] == list(range(1, 31))
    assert all(entry.title for entry in entries)


def test_row_without_title_raises_source_error(parser: HackerNewsParser) -> None:
    html = '<table><tr class="athing"><td><span class="rank">1.</span></td></tr></table>'

    with pytest.raises(SourceError, match="title"):
        parser.parse(html)
