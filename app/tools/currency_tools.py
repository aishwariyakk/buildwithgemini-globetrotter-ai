"""
Currency Exchange Rate tool for GlobeTrotter AI.
Fetches real live foreign exchange rates from the Frankfurter Public API.
"""

import json
import urllib.request
from typing import Any


def get_currency_exchange_rates(
    from_currency: str = "USD",
    to_currencies: str = "EUR,GBP,JPY,CAD,AUD",
) -> dict[str, Any]:
    """Fetches real-time foreign exchange conversion rates for international travel planning.

    Args:
        from_currency: Base currency code (e.g. 'USD', 'EUR', 'GBP').
        to_currencies: Comma-separated list of target currency codes (e.g. 'EUR,GBP,JPY,CAD,AUD').

    Returns:
        A dictionary containing the base currency, date, and live conversion rates.
    """
    base = from_currency.strip().upper()
    targets = to_currencies.strip().upper()

    url = f"https://api.frankfurter.dev/v1/latest?base={base}&symbols={targets}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "GlobeTrotter-AI/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "status": "success",
                "base_currency": data.get("base", base),
                "date": data.get("date"),
                "conversion_rates": data.get("rates", {}),
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch exchange rates for {base}: {str(e)}",
            "fallback_rates": {
                "EUR": 0.89,
                "GBP": 0.75,
                "JPY": 158.0,
                "CAD": 1.42,
                "AUD": 1.43,
            },
        }
