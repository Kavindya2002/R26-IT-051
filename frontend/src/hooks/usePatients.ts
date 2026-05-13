// src/hooks/usePatients.ts
import { useEffect, useState } from 'react'
import { supabase, Patient } from '../lib/supabase'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    fetch(`${API}/patients`)
      .then(r => r.json())
      .then(data => { setPatients(data); setLoading(false) })
  }, [])

  // Realtime risk_score updates
  useEffect(() => {
    const channel = supabase
      .channel('patients_changes')
      .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'patients' }, (payload) => {
        setPatients(prev =>
          prev.map(p => p.id === (payload.new as Patient).id ? { ...p, ...(payload.new as Patient) } : p)
        )
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [])

  return { patients, loading }
}
