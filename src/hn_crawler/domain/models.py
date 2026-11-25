"""Domain models"""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class Entry:
    """Represents one entry from hackernews page"""

    number: int
    title: str
    points: int
    comments: int


class CrawlResultStatus(StrEnum):
    """Possible states of a crawl attempt"""

    SUCCESS = "success"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class UsageRecord:
    """Track crawl request usage"""

    timestamp: datetime
    filter_name: str
    status: CrawlResultStatus
    entries_returned: int
    duration_ms: float
    error: str | None = None


@dataclass(frozen=True, slots=True)
class UsageSummary:
    """Aggregated view of all stored usage records."""

    total_requests: int
    requests_by_filter: Mapping[str, int]
    error_count: int
    average_duration_ms: float
