from __future__ import annotations

import os
from typing import Iterable, Mapping, Protocol, TextIO, Callable

from dotenv import load_dotenv

from .database_bq import DatabaseBQ
from .exchange_rate_service import ExchangeRateService


class SupportsReadRows(Protocol):
    def read_rows(self) -> Iterable[Mapping[str, object]]:
        ...


class SupportsConvertToUSD(Protocol):
    def convertToUSD(self, currency: str, amount: float) -> float:
        ...


def _format_header() -> str:
    """Pure formatting helper for the CSV header."""
    return "vendor,amount (USD)\n"


def _format_line(vendor: str, amount_usd: float) -> str:
    """Pure formatting helper for a single CSV line."""
    return f"{vendor},{amount_usd:.2f}\n"


def write_expenses_v1(output_path: str) -> None:
    """First attempt: tightly coupled version that is hard to test.

    Slides 3–7: complex method + first attempt.
    - Reaches out to the real database
    - Calls the real exchange-rate service
    - Opens a real file on disk
    """
    load_dotenv()

    # Build config inline; in the slides this might come from a config object.
    config = {
        "expenses": {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
            "dataset": os.environ.get("BIGQUERY_DATASET", ""),
            "table": os.environ.get("BIGQUERY_TABLE", ""),
        }
    }

    database = DatabaseBQ.connect("expenses", config)
    rows = database.read_rows()

    with open(output_path, mode="w", encoding="utf-8") as outfile:
        outfile.write(_format_header())
        for row in rows:
            vendor = str(row.get("vendor", "unknown"))
            amount = float(row.get("amount", 0.0))
            currency = str(row.get("currency", "USD"))

            amount_usd = ExchangeRateService.convertToUSD(currency, amount)
            outfile.write(_format_line(vendor, amount_usd))


def write_expenses_v2(
    outfile: TextIO,
    exchange_rate_service: SupportsConvertToUSD,
    database: SupportsReadRows,
) -> None:
    """Dependency-injected version.

    Slide 11: we inject dependencies (database, exchange-rate service, file).
    Slide 12: this makes using mocks/fakes/doubles straightforward in tests.
    """
    outfile.write(_format_header())

    for row in database.read_rows():
        vendor = str(row.get("vendor", "unknown"))
        amount = float(row.get("amount", 0.0))
        currency = str(row.get("currency", "USD"))

        amount_usd = exchange_rate_service.convertToUSD(currency, amount)
        outfile.write(_format_line(vendor, amount_usd))


def write_expenses_v3(
    outfile: TextIO,
    database: SupportsReadRows,
    currency_conversion_fn: Callable[[str, float], float] = ExchangeRateService.convertToUSD,
) -> None:
    """Function-injection version with a default argument.

    Slides 14–15: inject behavior via a function instead of a full object.
    Slide 16: uses a default argument to keep compatibility with existing calls.

    For simplicity we let any exceptions from currency_conversion_fn propagate
    to the caller; tests can then use side_effect to simulate API failures.
    """
    outfile.write(_format_header())

    for row in database.read_rows():
        vendor = str(row.get("vendor", "unknown"))
        amount = float(row.get("amount", 0.0))
        currency = str(row.get("currency", "USD"))

        amount_usd = currency_conversion_fn(currency, amount)
        outfile.write(_format_line(vendor, amount_usd))

