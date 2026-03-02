from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .example.expense_report import write_expenses_v1


def main() -> None:
    """Entry point for the end-to-end CLI.

    Slides 31–33: this represents the full E2E execution path:
    - load config
    - call into application code
    - write a file as the final side-effect
    """
    load_dotenv()

    # Default output file in the repo root.
    output_path = Path(os.getcwd()) / "expenses.csv"

    write_expenses_v1(str(output_path))

    print(f"Expense report written to: {output_path}")


if __name__ == "__main__":
    main()

