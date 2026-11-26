from collections.abc import Callable

import httpx
import pytest

from hn_crawler.adapters.hacker_news.client import HackerNewsClient
from hn_crawler.application.ports import SourceError


def client_with(handler: Callable[[httpx.Request], httpx.Response]) -> HackerNewsClient:
    """A client whose requests are answered by `handler` instead of the internet."""
    return HackerNewsClient(httpx.Client(transport=httpx.MockTransport(handler)))


def test_returns_the_page_html() -> None:
    client = client_with(lambda request: httpx.Response(200, text="<html>front page</html>"))

    assert client.fetch_front_page() == "<html>front page</html>"


def test_http_error_status_raises_source_error() -> None:
    client = client_with(lambda request: httpx.Response(503))

    with pytest.raises(SourceError, match="503"):
        client.fetch_front_page()


def test_network_failure_raises_source_error() -> None:
    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    with pytest.raises(SourceError, match="connection refused"):
        client_with(fail).fetch_front_page()