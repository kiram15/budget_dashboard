import { useSearchParams } from 'react-router-dom'

export const RANGE_OPTIONS = [
  { value: 'month', label: 'Month' },
  { value: '6m', label: '6 Month' },
  { value: 'year', label: 'Year' },
  { value: 'all', label: 'All Time' },
]

const DEFAULT_RANGE = 'month'

// Reads/writes ?range= so the selected window survives a page refresh and
// is shareable — and so it's a single value pages pass straight through
// to the API client rather than each page keeping its own local state.
export function useRange() {
  const [searchParams, setSearchParams] = useSearchParams()
  const range = searchParams.get('range') || DEFAULT_RANGE

  const setRange = (value) => {
    const next = new URLSearchParams(searchParams)
    next.set('range', value)
    setSearchParams(next, { replace: true })
  }

  return [range, setRange]
}

export default function RangeSelector({ range, onChange }) {
  return (
    <div
      role="tablist"
      aria-label="Time range"
      className="inline-flex rounded border border-subtle bg-surface p-0.5"
    >
      {RANGE_OPTIONS.map((opt) => {
        const active = opt.value === range
        return (
          <button
            key={opt.value}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(opt.value)}
            className={[
              'rounded px-3 py-1.5 text-sm font-medium transition-colors',
              active
                ? 'bg-accent text-white'
                : 'text-muted hover:text-ink',
            ].join(' ')}
          >
            {opt.label}
          </button>
        )
      })}
    </div>
  )
}
