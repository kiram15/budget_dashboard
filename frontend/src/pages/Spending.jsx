import { useEffect, useState } from 'react'
import RangeSelector, { useRange } from '../components/RangeSelector'
import StatCard from '../components/StatCard'
import { getSpendingByCategory, getTransactions } from '../api/client'

function formatCurrency(value) {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

export default function Spending() {
  const [range, setRange] = useRange()
  const [byCategory, setByCategory] = useState([])
  const [transactions, setTransactions] = useState([])

  useEffect(() => {
    getSpendingByCategory(range).then(setByCategory)
    getTransactions(range).then(setTransactions)
  }, [range])

  const total = byCategory.reduce((sum, c) => sum + c.amount, 0)
  const max = Math.max(...byCategory.map((c) => c.amount), 1)

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Spending</h1>
          <p className="mt-1 text-sm text-muted">By category, over the selected range</p>
        </div>
        <RangeSelector range={range} onChange={setRange} />
      </div>

      <div className="mt-6">
        <StatCard label="Total spent" value={total} />
      </div>

      <div className="mt-6 rounded border border-subtle bg-surface p-4">
        <p className="mb-3 text-xs font-medium uppercase tracking-wide text-muted">
          By category
        </p>
        <div className="space-y-3">
          {byCategory.map((c) => (
            <div key={c.category}>
              <div className="mb-1 flex items-baseline justify-between text-sm">
                <span className="font-medium text-ink">{c.category}</span>
                <span className="num text-muted">{formatCurrency(c.amount)}</span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-subtle">
                <div
                  className="h-1.5 rounded-full bg-accent"
                  style={{ width: `${(c.amount / max) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 overflow-hidden rounded border border-subtle bg-surface">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-subtle bg-bg text-xs uppercase tracking-wide text-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Date</th>
              <th className="px-4 py-3 font-medium">Merchant</th>
              <th className="px-4 py-3 font-medium">Category</th>
              <th className="px-4 py-3 text-right font-medium">Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id} className="border-b border-subtle last:border-0">
                <td className="num px-4 py-3 text-muted">{t.date}</td>
                <td className="px-4 py-3 font-medium text-ink">{t.name}</td>
                <td className="px-4 py-3 text-muted">{t.display_category}</td>
                <td className="num px-4 py-3 text-right text-ink">{formatCurrency(t.amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
