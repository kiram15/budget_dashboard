import { useEffect, useState } from 'react'
import RangeSelector, { useRange } from '../components/RangeSelector'
import StatCard from '../components/StatCard'
import TrendLine from '../components/TrendLine'
import { getHoldings, getPortfolioSnapshots } from '../api/client'

function formatCurrency(value) {
  return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}

const LOSS_THRESHOLD = -0.08 // matches trailing_return()'s flagging threshold

export default function Investments() {
  const [range, setRange] = useRange()
  const [holdings, setHoldings] = useState([])
  const [snapshots, setSnapshots] = useState([])

  useEffect(() => {
    getHoldings().then(setHoldings)
  }, [])

  useEffect(() => {
    getPortfolioSnapshots(range).then(setSnapshots)
  }, [range])

  const totalValue = holdings.reduce((sum, h) => sum + h.value, 0)
  const flagged = holdings.filter((h) => h.trailing_30d_return <= LOSS_THRESHOLD)

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Investments</h1>
          <p className="mt-1 text-sm text-muted">Holdings and portfolio value over time</p>
        </div>
        <RangeSelector range={range} onChange={setRange} />
      </div>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <StatCard label="Portfolio value" value={totalValue} />
        <StatCard label="Holdings" value={holdings.length} deltaLabel="" />
        <div className="rounded border border-subtle bg-surface p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            Flagged (down &gt; 8%, 30d)
          </p>
          <p className="num mt-2 text-2xl font-medium text-negative">{flagged.length}</p>
        </div>
      </div>

      <div className="mt-6">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted">
          Value over selected range
        </p>
        <TrendLine data={snapshots} />
        <p className="mt-2 text-xs text-muted">
          Sourced from HoldingSnapshot, not current Holding state — expect gaps
          wherever a sync was skipped.
        </p>
      </div>

      <div className="mt-6 overflow-hidden rounded border border-subtle bg-surface">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-subtle bg-bg text-xs uppercase tracking-wide text-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Security</th>
              <th className="px-4 py-3 text-right font-medium">Qty</th>
              <th className="px-4 py-3 text-right font-medium">Price</th>
              <th className="px-4 py-3 text-right font-medium">Value</th>
              <th className="px-4 py-3 text-right font-medium">30d return</th>
            </tr>
          </thead>
          <tbody>
            {holdings.map((h) => {
              const isFlagged = h.trailing_30d_return <= LOSS_THRESHOLD
              return (
                <tr key={h.id} className="border-b border-subtle last:border-0">
                  <td className="px-4 py-3">
                    <span className="font-medium text-ink">{h.security}</span>
                    <span className="ml-2 text-muted">{h.name}</span>
                  </td>
                  <td className="num px-4 py-3 text-right text-ink">{h.quantity}</td>
                  <td className="num px-4 py-3 text-right text-ink">{formatCurrency(h.price)}</td>
                  <td className="num px-4 py-3 text-right text-ink">{formatCurrency(h.value)}</td>
                  <td
                    className={`num px-4 py-3 text-right font-medium ${
                      h.trailing_30d_return >= 0 ? 'text-positive' : 'text-negative'
                    }`}
                  >
                    {(h.trailing_30d_return * 100).toFixed(1)}%
                    {isFlagged && (
                      <span className="ml-2 rounded bg-negative/10 px-1.5 py-0.5 text-[10px] font-sans font-medium text-negative">
                        FLAGGED
                      </span>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
