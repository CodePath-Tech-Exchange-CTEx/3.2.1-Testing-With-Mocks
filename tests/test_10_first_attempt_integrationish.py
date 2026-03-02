import os
from pathlib import Path

import pytest

from src.example.expense_report import write_expenses_v1


@pytest.mark.skipif(
    not os.getenv("RUN_BQ_TESTS"),
    reason="RUN_BQ_TESTS not set; skipping real BigQuery + file integration test.",
)
def test_write_expenses_v1_integrationish(tmp_path: Path) -> None:
    """"Integration-ish" test for the first attempt version.

    Slides 6–7: this version still touches real file I/O and (optionally) real
    external dependencies (BigQuery, exchange-rate service).
    """
    output_path = tmp_path / "expenses.csv"

    write_expenses_v1(str(output_path))

    # Keep assertions minimal to avoid brittleness.
    assert output_path.exists()
    contents = output_path.read_text(encoding="utf-8").splitlines()
    assert contents
    assert contents[0] == "vendor,amount (USD)"

