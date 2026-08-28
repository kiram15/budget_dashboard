import { useEffect, useState } from 'react'
import RangeSelector, { useRange } from '../components/RangeSelector'
import StatCard from '../components/StatCard'
import TrendLine from '../components/TrendLine'
import { getSavingsSnapshots } from '../api/client'

export default function Savings() {
  const [range, setRange] = useRange()
  const [snapshots, setSnapshots] = useState([])

  useEffect(() => {
    getSavingsSnapshots(range).then(setSnapshots)
  }, [range])

  const current = snapshots[snapshots.length - 1]?.total_value ?? 0
  const first = snapshots[0]?.total_value
  const delta = first ? (current - first) / first : undefined

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Savings</h1>
          <p className="mt-1 text-sm text-muted">Balance over the selected range</p>
        </div>
        <RangeSelector range={range} onChange={setRange} />
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <StatCard label="Current balance" value={current} delta={delta} deltaLabel="vs. start of range" />
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">Data points</p>
          <p className="num mt-2 text-2xl font-medium text-ink">{snapshots.length}</p>
        </div>
      </div>

      <div className="mt-6">
        <TrendLine data={snapshots} />
      </div>

      <p className="mt-3 text-xs text-muted">
        Open question: is "savings" a specific Account (e.g. the First Tech
        savings account) or a computed figure (income minus spending)? This
        page assumes the former — pulls straight from one account's balance
        history. Worth confirming before wiring to real data.
      </p>
    </div>
  )
}
