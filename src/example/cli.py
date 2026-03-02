from __future__ import annotations

import os
from typing import Iterable

from dotenv import load_dotenv

from .bigquery_client import fetch_expense_rows
from .expense_report import parse_expenses, summarize_by_category


def main() -> None:
    load_dotenv()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    dataset = os.environ.get("BIGQUERY_DATASET", "")
    table = os.environ.get("BIGQUERY_TABLE", "")

    rows: Iterable[dict] = fetch_expense_rows(
        project_id=project_id,
        dataset=dataset,
        table=table,
    )
    expenses = parse_expenses(rows)
    summary = summarize_by_category(expenses)

    print("Expense totals by category:")
    for category, total in summary.items():
        print(f"- {category}: {total:.2f}")


if __name__ == "__main__":
    main()

