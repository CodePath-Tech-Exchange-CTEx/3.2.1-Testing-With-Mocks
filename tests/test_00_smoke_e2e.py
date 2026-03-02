from pathlib import Path

from src import cli
from src.example.expense_report import write_expenses_v3


def test_smoke_e2e_cli_with_mocked_dependencies(monkeypatch, tmp_path: Path):
    """Slides 31–33: E2E "smoke" test.

    This is a light-weight end-to-end test:
    - we run the real CLI entrypoint (cli.main)
    - but we swap in mocked dependencies under the hood so it stays fast
      and deterministic.

    It is *not* a full integration test of BigQuery or real HTTP; those are
    covered elsewhere or behind feature flags. Here we only care that the
    whole flow runs and produces a plausible output file.
    """

    # Arrange: run CLI in an isolated temp directory so it writes to a temp file.
    monkeypatch.chdir(tmp_path)

    class FakeDatabase:
        def read_rows(self):
            return [
                {"vendor": "Coffee Shop", "amount": 3.0, "currency": "USD"},
                {"vendor": "Book Store", "amount": 12.5, "currency": "USD"},
            ]

    def fake_conversion(currency: str, amount: float) -> float:
        return amount  # keep it simple and deterministic

    def fake_write_expenses_v1(output_path: str) -> None:
        """Under the hood, call the DI-friendly version with fakes.

        Slides 31–33: CLI as E2E orchestrator, but dependencies can still be
        mocked so tests stay fast and reliable.
        """
        with open(output_path, mode="w", encoding="utf-8") as outfile:
            write_expenses_v3(outfile, FakeDatabase(), currency_conversion_fn=fake_conversion)

    # Patch just the one dependency used by cli.main, without changing its
    # signature. This keeps the test focused on the E2E call path.
    monkeypatch.setattr(cli, "write_expenses_v1", fake_write_expenses_v1)

    # Act: run the real CLI main.
    cli.main()

    # Assert: "smoke" level – file created, basic structure looks right.
    output_path = tmp_path / "expenses.csv"
    assert output_path.exists()
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 1  # at least header; we don't over-specify content here
    assert lines[0] == "vendor,amount (USD)"

