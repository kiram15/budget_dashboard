import { useEffect, useState } from 'react'
import RangeSelector, { useRange } from '../components/RangeSelector'
import { getRecurringBills, getAccounts } from '../api/client'

function formatCurrency(value) {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

const statusStyle = {
  paid: 'bg-accent-soft text-accent',
  pending: 'bg-subtle text-muted',
}

export default function HouseDashboard() {
  const [range, setRange] = useRange()
  const [bills, setBills] = useState([])
  const [accounts, setAccounts] = useState([])

  useEffect(() => {
    getRecurringBills(range).then(setBills)
    getAccounts().then(setAccounts)
  }, [range])

  const totalDue = bills.reduce((sum, b) => sum + b.amount, 0)
  const totalBalance = accounts.reduce((sum, a) => sum + a.balance, 0)

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Home</h1>
          <p className="mt-1 text-sm text-muted">Recurring bills and account balances</p>
        </div>
        <RangeSelector range={range} onChange={setRange} />
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Total balance across accounts
          </p>
          <p className="num mt-2 text-2xl font-medium text-ink">{formatCurrency(totalBalance)}</p>
        </div>
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Bills due this period
          </p>
          <p className="num mt-2 text-2xl font-medium text-ink">{formatCurrency(totalDue)}</p>
        </div>
      </div>

      <div className="mt-6 overflow-hidden rounded border border-subtle bg-surface">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-subtle bg-bg text-xs uppercase tracking-wide text-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Bill</th>
              <th className="px-4 py-3 font-medium">Category</th>
              <th className="px-4 py-3 font-medium">Due day</th>
              <th className="px-4 py-3 text-right font-medium">Amount</th>
              <th className="px-4 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {bills.map((bill) => (
              <tr key={bill.id} className="border-b border-subtle last:border-0">
                <td className="px-4 py-3 font-medium text-ink">{bill.name}</td>
                <td className="px-4 py-3 text-muted">{bill.display_category}</td>
                <td className="num px-4 py-3 text-muted">{bill.due_day}</td>
                <td className="num px-4 py-3 text-right text-ink">{formatCurrency(bill.amount)}</td>
                <td className="px-4 py-3">
                  <span className={`rounded px-2 py-0.5 text-xs font-medium ${statusStyle[bill.status]}`}>
                    {bill.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-3 text-xs text-muted">
        Bills are transactions filtered by category — confirm whether "Utilities" /
        "Insurance" / "Housing" categories are enough, or whether these need an
        explicit is_recurring flag once this is wired to real data.
      </p>
    </div>
  )
}
