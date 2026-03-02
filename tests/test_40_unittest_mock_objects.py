from unittest.mock import Mock

from src.example.expense_report import write_expenses_v3


class MockFile:
    """Minimal file-like object that captures written text."""

    def __init__(self) -> None:
        self.contents = ""

    def write(self, text: str) -> None:
        self.contents += text


def test_write_expenses_v3_with_unittest_mocks():
    """Slides 17–20: using unittest.mock objects for collaborators."""
    outfile = MockFile()

    # Mock for the database dependency.
    database = Mock()
    database.read_rows.return_value = [
        {"vendor": "Coffee Shop", "amount": 3.0, "currency": "USD"},
        {"vendor": "Book Store", "amount": 12.5, "currency": "EUR"},
    ]

    # Mock for the currency conversion function.
    currency_conversion_fn = Mock(return_value=42.0)

    write_expenses_v3(
        outfile,
        database,
        currency_conversion_fn=currency_conversion_fn,
    )

    # Slides 17–20: verify how our code interacted with its collaborators.
    # Note: we *prefer* behavior/interaction assertions over internal
    # implementation details (how the function is written).
    database.read_rows.assert_called_once()

    # Assert the conversion function was called at least once, and check
    # arguments for exactly one of the rows (to keep the test focused).
    assert currency_conversion_fn.call_count >= 1
    currency_conversion_fn.assert_any_call("USD", 3.0)

    # Behavior assertion: output text should match the number of input rows.
    lines = outfile.contents.splitlines()
    assert len(lines) == 1 + 2  # header + two data lines

