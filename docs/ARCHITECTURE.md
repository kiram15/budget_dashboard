# Architecture decisions

## Why Plaid, not direct bank APIs
Individual banks/brokerages (Chase, Fidelity) don't offer public developer
APIs to individual consumers — that access is gated to licensed fintechs.
Plaid sits in between: your app only ever talks to Plaid's API, and Plaid
handles the actual institution connection. See docs discussion from
[date you built this] for SimpleFIN as the alternative we considered.

## Why access tokens live in the OS keychain, not the database
The database is a plain SQLite/Postgres file relying on your laptop's
disk encryption (FileVault/BitLocker) for protection — same trust boundary
as every other sensitive file on the machine. If that file ever leaked
(backup, accidental commit, etc.), it should only expose historical
account data, never something that lets an attacker pull fresh data.
The OS keychain is a separate, OS-managed secret store — see
`apps/plaid_integration/token_store.py`. `PlaidItem.keychain_ref` is a
*name*, never the secret itself — this is enforced by convention (there's
no access_token field on any model), not by code, so don't add one later
without re-reading this note.

## Why transactions/sync (cursor-based) instead of webhooks
Webhooks assume Plaid can reach a public endpoint on your server. This app
has no public endpoint — it runs on-demand, on your laptop, at 127.0.0.1.
`transactions/sync` is pull-based and idempotent: call it whenever you
open the app, it tells you what's changed since your last cursor.

## Why HoldingSnapshot exists separately from Holding
Plaid's `Holding` data is always "current state" — it gets overwritten on
every sync. If you want to chart portfolio value over time, you need to
persist your own history, since Plaid doesn't provide a holdings time series.
Practical consequence: your history has gaps wherever you went a while
without syncing. That's expected given the on-demand design, not a bug.

## Why the market-summary feature only uses generic index data
Deliberate choice, made explicitly to avoid sending any personal financial
data to an external LLM API — see `apps/investments/analysis.py`. The
"is MY stuff losing money" logic is 100% local math (`trailing_return`);
only "what's the market broadly doing" touches an external API, and only
with public S&P 500 / Nasdaq numbers, never your tickers or balances.

## Why no Celery/background scheduler
Deliberately skipped for v1 given the on-demand, laptop-only usage pattern
— it's infra you'd be maintaining for a use case ("sync while I'm not
looking") that doesn't currently exist. Revisit this if usage patterns
change (e.g. you move this to an always-on home server later).
