# Adding a new institution (bank/card/brokerage)

1. **Confirm it's supported first** — don't skip this, saves a wasted trip
   through Link:
   ```
   python manage.py check_institution "Name of bank"
   ```
   Look at the `oauth` field in the output — `True` means the institution
   uses a redirect-to-their-site OAuth flow (need PLAID_REDIRECT_URI
   configured with a real https tunnel, see step 2 note). `False` means
   the classic Plaid-hosted username/password widget — no tunnel needed.

2. **Start the Django dev server and visit `/plaid/link/`** in your browser.
   - If the institution is OAuth-based, first point PLAID_REDIRECT_URI (in
     .env) at a local HTTPS tunnel — `ngrok http 8000` or `cloudflared
     tunnel --url http://localhost:8000` both work, or use `mkcert` for a
     trusted local cert if you want no external tunnel dependency at all.
     This is ONLY needed for this one-time Link step, not for ongoing syncs.

3. **Type your bank credentials into the Plaid widget itself** — not
   anywhere on your own page. If you're ever prompted for a bank password
   outside that widget, stop, something's wrong.

4. On success, the page calls `/plaid/link/exchange/` automatically, which:
   - creates an `Institution` row if new
   - stores the access token in your OS keychain
   - creates a `PlaidItem` and its `Account` row(s)
   - runs an initial sync

5. **Backfill price history** if this is an investment account:
   ```
   python manage.py backfill_prices --days 365
   ```

6. Note the `keychain_ref` printed in the response JSON somewhere memorable
   (or just query `PlaidItem.objects.all()` later) — it's what you'd need
   if you ever want to manually inspect or rotate the token.

## If linking fails partway through
Nothing destructive happens until step 4 succeeds — if Link exits early
(you closed the widget, entered wrong credentials, etc.) no PlaidItem or
Account gets created. Just revisit `/plaid/link/` and try again.

## If the institution isn't in Plaid's directory at all
Fall back options, roughly in order of effort:
- Check SimpleFIN's institution list as a second aggregator (see
  ARCHITECTURE.md for why we didn't start there)
- Manual CSV import — most banks let you export transaction history;
  worth building a one-off `import_csv` management command per format
  rather than trying to generalize this until you actually need a second one
