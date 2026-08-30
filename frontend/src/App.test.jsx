import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import { AuthProvider } from './context/AuthContext'
import { ToastProvider } from './context/ToastContext'

vi.mock('./services/authService', () => ({
  authService: {
    getCurrentUser: vi.fn().mockRejectedValue(new Error('not authenticated')),
  },
}))

describe('routing', () => {
  it('shows login page for unauthenticated users', async () => {
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <ToastProvider>
          <AuthProvider>
            <App />
          </AuthProvider>
        </ToastProvider>
      </MemoryRouter>,
    )

    expect(await screen.findByText('Login / Register')).toBeInTheDocument()
  })
})
