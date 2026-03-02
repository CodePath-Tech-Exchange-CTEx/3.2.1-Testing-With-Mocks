from __future__ import annotations

"""
Thin wrapper CLI kept for backwards compatibility with the slides.

Instead of having its own logic, this module simply delegates to the
top-level `src.cli.main`, so there is a single end-to-end entrypoint.
"""

from ..cli import main


if __name__ == "__main__":
    main()

