-- ============================================================
--  MediFlow – Supabase Schema
--  Run this in Supabase → SQL Editor
-- ============================================================

-- 1. PATIENTS
CREATE TABLE patients (
  id          SERIAL PRIMARY KEY,
  bed         VARCHAR(10) NOT NULL UNIQUE,   -- "Bed 05"
  name        VARCHAR(100) NOT NULL,
  status      VARCHAR(10) DEFAULT 'stable',  -- stable | caution | critical
  risk_score  INTEGER DEFAULT 0,             -- 0–100
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 2. ALERT LOG
CREATE TABLE alert_log (
  id          SERIAL PRIMARY KEY,
  patient_id  INTEGER REFERENCES patients(id) ON DELETE CASCADE,
  alert_type  VARCHAR(20) NOT NULL,          -- ALERT | NEAR-MISS | INFO
  severity    VARCHAR(10) NOT NULL,          -- critical | warning | info
  message     TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 3. GAIT DATA  (latest snapshot per patient)
CREATE TABLE gait_data (
  id            SERIAL PRIMARY KEY,
  patient_id    INTEGER REFERENCES patients(id) ON DELETE CASCADE,
  tilt_angle    FLOAT[],    -- array of 41 readings
  movement_speed FLOAT[],
  balance_level  FLOAT[],
  com_fluctuation FLOAT[],
  recorded_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ── Enable Realtime on alert_log ──
ALTER PUBLICATION supabase_realtime ADD TABLE alert_log;
ALTER PUBLICATION supabase_realtime ADD TABLE patients;

-- ── Row Level Security (optional – disable for dev) ──
ALTER TABLE patients    ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_log   ENABLE ROW LEVEL SECURITY;
ALTER TABLE gait_data   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all" ON patients    FOR ALL USING (true);
CREATE POLICY "Allow all" ON alert_log   FOR ALL USING (true);
CREATE POLICY "Allow all" ON gait_data   FOR ALL USING (true);

-- ── Seed patients ──
INSERT INTO patients (bed, name, status, risk_score) VALUES
  ('Bed 00', 'John Diamson',    'stable',   12),
  ('Bed 01', 'Actire Bringer',  'caution',  45),
  ('Bed 02', 'Lady Manc',       'caution',  52),
  ('Bed 03', 'Patient Dloex',   'stable',   18),
  ('Bed 04', 'Kathe Soktwoon',  'stable',   22),
  ('Bed 05', 'John Doe',        'critical', 78),
  ('Bed 06', 'Anicar Carliner', 'caution',  41),
  ('Bed 07', 'Roige Huck',      'caution',  38),
  ('Bed 08', 'Jenme Werse',     'stable',   15),
  ('Bed 09', 'Jenne Elifier',   'stable',   20),
  ('Bed 10', 'Stapina Sherity', 'stable',   10),
  ('Bed 11', 'Tourm Rurkrimom', 'stable',    8),
  ('Bed 12', 'Christ Dafton',   'critical', 81),
  ('Bed 13', 'John Inartz',     'critical', 76),
  ('Bed 14', 'Marielll Seave',  'critical', 88);

-- ── Seed alert_log ──
INSERT INTO alert_log (patient_id, alert_type, severity, message) VALUES
  (6, 'ALERT',     'critical', 'Imbalance detected due to excessive left lateral tilt.'),
  (6, 'NEAR-MISS', 'warning',  'Patient caught leaning forward – intervention prevented fall.'),
  (4, 'NEAR-MISS', 'info',     'Patient Bed 03 caught leaning forward – caregiver notified.'),
  (6, 'NEAR-MISS', 'critical', 'Sudden 45° body tilt detected – high fall risk.'),
  (13,'ALERT',     'critical', 'Christ Dafton – abrupt drop in balance score.'),
  (14,'NEAR-MISS', 'warning',  'John Inartz – movement speed spike detected.'),
  (15,'ALERT',     'critical', 'Marielll Seave – critical imbalance, caregiver dispatched.');
