from __future__ import annotations

from typing import TextIO


def open_outfile(path: str) -> TextIO:
    """Open a file for writing output.

    This is intentionally a very thin wrapper around Python's built-in
    file I/O so we can patch or mock it in tests.

    Slide 10: the "file" dependency here is local disk I/O.
    """
    return open(path, mode="w", encoding="utf-8")

