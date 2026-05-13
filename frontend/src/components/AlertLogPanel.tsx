// src/components/AlertLogPanel.tsx
import React, { useState } from 'react'
import { AlertLog } from '../lib/supabase'
import { useAlerts } from '../hooks/useAlerts'

interface Props {
  patientId?: number
  patientName?: string
}

const SEVERITY_STYLES: Record<string, React.CSSProperties> = {
  critical: { borderLeftColor: '#f85149', background: 'rgba(248,81,73,0.06)' },
  warning:  { borderLeftColor: '#d29922', background: 'rgba(210,153,34,0.06)' },
  info:     { borderLeftColor: '#3fb950', background: 'rgba(63,185,80,0.06)'  },
}
const BADGE_COLORS: Record<string, string> = {
  ALERT:      '#f85149',
  'NEAR-MISS':'#d29922',
  INFO:       '#3fb950',
}

function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const s = Math.floor(diff / 1000)
  if (s < 60)  return `${s}s ago`
  if (s < 3600) return `${Math.floor(s/60)}m ago`
  return new Date(iso).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

export default function AlertLogPanel({ patientId, patientName }: Props) {
  const { alerts, loading } = useAlerts(patientId)
  const [filter, setFilter] = useState<string>('ALL')

  const visible = filter === 'ALL'
    ? alerts
    : alerts.filter(a => a.alert_type === filter)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ padding: '8px 12px 5px', borderBottom: '1px solid #21262d' }}>
        <div style={{ fontSize: 15, fontWeight: 700, color: '#e6edf3', letterSpacing: 0.5 }}>
          AI DECISION &amp; ALERT LOG
        </div>
        <div style={{ fontSize: 15, color: '#6e7681', marginTop: 5 }}>
          {patientName ? `Patient: ${patientName}` : 'All patients'} · Live
          <span style={{
            display: 'inline-block', width: 6, height: 6,
            borderRadius: '50%', background: '#3fb950',
            marginLeft: 5, verticalAlign: 'middle',
            animation: 'pulse 1.5s infinite'
          }} />
        </div>
      </div>

      {/* Filter tabs */}
      <div style={{ display: 'flex', gap: 4, padding: '5px 10px', borderBottom: '1px solid #21262d' }}>
        {['ALL', 'ALERT', 'NEAR-MISS', 'INFO'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            fontSize: 9, padding: '2px 7px', borderRadius: 4, border: 'none',
            cursor: 'pointer', fontWeight: filter === f ? 700 : 400,
            background: filter === f ? '#21262d' : 'transparent',
            color: filter === f ? '#e6edf3' : '#6e7681',
          }}>{f}</button>
        ))}
        <span style={{ marginLeft: 'auto', fontSize: 9, color: '#6e7681', alignSelf: 'center' }}>
          {alerts.length} total
        </span>
      </div>

      {/* Alert list */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {loading && (
          <div style={{ padding: 16, color: '#6e7681', fontSize: 12, textAlign: 'center' }}>
            Loading alerts...
          </div>
        )}
        {!loading && visible.length === 0 && (
          <div style={{ padding: 16, color: '#6e7681', fontSize: 12, textAlign: 'center' }}>
            No alerts found
          </div>
        )}
        {visible.map(a => (
          <AlertItem key={a.id} alert={a} />
        ))}
      </div>

      <style>{`
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-thumb { background: #30363d; }
      `}</style>
    </div>
  )
}

function AlertItem({ alert }: { alert: AlertLog }) {
  const style = SEVERITY_STYLES[alert.severity] || SEVERITY_STYLES.info
  const badgeColor = BADGE_COLORS[alert.alert_type] || '#3fb950'

  return (
    <div style={{
      padding: '7px 10px',
      borderBottom: '1px solid rgba(33,38,45,0.4)',
      borderLeft: '3px solid transparent',
      transition: 'background 0.2s',
      ...style,
    }}>
      <div style={{ fontSize: 12, color: '#6e7681', marginBottom: 2, display: 'flex', justifyContent: 'space-between' }}>
        <span>{timeAgo(alert.created_at)}</span>
        {alert.patients && (
          <span style={{ color: '#8b949e' }}>{alert.patients.bed} · {alert.patients.name}</span>
        )}
      </div>
      <div style={{ fontSize: 14, lineHeight: 1.45, color: '#c9d1d9' }}>
        <span style={{ fontWeight: 700, color: badgeColor, marginRight: 3 }}>
          {alert.alert_type}:
        </span>
        {alert.message}
      </div>
    </div>
  )
}
