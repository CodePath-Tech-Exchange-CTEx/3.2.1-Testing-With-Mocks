from src.example.expense_report import write_expenses_v3


class MockFile:
    """Minimal file-like object that captures written text in-memory."""

    def __init__(self) -> None:
        self.contents = ""

    def write(self, text: str) -> None:
        self.contents += text


class MockDatabase:
    """Fake database that returns a fixed set of rows."""

    def read_rows(self):
        return [
            {"vendor": "Coffee Shop", "amount": 3.0, "currency": "USD"},
            {"vendor": "Book Store", "amount": 12.5, "currency": "EUR"},
        ]


def constant_conversion(currency: str, amount: float) -> float:
    """Slides 14–15: example of injecting a simple function instead of an object.

    For the purposes of the test, always return a constant value so we can make
    assertions very clear and focused.

    Note: in the real code, write_expenses_v3 has a default argument pointing
    at the real ExchangeRateService, but here we override it in the test.
    """
    return 30.0


def test_write_expenses_v3_with_injected_function():
    """Slides 14–15: inject a function + rely on default argument shape."""
    outfile = MockFile()
    database = MockDatabase()

    write_expenses_v3(outfile, database, currency_conversion_fn=constant_conversion)

    lines = outfile.contents.splitlines()

    # Expect header + one line per row from the fake database.
    assert len(lines) == 1 + 2
    assert lines[0] == "vendor,amount (USD)"
    assert lines[1] == "Coffee Shop,30.00"
    assert lines[2] == "Book Store,30.00"

