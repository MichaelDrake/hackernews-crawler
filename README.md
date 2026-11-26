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
<img width="783" height="310" alt="image" src="https://github.com/user-attachments/assets/087329ab-c5e8-40b9-9d36-24ed6baa88f6" />

<img width="612" height="167" alt="image" src="https://github.com/user-attachments/assets/ddc370bb-3df9-49e9-bf9d-22362f32a26a" />


<img width="550" height="102" alt="image" src="https://github.com/user-attachments/assets/d324282e-fe27-4108-b5ce-39e84db589ed" />

## Usage data

Every request is saved as a row in the `usage` table of `usage.db`: timestamp (UTC), filter name, status (`success` or `error`), entries returned, duration in ms, and error message.

```bash
sqlite3 -header -column usage.db "SELECT * FROM usage;"
```

<img width="783" height="71" alt="image" src="https://github.com/user-attachments/assets/cec28789-10ea-42a3-870e-8fc8af6bcd3c" />

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

## Future work

This first version is a **command-line tool**, but the hexagonal architecture means new ways to use and store the data are just new adapters. The core (`domain/` and `application/`) stays the same.

<img width="2044" height="868" alt="image" src="https://github.com/user-attachments/assets/ada05ec1-aa46-4db6-8f75-768d2dcc84b7" />
