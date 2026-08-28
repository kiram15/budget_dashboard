function formatCurrency(value) {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

function formatPercent(value) {
  const pct = (value * 100).toFixed(1)
  return `${value >= 0 ? '+' : ''}${pct}%`
}

// `delta` is an optional fraction (e.g. 0.021 for +2.1%). Positive/negative
// use the ledger green/rust pair defined in tailwind.config.js, not
// stoplight red/green.
export default function StatCard({ label, value, delta, deltaLabel }) {
  const hasDelta = typeof delta === 'number'
  const deltaColor = hasDelta ? (delta >= 0 ? 'text-positive' : 'text-negative') : ''

  return (
    <div className="rounded border border-subtle bg-surface p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-muted">{label}</p>
      <p className="num mt-2 text-2xl font-medium text-ink">{formatCurrency(value)}</p>
      {hasDelta && (
        <p className={`num mt-1 text-xs font-medium ${deltaColor}`}>
          {formatPercent(delta)}
          {deltaLabel ? <span className="ml-1 font-sans text-muted">{deltaLabel}</span> : null}
        </p>
      )}
    </div>
  )
}
