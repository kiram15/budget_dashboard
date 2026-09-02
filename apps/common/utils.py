"""
Small shared helpers used by more than one app's views. Not a Django app
itself (no models/admin) — just a plain importable package, so it does NOT
need to be added to INSTALLED_APPS.
"""
from __future__ import annotations
from datetime import date, timedelta

from django.utils import timezone

# Keep in sync with frontend/src/components/RangeSelector.jsx RANGE_OPTIONS.
# If you add a range there, add it here too — the frontend passes the raw
# string straight through as a query param.
VALID_RANGES = {"month", "6m", "year", "all"}


def resolve_range(range_str: str) -> date | None:
    """
    Turn a `?range=` query param into a start date, computed against the
    SERVER's "today" — not the browser's clock. This matters because this
    is financial data: if the client's clock is wrong (travel, a stale
    laptop clock, whatever), you don't want that to silently shift which
    transactions/snapshots show up. See the note left in
    frontend/src/api/client.js for the original intent here.

    Returns None for "all" (and for anything unrecognized, to fail open
    rather than accidentally hiding all a user's data behind a typo'd
    range value) — callers should treat None as "don't filter by date".
    """
    today = timezone.localdate()

    if range_str == "month":
        return today - timedelta(days=30)
    if range_str == "6m":
        return today - timedelta(days=182)
    if range_str == "year":
        return today - timedelta(days=365)
    # "all" or anything unrecognized -> no lower bound
    return None
