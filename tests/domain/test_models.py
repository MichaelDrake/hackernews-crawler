import dataclasses

import pytest

from hn_crawler.domain.models import Entry


def test_entries_cannot_be_modified() -> None:
    entry = Entry(number=1, title="Some Title", points=2, comments=50)
    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.number = 3
