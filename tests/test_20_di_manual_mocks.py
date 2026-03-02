from src.example.expense_report import write_expenses_v2


class MockFile:
    """Captures written text in-memory instead of touching disk."""

    def __init__(self) -> None:
        self.contents = ""

    def write(self, text: str) -> None:
        self.contents += text


class MockDatabase:
    """Manual fake/stub for the database.

    Slides 12–13: this stands in for the real DatabaseBQ dependency.
    """

    def read_rows(self):
        # Three example rows, shaped like the slide example.
        return [
            {"vendor": "Coffee Shop", "amount": 3.0, "currency": "USD"},
            {"vendor": "Book Store", "amount": 12.5, "currency": "USD"},
            {"vendor": "Taxi", "amount": 20.0, "currency": "USD"},
        ]


class MockExchangeRateService:
    """Manual fake for the exchange-rate service.

    Slides 12–13: in the slide, convertToUSD just "adds 1" so it is very easy
    to reason about in tests.

    Note: you can think of this as both a *stub* (returns canned values) and a
    *mock* (a stand-in collaborator you can control in tests).
    """

    def convertToUSD(self, currency: str, amount: float) -> float:
        return amount + 1


def test_write_expenses_v2_with_manual_mocks():
    """Slides 12–13: Dependency Injection with manual mocks/fakes."""
    outfile = MockFile()
    database = MockDatabase()
    exchange_rate_service = MockExchangeRateService()

    write_expenses_v2(outfile, exchange_rate_service, database)

    expected = (
        "vendor,amount (USD)\n"
        "Coffee Shop,4.00\n"
        "Book Store,13.50\n"
        "Taxi,21.00\n"
    )

    assert outfile.contents == expected

