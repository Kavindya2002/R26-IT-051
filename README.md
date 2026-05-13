# MediFlow – Intelligent Monitoring Dashboard
**Stack:** React + TypeScript · Supabase · Python FastAPI · Chart.js

---

## Project Structure
```
mediflow/
├── supabase_schema.sql      ← Run in Supabase SQL Editor first
├── backend/
│   ├── main.py              ← FastAPI server
│   └── .env                 ← Supabase credentials
└── frontend/
    ├── src/
    │   ├── lib/supabase.ts  ← Supabase client + types
    │   ├── hooks/
    │   │   ├── useAlerts.ts   ← Realtime alert hook
    │   │   └── usePatients.ts ← Patient data hook
    │   ├── components/
    │   │   ├── AlertLogPanel.tsx  ← Alert history panel
    │   │   ├── GaitCharts.tsx     ← 4 Chart.js gait charts
    │   │   └── LiveRiskMeter.tsx  ← SVG gauge
    │   └── pages/Dashboard.tsx   ← Main page
    ├── .env                 ← Vite env vars
    └── package.json
```

---

## Step 1 – Supabase Setup

1. Go to https://supabase.com → New project
2. Open **SQL Editor** → paste contents of `supabase_schema.sql` → Run
3. Copy your **Project URL** and **anon key** from Settings → API

---

## Step 2 – Backend (FastAPI)

```bash
cd backend

# Install deps
pip install fastapi uvicorn supabase python-dotenv

# Fill in .env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...

# Run
uvicorn main:app --reload --port 8000
```

API runs at http://localhost:8000
Swagger docs: http://localhost:8000/docs

---

## Step 3 – Frontend (React)

```bash
cd frontend

# Install deps
npm install

# Fill in .env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_API_URL=http://localhost:8000

# Run
npm run dev
```

App runs at http://localhost:5173

---

## Key Features

| Feature | How it works |
|---|---|
| Patient list | Fetched from Supabase `patients` table |
| Live Risk Meter | Reads `risk_score` from selected patient |
| Alert Log | Fetched from `alert_log` via FastAPI – filtered by patient |
| Realtime alerts | Supabase Realtime subscription on `alert_log` table |
| Gait charts | Chart.js – fetched from `/gait/{id}` endpoint |
| Filter tabs | ALL / ALERT / NEAR-MISS / INFO |
| Live clock | JS interval timer |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /patients | All patients |
| GET | /patients/{id} | Single patient |
| PATCH | /patients/{id}/risk | Update risk score |
| GET | /alerts?patient_id=6 | Alert history |
| POST | /alerts | Create new alert |
| GET | /gait/{id} | Latest gait data |
| POST | /gait/{id}/simulate | Push simulated gait |
| WS | /ws | WebSocket live feed |

---

## Trigger a Live Alert (Test)

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 6,
    "alert_type": "ALERT",
    "severity": "critical",
    "message": "Sudden fall detected – caregiver dispatched."
  }'
```

The alert appears instantly in the dashboard via Supabase Realtime.
