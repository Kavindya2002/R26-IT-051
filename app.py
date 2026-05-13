import streamlit as st
import json
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Fall Management Dashboard",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #1e1e2f;
}

.big-title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.sub-title {
    font-size: 20px;
    color: #9ca3af;
}

.result-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    margin-top: 20px;
}

.low-box {
    background-color: #14532d;
    color: #dcfce7;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.medium-box {
    background-color: #78350f;
    color: #fef3c7;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.high-box {
    background-color: #7f1d1d;
    color: #fecaca;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.guidance-box {
    background-color: #064e3b;
    padding: 18px;
    border-radius: 12px;
    font-size: 20px;
    color: #d1fae5;
    margin-top: 20px;
}

.alert-box {
    background-color: #7f1d1d;
    padding: 18px;
    border-radius: 12px;
    font-size: 20px;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Patient Risk Information")

risk_score = st.sidebar.slider(
    "Risk Score",
    0,
    100,
    35
)

age = st.sidebar.number_input(
    "Age",
    min_value=50,
    max_value=100,
    value=70
)

previous_falls = st.sidebar.number_input(
    "Previous Falls",
    min_value=0,
    max_value=20,
    value=1
)

location = st.sidebar.selectbox(
    "Location",
    [
        "living_room",
        "bathroom",
        "bedroom",
        "stairs",
        "kitchen"
    ]
)

movement = st.sidebar.selectbox(
    "Movement",
    [
        "no_movement",
        "slight_movement",
        "upper_body_movement",
        "crawling",
        "standing_stable",
        "unstable"
    ]
)

orientation = st.sidebar.selectbox(
    "Body Orientation",
    [
        "flat",
        "side",
        "kneeling",
        "standing"
    ]
)

balance = st.sidebar.selectbox(
    "Balance",
    [
        "stable",
        "unstable"
    ]
)

assistive_device = st.sidebar.selectbox(
    "Assistive Device",
    [
        "yes",
        "no"
    ]
)

heart_rate = st.sidebar.slider(
    "Heart Rate",
    40,
    150,
    75
)

# =========================================================
# RISK LEVEL CLASSIFICATION
# =========================================================

if risk_score < 40:
    risk_level = "LOW"

elif risk_score < 70:
    risk_level = "MEDIUM"

else:
    risk_level = "HIGH"

# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<p class="big-title">🧠 AI Fall Management Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Dynamic Fall Detection & Recovery Guidance System</p>',
    unsafe_allow_html=True
)

# =========================================================
# DISPLAY RISK LEVEL
# =========================================================

st.markdown("## 🚨 Detected Risk Level")

if risk_level == "LOW":

    st.markdown(
        f'<div class="low-box">LOW RISK ({risk_score})</div>',
        unsafe_allow_html=True
    )

elif risk_level == "MEDIUM":

    st.markdown(
        f'<div class="medium-box">MEDIUM RISK ({risk_score})</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f'<div class="high-box">HIGH RISK ({risk_score})</div>',
        unsafe_allow_html=True
    )

# =========================================================
# RUN BUTTON
# =========================================================

run = st.button("🚀 Run Guidance Engine")

# =========================================================
# GUIDANCE ENGINE
# =========================================================

if run:

    st.markdown("---")

    current_step = ""
    instruction = ""
    sensor_status = ""
    next_action = ""
    alert_status = ""

    # =====================================================
    # LOW RISK
    # =====================================================

    if risk_level == "LOW":

        # STEP 1
        if movement == "no_movement":

            current_step = "Consciousness Check"

            instruction = "Are you okay? Please try to move slowly."

            sensor_status = "No movement detected"

            next_action = "Wait for movement"

            alert_status = "Monitoring"

        # STEP 2
        elif movement == "slight_movement":

            current_step = "Movement Confirmed"

            instruction = "You are safe. Please stay calm."

            sensor_status = "Slight movement detected"

            next_action = "Check body orientation"

            alert_status = "No alerts triggered"

        # STEP 3
        if orientation == "flat":

            current_step = "Body Orientation Detection"

            instruction = "Slowly turn onto your side."

            sensor_status = "Flat position detected"

            next_action = "Wait for side confirmation"

        # STEP 4
        elif orientation == "side":

            current_step = "Side Position Confirmed"

            instruction = "Use your hands to support your body."

            sensor_status = "Side position stable."

            next_action = "Push upper body upward slowly."

        # STEP 5
        if movement == "upper_body_movement":

            current_step = "Upper Body Movement"

            instruction = "Slowly move into a crawling position."

            sensor_status = "Upper body movement detected"

            next_action = "Monitor crawling stability"

        # STEP 6
        if movement == "crawling":

            current_step = "Crawling Stability"

            instruction = "Move carefully toward stable furniture or a wall."

            sensor_status = "Crawling stable"

            next_action = "Reach stable support"

        # STEP 7
        if orientation == "kneeling":

            current_step = "Support Assistance"

            instruction = "Place both hands on support and slowly kneel."

            sensor_status = "Kneeling stable"

            next_action = "Prepare standing"

        # STEP 8
        if orientation == "standing":

            current_step = "Standing Transition"

            instruction = "Slowly stand while maintaining balance."

            sensor_status = "Standing detected"

            next_action = "Monitor balance"

        # STEP 9
        if orientation == "standing" and balance == "stable":

            current_step = "Recovery Completed"

            instruction = "Recovery completed successfully."

            sensor_status = "Stable standing confirmed"

            next_action = "Continue monitoring"

            alert_status = "No alerts triggered"

        # =====================================================
        # SAFETY ESCALATION
        # =====================================================

        if balance == "unstable":

            alert_status = "Caregiver alert triggered"

        if heart_rate > 120:

            alert_status = "Medical emergency alert"

        if previous_falls > 3:

            alert_status = "High monitoring sensitivity enabled"

        if location == "bathroom" or location == "stairs":

            alert_status = "Dangerous location monitoring active"

    # =====================================================
    # MEDIUM RISK
    # =====================================================

    elif risk_level == "MEDIUM":

        current_step = "Caregiver Alert"

        instruction = "Please remain still. Help is being contacted."

        sensor_status = "Continuous monitoring active"

        next_action = "Wait for caregiver assistance"

        alert_status = "Caregiver alert sent"

    # =====================================================
    # HIGH RISK
    # =====================================================

    else:

        current_step = "Emergency Response"

        instruction = "Do not move. Emergency services are being contacted."

        sensor_status = "Critical monitoring active"

        next_action = "Await emergency assistance"

        alert_status = "Emergency alert sent"

    # =====================================================
    # DISPLAY RESULT
    # =====================================================

    st.markdown("## 📊 Guidance Result")

    output = {
        "CurrentRisk": risk_level,
        "RiskScore": risk_score,
        "CurrentStep": current_step,
        "Instruction": instruction,
        "SensorStatus": sensor_status,
        "NextExpectedAction": next_action,
        "AlertStatus": alert_status
    }

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.json(output)

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # DISPLAY INSTRUCTION
    # =====================================================

    if risk_level == "LOW":

        st.markdown(
            f'<div class="guidance-box">{instruction}</div>',
            unsafe_allow_html=True
        )

    elif risk_level == "MEDIUM":

        st.markdown(
            f'<div class="alert-box">⚠️ {instruction}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="alert-box">🚨 {instruction}</div>',
            unsafe_allow_html=True
        )

    # =====================================================
    # SIMULATED MONITORING
    # =====================================================

    st.markdown("## 📡 Real-Time Monitoring")

    progress = st.progress(0)

    for i in range(100):

        time.sleep(0.01)

        progress.progress(i + 1)

    st.success("Monitoring Active")