const variantClass = {
  info: 'border-sky-400',
  warning: 'border-amber-400',
  error: 'border-red-400',
  success: 'border-emerald-400',
}

export function ToastContainer({ toasts }) {
  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <div key={toast.id} className={`min-w-52 rounded-md border bg-slate-800 px-4 py-2 text-sm ${variantClass[toast.type] || variantClass.info}`}>
          {toast.message}
        </div>
      ))}
    </div>
  )
}
