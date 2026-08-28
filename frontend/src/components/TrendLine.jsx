// Deliberately dependency-free for the shell phase. Data has the same
// shape a HoldingSnapshot/portfolio-history endpoint would return:
// [{ date, total_value }]. When real charting lands (Tremor's AreaChart
// is a good fit, per the earlier recommendation) this component's props
// can stay the same — only the internals change.
export default function TrendLine({ data, valueKey = 'total_value', height = 96 }) {
  if (!data || data.length < 2) {
    return (
      <div
        className="flex items-center justify-center rounded border border-dashed border-subtle text-sm text-muted"
        style={{ height }}
      >
        Not enough data yet
      </div>
    )
  }

  const values = data.map((d) => d[valueKey])
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const width = 100

  const points = values
    .map((v, i) => {
      const x = (i / (values.length - 1)) * width
      const y = height - ((v - min) / range) * height
      return `${x},${y}`
    })
    .join(' ')

  const last = values[values.length - 1]
  const first = values[0]
  const up = last >= first

  return (
    <div className="rounded border border-subtle bg-surface p-4">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="none"
        className="h-24 w-full"
      >
        <polyline
          points={points}
          fill="none"
          stroke={up ? '#1F8A5F' : '#A6402A'}
          strokeWidth="1.5"
          vectorEffect="non-scaling-stroke"
        />
      </svg>
      <div className="num mt-2 flex justify-between text-xs text-muted">
        <span>{data[0].date}</span>
        <span>{data[data.length - 1].date}</span>
      </div>
    </div>
  )
}
