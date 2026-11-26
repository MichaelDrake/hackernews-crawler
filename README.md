# hackernews-crawler

Command-line crawler that scrapes the first 30 entries of [Hacker News](https://news.ycombinator.com/) (number, title, points, comments), filters them, and stores usage data in SQLite.

| Filter | Keeps | Ordered by |
|---|---|---|
| `long_title_filter` | titles with more than 5 words | comments, highest first |
| `short_title_filter` | titles with 5 words or fewer | points, smallest first |

Only space-separated words count, and symbols are ignored: `This is - a self-explained example` has 5 words.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

Dependencies: `httpx` (HTTP) and `beautifulsoup4` (HTML parsing). Dev tools: `pytest`, `ruff`, `mypy`. SQLite comes with Python.

## Install and run

```bash
git clone https://github.com/MichaelDrake/hackernews-crawler.git
cd hackernews-crawler
uv sync

uv run hn-crawler long_title_filter
uv run hn-crawler short_title_filter
uv run hn-crawler --stats
```

## Usage data

Every request is saved as a row in the `usage` table of `usage.db`: timestamp (UTC), filter name, status (`success` or `error`), entries returned, duration in ms, and error message.

```bash
sqlite3 -header -column usage.db "SELECT * FROM usage;"
```

## Architecture

The project uses a **hexagonal architecture** (ports and adapters). The business rules don't know about HTTP, HTML or SQLite. They talk to the outside world through two ports, which adapters implement.

<img width="2250" height="1458" alt="image" src="https://github.com/user-attachments/assets/791a0e57-d107-4cd2-908a-ffbb393b4385" />


| Folder | Contains |
|---|---|
| `domain/` | `Entry`, word counting, filters |
| `application/` | Ports and `CrawlerService` |
| `adapters/` | Hacker News scraper and SQLite repository |
| `cli.py` | Command line; |

**Patterns:** Template Method (`EntryFilter.apply`), Strategy (each filter), Registry (`FilterRegistry`), Repository (SQLite), dependency injection (`CrawlerService`).

## Tests

```bash
uv run pytest            # all tests (no internet needed)
```

Tests cover the word count, both filters, the service (with in-memory fakes), the parser (saved HTML), SQLite.

Code quality checks:

```bash
uv run ruff format . && uv run ruff check . && uv run mypy
```
