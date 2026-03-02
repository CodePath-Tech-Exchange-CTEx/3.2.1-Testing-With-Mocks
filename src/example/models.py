from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExpenseRow:
    """A single expense row as stored in the database.

    This is the shape we expect from BigQuery (or any other persistence layer):
    - vendor: who the money was paid to
    - amount: how much was spent (in the given currency)
    - currency: three-letter currency code, e.g. "USD"
    """

    vendor: str
    amount: float
    currency: str

