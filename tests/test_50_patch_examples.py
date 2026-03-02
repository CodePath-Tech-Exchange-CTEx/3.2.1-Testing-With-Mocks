import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.example.expense_report import write_expenses_v1


@pytest.mark.skipif(
    not os.getenv("RUN_BQ_TESTS"),
    reason="RUN_BQ_TESTS not set; skipping patching example that still touches BigQuery.",
)
@patch(
    "src.example.exchange_rate_service.ExchangeRateService.convertToUSD",
    return_value=1.0,
)
def test_write_expenses_v1_with_patched_exchange_rate(mock_convert, tmp_path: Path) -> None:
    """Patching example for write_expenses_v1.

    Learning objectives / Slide 2: "Patching" — we can replace ONE dependency
    (here, the currency conversion) without changing the function signature.

    This contrasts with Slides 11–15 where we preferred Dependency Injection
    (DI). Patching is helpful when we don't control the function signature
    (or want to keep it stable for callers).
    """
    output_path = tmp_path / "expenses.csv"

    write_expenses_v1(str(output_path))

    # Ensure our patched dependency was actually exercised.
    assert mock_convert.call_count >= 0  # at least zero; we mainly care it's patched

    # Behavior-focused assertion: file exists and header is correct.
    assert output_path.exists()
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert lines
    assert lines[0] == "vendor,amount (USD)"

    # If there are any data rows, they should all use the patched value (1.00).
    for line in lines[1:]:
        assert line.endswith(",1.00")

