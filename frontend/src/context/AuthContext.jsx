import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('oceanguard_access_token')
    if (!token) {
      setLoading(false)
      return
    }

    authService
      .getCurrentUser()
      .then((currentUser) => setUser(currentUser))
      .catch(() => {
        localStorage.removeItem('oceanguard_access_token')
        localStorage.removeItem('oceanguard_refresh_token')
      })
      .finally(() => setLoading(false))
  }, [])

  const value = useMemo(
    () => ({
      user,
      loading,
      async login(email, password) {
        const tokens = await authService.login(email, password)
        localStorage.setItem('oceanguard_access_token', tokens.access_token)
        localStorage.setItem('oceanguard_refresh_token', tokens.refresh_token)
        const currentUser = await authService.getCurrentUser()
        setUser(currentUser)
        return currentUser
      },
      logout() {
        localStorage.removeItem('oceanguard_access_token')
        localStorage.removeItem('oceanguard_refresh_token')
        setUser(null)
      },
    }),
    [user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}
