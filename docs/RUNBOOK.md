# Runbook

Task-oriented reference. If you're asking "how do I...", it's here.
For "why did I build it this way", see ARCHITECTURE.md instead.

## Adding a new institution
See `adding-an-institution.md`. Short version:
`check_institution` → visit `/plaid/link/` in browser → sync.

## Syncing manually
```
python manage.py sync_accounts              # all institutions
python manage.py sync_accounts --item <id>  # just one
```

## Backfilling historical prices for a new holding
```
python manage.py backfill_prices --days 365
```
Only works for securities with a real ticker symbol. Mutual funds/cash
positions will just start accumulating price history from your next sync
onward — there's no free historical source for those.

## An institution's sync started failing (status = needs_reauth)
The institution likely wants you to re-confirm login — this happens after
password changes, MFA policy changes, or Plaid periodically re-verifying
long-lived connections. Re-run the Link flow in "update mode":
```python
# in a Django shell (python manage.py shell)
from apps.accounts.models import PlaidItem
from apps.plaid_integration.link import create_update_link_token

item = PlaidItem.objects.get(item_id="...")
token = create_update_link_token(item)
# then load link.html with this token instead of a fresh one —
# same widget, but it reuses the existing Item so history isn't lost
```

## Removing an institution entirely
```python
from apps.accounts.models import PlaidItem
from apps.plaid_integration.token_store import delete_access_token

item = PlaidItem.objects.get(item_id="...")
delete_access_token(item.keychain_ref)   # remove from OS keychain first
item.delete()                             # cascades to accounts/transactions
```

## Categorization
`Transaction.category_primary` is Plaid's auto-guess. `Transaction.user_category`
is yours — set it via the Django admin or a view once you build the dashboard.
`display_category` on the model prefers your override, falls back to Plaid's.

## Checking Plaid's current pricing/limits
Don't trust a number you remember from a year ago — check
https://plaid.com/pricing directly, it changes.
