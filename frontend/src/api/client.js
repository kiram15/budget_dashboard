// Every function below currently resolves mock data. Swapping to the real
// DRF backend should mean editing this file only — no page component
// should know or care whether its data came from mockData.js or a fetch().
//
// Shape to follow once DRF exists, e.g.:
//   export async function getAccounts() {
//     const res = await fetch('/api/accounts/')
//     if (!res.ok) throw new Error('Failed to load accounts')
//     return res.json()
//   }
//
// `range` is one of 'month' | '6m' | 'year' | 'all' (see RangeSelector).
// Resolve it to a start date server-side against the request's own
// "today", not client-side, so the browser's clock is never the source of
// truth for financial reporting.

import {
  accounts,
  recurringBills,
  transactions,
  spendingByCategory,
  income,
  holdings,
  portfolioSnapshots,
  savingsSnapshots,
} from './mockData'

const fakeLatency = (data) => new Promise((resolve) => setTimeout(() => resolve(data), 200))

export async function getAccounts() {
  return fakeLatency(accounts)
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
  return fakeLatency(holdings)
}

export async function getPortfolioSnapshots(range) {
  return fakeLatency(portfolioSnapshots)
}

export async function getSavingsSnapshots(range) {
  return fakeLatency(savingsSnapshots)
}
