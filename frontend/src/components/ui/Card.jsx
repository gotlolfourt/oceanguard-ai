export function Card({ title, footer, children }) {
  return (
    <section className="rounded-lg bg-slate-800 p-6 shadow-sm">
      {title ? <h3 className="mb-4 text-lg font-semibold text-slate-100">{title}</h3> : null}
      <div className="space-y-4">{children}</div>
      {footer ? <footer className="mt-4 border-t border-slate-700 pt-4">{footer}</footer> : null}
    </section>
  )
}
