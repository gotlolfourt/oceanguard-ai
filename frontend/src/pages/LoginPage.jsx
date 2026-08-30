import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { InputField } from '../components/forms/FormFields'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import { authService } from '../services/authService'

export function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const { notify } = useToast()
  const [mode, setMode] = useState('login')
  const [firstName, setFirstName] = useState('New')
  const [lastName, setLastName] = useState('User')
  const [email, setEmail] = useState('admin@oceanguard.com')
  const [password, setPassword] = useState('password123')
  const [loading, setLoading] = useState(false)

  const onSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    try {
      if (mode === 'register') {
        await authService.register({ first_name: firstName, last_name: lastName, email, password })
      }
      await login(email, password)
      notify(mode === 'register' ? 'Registration successful' : 'Login successful', 'success')
      navigate('/dashboard')
    } catch {
      notify(mode === 'register' ? 'Registration failed' : 'Invalid credentials', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 px-4 text-slate-100">
      <div className="w-full max-w-md">
        <Card title="Login / Register">
          <div className="mb-4 flex gap-2">
            <Button variant={mode === 'login' ? 'primary' : 'secondary'} type="button" onClick={() => setMode('login')}>
              Login
            </Button>
            <Button variant={mode === 'register' ? 'primary' : 'secondary'} type="button" onClick={() => setMode('register')}>
              Register
            </Button>
          </div>
          <form className="space-y-4" onSubmit={onSubmit}>
            {mode === 'register' ? (
              <>
                <InputField label="First Name" value={firstName} onChange={(event) => setFirstName(event.target.value)} required />
                <InputField label="Last Name" value={lastName} onChange={(event) => setLastName(event.target.value)} required />
              </>
            ) : null}
            <InputField label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            <InputField label="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            <Button disabled={loading} className="w-full" type="submit">
              {loading ? 'Processing...' : mode === 'register' ? 'Create account' : 'Sign in'}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  )
}
