# Budget frontend — shell

React + Vite + Tailwind + React Router shell for the four dashboard pages
(Home, Investments, Savings, Spending). All data currently comes from
`src/api/mockData.js` via `src/api/client.js` — nothing here talks to Django
yet, and no real financial data should ever be pasted into this project's
chat history (see the project's own core design principle on that).

This was built without network access, so dependencies have **not** been
installed or run — do that locally:

```bash
npm install
npm run dev
```

Opens on `http://127.0.0.1:5173` (matches the Django backend's
localhost-only convention).

## Structure

```
src/
  api/
    client.js       — every function here should become a fetch() to DRF later;
                       page components don't know or care where data comes from
    mockData.js      — placeholder data shaped like the Django models
  components/
    Layout.jsx       — sidebar + routed page outlet
    Sidebar.jsx       — nav
    RangeSelector.jsx — shared Month/6mo/Year/All-time control, synced to ?range=
    StatCard.jsx      — KPI card with tabular-figure numbers
    TrendLine.jsx      — dependency-free placeholder chart (swap for Tremor/Recharts later)
  pages/
    HouseDashboard.jsx  — recurring bills: utilities, insurance, mortgage
    Investments.jsx    — holdings + portfolio value trend + trailing_return() flags
    Savings.jsx        — balance trend for a savings account
    Spending.jsx        — category breakdown + transaction list
```

## Design decisions

- **Palette**: cool paper background (`#F6F7F5`) + deep pine ink
  (`#1C2B2D`) + a ledger green accent (`#1F6F5C`). Positive/negative deltas
  use green/rust (`#1F8A5F` / `#A6402A`) rather than stoplight red-green.
- **Type**: Space Grotesk for headings, Inter for UI text, **IBM Plex Mono
  with tabular figures for every number** (balances, percentages, dates).
  That's the one signature detail worth keeping consistent as more pages
  get built — every number in the app should carry the `.num` utility
  class (defined in `src/index.css`) so columns line up like a real
  statement.
- **Range selector**: lives in the URL (`?range=month|6m|year|all`) via
  `useRange()` in `RangeSelector.jsx`, not local component state — so a
  refresh doesn't reset it and it's trivial to pass straight into an API
  call.

## Known gaps / open questions (carried over from planning)

- Home Dashboard: bills are currently just category-filtered transactions.
  Decide whether that's sufficient or whether recurring bills need their
  own flag/model.
- Investments: `TrendLine` is intentionally dependency-free for the shell.
  Tremor's `AreaChart` (or Recharts directly) is the natural next step —
  props were kept simple (`data`, `valueKey`) so swapping the internals
  shouldn't require touching the page components.
- Savings: assumes "savings" means one specific `Account`, not a computed
  income-minus-spending figure. Confirm before wiring real data.
- No auth/login screen — matches the single-user, localhost-only backend,
  so there isn't one by design.

## Next step

Once you're happy with the shell, the natural next step is standing up the
DRF serializers/viewsets and replacing the bodies of the functions in
`src/api/client.js` one at a time.
