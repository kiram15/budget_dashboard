"""
Two independent pieces, deliberately kept separate:

1. trailing_return() — pure local math against your own price history.
   Never leaves your machine, no external calls.
2. generic_market_summary() — calls an LLM, but ONLY with public index
   numbers (S&P 500 / Nasdaq performance). Your specific holdings, tickers,
   balances, and account info are never included in this call. See the
   docstring on the function itself for exactly what's sent.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings

from .models import SecurityPriceHistory


def trailing_return(security, days: int = 30) -> Decimal | None:
    """
    % change in close price over the trailing `days`. Returns None if
    there isn't enough price history yet to compute it (e.g. you just
    linked this account and haven't backfilled).
    """
    prices = list(
        SecurityPriceHistory.objects.filter(
            security=security, date__gte=date.today() - timedelta(days=days)
        ).order_by("date")
    )
    if len(prices) < 2:
        return None
    start, end = prices[0].close_price, prices[-1].close_price
    if start == 0:
        return None
    return (end - start) / start


def flag_losing_holdings(holdings, threshold: Decimal = Decimal("-0.08"), days: int = 30):
    """Returns holdings whose trailing return is below `threshold` (default -8%)."""
    flagged = []
    for holding in holdings:
        ret = trailing_return(holding.security, days=days)
        if ret is not None and ret <= threshold:
            flagged.append((holding, ret))
    return flagged


def generic_market_summary(index_performance: dict) -> str:
    """
    Calls Anthropic's API directly from your backend with ONLY public,
    generic index numbers — e.g.:

        {"S&P 500": {"6mo": 0.04, "1yr": 0.11}, "Nasdaq": {"6mo": 0.02, "1yr": 0.09}}

    No account data, ticker holdings, dollar amounts, or anything specific
    to you is included in this request. This is a plain API call, entirely
    separate from and unrelated to this chat conversation.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    prompt = (
        "Summarize general stock market conditions over the past 6-12 months "
        "in 5 sentences or fewer, in plain language, based on this public "
        f"index performance data: {index_performance}. "
        "Do not speculate about any individual's portfolio."
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
