from rest_framework import serializers

from .analysis import trailing_return
from .models import Holding


class HoldingSerializer(serializers.ModelSerializer):
    """
    Shape matches frontend/src/api/mockData.js `holdings`:
    { id, security, name, quantity, price, value, trailing_30d_return }

    Two fields need deriving rather than a direct model mapping:

    - `price`: Holding has no per-share price field. Deriving it as
      institution_value / quantity (Plaid's own reported value divided by
      quantity) rather than reading Security.close_price, since
      institution_value is the number Plaid/Fidelity actually reported for
      this specific holding — it's the source of truth per sync.py, and
      should already agree with close_price in the normal case anyway.

    - `trailing_30d_return`: not stored anywhere. Computed at request time
      via analysis.trailing_return(), which is pure local math over
      SecurityPriceHistory — no external calls, consistent with the
      project's "your specific holdings never touch an LLM" design.
      NOTE: this means one extra query per holding (N+1). Left as-is for
      now per project discussion — fine at single-user, single-account
      scale. Revisit with a prefetch (e.g. bulk-loading price history
      keyed by security_id and passing it through serializer context) if
      this ever needs to serve many holdings at once.
    """

    security = serializers.CharField(source="security.ticker_symbol", read_only=True)
    name = serializers.CharField(source="security.name", read_only=True)
    price = serializers.SerializerMethodField()
    value = serializers.DecimalField(
        source="institution_value", max_digits=14, decimal_places=2, read_only=True
    )
    trailing_30d_return = serializers.SerializerMethodField()

    class Meta:
        model = Holding
        fields = [
            "id",
            "security",
            "name",
            "quantity",
            "price",
            "value",
            "trailing_30d_return",
        ]

    def get_price(self, holding):
        if not holding.quantity:
            # Guard against a zero-quantity holding (e.g. a fully sold
            # position that hasn't dropped off yet) — avoid a 500 on a
            # perfectly valid API response.
            return None
        return holding.institution_value / holding.quantity

    def get_trailing_30d_return(self, holding):
        # Matches the -8%/30-day threshold used by flag_losing_holdings()
        # in analysis.py, so this number and the FLAGGED badge logic on
        # the frontend stay consistent with the backend's own flagging.
        return trailing_return(holding.security, days=30)
