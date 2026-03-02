from __future__ import annotations


class ExchangeRateService:
    """Simple, deterministic currency conversion service used in the examples.

    Slide 5/6: this stands in for a "currency conversion API call".
    Slide 10: this is a dependency that would normally talk to an external API.
    """

    # In a real app this data would come from an HTTP API call.
    # Slide 10: dependency identification — this would wrap external network I/O.
    _RATES_TO_USD = {
        "USD": 1.0,
        "GBP": 1.25,
        "EUR": 1.1,
        "JPY": 0.007,  # 1 JPY -> 0.007 USD (example only)
        "MXN": 0.055,
    }

    @staticmethod
    def convertToUSD(currency: str, amount: float) -> float:
        """Convert the given amount to USD using a fixed internal rate table.

        The implementation is deterministic so that tests can run without
        making any real HTTP requests.
        """
        code = (currency or "USD").upper()
        rate = ExchangeRateService._RATES_TO_USD.get(code)
        if rate is None:
            # For unknown currencies, we could raise or fall back.
            # Keeping it simple for the lesson: treat as USD.
            rate = 1.0
        return amount * rate

