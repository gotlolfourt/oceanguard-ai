const map = {
  active: 'bg-emerald-500/20 text-emerald-300',
  inactive: 'bg-slate-500/20 text-slate-200',
  critical: 'bg-red-500/20 text-red-300',
  warning: 'bg-amber-500/20 text-amber-300',
  success: 'bg-emerald-500/20 text-emerald-300',
  pending: 'bg-slate-500/20 text-slate-200',
}

export function StatusBadge({ status }) {
  return <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase ${map[status] || map.pending}`}>{status}</span>
}
