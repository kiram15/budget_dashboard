from django.db import models


class Security(models.Model):
    """A tradeable thing: a stock, ETF, mutual fund, bond, or cash position."""

    TYPE_CHOICES = [
        ("equity", "Equity"),
        ("etf", "ETF"),
        ("mutual fund", "Mutual Fund"),
        ("cash", "Cash"),
        ("fixed income", "Fixed Income"),
        ("derivative", "Derivative"),
        ("other", "Other"),
    ]

    plaid_security_id = models.CharField(max_length=64, unique=True)
    ticker_symbol = models.CharField(max_length=20, blank=True)  # blank for some bonds/funds
    cusip = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=200)
    security_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    close_price = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    close_price_date = models.DateField(null=True)
    iso_currency_code = models.CharField(max_length=3, default="USD")

    def __str__(self):
        return self.ticker_symbol or self.name


class Holding(models.Model):
    """
    CURRENT position only — 'you own X shares of Y in account Z right now'.
    This table is overwritten on every sync, it is NOT historical.
    For time-series/charting, see HoldingSnapshot below.
    """

    account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="holdings"
    )
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    cost_basis = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    institution_value = models.DecimalField(max_digits=14, decimal_places=2)
    institution_price_as_of = models.DateField(null=True)

    class Meta:
        unique_together = ("account", "security")

    def __str__(self):
        return f"{self.quantity} x {self.security} in {self.account}"


class InvestmentTransaction(models.Model):
    """Buy/sell/dividend/fee events — this IS historical, one row per event."""

    TYPE_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
        ("dividend", "Dividend"),
        ("fee", "Fee"),
        ("transfer", "Transfer"),
        ("cancel", "Cancel"),
    ]

    account = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="investment_transactions"
    )
    security = models.ForeignKey(Security, null=True, blank=True, on_delete=models.SET_NULL)
    plaid_investment_transaction_id = models.CharField(max_length=64, unique=True)

    date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subtype = models.CharField(max_length=40, blank=True)
    quantity = models.DecimalField(max_digits=16, decimal_places=6, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} {self.type} {self.security}"


class HoldingSnapshot(models.Model):
    """
    Point-in-time copy of a Holding, written every sync. This is what your
    net-worth / portfolio-value-over-time charts should query — Holding
    itself only ever reflects "right now".

    NOTE: your history is only as complete as how often you click Sync.
    Going a month without syncing means a gap in these charts, not an error.
    """

    synced_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    value = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        indexes = [models.Index(fields=["synced_at"])]


class SecurityPriceHistory(models.Model):
    """
    Daily close price per security. Populated two ways:
      - "plaid_sync": one row per day, written automatically whenever you sync
      - "backfilled_yfinance": historical rows pulled once via the
        backfill_prices management command, to fill in the past before
        you started using this app (see apps/investments/management/commands)
    """

    SOURCE_CHOICES = [
        ("plaid_sync", "Plaid sync"),
        ("backfilled_yfinance", "Backfilled (yfinance)"),
    ]

    security = models.ForeignKey(
        Security, on_delete=models.CASCADE, related_name="price_history"
    )
    date = models.DateField()
    close_price = models.DecimalField(max_digits=14, decimal_places=4)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="plaid_sync")

    class Meta:
        unique_together = ("security", "date")
        ordering = ["date"]
