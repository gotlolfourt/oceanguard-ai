export function InputField({ label, error, helpText, ...props }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm text-slate-200">{label}</span>
      <input className="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-sm" {...props} />
      {helpText ? <p className="text-xs text-slate-400">{helpText}</p> : null}
      {error ? <p className="text-xs text-red-400">{error}</p> : null}
    </label>
  )
}

export function SelectField({ label, options, ...props }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm text-slate-200">{label}</span>
      <select className="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-sm" {...props}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  )
}

export function TextAreaField({ label, ...props }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm text-slate-200">{label}</span>
      <textarea className="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-sm" {...props} />
    </label>
  )
}

export function CheckboxField({ label, ...props }) {
  return (
    <label className="flex items-center gap-2 text-sm text-slate-200">
      <input type="checkbox" {...props} />
      {label}
    </label>
  )
}
