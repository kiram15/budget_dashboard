// Placeholder data shaped to mirror the Django models described in the
// project's ARCHITECTURE.md, so swapping mockData.js for real fetch calls
// later doesn't require reshaping every component.
//
// IMPORTANT: this file must never contain real account data, even for local
// testing — that's the whole point of keeping this app's data out of any
// LLM-touching context. Keep these numbers obviously fake.

export const accounts = [
  { id: 1, name: 'Checking', type: 'checking', institution: 'Chase', balance: 4210.55 },
  { id: 2, name: 'Savings', type: 'savings', institution: 'First Tech FCU', balance: 18342.10 },
  { id: 3, name: 'Brokerage', type: 'investment', institution: 'Fidelity', balance: 52890.02 },
]

// display_category mirrors Transaction.display_category (user override
// falls back to Plaid's guess). Positive amount = money out, per Plaid's
// convention, preserved here on purpose.
export const recurringBills = [
  { id: 1, name: 'Electric', display_category: 'Utilities', amount: 84.12, due_day: 14, status: 'paid' },
  { id: 2, name: 'Water', display_category: 'Utilities', amount: 41.30, due_day: 18, status: 'paid' },
  { id: 3, name: 'Internet', display_category: 'Utilities', amount: 70.00, due_day: 3, status: 'paid' },
  { id: 4, name: 'Homeowners Insurance', display_category: 'Insurance', amount: 133.40, due_day: 1, status: 'paid' },
  { id: 5, name: 'Mortgage', display_category: 'Housing', amount: 2140.00, due_day: 1, status: 'pending' },
]

export const transactions = [
  { id: 1, date: '2026-08-24', name: 'Trader Joe\'s', display_category: 'Groceries', amount: 62.18 },
  { id: 2, date: '2026-08-22', name: 'Shell', display_category: 'Transport', amount: 41.02 },
  { id: 3, date: '2026-08-20', name: 'Netflix', display_category: 'Subscriptions', amount: 15.49 },
  { id: 4, date: '2026-08-19', name: 'Whole Foods', display_category: 'Groceries', amount: 88.73 },
  { id: 5, date: '2026-08-15', name: 'REI', display_category: 'Shopping', amount: 129.00 },
]

export const spendingByCategory = [
  { category: 'Housing', amount: 2140.00 },
  { category: 'Groceries', amount: 512.30 },
  { category: 'Utilities', amount: 195.42 },
  { category: 'Transport', amount: 168.90 },
  { category: 'Subscriptions', amount: 64.47 },
  { category: 'Shopping', amount: 301.15 },
  { category: 'Dining Out', amount: 187.20 },
  { category: 'Investment Contributions', amount: 800.00 },
]

// Mirrors income-side Transactions (Plaid's negative-amount convention for
// money in, flipped to positive here for display).
export const income = [
  { id: 1, source: 'Paycheck', amount: 5200.00, date: '2026-08-15' },
  { id: 2, source: 'Paycheck', amount: 5200.00, date: '2026-08-01' },
  { id: 3, source: 'Side project', amount: 340.00, date: '2026-08-10' },
]

// Mirrors Holding — current state only, overwritten each sync.
export const holdings = [
  { id: 1, security: 'VTI', name: 'Vanguard Total Stock Mkt ETF', quantity: 42, price: 289.14, value: 12143.88, trailing_30d_return: 0.021 },
  { id: 2, security: 'VXUS', name: 'Vanguard Total Intl Stock ETF', quantity: 60, price: 63.02, value: 3781.20, trailing_30d_return: -0.094 },
  { id: 3, security: 'BND', name: 'Vanguard Total Bond Mkt ETF', quantity: 80, price: 72.55, value: 5804.00, trailing_30d_return: -0.006 },
  { id: 4, security: 'AAPL', name: 'Apple Inc.', quantity: 15, price: 231.40, value: 3471.00, trailing_30d_return: 0.041 },
]

// Mirrors HoldingSnapshot — point-in-time portfolio value, the correct
// source for any "over time" chart per the project's own notes. Gaps are
// expected wherever a sync was skipped; this mock keeps that in mind by
// not pretending every day is populated.
export const portfolioSnapshots = [
  { date: '2026-06-01', total_value: 23890.12 },
  { date: '2026-06-15', total_value: 24310.55 },
  { date: '2026-07-02', total_value: 23980.40 },
  { date: '2026-07-20', total_value: 24660.90 },
  { date: '2026-08-05', total_value: 25100.30 },
  { date: '2026-08-25', total_value: 25200.08 },
]

export const savingsSnapshots = [
  { date: '2026-03-01', total_value: 15200.00 },
  { date: '2026-04-01', total_value: 15900.00 },
  { date: '2026-05-01', total_value: 16400.00 },
  { date: '2026-06-01', total_value: 17100.00 },
  { date: '2026-07-01', total_value: 17650.00 },
  { date: '2026-08-01', total_value: 18342.10 },
]
