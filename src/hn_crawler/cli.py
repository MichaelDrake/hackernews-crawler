"""Command-line interface: reads the arguments, builds the objects, prints the result."""

import argparse
import sys
from collections.abc import Callable, Sequence

from hn_crawler.adapters.hacker_news.client import HackerNewsClient
from hn_crawler.adapters.hacker_news.parser import HackerNewsParser
from hn_crawler.adapters.hacker_news.source import HackerNewsSource
from hn_crawler.adapters.sqlite.usage_repository import SqliteUsageRepository
from hn_crawler.application.crawler_service import CrawlerService
from hn_crawler.application.ports import SourceError
from hn_crawler.domain.filters import default_registry
from hn_crawler.domain.models import Entry, UsageSummary
from hn_crawler.domain.text import count_words

DATABASE_PATH = "usage.db"

ServiceFactory = Callable[[], CrawlerService]


def build_service() -> CrawlerService:
    """Create the real adapters and plug them into the service."""
    return CrawlerService(
        source=HackerNewsSource(HackerNewsClient(), HackerNewsParser()),
        repository=SqliteUsageRepository(DATABASE_PATH),
        registry=default_registry(),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hn-crawler", description="Filter the first 30 entries of Hacker News."
    )
    parser.add_argument("filter", nargs="?", choices=default_registry().names)
    parser.add_argument("--stats", action="store_true", help="show usage statistics")
    return parser


def main(argv: Sequence[str] | None = None, service_factory: ServiceFactory = build_service) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.filter is None and not args.stats:
        parser.error("choose a filter or use --stats")

    service = service_factory()
    if args.stats:
        print(format_summary(service.usage_summary()))
        return 0

    try:
        entries = service.run(args.filter)
    except SourceError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(format_entries(entries))
    return 0


def format_entries(entries: Sequence[Entry]) -> str:
    if not entries:
        return "No entries match this filter."
    header = f"{'#':>3}  {'Points':>6}  {'Comments':>8}  {'Words':>5}  Title"
    rows = [
        f"{e.number:>3}  {e.points:>6}  {e.comments:>8}  {count_words(e.title):>5}  {e.title}"
        for e in entries
    ]
    return "\n".join([header, *rows])


def format_summary(summary: UsageSummary) -> str:
    lines = [
        f"Total requests:   {summary.total_requests}",
        f"Errors:           {summary.error_count}",
        f"Average duration: {summary.average_duration_ms:.1f} ms",
        "Requests by filter:",
    ]
    lines += [f"  {name}: {count}" for name, count in summary.requests_by_filter.items()]
    return "\n".join(lines)
