// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = (import.meta as any).env.VITE_SUPABASE_URL as string
const SUPABASE_ANON  = (import.meta as any).env.VITE_SUPABASE_ANON_KEY as string

//const SUPABASE_URL  = import.meta.env.VITE_SUPABASE_URL  as string
// const SUPABASE_ANON = import.meta.env.VITE_SUPABASE_ANON_KEY as string

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON)

// ── Types ──────────────────────────────────────────────────
export type Status = 'stable' | 'caution' | 'critical'

export interface Patient {
  id: number
  bed: string
  name: string
  status: Status
  risk_score: number
  created_at: string
  tilt_angle?: number;      
  movement_speed?: number;
}

export interface AlertLog {
  id: number
  patient_id: number
  alert_type: 'ALERT' | 'NEAR-MISS' | 'INFO'
  severity: 'critical' | 'warning' | 'info'
  message: string
  created_at: string
  patients?: { name: string; bed: string }
}

export interface GaitData {
  id: number
  patient_id: number
  tilt_angle: number[]
  movement_speed: number[]
  balance_level: number[]
  com_fluctuation: number[]
  recorded_at: string
}
