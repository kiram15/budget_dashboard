# Wire Investments (Fidelity) + Home balance card to real Django data

## Summary

First slice of "stop using mockData.js" work. Adds real DRF endpoints for
accounts and investment holdings, and points `frontend/src/api/client.js`
at them for the three functions that back the Investments page and the
Home dashboard's balance card. Transactions/spending endpoints are
intentionally **not** part of this PR — `apps/transactions/models.py`
wasn't available to review against, so that's a separate follow-up.

## 1. Fixed the duplicate `plaid_integration` package

`apps/plaid_integration/` had two copies of everything: real logic nested
one level down at `apps/plaid_integration/plaid_integration/{views,urls,
sync,link,client,token_store}.py` and management commands, plus stub
files (`from django.shortcuts import render` and nothing else) at the
outer `apps/plaid_integration/{views,models}.py`.

`config/urls.py` already pointed at `apps.plaid_integration.urls` — the
**outer**, non-nested path — so the nested copy was dead code that Django
never actually executed; `check_institution`, `sync_accounts`, and the
Link flow were only ever running because someone had presumably tested
against the nested copy directly, or this hadn't been run end-to-end yet.

Fix: moved the real content up to `apps/plaid_integration/*.py` (client,
token_store, link, sync, views, urls, management commands), replacing the
stubs. **You'll need to manually delete
`apps/plaid_integration/plaid_integration/` after applying this patch** —
see APPLY_INSTRUCTIONS.md, I didn't want to silently delete files you
might have uncommitted changes in.

No logic changed in any moved file — every moved file's docstring says so
and points back to where it came from, in case you want to diff them.

## 2. New: `apps/common/utils.py` — `resolve_range()`

Not a Django app (no models), just a shared helper so accounts and
investments views resolve `?range=month|6m|year|all` the same way, against
the server's date rather than the browser's clock — this was already
flagged as a requirement in `client.js`'s own comments, just not
implemented yet.

## 3. New: `apps/accounts/serializers.py` + filled-in `views.py`

`GET /api/accounts/` → shape matches `mockData.accounts`. `institution`
and `balance` are renamed/traversed in the serializer (`item.institution.
name`, `current_balance`) so the frontend doesn't need to know Django's
field names.

**Flagged, not fixed:** `Account.type` uses Plaid's vocabulary
(`depository`/`credit`/`investment`/`loan`); mockData used `checking`/
`savings`/`investment`. Left alone since translating it is a product
decision, not a serializer's job — see the comment in the file.

## 4. New: `apps/investments/serializers.py` + filled-in `views.py`

`GET /api/investments/holdings/` → shape matches `mockData.holdings`.

- **Price** = `institution_value / quantity` (per your call — Plaid's own
  reported value for that specific holding, not `Security.close_price`).
- **`trailing_30d_return`** calls the existing `analysis.trailing_return()`
  per holding at request time. This is an N+1 query pattern (one
  `SecurityPriceHistory` query per holding) — left as-is per your call,
  since it's a single-user account with a handful of holdings. Commented
  in the serializer with a pointer to how you'd prefetch later if this
  ever needs to scale.

`GET /api/investments/portfolio-history/?range=...` → shape matches
`mockData.portfolioSnapshots`.

**Correctness note worth reading closely:** `HoldingSnapshot` gets a new
row every time `sync_all()` runs, and syncing twice in one day is
explicitly supported/expected by the on-demand design. A naive "group by
day, `Sum(value)`" would double-count anything synced more than once in a
day. This view instead keeps only the latest snapshot per
`(account, security)` per day before summing — done in Python rather than
a SQL window function, since at single-user scale it's a handful of rows
and the extra clarity seemed worth more than the extra few lines of SQL.

## 5. Django/DRF plumbing

- `requirements.txt`: added `djangorestframework`
- `config/settings.py`: registered `rest_framework`; added an **explicit**
  `AllowAny` permission default with a comment explaining why (no auth
  system exists yet, localhost-only) — flagged as something to revisit
  the moment this app is ever exposed beyond 127.0.0.1
- `config/urls.py`: added `api/accounts/` and `api/investments/`,
  namespaced per-app rather than one flat `api/urls.py`

## 6. Frontend

- `frontend/vite.config.js`: uncommented the `/api` dev proxy so the
  frontend can keep calling relative paths without CORS config
- `frontend/src/api/client.js`: `getAccounts()`, `getHoldings()`, and
  `getPortfolioSnapshots(range)` now do real `fetch()` calls.
  `getRecurringBills`, `getTransactions`, `getSpendingByCategory`,
  `getIncome`, and `getSavingsSnapshots` are untouched (still mock) —
  next PR's scope.
  - `mockData.js` itself is untouched; `accounts`, `holdings`, and
    `portfolioSnapshots` are now unused exports there. Left them rather
    than deleting, in case you still want them for quick UI iteration
    without the backend running — happy to remove in a follow-up if not.

## Not in this PR (follow-ups)

- Transactions/Spending/Breakdown/Home-bills endpoints — blocked on
  seeing `apps/transactions/models.py`
- Any real auth — currently `AllowAny`, matches the app's existing
  localhost-only trust model, but flagged above as a thing to revisit
- Institution-specific filtering (e.g. `?institution=fidelity`) — skipped
  per discussion, since it's single-user and Fidelity is the only
  brokerage linked right now

## How to test locally

```bash
# backend
pip install -r requirements.txt --break-system-packages  # or your usual venv flow
python manage.py migrate
python manage.py runserver

# frontend, separate terminal
cd frontend
npm install
npm run dev
```

Visit `http://127.0.0.1:5173/investments` — if you've already linked
Fidelity via `/plaid/link/` and run a sync, you should see real holdings
and portfolio history instead of the mock data. If nothing's linked yet,
you'll get empty lists rather than an error (no holdings/snapshots to
query yet is a valid, expected state).
