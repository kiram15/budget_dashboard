import { useEffect, useMemo, useState } from 'react'
import RangeSelector, { useRange } from '../components/RangeSelector'
import StatCard from '../components/StatCard'
import { getIncome, getSpendingByCategory } from '../api/client'
import { BUCKETS, bucketFor } from '../lib/categoryGroups'

function formatCurrency(value) {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

const barColor = {
  unavoidable: 'bg-ink',
  fun: 'bg-discretionary',
  investments: 'bg-accent',
  leftover: 'bg-subtle',
}

export default function Breakdown() {
  const [range, setRange] = useRange()
  const [incomeItems, setIncomeItems] = useState([])
  const [categories, setCategories] = useState([])

  useEffect(() => {
    getIncome(range).then(setIncomeItems)
    getSpendingByCategory(range).then(setCategories)
  }, [range])

  const { totalIncome, bucketTotals, byBucket, leftover, overspent } = useMemo(() => {
    const totalIncome = incomeItems.reduce((sum, i) => sum + i.amount, 0)

    const byBucket = { unavoidable: [], fun: [], investments: [] }
    categories.forEach((c) => {
      byBucket[bucketFor(c.category)].push(c)
    })

    const bucketTotals = Object.fromEntries(
      Object.entries(byBucket).map(([key, items]) => [
        key,
        items.reduce((sum, i) => sum + i.amount, 0),
      ]),
    )

    const allocated = bucketTotals.unavoidable + bucketTotals.fun + bucketTotals.investments
    const leftover = totalIncome - allocated

    return { totalIncome, bucketTotals, byBucket, leftover, overspent: leftover < 0 }
  }, [incomeItems, categories])

  // Bar segments are proportional to income. If spending exceeds income,
  // scale to the larger of the two so the overage is still visible rather
  // than silently clipped.
  const barBase = Math.max(totalIncome, bucketTotals.unavoidable + bucketTotals.fun + bucketTotals.investments || 0, 1)
  const segments = [
    { key: 'unavoidable', value: bucketTotals.unavoidable },
    { key: 'fun', value: bucketTotals.fun },
    { key: 'investments', value: bucketTotals.investments },
    { key: 'leftover', value: Math.max(leftover, 0) },
  ]

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Breakdown</h1>
          <p className="mt-1 text-sm text-muted">Where money comes from, and where it goes</p>
        </div>
        <RangeSelector range={range} onChange={setRange} />
      </div>

      <div className="mt-6 grid grid-cols-4 gap-4">
        <StatCard label="Income" value={totalIncome} />
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">Unavoidable</p>
          <p className="num mt-2 text-2xl font-medium text-ink">{formatCurrency(bucketTotals.unavoidable)}</p>
        </div>
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">Fun</p>
          <p className="num mt-2 text-2xl font-medium text-discretionary">{formatCurrency(bucketTotals.fun)}</p>
        </div>
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">Investments</p>
          <p className="num mt-2 text-2xl font-medium text-accent">{formatCurrency(bucketTotals.investments)}</p>
        </div>
      </div>

      {/* Allocation bar: income split across the three buckets, with
          whatever's left (or the overage, if spending exceeds income) as
          the final segment. */}
      <div className="mt-6 rounded border border-subtle bg-surface p-4">
        <div className="mb-2 flex items-baseline justify-between">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Allocation of income
          </p>
          <p className={`num text-xs font-medium ${overspent ? 'text-negative' : 'text-muted'}`}>
            {overspent
              ? `${formatCurrency(Math.abs(leftover))} over income`
              : `${formatCurrency(leftover)} left over`}
          </p>
        </div>
        <div className="flex h-3 w-full overflow-hidden rounded-full bg-subtle">
          {segments.map((seg) =>
            seg.value > 0 ? (
              <div
                key={seg.key}
                className={barColor[seg.key]}
                style={{ width: `${(seg.value / barBase) * 100}%` }}
                title={`${seg.key}: ${formatCurrency(seg.value)}`}
              />
            ) : null,
          )}
        </div>
        <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1 text-xs text-muted">
          <LegendItem swatch="bg-ink" label="Unavoidable" />
          <LegendItem swatch="bg-discretionary" label="Fun" />
          <LegendItem swatch="bg-accent" label="Investments" />
          <LegendItem swatch="bg-subtle" label={overspent ? 'Over income' : 'Left over'} />
        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <BucketCard title={BUCKETS.unavoidable.label} items={byBucket.unavoidable} accentClass="text-ink" />
        <BucketCard title={BUCKETS.fun.label} items={byBucket.fun} accentClass="text-discretionary" />
        <BucketCard title={BUCKETS.investments.label} items={byBucket.investments} accentClass="text-accent" />
      </div>

      <p className="mt-3 text-xs text-muted">
        Category → bucket mapping lives in src/lib/categoryGroups.js for now.
        Once wired to real data, this probably wants to be a field on the
        user's own Category model rather than a hardcoded list here.
      </p>
    </div>
  )
}

function LegendItem({ swatch, label }) {
  return (
    <span className="flex items-center gap-1.5">
      <span className={`h-2 w-2 rounded-full ${swatch}`} />
      {label}
    </span>
  )
}

function BucketCard({ title, items, accentClass }) {
  const total = items.reduce((sum, i) => sum + i.amount, 0)
  return (
    <div className="rounded border border-subtle bg-surface p-4">
      <div className="mb-3 flex items-baseline justify-between">
        <p className="text-sm font-medium text-ink">{title}</p>
        <p className={`num text-sm font-medium ${accentClass}`}>{formatCurrency(total)}</p>
      </div>
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item.category} className="flex items-baseline justify-between text-sm">
            <span className="text-muted">{item.category}</span>
            <span className="num text-ink">{formatCurrency(item.amount)}</span>
          </li>
        ))}
        {items.length === 0 && <li className="text-sm text-muted">No categories yet</li>}
      </ul>
    </div>
  )
}
