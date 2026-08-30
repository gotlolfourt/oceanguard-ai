const variants = {
  info: 'border-sky-500/30 bg-sky-500/10 text-sky-100',
  warning: 'border-amber-500/30 bg-amber-500/10 text-amber-100',
  error: 'border-red-500/30 bg-red-500/10 text-red-100',
  success: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100',
}

export function Alert({ variant = 'info', children }) {
  return <div className={`rounded-md border px-4 py-3 text-sm ${variants[variant]}`}>{children}</div>
}
