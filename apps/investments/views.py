from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils import resolve_range
from .models import Holding, HoldingSnapshot
from .serializers import HoldingSerializer


class HoldingListView(ListAPIView):
    """
    GET /api/investments/holdings/

    Current holdings across every investment account — generic on purpose
    (single-user app; Fidelity is the only investment account today, so no
    institution filter). See HoldingSerializer for how price/return are
    derived, since neither is a direct model field.
    """

    serializer_class = HoldingSerializer

    def get_queryset(self):
        return Holding.objects.filter(account__type="investment").select_related(
            "security", "account"
        )


class PortfolioHistoryView(APIView):
    """
    GET /api/investments/portfolio-history/?range=month|6m|year|all

    Returns [{date, total_value}, ...] for TrendLine on the Investments
    page. Sourced from HoldingSnapshot (point-in-time copies written every
    sync), NOT current Holding state — Holding only ever reflects "right
    now" (see models.py / ARCHITECTURE.md). Expect gaps wherever a sync
    was skipped; that's expected given the on-demand design, not a bug.
    """

    def get(self, request):
        range_str = request.query_params.get("range", "all")
        start_date = resolve_range(range_str)

        qs = (
            HoldingSnapshot.objects.filter(account__type="investment")
            .order_by("synced_at")
        )
        if start_date is not None:
            qs = qs.filter(synced_at__date__gte=start_date)

        # Deliberately aggregated in Python rather than a single grouped
        # SQL `Sum(...)` — sync_all() is safe to call more than once a
        # day (that's the whole point of on-demand syncing), which means
        # more than one HoldingSnapshot row per (account, security) can
        # land on the same calendar day. A naive "group by day, sum
        # value" would double- or triple-count anything synced more than
        # once in a day. Instead: keep only the LATEST snapshot per
        # (account, security) per day, then sum those.
        #
        # At single-user, single-machine scale this is a handful of rows
        # per day at most, so the extra pass in Python costs nothing
        # meaningful — correctness here matters more than avoiding a loop.
        latest_per_day: dict[tuple, HoldingSnapshot] = {}
        for snap in qs:
            day = snap.synced_at.date()
            key = (day, snap.account_id, snap.security_id)
            existing = latest_per_day.get(key)
            if existing is None or snap.synced_at > existing.synced_at:
                latest_per_day[key] = snap

        totals_by_day: dict = {}
        for (day, _account_id, _security_id), snap in latest_per_day.items():
            totals_by_day[day] = totals_by_day.get(day, 0) + snap.value

        data = [
            {"date": day.isoformat(), "total_value": total}
            for day, total in sorted(totals_by_day.items())
        ]
        return Response(data)
