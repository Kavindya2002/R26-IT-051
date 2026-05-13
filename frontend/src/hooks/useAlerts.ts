// src/hooks/useAlerts.ts
import { useEffect, useState, useCallback } from 'react'
import { supabase, AlertLog } from '../lib/supabase'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useAlerts(patientId?: number) {
  const [alerts, setAlerts]   = useState<AlertLog[]>([])
  const [loading, setLoading] = useState(true)

  // Initial fetch
  const fetchAlerts = useCallback(async () => {
    setLoading(true)
    const url = patientId
      ? `${API}/alerts?patient_id=${patientId}&limit=50`
      : `${API}/alerts?limit=50`
    const res  = await fetch(url)
    const data = await res.json()
    setAlerts(data)
    setLoading(false)
  }, [patientId])

  useEffect(() => { fetchAlerts() }, [fetchAlerts])

  // Supabase Realtime subscription
  useEffect(() => {
    const channel = supabase
      .channel('alert_log_changes')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'alert_log',
          ...(patientId ? { filter: `patient_id=eq.${patientId}` } : {}),
        },
        (payload) => {
          setAlerts(prev => [payload.new as AlertLog, ...prev])
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [patientId])

  return { alerts, loading, refetch: fetchAlerts }
}
