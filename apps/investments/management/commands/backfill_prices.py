from datetime import date, timedelta
from decimal import Decimal

import yfinance as yf
from django.core.management.base import BaseCommand

from apps.investments.models import Security, SecurityPriceHistory


class Command(BaseCommand):
    help = (
        "Backfill historical daily close prices for securities with a real "
        "ticker symbol, using yfinance (free, unofficial Yahoo Finance data — "
        "fine for personal charting, not guaranteed-accurate for anything "
        "beyond that). Mutual funds/cash positions without a clean ticker "
        "are skipped and will just start accumulating from your next sync."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days", type=int, default=365, help="How many days back to backfill (default 365)"
        )

    def handle(self, *args, **options):
        days = options["days"]
        start = date.today() - timedelta(days=days)

        securities = Security.objects.exclude(ticker_symbol="")
        for security in securities:
            self.stdout.write(f"Backfilling {security.ticker_symbol}...")
            try:
                history = yf.Ticker(security.ticker_symbol).history(start=start)
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  failed: {exc}"))
                continue

            created = 0
            for idx, row in history.iterrows():
                _, was_created = SecurityPriceHistory.objects.get_or_create(
                    security=security,
                    date=idx.date(),
                    defaults={
                        "close_price": Decimal(str(round(row["Close"], 4))),
                        "source": "backfilled_yfinance",
                    },
                )
                created += was_created

            self.stdout.write(self.style.SUCCESS(f"  added {created} days"))
