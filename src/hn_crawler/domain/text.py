"""Text Rules"""


def count_words(text: str | None) -> int:
    if text is None:
        text = ""
    return sum(1 for separated_word in text.split() if is_word(separated_word))


def is_word(word: str) -> bool:
    return any(char.isalnum() for char in word)
