import { useMemo } from 'react'

export function useWebSocketPlaceholder() {
  return useMemo(
    () => ({
      url: import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws',
      status: 'ready',
      connect: () => null,
      disconnect: () => null,
    }),
    [],
  )
}
