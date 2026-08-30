import { Card } from '../components/ui/Card'
import { EmptyState } from '../components/ui/EmptyState'
import { Alert } from '../components/ui/Alert'
import { StatusBadge } from '../components/ui/StatusBadge'
import { Table } from '../components/ui/Table'
import { useAuth } from '../context/AuthContext'
import { useWebSocketPlaceholder } from '../hooks/useWebSocketPlaceholder'

export function DashboardPage() {
  const { user } = useAuth()
  const ws = useWebSocketPlaceholder()

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Dashboard</h2>
      <Alert variant="info">WebSocket placeholder status: {ws.status} ({ws.url})</Alert>
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        <Card title="System Status">
          <StatusBadge status="active" />
          <p className="text-sm text-slate-300">Backend/API and AI services connected.</p>
        </Card>
        <Card title="Alerts">
          <StatusBadge status="warning" />
          <p className="text-sm text-slate-300">3 open alerts across monitoring zones.</p>
        </Card>
        <Card title="Map Placeholder">
          <div className="rounded-md border border-slate-700 bg-slate-900 p-4 text-sm">Leaflet map integration placeholder</div>
        </Card>
      </div>
      <Card title="Recent Alerts">
        <Table
          columns={[
            { key: 'zone', label: 'Zone' },
            { key: 'risk', label: 'Risk' },
            { key: 'status', label: 'Status' },
          ]}
          rows={[
            { id: 1, zone: 'North Bay', risk: 'high', status: 'new' },
            { id: 2, zone: 'South Bay', risk: 'medium', status: 'acknowledged' },
          ]}
        />
      </Card>
      {user?.role === 'admin' ? <Alert variant="success">Admin controls are enabled for this account.</Alert> : null}
      <EmptyState title="No live detections" description="Connect cameras or upload media to start receiving detections." />
    </div>
  )
}
