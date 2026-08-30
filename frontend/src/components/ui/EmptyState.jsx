export function EmptyState({ title, description }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-600 p-6 text-center">
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-slate-300">{description}</p>
    </div>
  )
}
