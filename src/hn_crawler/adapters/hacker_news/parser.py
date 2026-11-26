"""Turns the Hacker News front-page HTML into Entry objects.

Every detail of Hacker News' markup lives in this file, so a change in their
HTML only requires changes here.
"""

import re

from bs4 import BeautifulSoup, Tag

from hn_crawler.application.ports import SourceError
from hn_crawler.domain.models import Entry

_NUMBER = re.compile(r"\d+")
_COMMENTS = re.compile(r"(\d+)\s*comments?")


class HackerNewsParser:
    """Parses the story rows of the front page.

    Each story is a `tr.athing` row (number and title) followed by a row whose
    `td.subtext` holds the points and the comments link. Job posts have no
    points or comments, and "discuss" means zero comments.
    """

    def parse(self, html: str, limit: int = 30) -> list[Entry]:
        soup = BeautifulSoup(html, "html.parser")
        return [self._parse_story(row) for row in soup.select("tr.athing")[:limit]]

    def _parse_story(self, row: Tag) -> Entry:
        subtext = self._subtext_of(row)
        return Entry(
            number=self._number(row),
            title=self._title(row),
            points=self._points(subtext),
            comments=self._comments(subtext),
        )

    @staticmethod
    def _number(row: Tag) -> int:
        rank = row.select_one("span.rank")  # Hacker News calls the number "rank" in its HTML
        match = _NUMBER.search(rank.get_text()) if rank else None
        if match is None:
            raise SourceError("Story row without a number")
        return int(match.group())

    @staticmethod
    def _title(row: Tag) -> str:
        link = row.select_one("span.titleline > a")
        if link is None:
            raise SourceError("Story row without a title")
        return link.get_text(strip=True)

    @staticmethod
    def _subtext_of(row: Tag) -> Tag | None:
        details = row.find_next_sibling("tr")
        if not isinstance(details, Tag):
            return None
        return details.select_one("td.subtext")

    @staticmethod
    def _points(subtext: Tag | None) -> int:
        score = subtext.select_one("span.score") if subtext else None
        match = _NUMBER.search(score.get_text()) if score else None
        return int(match.group()) if match else 0

    @staticmethod
    def _comments(subtext: Tag | None) -> int:
        if subtext is None:
            return 0
        for link in subtext.find_all("a"):
            match = _COMMENTS.search(link.get_text())
            if match:
                return int(match.group(1))
        return 0
