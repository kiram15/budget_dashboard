import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Home', end: true },
  { to: '/investments', label: 'Investments' },
  { to: '/savings', label: 'Savings' },
  { to: '/spending', label: 'Spending' },
  { to: '/breakdown', label: 'Breakdown' },
]

export default function Sidebar() {
  return (
    <aside className="flex w-56 shrink-0 flex-col bg-ink text-white">
      <div className="border-b border-white/10 px-6 py-5">
        <p className="font-display text-lg font-semibold tracking-tight">Ledger</p>
        <p className="text-xs text-white/50">Personal finance</p>
      </div>
      <nav className="flex flex-1 flex-col gap-1 px-3 py-4">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              [
                'rounded px-3 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-white/10 text-white border-l-2 border-accent -ml-px pl-[11px]'
                  : 'text-white/60 hover:bg-white/5 hover:text-white',
              ].join(' ')
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-white/10 px-6 py-4 text-xs text-white/40">
        Local only &middot; no cloud sync
      </div>
    </aside>
  )
}
