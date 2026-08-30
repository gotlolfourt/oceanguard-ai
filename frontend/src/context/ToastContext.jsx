import { createContext, useContext, useMemo, useState } from 'react'
import { ToastContainer } from '../components/ui/Toast'

const ToastContext = createContext(null)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const value = useMemo(
    () => ({
      notify(message, type = 'info') {
        const id =
          typeof globalThis.crypto?.randomUUID === 'function'
            ? globalThis.crypto.randomUUID()
            : `${Date.now()}-${Math.random()}`
        setToasts((prev) => [...prev, { id, message, type }])
        setTimeout(() => {
          setToasts((prev) => prev.filter((toast) => toast.id !== id))
        }, 3000)
      },
    }),
    [],
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used inside ToastProvider')
  }
  return context
}
