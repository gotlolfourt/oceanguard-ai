import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-900 text-slate-100">
      <h1 className="text-4xl font-bold">404</h1>
      <p className="mt-2 text-slate-400">Page not found</p>
      <Link to="/dashboard" className="mt-4 rounded-md bg-sky-500 px-4 py-2 text-sm">
        Go to dashboard
      </Link>
    </div>
  )
}
