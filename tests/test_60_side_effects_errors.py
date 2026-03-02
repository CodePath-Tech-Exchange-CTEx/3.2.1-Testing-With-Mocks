import pytest

from src.example.expense_report import write_expenses_v3


class MockFile:
    """Simple file-like object capturing text."""

    def __init__(self) -> None:
        self.contents = ""

    def write(self, text: str) -> None:
        self.contents += text


class MockDatabase:
    """Fake database that returns a single row."""

    def read_rows(self):
        return [
            {"vendor": "Coffee Shop", "amount": 3.0, "currency": "USD"},
        ]


def erroring_conversion(currency: str, amount: float) -> float:
    """Slides 21: side_effect example — simulate API error via exception."""
    raise Exception("API Error")


def test_write_expenses_v3_propagates_conversion_error():
    """Slide 21: exception via side_effect.

    We choose to *propagate* exceptions from the currency_conversion_fn rather
    than swallow them. Tests can then verify behavior by using a function with
    a side_effect (or a mock configured with side_effect).
    """
    outfile = MockFile()
    database = MockDatabase()

    with pytest.raises(Exception, match="API Error"):
        write_expenses_v3(
            outfile,
            database,
            currency_conversion_fn=erroring_conversion,
        )

