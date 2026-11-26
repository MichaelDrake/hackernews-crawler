"""HTTP client that downloads the Hacker News front page."""

import httpx

from hn_crawler.application.ports import SourceError

FRONT_PAGE_URL = "https://news.ycombinator.com/"


class HackerNewsClient:
    """Downloads the front page HTML with a single GET request."""

    def __init__(self, http: httpx.Client | None = None, timeout_seconds: float = 10.0) -> None:
        self._http = http or httpx.Client(timeout=timeout_seconds)

    def fetch_front_page(self) -> str:
        try:
            response = self._http.get(FRONT_PAGE_URL)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise SourceError(f"Could not download the front page: {error}") from error
        return response.text