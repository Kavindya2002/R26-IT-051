<div align="center">

# 🛡️ Multimodal Intelligent Fall Monitoring System for Elderly Care

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Realtime-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![IoT](https://img.shields.io/badge/IoT-ESP32%20%7C%20RPi-E7352C?logo=espressif&logoColor=white)](https://www.espressif.com/)
[![Research](https://img.shields.io/badge/IT4010-Research%20Project%202026-9C27B0)](.)

<br/>

> **A proactive, AI-powered, multimodal monitoring system that predicts, detects, and responds to elderly fall risks in real time — before injury occurs.**

<br/>

![System Banner](https://img.shields.io/badge/SDG%203-Good%20Health%20%26%20Well--being-4C9F38) &nbsp;
![System Banner](https://img.shields.io/badge/SDG%209-Industry%20%26%20Innovation-F36D25) &nbsp;
![System Banner](https://img.shields.io/badge/SDG%2011-Sustainable%20Cities-F99D26)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Modules](#-modules)
- [Tech Stack](#-tech-stack)
- [Team](#-team)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Research & References](#-research--references)
- [License](#-license)

---

## 🔍 Overview

The **Multimodal Intelligent Fall Monitoring System** is a final-year research project (IT4010 – 2026) developed at the **SST – Software Systems & Technologies** research group. It addresses one of the most pressing challenges in elderly healthcare: fall prevention and rapid response.

Unlike traditional reactive fall detection systems, this solution takes a **proactive, context-aware, and explainable approach** — fusing AI, IoT, wearable sensors, and real-time dashboards to identify and mitigate fall risks *before* incidents occur.

**Project ID:** `R26-IT-051`

---

## ⚠️ Problem Statement

Falls are among the leading causes of injury, disability, hospitalization, and mortality among elderly individuals worldwide. Existing systems are predominantly **reactive** — they only alert after a fall has happened. Key gaps in current technology include:

| Gap | Description |
|-----|-------------|
| 🔴 Reactive-only detection | No proactive fall risk prediction |
| 🔴 Limited context awareness | Cannot analyze environmental conditions or activity sequences |
| 🔴 Poor environmental monitoring | Wet floors, poor lighting, and obstacles are ignored |
| 🔴 Insufficient explainability | Black-box AI outputs with no reasoning |
| 🔴 High false alarm rates | Single-sensor approaches lack redundancy |
| 🔴 No recovery guidance | Systems stop at detection, offering no post-fall support |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    INPUT LAYER (Sensor Fusion)                    │
│  Wearable Sensors (IMU)  │  IoT Sensors (Env)  │  Vision (Opt.) │
└──────────────┬───────────┴─────────┬───────────┴────────┬───────┘
               │                     │                     │
               ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                            │
│  Activity Recognition  │  Risk Mapping  │  ML Prediction Engine │
└──────────────┬─────────┴───────┬────────┴──────────────┬────────┘
               │                 │                        │
               ▼                 ▼                        ▼
┌──────────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                               │
│  Explainable Dashboard  │  Smart Alerts  │  Recovery Guidance   │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- 🔮 **Proactive Fall Prediction** — ML models identify risky patterns before a fall occurs
- 🗺️ **Dynamic Environmental Risk Maps** — Real-time hazard zones (low / medium / high risk)
- 🧠 **Explainable AI (XAI)** — Human-readable insights into every prediction
- 📊 **Live Monitoring Dashboard** — WebSocket-powered gait analytics and telemetry
- 🚨 **Adaptive Alert System** — Tiered responses from caregiver notifications to emergency calls
- 🩺 **Post-Fall Recovery Guidance** — Personalized instructions based on fall severity and patient profile
- 🔋 **Device Health Monitoring** — Real-time status tracking of all connected sensors

---

## 🧩 Modules

### 1. 🏃 Context-Aware Activity Recognition & Early Fall Risk Prediction
**Owner:** Chathuri M.T.K — `IT22548078`

Processes wearable sensor streams (accelerometer + gyroscope) to classify activities and detect unstable movement sequences. Outputs a **confidence-based fall risk score** with explainable reasoning.

- Data collection, preprocessing, and windowed feature extraction
- ML-based activity classification (SVM, Neural Networks, etc.)
- Sequence analysis for behavioral instability detection
- Confidence percentage generation per prediction

---

### 2. 🌍 Environmental Risk Mapping & Smart Safety Zone System
**Owner:** Diwyangi D.H.S — `IT22559968`

Continuously monitors surroundings using IoT sensors to detect environmental hazards. Generates **dynamic spatial risk maps** and guides users toward safe paths proactively.

- Light, moisture, and distance sensor integration
- Real-time hazard classification into safety zones
- Proactive path guidance and smart alerts
- Optional vision-based environmental analysis

---

### 3. 📡 Intelligent Monitoring & Explainable Dashboard
**Owner:** Divyanjalie W.A.H — `IT22227690`

A high-concurrency real-time dashboard that streams live sensor data, visualizes patient gait with 3D analytics, and displays a **Live Risk Meter** for healthcare staff.

- FastAPI + WebSocket-based live data streaming
- Supabase Realtime for low-latency alerts
- 3D gait visualization and live risk charts
- Device health and alert history panels

---

### 4. 🤖 AI-Assisted Report Analysis & Smart Alert Engine
**Owner:** Kulathunga E.D.K.M — `IT21066948`

After a fall event, this module evaluates severity using contextual factors (age, posture, location, fall history) and triggers **adaptive responses** — from recovery tips to emergency dispatch.

- Risk level classification and severity scoring
- Personalized recovery guidance generation
- Smart caregiver notification system
- Emergency response activation logic

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **AI / ML** | Python, scikit-learn, TensorFlow / PyTorch, XAI libraries |
| **Backend** | FastAPI, WebSockets, REST APIs |
| **Database & Realtime** | Supabase, PostgreSQL |
| **IoT / Embedded** | ESP32, Raspberry Pi, Arduino |
| **Sensors** | MPU-6050 (IMU), HC-SR04 (Distance), LDR (Light), Moisture Sensors |
| **Frontend** | React.js / Next.js, Chart.js, Three.js (3D Gait) |
| **Cloud & DevOps** | Docker, GitHub Actions, Cloud Hosting |

---

## 👥 Team

| Name | Reg. No. | Module |
|------|----------|--------|
| Chathuri M.T.K | IT22548078 | Activity Recognition & Fall Risk Prediction |
| Diwyangi D.H.S | IT22559968 | Environmental Risk Mapping & Safety Zones |
| Divyanjalie W.A.H | IT22227690 | Intelligent Dashboard & Real-time Monitoring |
| Kulathunga E.D.K.M | IT21066948 | AI Report Analysis & Smart Alert Engine |

**Research Group:** SST – Software Systems & Technologies
**Specialization:** Information Technology (IT)

---

## 📁 Project Structure

```
multimodal-fall-monitor/
├── 📂 activity-recognition/       # Module 1 – Wearable sensor ML pipeline
│   ├── data/
│   ├── models/
│   └── src/
├── 📂 environmental-mapping/      # Module 2 – IoT hazard detection & risk maps
│   ├── sensors/
│   ├── mapping/
│   └── src/
├── 📂 dashboard/                  # Module 3 – Real-time monitoring frontend & backend
│   ├── frontend/
│   ├── backend/
│   └── websocket/
├── 📂 alert-engine/               # Module 4 – Post-fall analysis & alert system
│   ├── classifier/
│   ├── guidance/
│   └── notifications/
├── 📂 docs/                       # Project documentation & research assets
├── 📂 hardware/                   # Circuit diagrams & firmware
├── 📄 docker-compose.yml
├── 📄 requirements.txt
└── 📄 README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Supabase account (for real-time database)
- ESP32 / Raspberry Pi (for hardware deployment)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/multimodal-fall-monitor.git
cd multimodal-fall-monitor

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your Supabase credentials and config

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
cd dashboard/frontend && npm install

# 5. Start all services with Docker
docker-compose up --build
```

### Running Individual Modules

```bash
# Start the FastAPI backend
uvicorn dashboard.backend.main:app --reload

# Run the activity recognition pipeline
python activity-recognition/src/pipeline.py

# Run the environmental mapping service
python environmental-mapping/src/hazard_monitor.py
```

---

## 📚 Research & References

1. Stephen et al. — *AI-Based Fall Prevention and Monitoring Systems for Aged Adults in Residential Care Facilities*, 2025
2. Wang et al. — *Intelligent Fall Detection System for Drones in Agricultural Field Scenarios*, BIT, 2025
3. Aravindan et al. — *IoT-Based Real-Time Fall Detection and Pulse Monitoring Alert System*, Sathyabama Institute, 2025
4. Chen, W. — *Real-time Fall Monitoring System Based on Multimodal Sensor Fusion*, Yanshan University, 2025
5. Dogu et al. — *Reimagining Falls Prevention with Millimetre-Wave Radar*, Health Informatics, 2025
6. Sadhu et al. — *Prospect of Internet of Medical Things: Security Requirements and Solutions*, Sensors, 2022

---

## 🌐 UN Sustainable Development Goals

This research directly contributes to:

- **SDG 3** – Good Health and Well-being *(elderly safety, preventive healthcare)*
- **SDG 9** – Industry, Innovation and Infrastructure *(AI & IoT integration)*
- **SDG 11** – Sustainable Cities and Communities *(safer smart living environments)*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**IT4010 Research Project · 2026 · SST Research Group**

*Building smarter, safer environments for elderly independence.*

</div>
