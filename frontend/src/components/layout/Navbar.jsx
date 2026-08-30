import { useAuth } from '../../context/AuthContext'
import { Button } from '../ui/Button'

export function Navbar() {
  const { user, logout } = useAuth()

  return (
    <header className="flex items-center justify-between border-b border-slate-700 bg-slate-800 px-6 py-4">
      <div>
        <h1 className="text-xl font-bold">OceanGuard AI</h1>
        <p className="text-xs text-slate-400">Marine Debris Monitoring & Response</p>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-200">{user?.email}</span>
        <Button variant="secondary" onClick={logout}>
          Logout
        </Button>
      </div>
    </header>
  )
}
