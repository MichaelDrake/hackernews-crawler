import pytest

from hn_crawler.domain.text import count_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        (None, 0),
        ("This is - a self-explained example", 5),
        ("   ", 0),
        ("Hello", 1),
        ("one two three four five", 5),
        ("one two three four five six", 6),
        ("multiple    spaces   between", 3),
        ("- – — | / :", 0),
        ("Show HN: My new project", 5),
        ("C++ vs. Rust (2026)", 4),
        ("Año nuevo, código nuevo", 4),
        ("tabs\tand\nnewlines", 3),
        ("non\u00a0breaking space", 3),
    ],
)
def test_count_words(text: str | None, expected: int) -> None:
    assert count_words(text) == expected
