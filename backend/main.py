# ============================================================
#  MediFlow – FastAPI Backend
#  pip install fastapi uvicorn supabase python-dotenv
# ============================================================

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import asyncio, json, os, random, datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="MediFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
#  Pydantic Models
# ─────────────────────────────────────────
class AlertCreate(BaseModel):
    patient_id: int
    alert_type: str          # ALERT | NEAR-MISS | INFO
    severity: str            # critical | warning | info
    message: str

class RiskUpdate(BaseModel):
    risk_score: int
    status: str

# ─────────────────────────────────────────
#  WebSocket manager
# ─────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.active:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                pass

manager = ConnectionManager()

# ─────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "MediFlow API running"}


# -- Patients --
@app.get("/patients")
def get_patients():
    res = supabase.table("patients").select("*").order("id").execute()
    return res.data


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    res = supabase.table("patients").select("*").eq("id", patient_id).single().execute()
    if not res.data:
        raise HTTPException(404, "Patient not found")
    return res.data


@app.patch("/patients/{patient_id}/risk")
async def update_risk(patient_id: int, body: RiskUpdate):
    res = supabase.table("patients").update({
        "risk_score": body.risk_score,
        "status": body.status
    }).eq("id", patient_id).execute()
    # broadcast to all WS clients
    await manager.broadcast({"event": "risk_update", "patient_id": patient_id, "data": body.dict()})
    return res.data


# -- Alert Log --
@app.get("/alerts")
def get_alerts(patient_id: Optional[int] = None, limit: int = 50):
    """Get alert history – filter by patient or return all."""
    query = (
        supabase.table("alert_log")
        .select("*, patients(name, bed)")
        .order("created_at", desc=True)
        .limit(limit)
    )
    if patient_id:
        query = query.eq("patient_id", patient_id)
    res = query.execute()
    return res.data


@app.post("/alerts")
async def create_alert(body: AlertCreate):
    """Insert a new alert and broadcast via WebSocket."""
    res = supabase.table("alert_log").insert(body.dict()).execute()
    new_alert = res.data[0] if res.data else {}
    await manager.broadcast({"event": "new_alert", "data": new_alert})
    return new_alert


# -- Gait Data --
@app.get("/gait/{patient_id}")
def get_gait(patient_id: int):
    """Latest gait snapshot for a patient."""
    res = (
        supabase.table("gait_data")
        .select("*")
        .eq("patient_id", patient_id)
        .order("recorded_at", desc=True)
        .limit(1)
        .execute()
    )
    if res.data:
        return res.data[0]
    # Generate random if no data
    return _random_gait(patient_id)


@app.post("/gait/{patient_id}/simulate")
async def simulate_gait(patient_id: int):
    """Push simulated gait data (demo helper)."""
    data = _random_gait(patient_id)
    supabase.table("gait_data").insert({
        "patient_id": patient_id,
        **{k: v for k, v in data.items() if k != "patient_id"},
    }).execute()
    await manager.broadcast({"event": "gait_update", "patient_id": patient_id, "data": data})
    return data


# -- WebSocket --
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep alive ping every 20s
            await asyncio.sleep(20)
            await websocket.send_text(json.dumps({"event": "ping"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ─────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────
def _rand_series(n=41, lo=-20, hi=30):
    return [round(random.uniform(lo, hi), 2) for _ in range(n)]

def _random_gait(patient_id: int):
    return {
        "patient_id": patient_id,
        "tilt_angle":      _rand_series(41, -20, 30),
        "movement_speed":  _rand_series(41, -1.0, 2.0),
        "balance_level":   _rand_series(41, 0, 50),
        "com_fluctuation": _rand_series(41, -0.4, 0.6),
        "recorded_at":     datetime.datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────
#  Run
# ─────────────────────────────────────────
# uvicorn main:app --reload --port 8000
