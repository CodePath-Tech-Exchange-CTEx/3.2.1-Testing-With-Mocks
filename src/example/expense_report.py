from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Expense:
    category: str
    amount: float


def parse_expenses(rows: Iterable[dict]) -> List[Expense]:
    """Turn raw rows (e.g. from BigQuery) into Expense objects.

    This function is intentionally simple and pure so that it is easy
    to test without any external systems.
    """
    expenses: List[Expense] = []
    for row in rows:
        expenses.append(
            Expense(
                category=str(row.get("category", "unknown")),
                amount=float(row.get("amount", 0)),
            )
        )
    return expenses


def summarize_by_category(expenses: Iterable[Expense]) -> dict[str, float]:
    """Return a simple {category: total_amount} summary."""
    totals: dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return totals

