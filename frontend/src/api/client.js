// getAccounts / getHoldings / getPortfolioSnapshots now hit the real DRF
// backend (see apps/accounts/views.py and apps/investments/views.py).
// Everything else here still resolves mock data until the transactions/
// spending endpoints exist — swap those the same way, one at a time.
//
// `range` is one of 'month' | '6m' | 'year' | 'all' (see RangeSelector).
// It's resolved to a start date server-side, against the request's own
// "today" (see apps/common/utils.py resolve_range()) — the browser's
// clock is never the source of truth for financial reporting.

import {
  recurringBills,
  transactions,
  spendingByCategory,
  income,
  savingsSnapshots,
} from './mockData'

const fakeLatency = (data) => new Promise((resolve) => setTimeout(() => resolve(data), 200))

async function getJSON(path) {
  const res = await fetch(path)
  if (!res.ok) {
    throw new Error(`Request to ${path} failed: ${res.status}`)
  }
  return res.json()
}

export async function getAccounts() {
  return getJSON('/api/accounts/')
}

export async function getRecurringBills(range) {
  return fakeLatency(recurringBills)
}

export async function getTransactions(range) {
  return fakeLatency(transactions)
}

export async function getSpendingByCategory(range) {
  return fakeLatency(spendingByCategory)
}

export async function getIncome(range) {
  return fakeLatency(income)
}

export async function getHoldings() {
  return getJSON('/api/investments/holdings/')
}

export async function getPortfolioSnapshots(range) {
  return getJSON(`/api/investments/portfolio-history/?range=${encodeURIComponent(range)}`)
}

export async function getSavingsSnapshots(range) {
  return fakeLatency(savingsSnapshots)
}
