"""The module responsible for testing the human_readable module."""

from typing import List

import pytest

from app.utils.human_readable import readable_memory


@pytest.mark.parametrize(
    "memory, prefix",
    [(2, "B"), (2 * 1024, "KB"), (2 * 1024**2, "MB"), (2 * 1024**3, "GB")],
)
def test_readable_memory(memory, prefix):
    """Test the func readable_memory."""
    memory_str: str = readable_memory(memory)
    words: List[str] = memory_str.split(" ")

    assert len(words) == 2
    assert words[1] == prefix
    try:
        float(words[0])
    except ValueError:
        pytest.fail(f"{words[0]} is not float!")
